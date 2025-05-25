import os
import shutil
from datetime import datetime

# Path to your Downloads directory
downloads_dir = "Downloads"

# List all files in the Downloads directory
files = os.listdir(downloads_dir)

# Iterate over each file in the Downloads folder
for file in files:
    file_path = os.path.join(downloads_dir, file) 

    # Get the modification time of the file
    modified_time = os.path.getmtime(file_path)

    # Convert the modification time to a datetime object
    date = datetime.fromtimestamp(modified_time)
    year = date.year
    month = date.strftime("%B")

    # Print each file and their modification dates (for testing purposes)
    # print(f"File: {file}, Modified: {month} {year}")

    # Create the directory path for the year and month
    directory = os.path.join(downloads_dir, f"{year}/{month}")
 
    # Create the directory if it doesn't exist
    os.makedirs(directory, exist_ok=True)

    # Move the file to the new directory
    shutil.move(file_path, directory)
    

    # Print a confirmation message
    print(f"Moved '{file}' to '{directory}'")
    