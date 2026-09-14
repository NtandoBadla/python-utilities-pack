"""
report_generator.py

Week 4 Monday deliverable: convert system data into a structured
report (CSV, JSON, HTML, or text), satisfying the capstone's
Reporting requirement.

A report includes: the date, checks performed, problems detected,
and recommended actions — not just raw numbers.
"""

import csv
import json
import logging
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)

REPORT_DIR = Path("reports")

RECOMMENDATIONS = {
    "cpu_usage": "Investigate high-CPU processes (see performance_monitor.py) and close unnecessary applications.",
    "memory_usage": "Close unused applications or browser tabs; consider adding more RAM if this recurs.",
    "disk_usage": "Free up disk space — remove temporary files, empty the recycle bin, or move files to external storage.",
}


def build_report(health, statuses):
    """
    Build a structured report dictionary from health data and their
    corresponding statuses.

    health: dict from get_system_health() (system_health_checker.py)
    statuses: dict mapping the same keys to HEALTHY/WARNING/CRITICAL/UNKNOWN
    """
    timestamp = datetime.now().isoformat(timespec="seconds")

    checks_performed = []
    problems_detected = []
    recommended_actions = []

    metric_labels = {
        "cpu_usage": "CPU Usage",
        "memory_usage": "Memory Usage",
        "disk_usage": "Disk Usage",
    }

    for key, label in metric_labels.items():
        value = health.get(key)
        status = statuses.get(key, "UNKNOWN")
        checks_performed.append(f"{label}: {value if value is not None else 'N/A'}% [{status}]")

        if status in ("WARNING", "CRITICAL"):
            problems_detected.append(f"{label} is {status} ({value}%)")
            if key in RECOMMENDATIONS:
                recommended_actions.append(RECOMMENDATIONS[key])

    report = {
        "report_generated": timestamp,
        "hostname": health.get("hostname", "Unknown"),
        "operating_system": health.get("operating_system", "Unknown"),
        "checks_performed": checks_performed,
        "problems_detected": problems_detected if problems_detected else ["None — all metrics healthy"],
        "recommended_actions": recommended_actions if recommended_actions else ["No action required"],
    }

    return report


def save_report_json(report, filename="health_report.json"):
    REPORT_DIR.mkdir(exist_ok=True)
    path = REPORT_DIR / filename
    with open(path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=4)
    logger.info(f"JSON report saved to '{path}'.")
    return path


def save_report_csv(report, filename="health_report.csv"):
    REPORT_DIR.mkdir(exist_ok=True)
    path = REPORT_DIR / filename
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Field", "Value"])
        writer.writerow(["Report Generated", report["report_generated"]])
        writer.writerow(["Hostname", report["hostname"]])
        writer.writerow(["Operating System", report["operating_system"]])
        writer.writerow([])
        writer.writerow(["Checks Performed"])
        for check in report["checks_performed"]:
            writer.writerow([check])
        writer.writerow([])
        writer.writerow(["Problems Detected"])
        for problem in report["problems_detected"]:
            writer.writerow([problem])
        writer.writerow([])
        writer.writerow(["Recommended Actions"])
        for action in report["recommended_actions"]:
            writer.writerow([action])
    logger.info(f"CSV report saved to '{path}'.")
    return path


def save_report_html(report, filename="health_report.html"):
    REPORT_DIR.mkdir(exist_ok=True)
    path = REPORT_DIR / filename

    def list_items(items):
        return "".join(f"<li>{item}</li>" for item in items)

    html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>System Health Report</title>
<style>
    body {{ font-family: Arial, sans-serif; margin: 2em; color: #222; }}
    h1 {{ color: #2E9EF7; }}
    h2 {{ border-bottom: 1px solid #ccc; padding-bottom: 4px; }}
    .meta {{ color: #555; margin-bottom: 1.5em; }}
    .problems li {{ color: #c0392b; }}
    .actions li {{ color: #1e7e34; }}
</style>
</head>
<body>
    <h1>System Health Report</h1>
    <p class="meta">
        Generated: {report['report_generated']}<br>
        Hostname: {report['hostname']}<br>
        Operating System: {report['operating_system']}
    </p>

    <h2>Checks Performed</h2>
    <ul>{list_items(report['checks_performed'])}</ul>

    <h2>Problems Detected</h2>
    <ul class="problems">{list_items(report['problems_detected'])}</ul>

    <h2>Recommended Actions</h2>
    <ul class="actions">{list_items(report['recommended_actions'])}</ul>
</body>
</html>
"""
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    logger.info(f"HTML report saved to '{path}'.")
    return path


def save_report_text(report, filename="health_report.txt"):
    REPORT_DIR.mkdir(exist_ok=True)
    path = REPORT_DIR / filename

    lines = [
        "===== SYSTEM HEALTH REPORT =====",
        f"Generated: {report['report_generated']}",
        f"Hostname: {report['hostname']}",
        f"Operating System: {report['operating_system']}",
        "",
        "--- Checks Performed ---",
        *report["checks_performed"],
        "",
        "--- Problems Detected ---",
        *report["problems_detected"],
        "",
        "--- Recommended Actions ---",
        *report["recommended_actions"],
    ]

    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    logger.info(f"Text report saved to '{path}'.")
    return path


SAVE_FUNCTIONS = {
    "json": save_report_json,
    "csv": save_report_csv,
    "html": save_report_html,
    "text": save_report_text,
}


def generate_report(health, statuses, output_format="text"):
    """
    Build and save a report in the requested format.

    output_format: 'json', 'csv', 'html', or 'text'
    Returns the path to the saved report file.
    """
    if output_format not in SAVE_FUNCTIONS:
        raise ValueError(
            f"Unsupported format '{output_format}'. "
            f"Choose from: {', '.join(SAVE_FUNCTIONS)}"
        )

    report = build_report(health, statuses)
    save_function = SAVE_FUNCTIONS[output_format]
    return save_function(report)