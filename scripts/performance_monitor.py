"""
performance_monitor.py

Week 3 Wednesday deliverable: identify slow or resource-intensive
operations.

Two tools in one script:
  1. @timed decorator — measure how long any function takes to run.
  2. top_processes() — list the processes consuming the most CPU/memory
     right now, so you can see what's actually loading the system.
"""

import argparse
import functools
import logging
import time
from pathlib import Path

import psutil

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)
LOG_FILE = LOG_DIR / "performance_monitor.log"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def timed(func):
    """
    Decorator that logs how long a function took to run.

    Usage:
        @timed
        def slow_function():
            ...
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        try:
            result = func(*args, **kwargs)
            return result
        finally:
            elapsed = time.perf_counter() - start
            logger.info(f"'{func.__name__}' took {elapsed:.4f} seconds")
    return wrapper


def top_processes(limit=5, sort_by="cpu"):
    """
    Return the top N processes by CPU or memory usage.

    sort_by: 'cpu' or 'memory'
    """
    if sort_by not in ("cpu", "memory"):
        raise ValueError("sort_by must be 'cpu' or 'memory'")

    for proc in psutil.process_iter():
        proc.cpu_percent(interval=None)
    time.sleep(0.5)

    processes = []

    for proc in psutil.process_iter(["pid", "name", "cpu_percent", "memory_percent"]):
        try:
            info = proc.info
            processes.append(info)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    key = "cpu_percent" if sort_by == "cpu" else "memory_percent"
    processes.sort(key=lambda p: p.get(key) or 0, reverse=True)

    return processes[:limit]


def display_top_processes(processes, sort_by):
    label = "CPU %" if sort_by == "cpu" else "Memory %"
    key = "cpu_percent" if sort_by == "cpu" else "memory_percent"

    print(f"\n===== TOP {len(processes)} PROCESSES BY {label} =====")
    print(f"{'PID':<8}{'Name':<30}{label}")
    print("-" * 50)

    for proc in processes:
        pid = proc.get("pid", "?")
        name = proc.get("name", "unknown") or "unknown"
        value = proc.get(key) or 0.0
        print(f"{pid:<8}{name[:28]:<30}{value:.2f}")


@timed
def example_slow_operation():
    """A deliberately slow function, just to demonstrate @timed in action."""
    total = 0
    for i in range(5_000_000):
        total += i
    return total


def main():
    parser = argparse.ArgumentParser(
        description="Identify slow or resource-intensive operations."
    )
    parser.add_argument(
        "--sort-by",
        choices=["cpu", "memory"],
        default="cpu",
        help="Sort top processes by cpu or memory usage (default: cpu)"
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=5,
        help="Number of top processes to display (default: 5)"
    )
    parser.add_argument(
        "--demo-timing",
        action="store_true",
        help="Run a deliberately slow example function to show @timed in action"
    )

    args = parser.parse_args()

    logger.info("Performance scan started.")

    try:
        for proc in psutil.process_iter():
            proc.cpu_percent(interval=None)
        time.sleep(0.5)

        processes = top_processes(limit=args.limit, sort_by=args.sort_by)
        display_top_processes(processes, args.sort_by)

        if args.demo_timing:
            print("\nRunning example slow operation...")
            example_slow_operation()

        logger.info("Performance scan completed successfully.")

    except Exception as error:
        logger.exception(f"Unexpected error during performance scan: {error}")
        print(f"Unable to complete performance scan: {error}")


if __name__ == "__main__":
    main()