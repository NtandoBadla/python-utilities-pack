import platform
import socket
import psutil
import argparse


def get_system_health():
    """Collect system health information."""

    health = {
        "hostname": socket.gethostname(),
        "operating_system": platform.system(),
        "os_version": platform.version(),
        "cpu_usage": psutil.cpu_percent(interval=1),
        "memory_usage": psutil.virtual_memory().percent,
        "disk_usage": psutil.disk_usage("C:\\").percent
    }

    return health


def determine_status(usage):
    """Determine health status based on usage percentage."""

    if usage >= 90:
        return "CRITICAL"
    elif usage >= 75:
        return "WARNING"
    else:
        return "HEALTHY"


def display_health(health, show_system=True):
    """Display system health information."""

    print("\n===== SYSTEM HEALTH REPORT =====")

    if show_system:
        print(f"Hostname: {health['hostname']}")
        print(f"Operating System: {health['operating_system']}")
        print(f"OS Version: {health['os_version']}")

    print(
        f"CPU Usage: {health['cpu_usage']}% "
        f"[{determine_status(health['cpu_usage'])}]"
    )

    print(
        f"Memory Usage: {health['memory_usage']}% "
        f"[{determine_status(health['memory_usage'])}]"
    )

    print(
        f"Disk Usage: {health['disk_usage']}% "
        f"[{determine_status(health['disk_usage'])}]"
    )


def main():
    parser = argparse.ArgumentParser(
        description="IT System Health Checker"
    )

    parser.add_argument(
        "--system",
        action="store_true",
        help="Display system information"
    )

    parser.add_argument(
        "--resources",
        action="store_true",
        help="Display CPU, memory and disk usage"
    )

    parser.add_argument(
        "--all",
        action="store_true",
        help="Display all health information"
    )

    args = parser.parse_args()

    try:
        health = get_system_health()

        if args.all or (not args.system and not args.resources):
            display_health(health)

        elif args.system:
            print("\n===== SYSTEM INFORMATION =====")
            print(f"Hostname: {health['hostname']}")
            print(f"Operating System: {health['operating_system']}")
            print(f"OS Version: {health['os_version']}")

        elif args.resources:
            print("\n===== RESOURCE HEALTH =====")
            print(
                f"CPU Usage: {health['cpu_usage']}% "
                f"[{determine_status(health['cpu_usage'])}]"
            )
            print(
                f"Memory Usage: {health['memory_usage']}% "
                f"[{determine_status(health['memory_usage'])}]"
            )
            print(
                f"Disk Usage: {health['disk_usage']}% "
                f"[{determine_status(health['disk_usage'])}]"
            )

    except Exception as error:
        print(f"Unable to retrieve system health information: {error}")


if __name__ == "__main__":
    main()
