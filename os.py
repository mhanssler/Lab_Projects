'''This is a test of the os library and what it can do'''

import csv
import os

folder = 'csv_files'

if not os.path.exists(folder):
    os.makedirs(folder)

list = ['hello 1', 'hello 3', 'hello 2']

for i in list:
    file_path = os.path.join(folder, f'{i}.csv')
    with open(file_path, 'w', newline='') as file:
        writer = csv.writer(file)

        writer.writerow([i])

sort = sorted(list)
print(sort)