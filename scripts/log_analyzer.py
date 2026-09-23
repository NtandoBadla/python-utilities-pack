"""
log_analyzer.py

Reads a system or application log file, identifies INFO, WARNING and
ERROR entries using regular expressions, groups repeated errors to
surface the most frequent ones, and generates a structured error
summary.
"""

import argparse
import logging
import re
from collections import Counter
from pathlib import Path

# ---------------------------------------------------------------------------
# Module-level logger — writes to logs/log_analyzer.log AND the console
# ---------------------------------------------------------------------------
_LOG_DIR = Path("logs")
_LOG_DIR.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(
            _LOG_DIR / "log_analyzer.log",
            encoding="utf-8",
        ),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Regular expressions
# ---------------------------------------------------------------------------

# Match a log level keyword that appears as a whole word or inside
# common bracketed patterns like [INFO], [WARNING], [ERROR].
_RE_INFO    = re.compile(r"\bINFO\b",    re.IGNORECASE)
_RE_WARNING = re.compile(r"\bWARNING\b", re.IGNORECASE)
_RE_ERROR   = re.compile(r"\bERROR\b",   re.IGNORECASE)

# Extract the message portion that follows the log level keyword so
# repeated errors can be grouped regardless of timestamp or PID prefix.
# Supports common formats:
#   2024-01-01 12:00:00 [ERROR] Connection refused
#   ERROR - Connection refused
#   [ERROR]: Connection refused
_RE_ERROR_MSG = re.compile(
    r"\bERROR\b[\s:\-\]]*(.+)",
    re.IGNORECASE,
)


def _normalise_error_message(line: str) -> str:
    """
    Strip the variable parts of an error line (timestamps, PIDs, hex
    addresses) so that two lines that describe the same fault are
    treated as identical when counting repeats.
    """
    # Remove ISO-style timestamps: 2024-01-01 or 2024-01-01T12:00:00
    msg = re.sub(r"\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2}[\.\d]*", "", line)
    # Remove standalone integers (PIDs, line numbers, etc.)
    msg = re.sub(r"\b\d+\b", "<N>", msg)
    # Remove hex addresses like 0x7f3a1b2c
    msg = re.sub(r"0x[0-9a-fA-F]+", "<HEX>", msg)
    return msg.strip()


# ---------------------------------------------------------------------------
# Core analysis function
# ---------------------------------------------------------------------------

def analyze_log_file(file_path: str) -> tuple:
    """
    Parse *file_path* and return a 4-tuple:

        (info_count, warning_count, error_count, errors)

    where *errors* is a list of the raw error lines (preserving the
    original contract expected by the API layer and display_results).

    Additionally logs a repeated-error summary internally.
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Log file not found: {file_path}")

    logger.info(f"Analysing log file: {path}")

    info_count    = 0
    warning_count = 0
    error_count   = 0
    errors: list[str] = []

    # Counter for grouping repeated errors
    error_message_counts: Counter = Counter()

    try:
        with open(path, "r", encoding="utf-8", errors="replace") as fh:
            for line in fh:
                stripped = line.rstrip()

                if _RE_ERROR.search(stripped):
                    error_count += 1
                    errors.append(stripped)

                    # Extract normalised message for repeat-counting
                    match = _RE_ERROR_MSG.search(stripped)
                    if match:
                        normalised = _normalise_error_message(match.group(1))
                    else:
                        normalised = _normalise_error_message(stripped)
                    error_message_counts[normalised] += 1

                elif _RE_WARNING.search(stripped):
                    warning_count += 1

                elif _RE_INFO.search(stripped):
                    info_count += 1

    except PermissionError as exc:
        logger.error(f"Permission denied reading '{file_path}': {exc}")
        raise
    except Exception as exc:
        logger.error(f"Unexpected error reading '{file_path}': {exc}")
        raise

    logger.info(
        f"Analysis complete — INFO: {info_count}, "
        f"WARNING: {warning_count}, ERROR: {error_count}"
    )

    # Log the repeated-error summary (top 5)
    if error_message_counts:
        logger.info("Top repeated errors:")
        for msg, count in error_message_counts.most_common(5):
            logger.info(f"  x{count}  {msg[:120]}")

    return info_count, warning_count, error_count, errors


def get_error_summary(errors: list[str], top_n: int = 10) -> list[dict]:
    """
    Group *errors* by normalised message and return the *top_n* most
    frequent ones as a list of dicts:

        [{"message": "...", "count": N, "example": "..."}, ...]

    Exposed separately so callers (e.g. the API) can request a richer
    summary without re-parsing the file.
    """
    counts: Counter = Counter()
    examples: dict[str, str] = {}

    for line in errors:
        match = _RE_ERROR_MSG.search(line)
        key = _normalise_error_message(
            match.group(1) if match else line
        )
        counts[key] += 1
        if key not in examples:
            examples[key] = line  # store first occurrence as the example

    return [
        {"message": msg, "count": cnt, "example": examples[msg]}
        for msg, cnt in counts.most_common(top_n)
    ]


# ---------------------------------------------------------------------------
# Display helpers
# ---------------------------------------------------------------------------

def display_results(
    info_count: int,
    warning_count: int,
    error_count: int,
    errors: list[str],
) -> None:
    """Print a human-readable summary to the console."""
    total = info_count + warning_count + error_count

    print("\n=============================================")
    print("              LOG ANALYZER")
    print("=============================================")
    print(f"Total Log Entries : {total}")
    print(f"INFO Messages     : {info_count}")
    print(f"WARNING Messages  : {warning_count}")
    print(f"ERROR Messages    : {error_count}")

    print("\nERROR DETAILS")
    print("---------------------------------------------")
    if errors:
        for error in errors:
            print(error)
    else:
        print("No errors found.")

    # Repeated-error summary
    if errors:
        summary = get_error_summary(errors, top_n=5)
        if any(item["count"] > 1 for item in summary):
            print("\nREPEATED ERRORS (top 5)")
            print("---------------------------------------------")
            for item in summary:
                if item["count"] > 1:
                    print(f"  x{item['count']:>4}  {item['example'][:100]}")

    print("=============================================")


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Analyse a log file and report warnings and errors."
    )
    parser.add_argument(
        "--file",
        help="Path to the log file (omit to be prompted interactively)",
    )
    args = parser.parse_args()

    file_path = args.file if args.file else input("Enter the log file path: ")

    try:
        info_count, warning_count, error_count, errors = analyze_log_file(
            file_path
        )
        display_results(info_count, warning_count, error_count, errors)

    except FileNotFoundError:
        print("Error: Log file not found.")
    except PermissionError:
        print("Error: You do not have permission to read this file.")
    except Exception as error:
        print(f"Unexpected error: {error}")


if __name__ == "__main__":
    main()
