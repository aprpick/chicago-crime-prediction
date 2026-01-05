"""
Create 100-row preview CSV for quick testing
"""

import pandas as pd
import os

# Get the directory where this script is located
script_dir = os.path.dirname(os.path.abspath(__file__))

# Path to your Chicago crime CSV (in same folder as this script)
csv_file = os.path.join(script_dir, 'chicago_crime_2023_2025(working).csv')
output_file = os.path.join(script_dir, '02_preview.csv')

print("=" * 70)
print("CREATING PREVIEW CSV")
print("=" * 70)

# Read only first 100 rows (very fast!)
print(f"\nReading first 100 rows from: {csv_file}")
df = pd.read_csv(csv_file, nrows=100)

print(f"✓ Loaded {len(df)} rows with {len(df.columns)} columns")

# Save to new CSV
print(f"\nSaving to: {output_file}")
df.to_csv(output_file, index=False)

print(f"✓ Saved successfully!")

# Quick summary
print("\n" + "=" * 70)
print("PREVIEW SUMMARY:")
print("=" * 70)
print(f"Rows: {len(df)}")
print(f"Columns: {len(df.columns)}")

if 'Date' in df.columns:
    print(f"Date range: {df['Date'].min()} to {df['Date'].max()}")

if 'Primary Type' in df.columns:
    print(f"\nCrime types in preview:")
    for crime, count in df['Primary Type'].value_counts().head(5).items():
        print(f"  {crime}: {count}")

print("\n" + "=" * 70)
print(f"✓ Done! Use '02_preview.csv' for quick testing")
print("=" * 70)