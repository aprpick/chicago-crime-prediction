"""
Create filtered dataset - Take first 750K rows (2023-2025 crimes)
Since file is sorted descending by date, row 750K = first 2023 record
"""

import pandas as pd
import os

# Get script directory and find CSV
script_dir = os.path.dirname(os.path.abspath(__file__))
input_file = os.path.join(script_dir, 'chicago_crime_2001_2025_(raw).csv')
output_file = os.path.join(script_dir, 'chicago_crime_2023_2025.csv')

print("=" * 70)
print("CREATING FILTERED DATASET - 2023-2025 (750K ROWS)")
print("=" * 70)

print(f"\n[1/4] Reading first 750,000 rows...")
print("      (This gives us 2023-2025 data)")

# Read first 750K rows - ALL COLUMNS (no usecols needed!)
df = pd.read_csv(input_file, nrows=750000)

print(f"      ✓ Loaded {len(df):,} rows")
print(f"      Columns: {', '.join(df.columns)}")

# Convert Date to datetime to check range
print("\n[2/4] Checking date range...")
df['Date'] = pd.to_datetime(df['Date'], format='%m/%d/%Y %I:%M:%S %p')

print(f"      Date range: {df['Date'].min()} to {df['Date'].max()}")

# Remove rows without coordinates
print("\n[3/4] Removing rows with missing coordinates...")
before = len(df)
df = df.dropna(subset=['Latitude', 'Longitude'])
removed = before - len(df)
print(f"      Removed {removed:,} rows ({removed/before*100:.1f}%)")
print(f"      Remaining: {len(df):,} rows")

# Save
print(f"\n[4/4] Saving to: {output_file}")
df.to_csv(output_file, index=False)

file_size_mb = os.path.getsize(output_file) / (1024 * 1024)

print("\n" + "=" * 70)
print("✓ SUCCESS!")
print("=" * 70)
print(f"File: chicago_crime_2023_2025.csv")
print(f"Rows: {len(df):,}")
print(f"Size: {file_size_mb:.1f} MB")
print(f"Date range: {df['Date'].min().date()} to {df['Date'].max().date()}")
print(f"Crime types: {df['Primary Type'].nunique()}")
print(f"Communities: {df['Community Area'].nunique()}")
print("=" * 70)
print("\n✓ Ready for feature engineering!")