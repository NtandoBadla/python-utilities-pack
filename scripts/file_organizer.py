import shutil
from pathlib import Path


FILE_CATEGORIES = {
    "Documents": [".pdf", ".docx", ".doc", ".txt"],
    "Images": [".jpg", ".jpeg", ".png", ".gif"],
    "Audio": [".mp3", ".wav"],
    "Videos": [".mp4", ".avi", ".mkv"],
    "Spreadsheets": [".xlsx", ".xls", ".csv"],
    "Presentations": [".pptx", ".ppt"],
}


def get_category(extension):
    extension = extension.lower()

    for category, extensions in FILE_CATEGORIES.items():
        if extension in extensions:
            return category

    return None


def organize_files(folder_path):
    folder = Path(folder_path)

    if not folder.exists():
        raise FileNotFoundError(
            f"Folder does not exist: {folder}"
        )

    if not folder.is_dir():
        raise NotADirectoryError(
            f"Path is not a directory: {folder}"
        )

    moved = []
    skipped = []
    errors = []

    for file in folder.iterdir():

        if not file.is_file():
            continue

        category = get_category(file.suffix)

        if not category:
            skipped.append({
                "file": file.name,
                "reason": (
                    f"Unsupported file type: "
                    f"{file.suffix or 'no extension'}"
                ),
            })
            continue

        destination_folder = folder / category

        try:
            destination_folder.mkdir(
                parents=True,
                exist_ok=True,
            )

        except PermissionError as exc:
            errors.append({
                "file": file.name,
                "operation": "create destination folder",
                "destination": str(destination_folder),
                "error_type": type(exc).__name__,
                "reason": str(exc),
            })
            continue

        destination = destination_folder / file.name

        # Prevent overwriting an existing file.
        if destination.exists():
            skipped.append({
                "file": file.name,
                "reason": "A file with the same name already exists.",
                "destination": str(destination),
            })
            continue

        try:
            shutil.move(
                str(file),
                str(destination),
            )

            moved.append({
                "file": file.name,
                "category": category,
                "destination": str(destination),
            })

        except PermissionError as exc:
            errors.append({
                "file": file.name,
                "operation": "move",
                "destination": str(destination),
                "error_type": type(exc).__name__,
                "reason": str(exc),
                "suggestion": (
                    "Close the file if it is currently open "
                    "and make sure you have permission to move it."
                ),
            })

        except OSError as exc:
            errors.append({
                "file": file.name,
                "operation": "move",
                "destination": str(destination),
                "error_type": type(exc).__name__,
                "reason": str(exc),
            })

        except Exception as exc:
            errors.append({
                "file": file.name,
                "operation": "move",
                "destination": str(destination),
                "error_type": type(exc).__name__,
                "reason": str(exc),
            })

    return {
        "moved": moved,
        "skipped": skipped,
        "errors": errors,
    }


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Organize files by type."
    )

    parser.add_argument(
        "--path",
        required=True,
        help="Folder to organize",
    )

    args = parser.parse_args()

    result = organize_files(args.path)

    print("\n===== FILE ORGANIZER REPORT =====")

    print(f"\nMoved: {len(result['moved'])}")
    for item in result["moved"]:
        print(
            f"  ✓ {item['file']} -> "
            f"{item['category']}"
        )

    print(f"\nSkipped: {len(result['skipped'])}")
    for item in result["skipped"]:
        print(
            f"  - {item['file']}: "
            f"{item['reason']}"
        )

    print(f"\nErrors: {len(result['errors'])}")
    for item in result["errors"]:
        print(
            f"  ✗ {item['file']}: "
            f"{item['reason']}"
        )