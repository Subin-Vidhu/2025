import os
import shutil
import datetime

def create_mock_files(directory="Downloads"):
    """Creates a directory and populates it with mock files with specific modified dates."""

    os.makedirs(directory, exist_ok=True)

    files = [
        {"name": "report.pdf", "date": datetime.datetime(2024, 10, 1).timestamp()},
        {"name": "image.jpg", "date": datetime.datetime(2024, 9, 15).timestamp()},
        {"name": "document.docx", "date": datetime.datetime(2024, 10, 5).timestamp()},
    ]

    for file in files:
        file_path = os.path.join(directory, file["name"])
        try:
            with open(file_path, 'w') as f:  # Create an empty file
                pass
            os.utime(file_path, (file["date"], file["date"]))
        except OSError as e:
            print(f"Error creating or modifying file {file_path}: {e}")

def delete_downloads_folder(directory="Downloads"):
    """Deletes the specified directory and its contents."""

    try:
        shutil.rmtree(directory)
        print(f"{directory} folder deleted successfully.")
    except OSError as e:
        print(f"Error deleting {directory}: {e}")

def reset_files(directory="Downloads"):
    """Resets the Downloads folder by deleting and recreating it with mock files."""

    delete_downloads_folder(directory)
    create_mock_files(directory)
    print(f"{directory} folder reset with mock files.")

reset_files()