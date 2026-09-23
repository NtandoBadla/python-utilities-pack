"""
file_organizer.py

Organises files in a directory by type, detects content-based
duplicates (MD5 hash), flags potentially misnamed files (extension
does not match the category implied by the file's magic bytes), and
records every action to a log file.
"""

import hashlib
import logging
import shutil
from pathlib import Path

# ---------------------------------------------------------------------------
# Logging — writes to logs/file_organizer.log AND the console
# ---------------------------------------------------------------------------
_LOG_DIR = Path("logs")
_LOG_DIR.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(
            _LOG_DIR / "file_organizer.log",
            encoding="utf-8",
        ),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Category map  (extension → folder name)
# ---------------------------------------------------------------------------
FILE_CATEGORIES = {
    "Documents":     [".pdf", ".docx", ".doc", ".txt"],
    "Images":        [".jpg", ".jpeg", ".png", ".gif"],
    "Audio":         [".mp3", ".wav"],
    "Videos":        [".mp4", ".avi", ".mkv"],
    "Spreadsheets":  [".xlsx", ".xls", ".csv"],
    "Presentations": [".pptx", ".ppt"],
}

# Reverse lookup: extension → category
_EXT_TO_CATEGORY = {
    ext: cat
    for cat, exts in FILE_CATEGORIES.items()
    for ext in exts
}

# Magic-byte signatures used for misname detection.
# Each entry: (byte_offset, bytes_to_match, expected_category_name)
_MAGIC_SIGNATURES = [
    (0, b"\x89PNG\r\n\x1a\n",  "Images"),        # PNG
    (0, b"\xff\xd8\xff",        "Images"),        # JPEG
    (0, b"GIF87a",              "Images"),        # GIF87
    (0, b"GIF89a",              "Images"),        # GIF89
    (0, b"%PDF",                "Documents"),     # PDF
    (0, b"PK\x03\x04",         None),             # ZIP-based (docx/xlsx/pptx) — see below
    (0, b"ID3",                 "Audio"),         # MP3 with ID3 tag
    (0, b"\xff\xfb",            "Audio"),         # MP3 raw frame
    (0, b"RIFF",                "Audio"),         # WAV
    (0, b"\x00\x00\x00\x18ftyp", "Videos"),      # MP4
    (0, b"\x00\x00\x00\x20ftyp", "Videos"),      # MP4 variant
]

# ZIP-based Office formats — distinguished by file extension after the PK header.
_ZIP_OFFICE_EXTS = {
    ".docx": "Documents",
    ".xlsx": "Spreadsheets",
    ".pptx": "Presentations",
}


def get_category(extension: str) -> str | None:
    """Return the category name for a file extension, or None if unsupported."""
    return _EXT_TO_CATEGORY.get(extension.lower())


# ---------------------------------------------------------------------------
# Duplicate detection
# ---------------------------------------------------------------------------

def _md5(path: Path, chunk: int = 65536) -> str:
    """Return the MD5 hex digest of a file's contents."""
    h = hashlib.md5()
    with open(path, "rb") as fh:
        while True:
            block = fh.read(chunk)
            if not block:
                break
            h.update(block)
    return h.hexdigest()


def find_duplicate_files(folder: Path) -> dict[str, list[str]]:
    """
    Scan *folder* (non-recursively) and group files that share the same
    MD5 hash.  Returns a dict mapping hash → [list of filenames] for
    every group that contains more than one file.
    """
    hashes: dict[str, list[str]] = {}

    for file in folder.iterdir():
        if not file.is_file():
            continue
        try:
            digest = _md5(file)
            hashes.setdefault(digest, []).append(file.name)
        except (PermissionError, OSError) as exc:
            logger.warning(f"Could not hash '{file.name}': {exc}")

    return {h: names for h, names in hashes.items() if len(names) > 1}


# ---------------------------------------------------------------------------
# Misname detection
# ---------------------------------------------------------------------------

def _detect_category_from_magic(path: Path) -> str | None:
    """
    Read the first 32 bytes of *path* and return the category implied
    by its magic bytes, or None if the format is unrecognised.
    """
    try:
        header = path.read_bytes()[:32]
    except (PermissionError, OSError):
        return None

    for offset, magic, category in _MAGIC_SIGNATURES:
        if header[offset: offset + len(magic)] == magic:
            if category is None:
                # ZIP-based Office format — use extension to refine.
                return _ZIP_OFFICE_EXTS.get(path.suffix.lower())
            return category

    return None


def detect_misnamed_files(folder: Path) -> list[dict]:
    """
    Check every file in *folder* whose extension maps to a known
    category.  If the file's magic bytes suggest a *different* category,
    it is flagged as potentially misnamed.

    Returns a list of dicts:
        {
            "file": filename,
            "declared_category": "Images",
            "detected_category": "Documents",
            "reason": "..."
        }
    """
    misnamed = []

    for file in folder.iterdir():
        if not file.is_file():
            continue

        declared = get_category(file.suffix)
        if declared is None:
            continue  # unknown extension — skip

        detected = _detect_category_from_magic(file)
        if detected is None:
            continue  # unrecognised magic — can't judge

        if detected != declared:
            detail = {
                "file": file.name,
                "declared_category": declared,
                "detected_category": detected,
                "reason": (
                    f"Extension '{file.suffix}' suggests {declared}, "
                    f"but file content looks like {detected}."
                ),
            }
            misnamed.append(detail)
            logger.warning(
                f"Possibly misnamed: '{file.name}' — {detail['reason']}"
            )

    return misnamed


