"""
Remove domestic crimes from dataset
Reads from: chicago_crime_2023_2025_7_columns.csv
Creates: chicago_crime_2023_2025_7_rows_(working).csv
"""

import pandas as pd
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
input_file = os.path.join(script_dir, 'chicago_crime_2023_2025(working).csv')
output_file = os.path.join(script_dir, 'chicago_crime_2023_2025(working).csv')

print("=" * 70)
print("REMOVING DOMESTIC CRIMES")
print("=" * 70)
print(f"\nInput:  {input_file}")
print(f"Output: {output_file}")

# Read data
print("\n[1/3] Reading data...")
df = pd.read_csv(input_file)
print(f"      Original rows: {len(df):,}")

# Show breakdown
domestic_count = df['Domestic'].sum()  # Count True values
non_domestic_count = len(df) - domestic_count

print(f"\n      Domestic crimes: {domestic_count:,} ({domestic_count/len(df)*100:.1f}%)")
print(f"      Non-domestic crimes: {non_domestic_count:,} ({non_domestic_count/len(df)*100:.1f}%)")

# Filter out domestic crimes
print("\n[2/3] Filtering out domestic crimes...")
df_filtered = df[df['Domestic'] == False].copy()

removed = len(df) - len(df_filtered)
print(f"      Removed: {removed:,} rows")
print(f"      Remaining: {len(df_filtered):,} rows")

# Save to new file
print(f"\n[3/3] Saving to: {output_file}")
df_filtered.to_csv(output_file, index=False)

file_size_mb = os.path.getsize(output_file) / (1024 * 1024)

print("\n" + "=" * 70)
print("✓ COMPLETE!")
print("=" * 70)
print(f"Input:  chicago_crime_2023_2025_7_columns.csv")
print(f"Output: chicago_crime_2023_2025_7_rows_(working).csv")
print(f"Rows: {len(df_filtered):,}")
print(f"File size: {file_size_mb:.1f} MB")
print(f"Domestic crimes removed: {removed:,}")
print("=" * 70)