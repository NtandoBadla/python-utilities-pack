import platform
import socket
import psutil


def get_system_health():
    cpu_usage = psutil.cpu_percent(interval=1)
    memory_usage = psutil.virtual_memory().percent
    disk_usage = psutil.disk_usage("/").percent

    return {
        "computer_name": socket.gethostname(),
        "operating_system": platform.system(),
        "os_version": platform.version(),
        "cpu_usage": cpu_usage,
        "memory_usage": memory_usage,
        "disk_usage": disk_usage
    }


def determine_status(usage):
    if usage >= 90:
        return "CRITICAL"
    elif usage >= 75:
        return "WARNING"
    else:
        return "HEALTHY"


def display_health(system_health):
    print("\n=============================================")
    print("          SYSTEM HEALTH CHECKER")
    print("=============================================")

    print(f"Computer Name : {system_health['computer_name']}")
    print(f"Operating System : {system_health['operating_system']}")
    print(f"OS Version : {system_health['os_version']}")

    print("\nRESOURCE USAGE")
    print("---------------------------------------------")

    cpu = system_health["cpu_usage"]
    memory = system_health["memory_usage"]
    disk = system_health["disk_usage"]

    print(f"CPU Usage    : {cpu}% - {determine_status(cpu)}")
    print(f"Memory Usage : {memory}% - {determine_status(memory)}")
    print(f"Disk Usage   : {disk}% - {determine_status(disk)}")

    print("=============================================")


def main():
    try:
        system_health = get_system_health()
        display_health(system_health)

    except Exception as error:
        print(f"Error while checking system health: {error}")


if __name__ == "__main__":
    main()