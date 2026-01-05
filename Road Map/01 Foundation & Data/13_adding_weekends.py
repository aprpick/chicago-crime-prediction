import pandas as pd
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
input_file = os.path.join(script_dir, 'chicago_crime_2023_2025(working).csv')

print("=" * 70)
print("ADDING TEMPORAL FEATURES")
print("=" * 70)
print(f"\nFile: {input_file}")
print("\n⚠️  WARNING: This will overwrite the file directly!")

us_holidays = [
    '2023-01-01', '2023-01-16', '2023-02-20', '2023-05-29', '2023-07-04', 
    '2023-09-04', '2023-10-09', '2023-11-11', '2023-11-23', '2023-12-25', '2023-12-31',
    '2024-01-01', '2024-01-15', '2024-02-19', '2024-05-27', '2024-07-04',
    '2024-09-02', '2024-10-14', '2024-11-11', '2024-11-28', '2024-12-25', '2024-12-31',
    '2025-01-01', '2025-01-20', '2025-02-17', '2025-05-26', '2025-07-04',
    '2025-09-01', '2025-10-13', '2025-11-11', '2025-11-27', '2025-12-25', '2025-12-31'
]

print("\n[1/2] Reading data...")
df = pd.read_csv(input_file)
print(f"      Rows: {len(df):,}")
print(f"      Current columns: {list(df.columns)}")

print("\n[2/2] Adding temporal features...")
df['Date'] = pd.to_datetime(df['Date'])

df['hour'] = df['Date'].dt.hour
df['day_of_week'] = df['Date'].dt.dayofweek
df['month'] = df['Date'].dt.month

# Weekend night peak: Fri 8pm-Sat 3am, Sat 8pm-Sun 3am
df['weekend_night_peak'] = (
    ((df['day_of_week'] == 4) & (df['hour'] >= 20)) |  # Fri 8pm-11pm
    ((df['day_of_week'] == 5) & (df['hour'] <= 3)) |   # Sat 12am-3am (late Fri)
    ((df['day_of_week'] == 5) & (df['hour'] >= 20)) |  # Sat 8pm-11pm
    ((df['day_of_week'] == 6) & (df['hour'] <= 3))     # Sun 12am-3am (late Sat)
).astype(int)

# Weekend regular: Fri 6-8pm, Sat/Sun daytime (not peak hours)
df['weekend_regular'] = (
    ((df['day_of_week'] == 4) & (df['hour'] >= 18) & (df['hour'] < 20)) |  # Fri 6-8pm
    ((df['day_of_week'] == 5) & (df['hour'] > 3) & (df['hour'] < 20)) |    # Sat 4am-7pm
    ((df['day_of_week'] == 6) & (df['hour'] > 3))                          # Sun after 3am
).astype(int)

# Holidays
df['date_only'] = df['Date'].dt.date.astype(str)
df['is_holiday'] = df['date_only'].isin(us_holidays).astype(int)
df.drop('date_only', axis=1, inplace=True)

print("      ✓ Added: hour, day_of_week, month, weekend_night_peak, weekend_regular, is_holiday")

col_order = ['Crime_ID', 'Date', 'Community Area', 'Severity_Score', 
             'hour', 'day_of_week', 'month', 'weekend_night_peak', 'weekend_regular', 'is_holiday']
col_order = [col for col in col_order if col in df.columns]
df = df[col_order]

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
print(f"  Holiday crimes: {df['is_holiday'].sum():,} ({df['is_holiday'].sum()/len(df)*100:.1f}%)")

print(f"\nSaving to: {input_file}")
df.to_csv(input_file, index=False)

file_size_mb = os.path.getsize(input_file) / (1024 * 1024)

print("\n" + "=" * 70)
print("✓ COMPLETE!")
print("=" * 70)
print(f"Rows: {len(df):,}")
print(f"Columns: {len(df.columns)}")
print(f"File size: {file_size_mb:.1f} MB")
print("\nReady for weather & sports data!")
print("=" * 70)
