employees = []
devices = []


def add_employee():
    print("\n--- Add Employee ---")

    employee_id = input("Employee ID: ")
    name = input("Name: ")
    department = input("Department: ")
    position = input("Position: ")

    employee = {
        "id": employee_id,
        "name": name,
        "department": department,
        "position": position
    }

    employees.append(employee)

    print("\nEmployee added successfully.")


def view_employees():
    print("\n--- Employees ---")

    if not employees:
        print("No employees have been added.")
        return

    for employee in employees:
        print("-" * 40)
        print(f"ID         : {employee['id']}")
        print(f"Name       : {employee['name']}")
        print(f"Department : {employee['department']}")
        print(f"Position   : {employee['position']}")

    print("-" * 40)


def search_employee():
    print("\n--- Search Employee ---")

    search_id = input("Enter employee ID: ")

    for employee in employees:
        if employee["id"].lower() == search_id.lower():
            print("\nEmployee found!")
            print(f"ID         : {employee['id']}")
            print(f"Name       : {employee['name']}")
            print(f"Department : {employee['department']}")
            print(f"Position   : {employee['position']}")
            return

    print("\nEmployee not found.")


def add_device():
    print("\n--- Add Device ---")

    device_id = input("Device ID: ")
    device_type = input("Device Type: ")
    assigned_to = input("Assigned Employee ID: ")
    status = input("Device Status: ")

    device = {
        "id": device_id,
        "type": device_type,
        "assigned_to": assigned_to,
        "status": status
    }

    devices.append(device)

    print("\nDevice added successfully.")


def view_devices():
    print("\n--- Devices ---")

    if not devices:
        print("No devices have been added.")
        return

    for device in devices:
        print("-" * 40)
        print(f"Device ID   : {device['id']}")
        print(f"Device Type : {device['type']}")
        print(f"Assigned To : {device['assigned_to']}")
        print(f"Status      : {device['status']}")

    print("-" * 40)


def display_menu():
    print("\n" + "=" * 45)
    print("          IT USER & DEVICE MANAGER")
    print("=" * 45)
    print("1. Add employee")
    print("2. View employees")
    print("3. Search employee")
    print("4. Add device")
    print("5. View devices")
    print("6. Exit")
    print("=" * 45)


def main():
    while True:
        display_menu()

        choice = input("Choose an option: ")

        if choice == "1":
            add_employee()

        elif choice == "2":
            view_employees()

        elif choice == "3":
            search_employee()

        elif choice == "4":
            add_device()

        elif choice == "5":
            view_devices()

        elif choice == "6":
            print("\nExiting IT Manager. Goodbye!")
            break

        else:
            print("\nInvalid option. Please choose between 1 and 6.")


if __name__ == "__main__":
    main()