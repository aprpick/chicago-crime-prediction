"""
Remove rare descriptions (< 100 occurrences)
Edits the file directly (overwrites it)
"""

import pandas as pd
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
input_file = os.path.join(script_dir, 'chicago_crime_2023_2025_7_rows_(working).csv')

print("=" * 70)
print("REMOVING RARE DESCRIPTIONS (< 100 crimes)")
print("=" * 70)
print(f"\nFile: {input_file}")
print("\n⚠️  WARNING: This will overwrite the file directly!")

# Read data
print("\n[1/3] Reading data...")
df = pd.read_csv(input_file)
print(f"      Original rows: {len(df):,}")
print(f"      Original unique descriptions: {df['Description'].nunique()}")

# Get description counts
desc_counts = df['Description'].value_counts()

# Identify rare descriptions (< 100 crimes)
threshold = 100
rare_descriptions = desc_counts[desc_counts < threshold].index.tolist()

print(f"\n[2/3] Filtering descriptions...")
print(f"      Threshold: {threshold} crimes")
print(f"      Descriptions to remove: {len(rare_descriptions)}")
print(f"      Descriptions to keep: {len(desc_counts) - len(rare_descriptions)}")

# Show what we're removing
print(f"\n      Removing these {len(rare_descriptions)} rare descriptions:")
for desc in sorted(rare_descriptions):
    count = desc_counts[desc]
    pct = (count / len(df)) * 100
    print(f"        {desc:50s}: {count:5,} ({pct:5.2f}%)")

# Filter out rare descriptions
df_filtered = df[~df['Description'].isin(rare_descriptions)].copy()

removed = len(df) - len(df_filtered)
removed_pct = (removed / len(df)) * 100

print(f"\n      Rows removed: {removed:,} ({removed_pct:.2f}%)")
print(f"      Rows remaining: {len(df_filtered):,} ({100-removed_pct:.2f}%)")

# Save
print(f"\n[3/3] Saving to: {input_file}")
df_filtered.to_csv(input_file, index=False)

file_size_mb = os.path.getsize(input_file) / (1024 * 1024)

print("\n" + "=" * 70)
print("✓ COMPLETE!")
print("=" * 70)
print(f"Rows: {len(df_filtered):,}")
print(f"Unique descriptions before: {df['Description'].nunique()}")
print(f"Unique descriptions after: {df_filtered['Description'].nunique()}")
print(f"File size: {file_size_mb:.1f} MB")
print(f"Data retained: {100-removed_pct:.2f}%")
print("=" * 70)