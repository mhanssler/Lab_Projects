import glob
import csv
import os

# Folder name
folder_name = 'csv_files'

# Pattern to match all CSV files in the folder
pattern = os.path.join(folder_name, '*.csv')
print(pattern)
# List all matching files and sort them
unsorted = glob.glob(pattern)
print(unsorted)
csv_files = sorted(glob.glob(pattern))
print(csv_files)
for file_path in csv_files:
    with open(file_path, 'r', newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            print(f"Contents of {file_path}: {row}")
