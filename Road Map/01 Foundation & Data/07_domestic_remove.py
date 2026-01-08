"""
Remove domestic crimes from dataset
Reads from: 05.1_columns_removed.csv
Creates: 07.1_domestics_removed.csv
Also removes the Domestic column after filtering
"""

# ============================================================
# FILE PATHS - CONFIGURE HERE
# ============================================================
INPUT_FILE = '05.1_columns_removed.csv'
OUTPUT_FILE = '07.1_domestics_removed.csv'
# ============================================================

import pandas as pd
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
input_file = os.path.join(script_dir, INPUT_FILE)
output_file = os.path.join(script_dir, OUTPUT_FILE)

print("=" * 70)
print("REMOVING DOMESTIC CRIMES")
print("=" * 70)
print(f"\nInput:  {INPUT_FILE}")
print(f"Output: {OUTPUT_FILE}")

# Read data
print("\n[1/4] Reading data...")
df = pd.read_csv(input_file)
print(f"      Original rows: {len(df):,}")
print(f"      Original columns: {len(df.columns)}")

# Show breakdown
domestic_count = df['Domestic'].sum()  # Count True values
non_domestic_count = len(df) - domestic_count

print(f"\n      Domestic crimes: {domestic_count:,} ({domestic_count/len(df)*100:.1f}%)")
print(f"      Non-domestic crimes: {non_domestic_count:,} ({non_domestic_count/len(df)*100:.1f}%)")

# Filter out domestic crimes
print("\n[2/4] Filtering out domestic crimes...")
df_filtered = df[df['Domestic'] == False].copy()

removed = len(df) - len(df_filtered)
print(f"      Removed: {removed:,} rows")
print(f"      Remaining: {len(df_filtered):,} rows")

# Remove the Domestic column
print("\n[3/4] Removing 'Domestic' column...")
df_filtered = df_filtered.drop('Domestic', axis=1)
print(f"      Remaining columns: {len(df_filtered.columns)}")
print(f"      Columns: {list(df_filtered.columns)}")

# Save to new file
print(f"\n[4/4] Saving to: {OUTPUT_FILE}")
df_filtered.to_csv(output_file, index=False)

file_size_mb = os.path.getsize(output_file) / (1024 * 1024)

print("\n" + "=" * 70)
print("✓ COMPLETE!")
print("=" * 70)
print(f"Input:  {INPUT_FILE}")
print(f"Output: {OUTPUT_FILE}")
print(f"Rows: {len(df_filtered):,}")
print(f"Columns: {len(df_filtered.columns)}")
print(f"File size: {file_size_mb:.1f} MB")
print(f"Domestic crimes removed: {removed:,}")
print(f"'Domestic' column removed: Yes")
print("=" * 70)