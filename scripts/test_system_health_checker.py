"""
Basic tests for system_health_checker.py

Run with:
    python -m unittest test_system_health_checker.py

These tests only cover the pure logic functions (determine_status,
format_metric) since get_system_health() depends on live system state
and psutil, which isn't something a unit test should assert exact
values for.
"""

import unittest
from system_health_checker import determine_status, format_metric


class TestDetermineStatus(unittest.TestCase):

    def test_healthy_below_75(self):
        self.assertEqual(determine_status(50), "HEALTHY")

    def test_warning_at_75(self):
        self.assertEqual(determine_status(75), "WARNING")

    def test_warning_below_90(self):
        self.assertEqual(determine_status(89.9), "WARNING")

    def test_critical_at_90(self):
        self.assertEqual(determine_status(90), "CRITICAL")

    def test_critical_above_90(self):
        self.assertEqual(determine_status(99.9), "CRITICAL")

    def test_unknown_when_none(self):
        self.assertEqual(determine_status(None), "UNKNOWN")

    def test_zero_usage_is_healthy(self):
        self.assertEqual(determine_status(0), "HEALTHY")


class TestFormatMetric(unittest.TestCase):

    def test_formats_healthy_metric(self):
        result = format_metric("CPU Usage", 50)
        self.assertIn("HEALTHY", result)
        self.assertIn("50", result)

    def test_formats_critical_metric(self):
        result = format_metric("Disk Usage", 95.4)
        self.assertIn("CRITICAL", result)

    def test_formats_missing_metric(self):
        result = format_metric("Memory Usage", None)
        self.assertIn("Unavailable", result)
        self.assertIn("UNKNOWN", result)


if __name__ == "__main__":
    unittest.main()