"""
Aggregate hourly crime data into 3-hour blocks and add zero-crime blocks
Reads from: 16.1_weather_DI_added.csv
Writes to: 18.1_3hour_blocks_with_zeros.csv

3-HOUR BLOCKS:
  0: 00-03 (midnight-3am)
  1: 03-06 (3am-6am)
  2: 06-09 (6am-9am)
  3: 09-12 (9am-noon)
  4: 12-15 (noon-3pm)
  5: 15-18 (3pm-6pm)
  6: 18-21 (6pm-9pm)
  7: 21-24 (9pm-midnight)
"""

# ============================================================
# FILE PATHS - CONFIGURE HERE
# ============================================================
INPUT_FILE = '16.1_weather_DI_added.csv'
OUTPUT_FILE = '18.1_3hour_blocks_with_zeros.csv'
# ============================================================

import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta

script_dir = os.path.dirname(os.path.abspath(__file__))
input_file = os.path.join(script_dir, INPUT_FILE)
output_file = os.path.join(script_dir, OUTPUT_FILE)

print("=" * 80)
print("AGGREGATING TO 3-HOUR BLOCKS AND ADDING ZERO-CRIME BLOCKS")
print("=" * 80)
print(f"\nInput:  {INPUT_FILE}")
print(f"Output: {OUTPUT_FILE}")

# Load data
print("\n[1/5] Reading hourly crime data...")
df = pd.read_csv(input_file)
df['Date'] = pd.to_datetime(df['Date'])
print(f"      Rows: {len(df):,}")
print(f"      Date range: {df['Date'].min()} to {df['Date'].max()}")
print(f"      Community areas: {df['Community Area'].nunique()}")

# Create 3-hour block identifier
print("\n[2/5] Creating 3-hour time blocks...")
df['time_block'] = df['hour'] // 3  # 0-7 (8 blocks per day)
df['block_date'] = df['Date'].dt.date  # Date without time

print(f"      Time blocks: 0-7 (0=00-03, 1=03-06, ..., 7=21-24)")

# Aggregate crimes into 3-hour blocks
print("\n[3/5] Aggregating crimes by Community Area + Date + Time Block...")
print("      Column operations:")
print("        - crime_count: COUNT of crimes (rows)")
print("        - Severity_Score: SUM of all crime severities")
print("        - Year: FIRST value (all same in block)")
print("        - day_of_week: FIRST value (all same in block)")
print("        - month: FIRST value (all same in block)")
print("        - weekend_night_peak: MAX (1 if ANY hour flagged)")
print("        - weekend_regular: MAX (1 if ANY hour flagged)")
print("        - is_violent_holiday: MAX (1 if ANY hour flagged)")
print("        - is_theft_holiday: MAX (1 if ANY hour flagged)")
print("        - heat_DI: MEAN (average heat stress)")
print("        - cold_DI: MEAN (average cold stress)")

aggregated = df.groupby(['Community Area', 'block_date', 'time_block']).agg({
    'ID': 'count',  # Count crimes
    'Severity_Score': 'sum',  # Sum severity
    'Year': 'first',
    'day_of_week': 'first',
    'month': 'first',
    'weekend_night_peak': 'max',  # 1 if any hour was flagged
    'weekend_regular': 'max',
    'is_violent_holiday': 'max',
    'is_theft_holiday': 'max',
    'heat_DI': 'mean',
    'cold_DI': 'mean'
}).reset_index()

# Rename ID count to crime_count
aggregated = aggregated.rename(columns={'ID': 'crime_count'})

print(f"      Aggregated blocks with crimes: {len(aggregated):,}")

# Generate all possible combinations (Community Area × Date × Time Block)
print("\n[4/5] Generating complete grid (all Community Areas × Dates × Time Blocks)...")

# Get date range
start_date = df['Date'].min().date()
end_date = df['Date'].max().date()
all_dates = pd.date_range(start_date, end_date, freq='D')

# Get all community areas
all_areas = df['Community Area'].dropna().unique()

# Create all combinations
from itertools import product
all_combinations = pd.DataFrame(
    list(product(all_areas, all_dates.date, range(8))),
    columns=['Community Area', 'block_date', 'time_block']
)

print(f"      Total Community Areas: {len(all_areas)}")
print(f"      Total Days: {len(all_dates)}")
print(f"      Time Blocks per day: 8")
print(f"      Total possible blocks: {len(all_combinations):,}")

# Merge to find missing blocks
print("\n      Merging with actual crime data...")
full_data = all_combinations.merge(
    aggregated,
    on=['Community Area', 'block_date', 'time_block'],
    how='left'
)

# Fill missing values (zero-crime blocks)
print("\n      Filling zero-crime blocks...")

# For zero-crime blocks, fill crime_count and Severity_Score with 0
full_data['crime_count'] = full_data['crime_count'].fillna(0).astype(int)
full_data['Severity_Score'] = full_data['Severity_Score'].fillna(0).astype(int)

# For zero-crime blocks, we need to derive Year, day_of_week, month from block_date
full_data['block_date'] = pd.to_datetime(full_data['block_date'])
full_data['Year'] = full_data['Year'].fillna(full_data['block_date'].dt.year).astype(int)
full_data['day_of_week'] = full_data['day_of_week'].fillna(full_data['block_date'].dt.dayofweek).astype(int)
full_data['month'] = full_data['month'].fillna(full_data['block_date'].dt.month).astype(int)

