"""
Add solar_altitude feature for 3-hour blocks
Reads from: 22.1_moon_phase_added.csv
Writes to: 23.1_solar_altitude_added.csv

Solar altitude: Angle of sun above horizon in degrees (-90 to 90)
Calculated at midpoint of each 3-hour block
"""

# ============================================================
# FILE PATHS - CONFIGURE HERE
# ============================================================
INPUT_FILE = '22.1_moon_phase_added.csv'
OUTPUT_FILE = '23.1_solar_altitude_added.csv'
# ============================================================

import pandas as pd
from astral import LocationInfo
from astral.sun import elevation
import pytz
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
input_file = os.path.join(script_dir, INPUT_FILE)
output_file = os.path.join(script_dir, OUTPUT_FILE)

# Chicago Coordinates
CITY_LAT = 41.8781
CITY_LON = -87.6298
city = LocationInfo("Chicago", "USA", "America/Chicago", CITY_LAT, CITY_LON)
chicago_tz = pytz.timezone("America/Chicago")

def get_solar_altitude_for_block(block_datetime, time_block):
    """
    Calculate solar altitude at the midpoint of a 3-hour block
    
    Block midpoints:
    0 (00-03): 01:30
    1 (03-06): 04:30
    2 (06-09): 07:30
    3 (09-12): 10:30
    4 (12-15): 13:30
    5 (15-18): 16:30
    6 (18-21): 19:30
    7 (21-24): 22:30
    """
    try:
        # Calculate midpoint: block start + 1.5 hours
        midpoint = block_datetime + pd.Timedelta(hours=1, minutes=30)
        
        # Localize to Chicago timezone
        local_dt = chicago_tz.localize(midpoint)
        
        # Calculate solar altitude
        alt = elevation(city.observer, local_dt)
        return round(float(alt), 2)
        
    except Exception:
        return -999.0  # Error value

print("=" * 70)
print("ADDING SOLAR ALTITUDE FEATURE (3-HOUR BLOCKS)")
print("=" * 70)
print(f"\nInput:  {INPUT_FILE}")
print(f"Output: {OUTPUT_FILE}")

# Load data
print("\n[1/3] Reading 3-hour block data...")
df = pd.read_csv(input_file)
df['block_datetime'] = pd.to_datetime(df['block_datetime'])
print(f"      Rows: {len(df):,}")
print(f"      Current columns: {list(df.columns)}")

# Add solar_altitude feature
print("\n[2/3] Calculating solar altitude...")
print("      Location: Chicago (41.88°N, 87.63°W)")
print("      Calculated at midpoint of each 3-hour block")
print("      Range: -90° (below horizon) to 90° (directly overhead)")

df['solar_altitude'] = df.apply(
    lambda row: get_solar_altitude_for_block(row['block_datetime'], row['time_block']),
    axis=1
)

# Statistics
total_rows = len(df)
avg_altitude = df[df['solar_altitude'] != -999.0]['solar_altitude'].mean()
min_altitude = df[df['solar_altitude'] != -999.0]['solar_altitude'].min()
max_altitude = df[df['solar_altitude'] != -999.0]['solar_altitude'].max()

# Count daytime vs nighttime blocks
daytime_count = len(df[df['solar_altitude'] > 0])
nighttime_count = len(df[df['solar_altitude'] <= 0])

print(f"\n      Statistics:")
print(f"        Total blocks: {total_rows:,}")
print(f"        Average altitude: {avg_altitude:.1f}°")
print(f"        Range: {min_altitude:.1f}° to {max_altitude:.1f}°")
print(f"        Daytime blocks (>0°): {daytime_count:,} ({daytime_count/total_rows*100:.1f}%)")
print(f"        Nighttime blocks (≤0°): {nighttime_count:,} ({nighttime_count/total_rows*100:.1f}%)")

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
print("\nSolar altitude interpretation:")
print("  > 0° = Sun above horizon (daytime)")
print("  0° = Sunrise/sunset")
print("  < 0° = Sun below horizon (nighttime)")
print("  -18° = End of astronomical twilight (full darkness)")
print("=" * 70)

# Show sample
print("\n=== SAMPLE SOLAR ALTITUDES ===")
sample = df[['block_datetime', 'time_block', 'solar_altitude', 'crime_count']].head(24)
print(sample)
print("=" * 70)