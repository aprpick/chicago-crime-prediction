"""
Add holiday features (violent holidays and theft holidays)
Reads from: 13.1_weekends_added.csv
Writes to: 14.1_holidays_added.csv
"""

# ============================================================
# FILE PATHS - CONFIGURE HERE
# ============================================================
INPUT_FILE = '13.1_temporals_added.csv'
OUTPUT_FILE = '14.1_holidays_added.csv'
# ============================================================

import pandas as pd
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
input_file = os.path.join(script_dir, INPUT_FILE)
output_file = os.path.join(script_dir, OUTPUT_FILE)

print("=" * 70)
print("ADDING HOLIDAY FEATURES")
print("=" * 70)
print(f"\nInput:  {INPUT_FILE}")
print(f"Output: {OUTPUT_FILE}")

# Violent crime holidays (NYE, July 4th, Thanksgiving)
violent_holidays = [
    # NEW YEAR'S (3 days - 9x violent crime spike)
    '2023-12-30', '2023-12-31', '2024-01-01',
    '2024-12-30', '2024-12-31', '2025-01-01',
    '2025-12-30', '2025-12-31', '2026-01-01',
    
    # JULY 4TH (3 days - most violent day of year)
    '2023-07-03', '2023-07-04', '2023-07-05',
    '2024-07-03', '2024-07-04', '2024-07-05',
    '2025-07-03', '2025-07-04', '2025-07-05',
    
    # THANKSGIVING (2 days - Thu + Black Friday)
    '2023-11-23', '2023-11-24',
    '2024-11-28', '2024-11-29',
    '2025-11-27', '2025-11-28',
]

# Theft/property crime holidays (Christmas shopping, Black Friday)
theft_holidays = [
    # CHRISTMAS SHOPPING PERIOD (6 days - 30% retail theft spike)
    '2023-12-20', '2023-12-21', '2023-12-22', '2023-12-23', '2023-12-24', '2023-12-25',
    '2024-12-20', '2024-12-21', '2024-12-22', '2024-12-23', '2024-12-24', '2024-12-25',
    '2025-12-20', '2025-12-21', '2025-12-22', '2025-12-23', '2025-12-24', '2025-12-25',
    
    # BLACK FRIDAY (already in violent_holidays, but also theft spike)
    '2023-11-24',
    '2024-11-29',
    '2025-11-28',
]

print("\n[1/3] Reading data...")
df = pd.read_csv(input_file)
print(f"      Rows: {len(df):,}")
print(f"      Current columns: {list(df.columns)}")

print("\n[2/3] Adding holiday features...")
df['Date'] = pd.to_datetime(df['Date'])

# Create date string for matching
df['date_only'] = df['Date'].dt.date.astype(str)

# Add violent holiday flag
df['is_violent_holiday'] = df['date_only'].isin(violent_holidays).astype(int)

# Add theft holiday flag
df['is_theft_holiday'] = df['date_only'].isin(theft_holidays).astype(int)

# Drop temp column
df.drop('date_only', axis=1, inplace=True)

print("      ✓ Added: is_violent_holiday, is_theft_holiday")

print("\n" + "=" * 70)
print("PREVIEW")
print("=" * 70)
print(f"\nFinal columns ({len(df.columns)}):")
for i, col in enumerate(df.columns, 1):
    print(f"  {i:2d}. {col}")

print("\nSample rows:")
print(df.head(10).to_string(index=False))

# Show holiday breakdown
violent_count = df['is_violent_holiday'].sum()
theft_count = df['is_theft_holiday'].sum()
both_count = df[(df['is_violent_holiday'] == 1) & (df['is_theft_holiday'] == 1)].shape[0]

print(f"\nHoliday statistics:")
print(f"  Violent holiday crimes: {violent_count:,} ({violent_count/len(df)*100:.2f}%)")
print(f"  Theft holiday crimes: {theft_count:,} ({theft_count/len(df)*100:.2f}%)")
print(f"  Both flags (overlap): {both_count:,} ({both_count/len(df)*100:.2f}%)")
print(f"  Regular days: {len(df) - violent_count - theft_count + both_count:,}")

print(f"\n[3/3] Saving to: {OUTPUT_FILE}")
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
print("\nHoliday features added:")
print("  - is_violent_holiday (NYE, July 4, Thanksgiving)")
print("  - is_theft_holiday (Christmas shopping, Black Friday)")
print("=" * 70)