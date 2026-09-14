"""
data_validator.py

Week 4 Wednesday deliverable: read, validate, and clean employee/device
records from a CSV file. Satisfies the capstone's "User or Device Data
Processing" requirement:
  - Read records from a CSV file.
  - Validate required fields.
  - Identify invalid or duplicate records.
  - Produce a cleaned output file.
"""

import csv
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

REQUIRED_FIELDS = ["name", "email", "department", "device_id"]


def read_records(csv_path):
    """
    Read records from a CSV file into a list of dicts.

    Raises FileNotFoundError with a clear message if the file doesn't
    exist, rather than letting a cryptic low-level error surface.
    """
    path = Path(csv_path)
    if not path.exists():
        raise FileNotFoundError(f"CSV file not found: {csv_path}")

    with open(path, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        records = list(reader)

    logger.info(f"Read {len(records)} record(s) from '{csv_path}'.")
    return records


def validate_record(record, required_fields=REQUIRED_FIELDS):
    """
    Check a single record for missing required fields.

    Returns a list of problems found (empty list = record is valid).
    """
    problems = []
    for field in required_fields:
        value = record.get(field, "").strip() if record.get(field) else ""
        if not value:
            problems.append(f"Missing '{field}'")
    return problems


def find_duplicates(records, key_fields=("name", "email")):
    """
    Identify duplicate records based on a combination of key fields
    (default: same name AND same email = duplicate).

    Returns a set of indices (into `records`) that are duplicates of
    an earlier record — the first occurrence is kept, later ones are
    flagged.
    """
    seen = set()
    duplicate_indices = set()

    for i, record in enumerate(records):
        key = tuple(record.get(field, "").strip().lower() for field in key_fields)
        if key in seen:
            duplicate_indices.add(i)
        else:
            seen.add(key)

    return duplicate_indices


def clean_records(records, required_fields=REQUIRED_FIELDS, key_fields=("name", "email")):
    """
    Validate and deduplicate a list of records.

    Returns a dict:
        {
            "clean": [...],       # records with no issues, deduplicated
            "invalid": [...],     # (record, problems) tuples for records missing fields
            "duplicates": [...],  # records identified as duplicates of an earlier row
        }
    """
    duplicate_indices = find_duplicates(records, key_fields=key_fields)

    clean = []
    invalid = []
    duplicates = []

    for i, record in enumerate(records):
        problems = validate_record(record, required_fields=required_fields)

        if i in duplicate_indices:
            duplicates.append(record)
            continue

        if problems:
            invalid.append((record, problems))
            continue

        clean.append(record)

    logger.info(
        f"Cleaning complete: {len(clean)} clean, "
        f"{len(invalid)} invalid, {len(duplicates)} duplicate(s)."
    )

    return {"clean": clean, "invalid": invalid, "duplicates": duplicates}


def write_cleaned_csv(clean_records, output_path, fieldnames=REQUIRED_FIELDS):
    """Write only the clean, deduplicated records to a new CSV file."""
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(clean_records)

    logger.info(f"Cleaned CSV written to '{path}' ({len(clean_records)} record(s)).")
    return path


def process_csv(input_path, output_path="output/cleaned_records.csv"):
    """
    End-to-end pipeline: read -> validate/dedupe -> write cleaned output.
    Returns the same dict as clean_records(), plus the output file path.
    """
    records = read_records(input_path)
    result = clean_records(records)
    output = write_cleaned_csv(result["clean"], output_path)
    result["output_path"] = output
    return result


if __name__ == "__main__":
    import argparse

    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

    parser = argparse.ArgumentParser(description="Validate and clean a CSV of employee/device records.")
    parser.add_argument("--file", required=True, help="Path to the input CSV file")
    parser.add_argument("--output", default="output/cleaned_records.csv", help="Path for the cleaned output CSV")
    args = parser.parse_args()

    try:
        result = process_csv(args.file, args.output)

        print(f"\n===== CSV VALIDATION REPORT =====")
        print(f"Clean records:     {len(result['clean'])}")
        print(f"Invalid records:   {len(result['invalid'])}")
        print(f"Duplicate records: {len(result['duplicates'])}")

        if result["invalid"]:
            print("\n--- Invalid Records ---")
            for record, problems in result["invalid"]:
                print(f"  {record.get('name', 'Unknown')}: {', '.join(problems)}")

        if result["duplicates"]:
            print("\n--- Duplicate Records ---")
            for record in result["duplicates"]:
                print(f"  {record.get('name', 'Unknown')} ({record.get('email', 'no email')})")

        print(f"\nCleaned file saved to: {result['output_path']}")

    except FileNotFoundError as error:
        print(f"Error: {error}")