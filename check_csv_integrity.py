
import csv
import glob
import os

# Find the CSV file in the Data folder
files = glob.glob(os.path.join("Data", "*.csv"))

if not files:
    print("ERROR: No CSV file found.")
else:
    path = files[0]
    count = 0

    try:
        with open(path, "r", encoding="utf-8-sig", newline="") as file:
            reader = csv.reader(file, strict=True)
            header = next(reader)

            for row in reader:
                count += 1

                if len(row) != len(header):
                    print("COLUMN MISMATCH!")
                    print("Record number:", count)
                    print("Expected columns:", len(header))
                    print("Actual columns:", len(row))
                    break
            else:
                print("SUCCESS: CSV structure is valid.")

    except (csv.Error, UnicodeError) as error:
        print("CSV ERROR:", error)
        print("Physical line:", reader.line_num)

    print("Records successfully read:", count)
    print("Expected columns:", len(header))
