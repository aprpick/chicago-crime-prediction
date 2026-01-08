"""
Remove unnecessary columns from dataset
Reads from: 16.1_weather_DI_added.csv
Writes to: 17.1_columns_truncated.csv
"""

# ============================================================
# FILE PATHS - CONFIGURE HERE
# ============================================================
INPUT_FILE = '16.1_weather_DI_added.csv'
OUTPUT_FILE = '17.1_columns_truncated.csv'

# Columns to REMOVE (list the column names you want to delete)
COLUMNS_TO_REMOVE = [
    'prcp',      # Precipitation
    'wdir',      # Wind direction
    'pres',      # Pressure
    'coco',      # Weather condition code
    'temp',
    'rhum',
    'wspd',
    'Primary Type',
    'Description',
    # Add more columns here as needed
]
# ============================================================

import pandas as pd
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
input_file = os.path.join(script_dir, INPUT_FILE)
output_file = os.path.join(script_dir, OUTPUT_FILE)

print("=" * 70)
print("REMOVING UNNECESSARY COLUMNS")
print("=" * 70)
print(f"\nInput:  {INPUT_FILE}")
print(f"Output: {OUTPUT_FILE}")

# Load data
print("\n[1/3] Reading data...")
df = pd.read_csv(input_file)
print(f"      Rows: {len(df):,}")
print(f"      Original columns: {len(df.columns)}")
print(f"\n      Current columns:")
for i, col in enumerate(df.columns, 1):
    print(f"        {i:2d}. {col}")

# Remove specified columns
print(f"\n[2/3] Removing columns...")
columns_to_remove = [col for col in COLUMNS_TO_REMOVE if col in df.columns]
columns_not_found = [col for col in COLUMNS_TO_REMOVE if col not in df.columns]

if columns_not_found:
    print(f"      ⚠️  Warning: These columns don't exist:")
    for col in columns_not_found:
        print(f"        - {col}")

if columns_to_remove:
    print(f"\n      Removing {len(columns_to_remove)} columns:")
    for col in columns_to_remove:
        print(f"        - {col}")
    
    df = df.drop(columns=columns_to_remove)
    print(f"\n      ✓ Columns removed successfully")
else:
    print(f"      No columns to remove")

print(f"\n      Remaining columns: {len(df.columns)}")
print(f"\n      Final columns:")
for i, col in enumerate(df.columns, 1):
    print(f"        {i:2d}. {col}")

# Save
print(f"\n[3/3] Saving to: {OUTPUT_FILE}")
df.to_csv(output_file, index=False)

# Make read-only
import stat
os.chmod(output_file, stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH)

file_size_mb = os.path.getsize(output_file) / (1024 * 1024)

print("\n" + "=" * 70)
print("✓ COMPLETE!")
print("=" * 70)
print(f"Input:  {INPUT_FILE}")
print(f"Output: {OUTPUT_FILE}")
print(f"Rows: {len(df):,}")
print(f"Original columns: {len(df.columns) + len(columns_to_remove)}")
print(f"Final columns: {len(df.columns)}")
print(f"Columns removed: {len(columns_to_remove)}")
print(f"File size: {file_size_mb:.1f} MB")
print(f"✓ File set to read-only")
print("=" * 70)