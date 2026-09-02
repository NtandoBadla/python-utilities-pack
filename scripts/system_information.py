import platform
import getpass
import os


def get_system_information():
    """Collect information about the current computer."""

    system_info = {
        "Computer Name": platform.node(),
        "Operating System": platform.system(),
        "OS Version": platform.version(),
        "Processor": platform.processor(),
        "Architecture": platform.machine(),
        "CPU Cores": os.cpu_count(),
        "Python Version": platform.python_version(),
        "Current User": getpass.getuser()
    }

    return system_info


def display_system_information(system_info):
    """Display system information in a readable format."""

    print("=" * 45)
    print("          SYSTEM INFORMATION")
    print("=" * 45)

    for name, value in system_info.items():
        print(f"{name:<17}: {value}")

    print("=" * 45)


def main():
    system_info = get_system_information()
    display_system_information(system_info)


if __name__ == "__main__":
    main()