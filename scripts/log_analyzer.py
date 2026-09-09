def analyze_log_file(file_path):
    info_count = 0
    warning_count = 0
    error_count = 0
    errors = []

    with open(file_path, "r") as log_file:
        for line in log_file:
            if "INFO" in line:
                info_count += 1

            elif "WARNING" in line:
                warning_count += 1

            elif "ERROR" in line:
                error_count += 1
                errors.append(line.strip())

    return info_count, warning_count, error_count, errors


def display_results(info_count, warning_count, error_count, errors):
    total_entries = info_count + warning_count + error_count

    print("\n=============================================")
    print("              LOG ANALYZER")
    print("=============================================")
    print(f"Total Log Entries : {total_entries}")
    print(f"INFO Messages     : {info_count}")
    print(f"WARNING Messages  : {warning_count}")
    print(f"ERROR Messages    : {error_count}")

    print("\nERROR DETAILS")
    print("---------------------------------------------")

    if errors:
        for error in errors:
            print(error)
    else:
        print("No errors found.")

    print("=============================================")


def main():
    file_path = input("Enter the log file path: ")

    try:
        info_count, warning_count, error_count, errors = analyze_log_file(
            file_path
        )

        display_results(
            info_count,
            warning_count,
            error_count,
            errors
        )

    except FileNotFoundError:
        print("Error: Log file not found.")

    except PermissionError:
        print("Error: You do not have permission to read this file.")

    except Exception as error:
        print(f"Unexpected error: {error}")


if __name__ == "__main__":
    main()