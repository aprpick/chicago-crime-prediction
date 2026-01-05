"""
Trim dataset to only essential columns (3 columns)
"""

import pandas as pd
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
input_file = os.path.join(script_dir, '15_chicago_weather_2023_2025.csv')
output_file = os.path.join(script_dir, '15_chicago_weather_2023_2025.csv')

print("=" * 70)
print("TRIMMING WEATHER DATASET TO ESSENTIAL COLUMNS (3 COLUMNS)")
print("=" * 70)

# Columns to keep (3 essential only)
keep_cols = [
    'temp',
    'rhum',
    'prcp',
]

print(f"\nReading: {input_file}")
df = pd.read_csv(input_file)

print(f"Original: {len(df.columns)} columns, {len(df):,} rows")

# Keep only selected columns
df_clean = df[keep_cols].copy()

print(f"Trimmed: {len(df_clean.columns)} columns, {len(df_clean):,} rows")

# Save
df_clean.to_csv(output_file, index=False)

file_size_mb = os.path.getsize(output_file) / (1024 * 1024)

print(f"\n✓ Saved to: {output_file}")
print(f"  Size: {file_size_mb:.1f} MB")
print(f"\nColumns kept:")
for i, col in enumerate(keep_cols, 1):
    print(f"  {i}. {col}")
print("=" * 70)