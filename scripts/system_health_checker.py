import platform
import socket
import argparse
import logging
from pathlib import Path

import psutil

# ---------------------------------------------------------------------------
# Logging setup
# ---------------------------------------------------------------------------
LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)
LOG_FILE = LOG_DIR / "system_health_checker.log"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
        logging.StreamHandler()  # also prints to console
    ]
)
logger = logging.getLogger(__name__)


def get_system_health():
    """
    Collect system health information.

    Each metric is gathered independently so that a failure reading one
    piece of data (e.g. disk usage on a missing drive) does not prevent
    the others from being collected.
    """
    health = {
        "hostname": None,
        "operating_system": None,
        "os_version": None,
        "cpu_usage": None,
        "memory_usage": None,
        "disk_usage": None,
    }

    try:
        health["hostname"] = socket.gethostname()
        health["operating_system"] = platform.system()
        health["os_version"] = platform.version()
        logger.info("System information collected successfully.")
    except Exception as error:
        logger.error(f"Failed to collect system information: {error}")

    try:
        health["cpu_usage"] = psutil.cpu_percent(interval=1)
        logger.info(f"CPU usage read: {health['cpu_usage']}%")
    except Exception as error:
        logger.error(f"Failed to read CPU usage: {error}")

    try:
        health["memory_usage"] = psutil.virtual_memory().percent
        logger.info(f"Memory usage read: {health['memory_usage']}%")
    except Exception as error:
        logger.error(f"Failed to read memory usage: {error}")

    try:
        drive = "C:\\" if platform.system() == "Windows" else "/"
        health["disk_usage"] = psutil.disk_usage(drive).percent
        logger.info(f"Disk usage read ({drive}): {health['disk_usage']}%")
    except FileNotFoundError:
        logger.error(f"Drive '{drive}' not found — skipping disk usage check.")
    except Exception as error:
        logger.error(f"Failed to read disk usage: {error}")

    return health


def determine_status(usage):
    """
    Determine health status based on a usage percentage.

    Returns 'UNKNOWN' if usage could not be measured (None), instead of
    crashing on a comparison against None.
    """
    if usage is None:
        return "UNKNOWN"

    if usage >= 90:
        return "CRITICAL"
    elif usage >= 75:
        return "WARNING"
    else:
        return "HEALTHY"


def format_metric(label, value):
    """Format a single metric line, handling missing data gracefully."""
    if value is None:
        return f"{label}: Unavailable [UNKNOWN]"
    return f"{label}: {value}% [{determine_status(value)}]"


def display_health(health, show_system=True):
    """Display system health information."""
    print("\n===== SYSTEM HEALTH REPORT =====")

    if show_system:
        print(f"Hostname: {health['hostname'] or 'Unavailable'}")
        print(f"Operating System: {health['operating_system'] or 'Unavailable'}")
        print(f"OS Version: {health['os_version'] or 'Unavailable'}")

    print(format_metric("CPU Usage", health["cpu_usage"]))
    print(format_metric("Memory Usage", health["memory_usage"]))
    print(format_metric("Disk Usage", health["disk_usage"]))


def main():
    parser = argparse.ArgumentParser(description="IT System Health Checker")

    parser.add_argument("--system", action="store_true", help="Display system information")
    parser.add_argument("--resources", action="store_true", help="Display CPU, memory and disk usage")
    parser.add_argument("--all", action="store_true", help="Display all health information")

    args = parser.parse_args()

    logger.info("Health check started.")

    try:
        health = get_system_health()

        if args.all or (not args.system and not args.resources):
            display_health(health)
        elif args.system:
            print("\n===== SYSTEM INFORMATION =====")
            print(f"Hostname: {health['hostname'] or 'Unavailable'}")
            print(f"Operating System: {health['operating_system'] or 'Unavailable'}")
            print(f"OS Version: {health['os_version'] or 'Unavailable'}")
        elif args.resources:
            print("\n===== RESOURCE HEALTH =====")
            print(format_metric("CPU Usage", health["cpu_usage"]))
            print(format_metric("Memory Usage", health["memory_usage"]))
            print(format_metric("Disk Usage", health["disk_usage"]))

        logger.info("Health check completed successfully.")

    except Exception as error:
        logger.exception(f"Unexpected error during health check: {error}")
        print(f"Unable to retrieve system health information: {error}")


if __name__ == "__main__":
    main()