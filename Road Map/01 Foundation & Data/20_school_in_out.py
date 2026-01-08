"""
Add school_in_session feature for 3-hour blocks
Reads from: 18.1_3hour_blocks_with_zeros.csv
Writes to: 19.1_school_calendar_added.csv

School hours: 8am-3pm (hours 8-14)
Maps to blocks: 2 (06-09), 3 (09-12), 4 (12-15)
Block flagged as school=1 if it overlaps with school hours
"""

# ============================================================
# FILE PATHS - CONFIGURE HERE
# ============================================================
INPUT_FILE = '18.1_3hour_blocks_with_zeros.csv'
OUTPUT_FILE = '20.1_school_calendar_added.csv'
# ============================================================

import pandas as pd
from datetime import datetime, date
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
input_file = os.path.join(script_dir, INPUT_FILE)
output_file = os.path.join(script_dir, OUTPUT_FILE)

# Chicago Public Schools Calendar Data (2023-2025)
SCHOOL_BREAKS = {
    # 2023
    '2023': {
        'winter_break_2022': ('2022-12-19', '2023-01-02'),
        'spring_break': ('2023-03-27', '2023-03-31'),
        'summer_break': ('2023-06-09', '2023-08-20'),
        'thanksgiving': ('2023-11-20', '2023-11-24'),
        'winter_break_2023': ('2023-12-22', '2024-01-07'),
    },
    
    # 2024
    '2024': {
        'spring_break': ('2024-03-25', '2024-03-29'),
        'summer_break': ('2024-06-07', '2024-08-25'),
        'thanksgiving': ('2024-11-25', '2024-11-29'),
        'winter_break': ('2024-12-23', '2025-01-03'),
    },
    
    # 2025
    '2025': {
        'spring_break': ('2025-03-24', '2025-03-28'),
        'summer_break': ('2025-06-13', '2025-08-17'),
        'thanksgiving': ('2025-11-24', '2025-11-28'),
        'winter_break': ('2025-12-22', '2026-01-02'),
    }
}

# Additional single-day holidays/breaks
SINGLE_DAY_BREAKS = {
    '2023': [
        '2023-01-16',  # MLK Day
        '2023-02-20',  # Presidents Day
        '2023-09-04',  # Labor Day
        '2023-10-09',  # Indigenous Peoples Day
        '2023-11-10',  # Veterans Day
    ],
    '2024': [
        '2024-01-15',  # MLK Day
        '2024-02-19',  # Presidents Day
        '2024-09-02',  # Labor Day
        '2024-09-27',  # Professional Development Day
        '2024-10-14',  # Indigenous Peoples Day
        '2024-10-28',  # Parent-Teacher Conference
        '2024-11-11',  # Veterans Day
    ],
    '2025': [
        '2025-01-20',  # MLK Day
        '2025-02-17',  # Presidents Day
        '2025-09-01',  # Labor Day
        '2025-09-26',  # Professional Development Day
        '2025-10-13',  # Indigenous Peoples Day
        '2025-10-27',  # Parent-Teacher Conference
        '2025-11-11',  # Veterans Day
    ]
}

def is_school_day(check_date, year_str):
    """
    Check if a given date is a school day (not weekend, holiday, or break)
    """
    # Check if weekend
    if check_date.weekday() >= 5:  # Saturday = 5, Sunday = 6
        return False
    
    # Check if date is in a break period
    if year_str in SCHOOL_BREAKS:
        for break_name, (start, end) in SCHOOL_BREAKS[year_str].items():
            start_date = datetime.strptime(start, '%Y-%m-%d').date()
            end_date = datetime.strptime(end, '%Y-%m-%d').date()
            
            if start_date <= check_date <= end_date:
                return False
    
    # Check single-day breaks
    if year_str in SINGLE_DAY_BREAKS:
        date_str = check_date.strftime('%Y-%m-%d')
        if date_str in SINGLE_DAY_BREAKS[year_str]:
            return False
    
    return True

def block_overlaps_school_hours(time_block):
    """
    Determine if a 3-hour block overlaps with school hours (8am-3pm)
    School hours: 8-14 (8am to 2:59pm)
    
    Block mapping:
    - Block 0 (00-03): No overlap
    - Block 1 (03-06): No overlap
    - Block 2 (06-09): Partial overlap (hours 8-9)
    - Block 3 (09-12): Full overlap
    - Block 4 (12-15): Partial overlap (hours 12-14)
    - Block 5 (15-18): No overlap
    - Block 6 (18-21): No overlap
    - Block 7 (21-24): No overlap
    """
    # Blocks that overlap school hours: 2, 3, 4
    return time_block in [2, 3, 4]

print("=" * 70)
print("ADDING SCHOOL CALENDAR FEATURE (3-HOUR BLOCKS)")
print("=" * 70)
print(f"\nInput:  {INPUT_FILE}")
print(f"Output: {OUTPUT_FILE}")

# Load data
print("\n[1/3] Reading 3-hour block data...")
df = pd.read_csv(input_file)
df['block_datetime'] = pd.to_datetime(df['block_datetime'])
print(f"      Rows: {len(df):,}")
print(f"      Current columns: {list(df.columns)}")

# Add school_in_session feature
print("\n[2/3] Adding school_in_session feature...")
print("      School hours: 8am-3pm (hours 8-14)")
print("      Blocks flagged: 2 (06-09), 3 (09-12), 4 (12-15)")

df['block_date'] = df['block_datetime'].dt.date
df['year_str'] = df['block_datetime'].dt.year.astype(str)

# Determine if block is during school
df['school_in_session'] = df.apply(
    lambda row: 1 if (
        is_school_day(row['block_date'], row['year_str']) and 
        block_overlaps_school_hours(row['time_block'])
    ) else 0,
    axis=1
)

# Drop temporary columns
df = df.drop(['block_date', 'year_str'], axis=1)

# Statistics
total_rows = len(df)
in_session = df['school_in_session'].sum()
not_in_session = total_rows - in_session

print(f"\n      Statistics:")
print(f"        Total blocks: {total_rows:,}")
print(f"        School in session: {in_session:,} ({in_session/total_rows*100:.1f}%)")
print(f"        School NOT in session: {not_in_session:,} ({not_in_session/total_rows*100:.1f}%)")

# Save
print(f"\n[3/3] Saving to: {OUTPUT_FILE}")
df.to_csv(output_file, index=False)

# Make read-only
import stat
os.chmod(output_file, stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH)

file_size_mb = os.path.getsize(output_file) / (1024 * 1024)

print("\n" + "=" * 70)
print("✓ COMPLETE!")
print("=" * 70)
print(f"Input:  {INPUT_FILE}")
print(f"Output: {OUTPUT_FILE}")
print(f"Rows: {len(df):,}")
print(f"Columns: {len(df.columns)}")
print(f"File size: {file_size_mb:.1f} MB")
print(f"✓ File set to read-only")
print("\nSchool-flagged blocks:")
print("  Block 2 (06-09): Overlaps hours 8-9")
print("  Block 3 (09-12): Full school hours")
print("  Block 4 (12-15): Overlaps hours 12-14")
print("=" * 70)

# Show sample
print("\n=== SAMPLE DATA ===")
sample_cols = ['block_datetime', 'time_block', 'crime_count', 'school_in_session']
print(df[sample_cols].head(20))
print("=" * 70)