# ---------------------------------------------------------------------------
# Main organiser
# ---------------------------------------------------------------------------

def organize_files(folder_path: str) -> dict:
    """
    Organise files in *folder_path* by type.

    Steps
    -----
    1. Detect content-based duplicates (MD5) and log them.
    2. Detect potentially misnamed files (magic-byte check) and log them.
    3. Move each recognised file into its category subfolder.
    4. Record every action (move / skip / error) to the log file.

    Returns
    -------
    {
        "moved":    [...],
        "skipped":  [...],
        "errors":   [...],
        "duplicates": {hash: [names], ...},
        "misnamed": [...],
    }
    """
    folder = Path(folder_path)

    if not folder.exists():
        raise FileNotFoundError(f"Folder does not exist: {folder}")

    if not folder.is_dir():
        raise NotADirectoryError(f"Path is not a directory: {folder}")

    logger.info(f"Starting file organisation for: {folder}")

    # --- 1. Duplicate detection -------------------------------------------
    duplicates = find_duplicate_files(folder)
    if duplicates:
        for digest, names in duplicates.items():
            logger.warning(
                f"Duplicate files detected (MD5 {digest[:8]}…): "
                + ", ".join(f"'{n}'" for n in names)
            )
    else:
        logger.info("No duplicate files detected.")

    # --- 2. Misname detection ---------------------------------------------
    misnamed = detect_misnamed_files(folder)
    if not misnamed:
        logger.info("No misnamed files detected.")

    # --- 3. Move files ----------------------------------------------------
    moved   = []
    skipped = []
    errors  = []

    for file in folder.iterdir():
        if not file.is_file():
            continue

        category = get_category(file.suffix)

        if not category:
            reason = (
                f"Unsupported file type: "
                f"{file.suffix or 'no extension'}"
            )
            skipped.append({"file": file.name, "reason": reason})
            logger.info(f"Skipped '{file.name}': {reason}")
            continue

        destination_folder = folder / category

        try:
            destination_folder.mkdir(parents=True, exist_ok=True)
        except PermissionError as exc:
            entry = {
                "file": file.name,
                "operation": "create destination folder",
                "destination": str(destination_folder),
                "error_type": type(exc).__name__,
                "reason": str(exc),
            }
            errors.append(entry)
            logger.error(
                f"Cannot create folder '{destination_folder}' "
                f"for '{file.name}': {exc}"
            )
            continue

        destination = destination_folder / file.name

        if destination.exists():
            reason = "A file with the same name already exists."
            skipped.append({
                "file": file.name,
                "reason": reason,
                "destination": str(destination),
            })
            logger.info(
                f"Skipped '{file.name}': {reason} "
                f"({destination})"
            )
            continue

        try:
            shutil.move(str(file), str(destination))
            entry = {
                "file": file.name,
                "category": category,
                "destination": str(destination),
            }
            moved.append(entry)
            logger.info(
                f"Moved '{file.name}' → {category}/ "
                f"({destination})"
            )

        except PermissionError as exc:
            entry = {
                "file": file.name,
                "operation": "move",
                "destination": str(destination),
                "error_type": type(exc).__name__,
                "reason": str(exc),
                "suggestion": (
                    "Close the file if it is currently open "
                    "and make sure you have permission to move it."
                ),
            }
            errors.append(entry)
            logger.error(f"Permission denied moving '{file.name}': {exc}")

        except OSError as exc:
            entry = {
                "file": file.name,
                "operation": "move",
                "destination": str(destination),
                "error_type": type(exc).__name__,
                "reason": str(exc),
            }
            errors.append(entry)
            logger.error(f"OS error moving '{file.name}': {exc}")

        except Exception as exc:
            entry = {
                "file": file.name,
                "operation": "move",
                "destination": str(destination),
                "error_type": type(exc).__name__,
                "reason": str(exc),
            }
            errors.append(entry)
            logger.error(f"Unexpected error moving '{file.name}': {exc}")

    logger.info(
        f"Organisation complete — moved: {len(moved)}, "
        f"skipped: {len(skipped)}, errors: {len(errors)}, "
        f"duplicate groups: {len(duplicates)}, "
        f"misnamed: {len(misnamed)}"
    )

    return {
        "moved":      moved,
        "skipped":    skipped,
        "errors":     errors,
        "duplicates": duplicates,
        "misnamed":   misnamed,
    }


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Organise files by type.")
    parser.add_argument("--path", required=True, help="Folder to organise")
    args = parser.parse_args()

    result = organize_files(args.path)

    print("\n===== FILE ORGANIZER REPORT =====")

    print(f"\nMoved: {len(result['moved'])}")
    for item in result["moved"]:
        print(f"  ✓ {item['file']} → {item['category']}")

    print(f"\nSkipped: {len(result['skipped'])}")
    for item in result["skipped"]:
        print(f"  - {item['file']}: {item['reason']}")

    print(f"\nErrors: {len(result['errors'])}")
    for item in result["errors"]:
        print(f"  ✗ {item['file']}: {item['reason']}")

    if result["duplicates"]:
        print(f"\nDuplicate Groups: {len(result['duplicates'])}")
        for digest, names in result["duplicates"].items():
            print(f"  [{digest[:8]}…] " + ", ".join(names))
    else:
        print("\nNo duplicate files detected.")

    if result["misnamed"]:
        print(f"\nPossibly Misnamed: {len(result['misnamed'])}")
        for item in result["misnamed"]:
            print(f"  ⚠ {item['file']}: {item['reason']}")
    else:
        print("No misnamed files detected.")
