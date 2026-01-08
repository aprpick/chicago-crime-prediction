"""
Add temporal features (hour, day_of_week, month, weekend patterns, holidays)
Reads from: 11.1_severity_added.csv
Writes to: 13.1_weekends_added.csv
"""

# ============================================================
# FILE PATHS - CONFIGURE HERE
# ============================================================
INPUT_FILE = '11.1_severity_added.csv'
OUTPUT_FILE = '13.1_weekends_added.csv'
# ============================================================

import pandas as pd
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
input_file = os.path.join(script_dir, INPUT_FILE)
output_file = os.path.join(script_dir, OUTPUT_FILE)

print("=" * 70)
print("ADDING TEMPORAL FEATURES")
print("=" * 70)
print(f"\nInput:  {INPUT_FILE}")
print(f"Output: {OUTPUT_FILE}")

print("\n[1/2] Reading data...")
df = pd.read_csv(input_file)
print(f"      Rows: {len(df):,}")
print(f"      Current columns: {list(df.columns)}")

print("\n[2/2] Adding temporal features...")
df['Date'] = pd.to_datetime(df['Date'])

df['hour'] = df['Date'].dt.hour
df['day_of_week'] = df['Date'].dt.dayofweek
df['month'] = df['Date'].dt.month

# Weekend night peak: Fri/Sat 9pm-midnight, Sat/Sun midnight-3am (aligned to 3-hour blocks)
df['weekend_night_peak'] = (
    ((df['day_of_week'] == 4) & (df['hour'] >= 21)) |  # Fri 9pm-11pm (21-24 block)
    ((df['day_of_week'] == 5) & (df['hour'] < 3)) |    # Sat 12am-2am (00-03 block)
    ((df['day_of_week'] == 5) & (df['hour'] >= 21)) |  # Sat 9pm-11pm (21-24 block)
    ((df['day_of_week'] == 6) & (df['hour'] < 3))      # Sun 12am-2am (00-03 block)
).astype(int)

# Weekend regular: Fri 6-9pm, Sat 3am-9pm, Sun 3am-midnight (aligned to 3-hour blocks)
df['weekend_regular'] = (
    ((df['day_of_week'] == 4) & (df['hour'] >= 18) & (df['hour'] < 21)) |  # Fri 6-9pm (18-21 block)
    ((df['day_of_week'] == 5) & (df['hour'] >= 3) & (df['hour'] < 21)) |   # Sat 3am-9pm (03-21 blocks)
    ((df['day_of_week'] == 6) & (df['hour'] >= 3))                          # Sun 3am-midnight (03-24 blocks)
).astype(int)

print("      ✓ Added: hour, day_of_week, month, weekend_night_peak, weekend_regular")

print("\n" + "=" * 70)
print("PREVIEW")
print("=" * 70)
print(f"\nFinal columns ({len(df.columns)}):")
for i, col in enumerate(df.columns, 1):
    print(f"  {i}. {col}")

print("\nSample rows:")
print(df.head(10).to_string(index=False))

# Show weekend breakdown
weekend_peak_count = df['weekend_night_peak'].sum()
weekend_regular_count = df['weekend_regular'].sum()
weekday_count = len(df) - weekend_peak_count - weekend_regular_count

print(f"\nWeekend period breakdown:")
print(f"  Weekday crimes: {weekday_count:,} ({weekday_count/len(df)*100:.1f}%)")
print(f"  Weekend regular: {weekend_regular_count:,} ({weekend_regular_count/len(df)*100:.1f}%)")
print(f"  Weekend night peak: {weekend_peak_count:,} ({weekend_peak_count/len(df)*100:.1f}%)")

print(f"\nOther statistics:")
print(f"  Hours: {df['hour'].min()}-{df['hour'].max()}")
print(f"  Days: 0-6 (Monday-Sunday)")
print(f"  Months: {df['month'].min()}-{df['month'].max()}")

print(f"\nSaving to: {OUTPUT_FILE}")
df.to_csv(output_file, index=False)

file_size_mb = os.path.getsize(output_file) / (1024 * 1024)

print("\n" + "=" * 70)
print("✓ COMPLETE!")
print("=" * 70)
print(f"Input:  {INPUT_FILE}")
print(f"Output: {OUTPUT_FILE}")
print(f"Rows: {len(df):,}")
print(f"Columns: {len(df.columns)}")
print(f"File size: {file_size_mb:.1f} MB")
print("\nReady for holiday features!")
print("=" * 70)