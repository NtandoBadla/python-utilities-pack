"""
Tests for data_validator.py

Run with:
    python -m unittest test_data_validator -v
"""

import unittest
from data_validator import validate_record, find_duplicates, clean_records


class TestValidateRecord(unittest.TestCase):

    def test_valid_record_has_no_problems(self):
        record = {"name": "Jane Doe", "email": "jane@co.com", "department": "IT", "device_id": "DEV-001"}
        self.assertEqual(validate_record(record), [])

    def test_missing_single_field(self):
        record = {"name": "Jane Doe", "email": "", "department": "IT", "device_id": "DEV-001"}
        problems = validate_record(record)
        self.assertEqual(len(problems), 1)
        self.assertIn("email", problems[0])

    def test_missing_multiple_fields(self):
        record = {"name": "Jane Doe", "email": "", "department": "", "device_id": "DEV-001"}
        problems = validate_record(record)
        self.assertEqual(len(problems), 2)

    def test_whitespace_only_counts_as_missing(self):
        record = {"name": "Jane Doe", "email": "   ", "department": "IT", "device_id": "DEV-001"}
        problems = validate_record(record)
        self.assertEqual(len(problems), 1)


class TestFindDuplicates(unittest.TestCase):

    def test_no_duplicates(self):
        records = [
            {"name": "A", "email": "a@co.com"},
            {"name": "B", "email": "b@co.com"},
        ]
        self.assertEqual(find_duplicates(records), set())

    def test_detects_exact_duplicate(self):
        records = [
            {"name": "A", "email": "a@co.com"},
            {"name": "A", "email": "a@co.com"},
        ]
        self.assertEqual(find_duplicates(records), {1})

    def test_case_insensitive_duplicate_detection(self):
        records = [
            {"name": "A", "email": "a@co.com"},
            {"name": "a", "email": "A@CO.COM"},
        ]
        self.assertEqual(find_duplicates(records), {1})

    def test_keeps_first_occurrence(self):
        records = [
            {"name": "A", "email": "a@co.com"},
            {"name": "A", "email": "a@co.com"},
            {"name": "A", "email": "a@co.com"},
        ]
        self.assertEqual(find_duplicates(records), {1, 2})


class TestCleanRecords(unittest.TestCase):

    def test_separates_clean_invalid_and_duplicate(self):
        records = [
            {"name": "A", "email": "a@co.com", "department": "IT", "device_id": "1"},
            {"name": "B", "email": "", "department": "IT", "device_id": "2"},
            {"name": "A", "email": "a@co.com", "department": "IT", "device_id": "1"},
        ]
        result = clean_records(records)
        self.assertEqual(len(result["clean"]), 1)
        self.assertEqual(len(result["invalid"]), 1)
        self.assertEqual(len(result["duplicates"]), 1)

    def test_empty_input_produces_empty_output(self):
        result = clean_records([])
        self.assertEqual(result["clean"], [])
        self.assertEqual(result["invalid"], [])
        self.assertEqual(result["duplicates"], [])


if __name__ == "__main__":
    unittest.main()