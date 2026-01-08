"""
Add moon_illumination feature for 3-hour blocks
Reads from: 20.1_major_events_added.csv
Writes to: 21.1_moon_phase_added.csv

Moon illumination: 0-100% (calculated for each block's start datetime)
"""

# ============================================================
# FILE PATHS - CONFIGURE HERE
# ============================================================
INPUT_FILE = '21.1_major_events_added.csv'
OUTPUT_FILE = '22.1_moon_phase_added.csv'
# ============================================================

import pandas as pd
from datetime import datetime
import math
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
input_file = os.path.join(script_dir, INPUT_FILE)
output_file = os.path.join(script_dir, OUTPUT_FILE)

def get_moon_illumination(date):
    """
    Calculate moon illumination percentage (0-100) for a given date
    Uses astronomical formula based on the synodic month (29.53 days)
    
    Returns: float between 0 (new moon) and 100 (full moon)
    """
    # Known new moon reference date (January 6, 2000 at 18:14 UTC)
    known_new_moon = datetime(2000, 1, 6, 18, 14)
    
    # Synodic month length in days (new moon to new moon)
    synodic_month = 29.53058867
    
    # Calculate days since known new moon
    if isinstance(date, str):
        date = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
    elif not isinstance(date, datetime):
        date = pd.to_datetime(date)
    
    days_since_new = (date - known_new_moon).total_seconds() / 86400
    
    # Calculate current position in lunar cycle (0 to 1)
    phase = (days_since_new % synodic_month) / synodic_month
    
    # Convert phase to illumination percentage
    illumination = (1 - math.cos(2 * math.pi * phase)) / 2
    
    # Return as percentage (0-100)
    return round(illumination * 100, 2)

def get_moon_phase_name(illumination):
    """Convert illumination percentage to moon phase name"""
    if illumination < 6.25:
        return "New Moon"
    elif illumination < 43.75:
        return "Waxing Crescent"
    elif illumination < 56.25:
        return "First Quarter"
    elif illumination < 93.75:
        return "Waxing Gibbous"
    elif illumination < 106.25:
        return "Full Moon"
    elif illumination < 143.75:
        return "Waning Gibbous"
    elif illumination < 156.25:
        return "Last Quarter"
    else:
        return "Waning Crescent"

print("=" * 70)
print("ADDING MOON ILLUMINATION FEATURE (3-HOUR BLOCKS)")
print("=" * 70)
print(f"\nInput:  {INPUT_FILE}")
print(f"Output: {OUTPUT_FILE}")

# Load data
print("\n[1/3] Reading 3-hour block data...")
df = pd.read_csv(input_file)
df['block_datetime'] = pd.to_datetime(df['block_datetime'])
print(f"      Rows: {len(df):,}")
print(f"      Current columns: {list(df.columns)}")

# Add moon_illumination feature
print("\n[2/3] Calculating moon illumination...")
print("      Using block start datetime for each calculation")
print("      Formula: Astronomical calculation based on 29.53-day synodic month")

df['moon_illumination'] = df['block_datetime'].apply(get_moon_illumination)

# Statistics
total_rows = len(df)
avg_illumination = df['moon_illumination'].mean()
min_illumination = df['moon_illumination'].min()
max_illumination = df['moon_illumination'].max()

# Count blocks during different moon phases
new_moon_count = len(df[df['moon_illumination'] < 25])
full_moon_count = len(df[df['moon_illumination'] > 75])

print(f"\n      Statistics:")
print(f"        Total blocks: {total_rows:,}")
print(f"        Average illumination: {avg_illumination:.1f}%")
print(f"        Range: {min_illumination:.1f}% to {max_illumination:.1f}%")
print(f"        New moon blocks (<25%): {new_moon_count:,} ({new_moon_count/total_rows*100:.1f}%)")
print(f"        Full moon blocks (>75%): {full_moon_count:,} ({full_moon_count/total_rows*100:.1f}%)")

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
print("\nMoon illumination: 0-100%")
print("  0% = New Moon (darkest)")
print("  50% = Quarter Moon")
print("  100% = Full Moon (brightest)")
print("=" * 70)

# Show sample
print("\n=== SAMPLE MOON PHASES ===")
sample = df[['block_datetime', 'time_block', 'crime_count', 'moon_illumination']].head(20).copy()
sample['moon_phase'] = sample['moon_illumination'].apply(get_moon_phase_name)
print(sample[['block_datetime', 'moon_illumination', 'moon_phase', 'crime_count']])
print("=" * 70)