"""
main.py

IT Operations Automation Toolkit - Capstone Project
Week 4 Thursday deliverable: integrate all modules into one system.

Wires together:
  - system_health_checker  (CPU/memory/disk health)
  - performance_monitor    (top resource-consuming processes)
  - data_validator          (CSV record validation/cleaning)
  - report_generator        (JSON/CSV/HTML/text reports)
  - api_client               (public IP + GitHub repo status)
  - file_organizer / log_analyzer (Week 2 scripts, run as subprocesses
    since they're standalone CLI tools with their own argparse setup)
"""

import argparse
import logging
import subprocess
import sys
from pathlib import Path

from config_manager import load_config
from system_health_checker import get_system_health, determine_status, display_health
from performance_monitor import top_processes, display_top_processes
from data_validator import process_csv
from report_generator import generate_report
from api_client import get_public_ip, get_repo_status

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(Path("logs") / "toolkit.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

Path("logs").mkdir(exist_ok=True)


def run_health_check(report_format=None):
    """Run a full system health check, optionally saving a report."""
    print("IT Automation Toolkit - System Health Check")
    print("=" * 44)

    health = get_system_health()
    display_health(health)

    if report_format:
        statuses = {
            "cpu_usage": determine_status(health["cpu_usage"]),
            "memory_usage": determine_status(health["memory_usage"]),
            "disk_usage": determine_status(health["disk_usage"]),
        }
        path = generate_report(health, statuses, output_format=report_format)
        print(f"\nReport saved to: {path}")


def run_performance_scan(sort_by="cpu", limit=5):
    """Show the top resource-consuming processes."""
    print("IT Automation Toolkit - Performance Scan")
    print("=" * 44)

    processes = top_processes(limit=limit, sort_by=sort_by)
    display_top_processes(processes, sort_by)


def run_csv_validation(input_file, output_file):
    """Validate and clean a CSV of employee or device records."""
    print("IT Automation Toolkit - CSV Data Validation")
    print("=" * 44)

    try:
        result = process_csv(input_file, output_file)
        print(f"Clean records:     {len(result['clean'])}")
        print(f"Invalid records:   {len(result['invalid'])}")
        print(f"Duplicate records: {len(result['duplicates'])}")
        print(f"Cleaned file saved to: {result['output_path']}")
    except FileNotFoundError as error:
        print(f"Error: {error}")


def run_ip_lookup():
    """Look up this machine's public IP address."""
    print("IT Automation Toolkit - Public IP Lookup")
    print("=" * 44)

    result = get_public_ip()
    if "error" in result:
        print(f"Error: {result['error']}")
    else:
        print(f"Public IP: {result['ip']}")
        print(f"Retrieved: {result['retrieved_at']}")


def run_repo_status(owner, repo):
    """Look up a GitHub repository's live status."""
    print("IT Automation Toolkit - GitHub Repo Status")
    print("=" * 44)

    result = get_repo_status(owner, repo)
    if "error" in result:
        print(f"Error: {result['error']}")
    else:
        for key, value in result.items():
            print(f"{key.replace('_', ' ').title()}: {value}")


def run_file_organizer(path):
    """
    Run file_organizer.py as a subprocess.
    """
    print("IT Automation Toolkit - File Organizer")
    print("=" * 44)

    script = Path(__file__).parent / "file_organizer.py"
    if not script.exists():
        print(f"file_organizer.py not found at {script}")
        return

    result = subprocess.run(
        [sys.executable, str(script), "--path", path],
        capture_output=True, text=True
    )
    print(result.stdout)
    if result.returncode != 0:
        print(f"file_organizer.py reported an error:\n{result.stderr}")


def run_log_analyzer(log_file):
    """Run log_analyzer.py as a subprocess."""
    print("IT Automation Toolkit - Log Analyzer")
    print("=" * 44)

    script = Path(__file__).parent / "log_analyzer.py"
    if not script.exists():
        print(f"log_analyzer.py not found at {script}")
        return

    result = subprocess.run(
        [sys.executable, str(script), "--file", log_file],
        capture_output=True, text=True
    )
    print(result.stdout)
    if result.returncode != 0:
        print(f"log_analyzer.py reported an error:\n{result.stderr}")


def run_full_scan(report_format="html"):
    """Run every diagnostic module in sequence and produce one report."""
    print("IT Automation Toolkit - Full System Scan")
    print("=" * 44)
    print()

    run_health_check(report_format=report_format)
    print()
    run_performance_scan()
    print()
    run_ip_lookup()

    print("\nFull scan complete.")


def main():
    parser = argparse.ArgumentParser(
        description="IT Operations Automation Toolkit - capstone entry point."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    p_health = subparsers.add_parser("health", help="Run a system health check")
    p_health.add_argument("--report", choices=["json", "csv", "html", "text"], help="Save a report in this format")

    p_perf = subparsers.add_parser("performance", help="Show top resource-consuming processes")
    p_perf.add_argument("--sort-by", choices=["cpu", "memory"], default="cpu")
    p_perf.add_argument("--limit", type=int, default=5)

    p_csv = subparsers.add_parser("validate-csv", help="Validate and clean a CSV of records")
    p_csv.add_argument("--file", required=True, help="Input CSV path")
    p_csv.add_argument("--output", default="output/cleaned_records.csv", help="Output CSV path")

    subparsers.add_parser("ip", help="Look up this machine's public IP")

    p_repo = subparsers.add_parser("repo-status", help="Look up a GitHub repo's live status")
    p_repo.add_argument("--owner", required=True)
    p_repo.add_argument("--repo", required=True)

    p_organize = subparsers.add_parser("organize", help="Organize files in a directory")
    p_organize.add_argument("--path", required=True)

    p_logs = subparsers.add_parser("analyze-logs", help="Analyze a log file")
    p_logs.add_argument("--file", required=True)

    p_full = subparsers.add_parser("full-scan", help="Run health, performance and IP checks and save a report")
    p_full.add_argument("--report", choices=["json", "csv", "html", "text"], default="html")

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(0)

    args = parser.parse_args()
    logger.info(f"Toolkit command started: {args.command}")

    try:
        if args.command == "health":
            run_health_check(report_format=args.report)
        elif args.command == "performance":
            run_performance_scan(sort_by=args.sort_by, limit=args.limit)
        elif args.command == "validate-csv":
            run_csv_validation(args.file, args.output)
        elif args.command == "ip":
            run_ip_lookup()
        elif args.command == "repo-status":
            run_repo_status(args.owner, args.repo)
        elif args.command == "organize":
            run_file_organizer(args.path)
        elif args.command == "analyze-logs":
            run_log_analyzer(args.file)
        elif args.command == "full-scan":
            run_full_scan(report_format=args.report)

        logger.info(f"Toolkit command completed: {args.command}")

    except Exception as error:
        logger.exception(f"Toolkit command '{args.command}' failed: {error}")
        print(f"An error occurred: {error}")


if __name__ == "__main__":
    main()
