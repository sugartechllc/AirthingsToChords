import csv
from datetime import datetime
import os
import sys
import argparse

parser = argparse.ArgumentParser(description="Split an Airthings CSV file into monthly files.")

parser.add_argument("-i", "--input_csv_file", help="Path to the input CSV file", required=True)

parser.add_argument("-o", "--output_directory", help="Directory to save monthly CSV files", required=True)

args = parser.parse_args()

input_file = args.input_csv_file
output_dir = args.output_directory

os.makedirs(output_dir, exist_ok=True)

input_file = args.input_csv_file
if not os.path.exists(input_file):
    print(f"Input file {input_file} does not exist.")
    sys.exit(1)
if not os.path.isfile(input_file):
    print(f"Input file {input_file} is not a valid file.")
    sys.exit(1)
if not os.access(input_file, os.R_OK):
    print(f"Input file {input_file} is not readable.")
    sys.exit(1)

if not os.access(args.output_directory, os.W_OK):
    print(f"Output directory {args.output_directory} is not writable.")
    sys.exit(1)

if not os.path.isdir(args.output_directory):
    print(f"Output directory {args.output_directory} is not a valid directory.")
    sys.exit(1)

output_dir = args.output_directory

with open(input_file, newline='') as f:
    reader = csv.reader(f, delimiter=';')
    header = next(reader)
    rows_by_month = {}

    for row in reader:
        if not row or not row[0]:
            continue
        try:
            dt = datetime.fromisoformat(row[0])
            month_key = dt.strftime('%Y-%m')
            rows_by_month.setdefault(month_key, []).append(row)
        except Exception:
            continue

    for month, rows in rows_by_month.items():
        out_path = os.path.join(output_dir, f'{month}.csv')
        with open(out_path, 'w', newline='') as out_f:
            writer = csv.writer(out_f, delimiter=';')
            writer.writerow(header)
            writer.writerows(rows)
