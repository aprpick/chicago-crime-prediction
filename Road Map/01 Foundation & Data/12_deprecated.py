"""
Drop unnecessary columns from working dataset
Removes: Description, Domestic, Latitude, Longitude
Edits file directly (overwrites it)
"""

exit("deprecated")


import pandas as pd
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
input_file = os.path.join(script_dir, 'chicago_crime_2023_2025(working).csv')

print("=" * 70)
print("DROPPING UNNECESSARY COLUMNS")
print("=" * 70)
print(f"\nFile: {input_file}")
print("\n⚠️  WARNING: This will overwrite the file directly!")

# Read data
print("\n[1/2] Reading data...")
df = pd.read_csv(input_file)
print(f"      Rows: {len(df):,}")
print(f"      Current columns ({len(df.columns)}): {list(df.columns)}")

# Drop unnecessary columns
print("\n[2/2] Dropping columns...")
cols_to_drop = ['Description', 'Domestic', 'Latitude', 'Longitude', 'Primary Type']
existing_drops = [col for col in cols_to_drop if col in df.columns]

if existing_drops:
    df.drop(columns=existing_drops, inplace=True)
    print(f"      ✓ Dropped: {', '.join(existing_drops)}")
    print(f"      Remaining columns ({len(df.columns)}): {list(df.columns)}")
else:
    print("      (No columns to drop - already clean)")

# Preview
print("\n" + "=" * 70)
print("PREVIEW")
print("=" * 70)
print("\nSample rows:")
print(df.head(5).to_string(index=False))

# Save
print(f"\nSaving to: {input_file}")
df.to_csv(input_file, index=False)

file_size_mb = os.path.getsize(input_file) / (1024 * 1024)

print("\n" + "=" * 70)
print("✓ COMPLETE!")
print("=" * 70)
print(f"Rows: {len(df):,}")
print(f"Columns: {len(df.columns)}")
print(f"File size: {file_size_mb:.1f} MB")
print(f"\nColumns remaining: {', '.join(df.columns)}")
print("=" * 70)
