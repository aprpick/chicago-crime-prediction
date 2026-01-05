"""
Print every 10,000th date value from Chicago crime data
"""

import pandas as pd
import os

# Get script directory and find CSV
script_dir = os.path.dirname(os.path.abspath(__file__))
csv_file = os.path.join(script_dir, 'Crimes_-_2001_to_Present_20260104.csv')

print("=" * 70)
print("SAMPLING EVERY 10,000th ROW - DATE COLUMN")
print("=" * 70)
print(f"\nReading from: {csv_file}")
print("Loading every 10,000th row (this will be fast!)...\n")

# Only read every 10,000th row + Date column only
# Row 0 = header, so skip rows where (row_number % 10000 != 0)
df = pd.read_csv(
    csv_file,
    usecols=['Date'],
    skiprows=lambda x: x % 10000 != 0 and x != 0  # Keep header + every 10,000th row
)

print(f"✓ Loaded {len(df)} rows\n")

# Print all the dates
print("=" * 70)
print("DATES (Every 10,000th row):")
print("=" * 70)

for i, date in enumerate(df['Date'], start=1):
    print(f"Row {i*10000:8d}: {date}")

print("\n" + "=" * 70)
print(f"✓ Printed {len(df)} dates")
print("=" * 70)