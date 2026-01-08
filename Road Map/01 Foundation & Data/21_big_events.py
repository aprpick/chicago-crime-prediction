"""
Add major_event feature for 3-hour blocks
Reads from: 19.1_school_calendar_added.csv
Writes to: 20.1_major_events_added.csv

Events: St. Patrick's Day Parade, Pride Parade, Chicago Marathon, Lollapalooza
Block flagged as major_event=1 if it overlaps with event hours
"""

# ============================================================
# FILE PATHS - CONFIGURE HERE
# ============================================================
INPUT_FILE = '20.1_school_calendar_added.csv'
OUTPUT_FILE = '21.1_major_events_added.csv'
# ============================================================

import pandas as pd
from datetime import datetime, timedelta
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
input_file = os.path.join(script_dir, INPUT_FILE)
output_file = os.path.join(script_dir, OUTPUT_FILE)

def get_st_patricks_parade_date(year):
    """St. Patrick's Day Parade: Saturday before or on March 17"""
    march_17 = datetime(year, 3, 17)
    day_of_week = march_17.weekday()
    
    if day_of_week == 5:  # Saturday
        return march_17.date()
    else:
        days_back = (day_of_week + 2) % 7
        parade_date = march_17 - timedelta(days=days_back)
        return parade_date.date()

def get_pride_parade_date(year):
    """Pride Parade: Last Sunday in June"""
    june_30 = datetime(year, 6, 30)
    day_of_week = june_30.weekday()
    
    if day_of_week == 6:  # Already Sunday
        return june_30.date()
    else:
        days_back = (day_of_week + 1) % 7
        parade_date = june_30 - timedelta(days=days_back)
        return parade_date.date()

def get_chicago_marathon_date(year):
    """Chicago Marathon: 2nd Sunday in October"""
    oct_1 = datetime(year, 10, 1)
    day_of_week = oct_1.weekday()
    
    if day_of_week == 6:  # Oct 1 is Sunday
        first_sunday = oct_1
    else:
        days_to_sunday = (6 - day_of_week) % 7
        first_sunday = oct_1 + timedelta(days=days_to_sunday)
    
    second_sunday = first_sunday + timedelta(days=7)
    return second_sunday.date()

def get_lollapalooza_dates(year):
    """Lollapalooza: First full weekend in August (Thu-Sun, 4 days)"""
    aug_1 = datetime(year, 8, 1)
    day_of_week = aug_1.weekday()
    
    if day_of_week <= 3:  # Mon-Thu
        days_to_thursday = 3 - day_of_week
    else:  # Fri-Sun, go to next week's Thursday
        days_to_thursday = (3 - day_of_week) % 7
    
    first_thursday = aug_1 + timedelta(days=days_to_thursday)
    
    dates = []
    for i in range(4):
        dates.append((first_thursday + timedelta(days=i)).date())
    
    return dates

def block_overlaps_event(check_date, time_block, year):
    """
    Check if a 3-hour block overlaps with major event hours
    
    Event hours (original):
    - St. Patrick's: 15:00-03:00 next day → Blocks 5,6,7 + next day block 0
    - Pride: 12:00-23:00 → Blocks 4,5,6,7
    - Marathon: 07:00-16:00 → Blocks 2,3,4,5
    - Lollapalooza: 11:00-22:00 (4 days) → Blocks 3,4,5,6,7
    
    3-hour blocks:
    0: 00-03, 1: 03-06, 2: 06-09, 3: 09-12, 4: 12-15, 5: 15-18, 6: 18-21, 7: 21-24
    """
    # Get all event dates for this year
    st_patricks = get_st_patricks_parade_date(year)
    pride = get_pride_parade_date(year)
    marathon = get_chicago_marathon_date(year)
    lolla_dates = get_lollapalooza_dates(year)
    
    # St. Patrick's Day: 15:00-03:00 (blocks 5,6,7 same day + block 0 next day)
    if check_date == st_patricks and time_block in [5, 6, 7]:
        return 1
    st_patricks_next = st_patricks + timedelta(days=1)
    if check_date == st_patricks_next and time_block == 0:
        return 1
    
    # Pride Parade: 12:00-23:00 (blocks 4,5,6,7)
    if check_date == pride and time_block in [4, 5, 6, 7]:
        return 1
    
    # Chicago Marathon: 07:00-16:00 (blocks 2,3,4,5)
    if check_date == marathon and time_block in [2, 3, 4, 5]:
        return 1
    
    # Lollapalooza: 11:00-22:00 for 4 days (blocks 3,4,5,6,7)
    if check_date in lolla_dates and time_block in [3, 4, 5, 6, 7]:
        return 1
    
    return 0

print("=" * 70)
print("ADDING MAJOR EVENTS FEATURE (3-HOUR BLOCKS)")
print("=" * 70)
print(f"\nInput:  {INPUT_FILE}")
print(f"Output: {OUTPUT_FILE}")

# Load data
print("\n[1/3] Reading 3-hour block data...")
df = pd.read_csv(input_file)
df['block_datetime'] = pd.to_datetime(df['block_datetime'])
print(f"      Rows: {len(df):,}")
print(f"      Current columns: {list(df.columns)}")

# Add major_event feature
print("\n[2/3] Adding major_event feature...")
print("      Events tracked:")
print("        - St. Patrick's Parade: 3pm-3am (blocks 5,6,7,0)")
print("        - Pride Parade: 12pm-11pm (blocks 4,5,6,7)")
print("        - Chicago Marathon: 7am-4pm (blocks 2,3,4,5)")
print("        - Lollapalooza: 11am-10pm, 4 days (blocks 3,4,5,6,7)")

df['block_date'] = df['block_datetime'].dt.date
df['year'] = df['block_datetime'].dt.year

df['major_event'] = df.apply(
    lambda row: block_overlaps_event(row['block_date'], row['time_block'], row['year']),
    axis=1
)

# Drop temporary columns
df = df.drop(['block_date', 'year'], axis=1)

# Statistics
total_rows = len(df)
event_blocks = df['major_event'].sum()

print(f"\n      Statistics:")
print(f"        Total blocks: {total_rows:,}")
print(f"        Event blocks: {event_blocks:,} ({event_blocks/total_rows*100:.2f}%)")

# Show which events were found
print("\n      Events detected by year:")
years = df['block_datetime'].dt.year.unique()
for year in sorted(years):
    print(f"\n      {year}:")
    print(f"        St. Patrick's: {get_st_patricks_parade_date(year)}")
    print(f"        Pride: {get_pride_parade_date(year)}")
    print(f"        Marathon: {get_chicago_marathon_date(year)}")
    lolla = get_lollapalooza_dates(year)
    print(f"        Lollapalooza: {lolla[0]} to {lolla[-1]} (4 days)")

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
print("\nEvent block mappings:")
print("  St. Patrick's: Blocks 5,6,7 (same day) + 0 (next day)")
print("  Pride: Blocks 4,5,6,7")
print("  Marathon: Blocks 2,3,4,5")
print("  Lollapalooza: Blocks 3,4,5,6,7 (4 days)")
print("=" * 70)

# Show sample of event blocks
event_samples = df[df['major_event'] == 1][['block_datetime', 'time_block', 'major_event']].head(20)
if len(event_samples) > 0:
    print("\n=== SAMPLE EVENT BLOCKS ===")
    print(event_samples)
print("=" * 70)