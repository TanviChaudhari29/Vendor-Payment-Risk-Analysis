
import csv
import glob
import os

# Find the CSV file inside our Data folder
csv_files = glob.glob(os.path.join("Data", "*.csv"))

if not csv_files:
    print("No CSV file found in the Data folder.")
else:
    file_path = csv_files[0]

    # Open the CSV and read only the first few rows
    with open(file_path, "r", encoding="utf-8-sig", newline="") as file:
        reader = csv.reader(file)

        columns = next(reader)

        print("TOTAL COLUMNS:", len(columns))
        print("\nCOLUMN NAMES:")

        for number, column in enumerate(columns, start=1):
            print(number, column)

        print("\nFIRST 5 RECORDS:")

        for number, row in enumerate(reader, start=1):
            if number > 5:
                break
            print(row)

            
# Check missing values in important columns
print("\nMISSING VALUE ANALYSIS")

fields_to_check = [
    "Supplier & Other Non-Supplier Payees",
    "Purchase Order",
    "Voucher",
    "Contract Number"
]

missing_counts = {field: 0 for field in fields_to_check}
total_rows = 0

with open(file_path, "r", encoding="utf-8-sig", newline="") as file:
    reader = csv.DictReader(file)

    for row in reader:
        total_rows += 1

        for field in fields_to_check:
            if not row[field].strip():
                missing_counts[field] += 1

for field in fields_to_check:
    count = missing_counts[field]
    percentage = (count / total_rows) * 100

    print(f"{field}: {count:,} missing ({percentage:.2f}%)")

    
# Validate payment amount columns
print("\nPAYMENT AMOUNT VALIDATION")

amount_fields = [
    "Vouchers Paid",
    "Vouchers Pending",
    "Vouchers Pending Retainage"
]

invalid_counts = {field: 0 for field in amount_fields}
negative_counts = {field: 0 for field in amount_fields}

with open(file_path, "r", encoding="utf-8-sig", newline="") as file:
    reader = csv.DictReader(file)

    for row in reader:
        for field in amount_fields:
            value = row[field].strip().replace(",", "")

            try:
                amount = float(value)

                if amount < 0:
                    negative_counts[field] += 1

            except ValueError:
                invalid_counts[field] += 1

for field in amount_fields:
    print(f"\n{field}")
    print(f"Invalid or blank amounts: {invalid_counts[field]:,}")
    print(f"Negative amounts: {negative_counts[field]:,}")

import pandas as pd
from pathlib import Path

csv_file = next(Path("Data").glob("*.csv"))

df = pd.read_csv(csv_file, low_memory=False)

print("Dataset shape:", df.shape)
print("\nFirst 5 rows:")
print(df.head())

# Department-wise payment analysis

df["paid_amount"] = pd.to_numeric(
    df["Vouchers Paid"].astype(str).str.replace(",", ""),
    errors="coerce"
)

department_summary = (
    df.groupby("Department")["paid_amount"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

print("\nTOP 10 DEPARTMENTS BY PAID AMOUNT")
print(department_summary)


# Create an initial procurement-focused dataset

procurement_df = df[
    df["Character"].isin([
        "Non-Personnel Services",
        "Materials & Supplies"
    ])
].copy()

print("\nPROCUREMENT-FOCUSED DATASET")
print("Total records:", len(procurement_df))
print("Total paid (USD):", round(procurement_df["paid_amount"].sum(), 2))
print("\nRecords by category:")
print(procurement_df["Character"].value_counts())


# STEP 54: Create payment review indicators

# Negative paid amounts
procurement_df["negative_payment_flag"] = (
    procurement_df["paid_amount"] < 0
)

# 99th percentile of positive amounts within each category
positive_payments = procurement_df["paid_amount"].where(
    procurement_df["paid_amount"] > 0
)

category_thresholds = positive_payments.groupby(
    procurement_df["Character"]
).transform(lambda values: values.quantile(0.99))

procurement_df["high_value_flag"] = (
    (procurement_df["paid_amount"] > 0)
    & (procurement_df["paid_amount"] > category_thresholds)
)

# Combined review indicator
procurement_df["review_flag"] = (
    procurement_df["negative_payment_flag"]
    | procurement_df["high_value_flag"]
)

print("\nPAYMENT REVIEW INDICATORS")
print("Negative payment rows:",
      procurement_df["negative_payment_flag"].sum())
print("High-value payment rows:",
      procurement_df["high_value_flag"].sum())
print("Total review candidate rows:",
      procurement_df["review_flag"].sum())


# STEP 55: Export final dataset for Power BI

from pathlib import Path

output_folder = Path("Data") / "Processed"
output_folder.mkdir(parents=True, exist_ok=True)

output_file = output_folder / "vendor_payment_analysis.csv"

procurement_df.to_csv(output_file, index=False)

print("\nPOWER BI DATASET EXPORTED")
print("File:", output_file)
print("Rows:", len(procurement_df))
print("Columns:", len(procurement_df.columns))


# FINAL RESUME METRICS VERIFICATION

import pandas as pd

data = pd.read_csv("Data/Processed/vendor_payment_analysis.csv")

print("\n===== FINAL PROJECT VERIFICATION =====")

print("Total records:", len(data))

print("Total paid (USD):",
      round(data["paid_amount"].sum(), 2))

print("Expenditure categories:")
print(data["Character"].value_counts())

print("Negative payment records:",
      data["negative_payment_flag"].sum())

print("High-value payment records:",
      data["high_value_flag"].sum())

print("Review candidate records:",
      data["review_flag"].sum())

print("Unique suppliers/payees:",
      data["Supplier & Other Non-Supplier Payees"].nunique())

print("Review rate (%):",
      round(data["review_flag"].mean() * 100, 2))


# BUSINESS INSIGHT: TOP 5 DEPARTMENTS

department_spend = (
    data.groupby("Department")["paid_amount"]
    .sum()
    .sort_values(ascending=False)
)

top_5_spend = department_spend.head(5).sum()
total_spend = data["paid_amount"].sum()

top_5_percentage = (top_5_spend / total_spend) * 100

print("\n===== BUSINESS INSIGHT =====")
print("Top 5 departments:")
print(department_spend.head(5))
print("Top 5 spending share:", round(top_5_percentage, 2), "%")

