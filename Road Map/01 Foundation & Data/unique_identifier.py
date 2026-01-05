"""
Add unique identifier column to dataset
Edits the file directly (overwrites it)
"""

import pandas as pd
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
input_file = os.path.join(script_dir, 'chicago_crime_2001_2025_(raw).csv')

print("=" * 70)
print("ADDING UNIQUE IDENTIFIER COLUMN")
print("=" * 70)
print(f"\nFile: {input_file}")
print("\n⚠️  WARNING: This will overwrite the file directly!")

# Read data
print("\n[1/3] Reading data...")
df = pd.read_csv(input_file)
print(f"      Original rows: {len(df):,}")
print(f"      Original columns: {list(df.columns)}")

# Add unique ID as first column
print("\n[2/3] Adding unique identifier...")
df.insert(0, 'Crime_ID', range(1, len(df) + 1))

print(f"      ID range: 1 to {len(df):,}")
print(f"      New columns: {list(df.columns)}")

# Preview (fixed column name - has space not underscore)
print("\n      Sample data with ID:")
print(df[['Crime_ID', 'Date', 'Primary Type', 'Community Area']].head(10).to_string(index=False))

# Save back to same file
print(f"\n[3/3] Saving to: {input_file}")
df.to_csv(input_file, index=False)

file_size_mb = os.path.getsize(input_file) / (1024 * 1024)

print("\n" + "=" * 70)
print("✓ COMPLETE!")
print("=" * 70)
print(f"Rows: {len(df):,}")
print(f"Columns: {len(df.columns)}")
print(f"File size: {file_size_mb:.1f} MB")
print(f"Unique IDs added: {df['Crime_ID'].nunique():,}")
print("=" * 70)