# For zero-crime blocks, calculate weekend/holiday flags based on date and time_block
def calculate_weekend_peak(row):
    if pd.notna(row['weekend_night_peak']):
        return int(row['weekend_night_peak'])
    dow = row['day_of_week']
    tb = row['time_block']
    # Friday (4) block 7 (21-24) OR Saturday (5) block 0 (00-03) OR Saturday block 7 OR Sunday (6) block 0
    if (dow == 4 and tb == 7) or (dow == 5 and (tb == 0 or tb == 7)) or (dow == 6 and tb == 0):
        return 1
    return 0

def calculate_weekend_regular(row):
    if pd.notna(row['weekend_regular']):
        return int(row['weekend_regular'])
    dow = row['day_of_week']
    tb = row['time_block']
    # Friday (4) block 6 (18-21) OR Saturday (5) blocks 1-6 (03-21) OR Sunday (6) blocks 1-7 (03-24)
    if (dow == 4 and tb == 6) or (dow == 5 and 1 <= tb <= 6) or (dow == 6 and tb >= 1):
        return 1
    return 0

full_data['weekend_night_peak'] = full_data.apply(calculate_weekend_peak, axis=1)
full_data['weekend_regular'] = full_data.apply(calculate_weekend_regular, axis=1)

# For holidays, fill with 0 (need actual holiday lookup for zero-crime blocks)
# We'll use a simple approach: if date is in holiday list, flag it
violent_holidays = [
    '2023-12-30', '2023-12-31', '2024-01-01',
    '2024-12-30', '2024-12-31', '2025-01-01',
    '2025-12-30', '2025-12-31', '2026-01-01',
    '2023-07-03', '2023-07-04', '2023-07-05',
    '2024-07-03', '2024-07-04', '2024-07-05',
    '2025-07-03', '2025-07-04', '2025-07-05',
    '2023-11-23', '2023-11-24',
    '2024-11-28', '2024-11-29',
    '2025-11-27', '2025-11-28',
]

theft_holidays = [
    '2023-12-20', '2023-12-21', '2023-12-22', '2023-12-23', '2023-12-24', '2023-12-25',
    '2024-12-20', '2024-12-21', '2024-12-22', '2024-12-23', '2024-12-24', '2024-12-25',
    '2025-12-20', '2025-12-21', '2025-12-22', '2025-12-23', '2025-12-24', '2025-12-25',
    '2023-11-24', '2024-11-29', '2025-11-28',
]

full_data['date_str'] = full_data['block_date'].dt.strftime('%Y-%m-%d')
full_data['is_violent_holiday'] = full_data['is_violent_holiday'].fillna(
    full_data['date_str'].isin(violent_holidays).astype(int)
)
full_data['is_theft_holiday'] = full_data['is_theft_holiday'].fillna(
    full_data['date_str'].isin(theft_holidays).astype(int)
)
full_data = full_data.drop('date_str', axis=1)

# For weather, fill with block average (forward fill, then backward fill)
full_data = full_data.sort_values(['Community Area', 'block_date', 'time_block'])
for col in ['heat_DI', 'cold_DI']:
    full_data[col] = full_data.groupby(['block_date', 'time_block'])[col].transform(
        lambda x: x.fillna(x.mean())
    )

# Round weather values
full_data['heat_DI'] = full_data['heat_DI'].round(2)
full_data['cold_DI'] = full_data['cold_DI'].round(2)

zero_blocks = (full_data['crime_count'] == 0).sum()
crime_blocks = (full_data['crime_count'] > 0).sum()

print(f"      Zero-crime blocks added: {zero_blocks:,}")
print(f"      Blocks with crimes: {crime_blocks:,}")
print(f"      Total blocks: {len(full_data):,}")

# Create readable datetime for the start of each block
print("\n[5/5] Creating block datetime...")
full_data['block_datetime'] = pd.to_datetime(full_data['block_date']) + pd.to_timedelta(full_data['time_block'] * 3, unit='h')

# Reorder columns
final_columns = [
    'Community Area', 'block_datetime', 'time_block', 'Year', 
    'crime_count', 'Severity_Score',
    'day_of_week', 'month',
    'weekend_night_peak', 'weekend_regular',
    'is_violent_holiday', 'is_theft_holiday',
    'heat_DI', 'cold_DI'
]

full_data = full_data[final_columns]

# Save
print(f"\n      Saving to: {OUTPUT_FILE}")
full_data.to_csv(output_file, index=False)

# Make read-only
import stat
os.chmod(output_file, stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH)

file_size_mb = os.path.getsize(output_file) / (1024 * 1024)

print("\n" + "=" * 80)
print("✓ COMPLETE!")
print("=" * 80)
print(f"Input:  {INPUT_FILE}")
print(f"Output: {OUTPUT_FILE}")
print(f"Total 3-hour blocks: {len(full_data):,}")
print(f"  Blocks with crimes: {crime_blocks:,} ({crime_blocks/len(full_data)*100:.1f}%)")
print(f"  Zero-crime blocks: {zero_blocks:,} ({zero_blocks/len(full_data)*100:.1f}%)")
print(f"Columns: {len(full_data.columns)}")
print(f"File size: {file_size_mb:.1f} MB")
print(f"✓ File set to read-only")
print("\n3-hour block encoding:")
print("  0 = 00-03 (midnight-3am)")
print("  1 = 03-06 (3am-6am)")
print("  2 = 06-09 (6am-9am)")
print("  3 = 09-12 (9am-noon)")
print("  4 = 12-15 (noon-3pm)")
print("  5 = 15-18 (3pm-6pm)")
print("  6 = 18-21 (6pm-9pm)")
print("  7 = 21-24 (9pm-midnight)")
print("=" * 80)

# Show sample
print("\n=== SAMPLE DATA ===")
print(full_data.head(20))
print("\n=== CRIME DISTRIBUTION ===")
print(full_data['crime_count'].value_counts().sort_index().head(10))
print("=" * 80)