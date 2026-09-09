import os
import shutil


def organize_files(folder_path):
    file_categories = {
        "Documents": [".pdf", ".docx", ".doc", ".txt"],
        "Images": [".jpg", ".jpeg", ".png", ".gif"],
        "Audio": [".mp3", ".wav"],
        "Videos": [".mp4", ".avi", ".mkv"],
        "Spreadsheets": [".xlsx", ".xls", ".csv"],
        "Presentations": [".pptx", ".ppt"]
    }

    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)

        if not os.path.isfile(file_path):
            continue

        file_extension = os.path.splitext(filename)[1].lower()

        category_found = False

        for category, extensions in file_categories.items():
            if file_extension in extensions:

                category_folder = os.path.join(folder_path, category)

                os.makedirs(category_folder, exist_ok=True)

                destination = os.path.join(category_folder, filename)

                shutil.move(file_path, destination)

                print(f"Moved: {filename} -> {category}")

                category_found = True
                break

        if not category_found:
            print(f"Skipped: {filename}")


def main():
    folder_path = input("Enter the folder path to organize: ")

    if not os.path.exists(folder_path):
        print("Error: Folder does not exist.")
        return

    if not os.path.isdir(folder_path):
        print("Error: The path is not a folder.")
        return

    organize_files(folder_path)

    print("\nFile organization complete!")


if __name__ == "__main__":
    main()