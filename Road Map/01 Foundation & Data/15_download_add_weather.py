"""
Download weather data and merge with crime data
Reads from: 14.1_holidays_added.csv
Downloads weather from Meteostat
Writes to: 15.1_weather_data_added.csv
"""

# ============================================================
# FILE PATHS - CONFIGURE HERE
# ============================================================
INPUT_FILE = '14.1_holidays_added.csv'
OUTPUT_FILE = '15.1_weather_data_added.csv'
# ============================================================

import pandas as pd
from datetime import datetime
import meteostat as ms
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
input_file = os.path.join(script_dir, INPUT_FILE)
output_file = os.path.join(script_dir, OUTPUT_FILE)

print("=" * 70)
print("ADDING WEATHER DATA TO CRIME DATASET")
print("=" * 70)
print(f"\nInput:  {INPUT_FILE}")
print(f"Output: {OUTPUT_FILE}")

# Step 1: Load crime data
print("\n[1/4] Reading crime data...")
df = pd.read_csv(input_file)
print(f"      Rows: {len(df):,}")
print(f"      Current columns: {list(df.columns)}")

# Parse dates
df['Date'] = pd.to_datetime(df['Date'])

# Step 2: Download weather data
print("\n[2/4] Downloading weather data from Meteostat...")
print("      Station: Chicago O'Hare (72530 / KORD)")
print("      Period: 2023-2025")

# Chicago O'Hare station ID
station = ms.Station(id='72530')

# Date range
start = datetime(2023, 1, 1)
end = datetime(2025, 12, 31, 23, 59)

# Fetch hourly data
ts = ms.hourly(station, start, end)
weather = ts.fetch()

if weather is None or weather.empty:
    print("      ✗ No weather data returned!")
    print("        - Check internet connection")
    print("        - Try deleting cache: C:\\Users\\14037\\.meteostat\\cache")
    exit()

print(f"      ✓ Downloaded {len(weather):,} hourly weather records")

# Process weather data
weather = weather.reset_index()
weather = weather.rename(columns={'time': 'datetime'})
weather['datetime'] = pd.to_datetime(weather['datetime'])

print(f"      Weather columns: {list(weather.columns)}")

# Step 3: Merge with crime data
print("\n[3/4] Merging weather with crime data...")

# Round both datetimes to nearest hour for matching
df['datetime_rounded'] = df['Date'].dt.round('h')  # Fixed: 'H' -> 'h'
weather['datetime_rounded'] = weather['datetime'].dt.round('h')  # Fixed: 'H' -> 'h'

# Get only columns that actually exist in weather data
weather_cols = ['datetime_rounded', 'temp', 'rhum', 'prcp', 'wspd', 'wdir', 'pres', 'coco']
available_weather_cols = [col for col in weather_cols if col in weather.columns]

# Merge on rounded datetime
df_merged = df.merge(
    weather[available_weather_cols], 
    on='datetime_rounded', 
    how='left'
)

# Drop the temporary rounded column
df_merged = df_merged.drop('datetime_rounded', axis=1)

# Check for unmatched records
unmatched = df_merged['temp'].isna().sum()
if unmatched > 0:
    print(f"      ⚠️  Warning: {unmatched:,} records have no weather data ({unmatched/len(df_merged)*100:.1f}%)")
else:
    print(f"      ✓ All records matched with weather data!")

# Show weather stats
print(f"\n      Weather data statistics:")
print(f"        Temperature range: {df_merged['temp'].min():.1f}°C to {df_merged['temp'].max():.1f}°C")
print(f"        Average temp: {df_merged['temp'].mean():.1f}°C")
print(f"        Humidity range: {df_merged['rhum'].min():.0f}% to {df_merged['rhum'].max():.0f}%")
print(f"        Records with precipitation: {(df_merged['prcp'] > 0).sum():,} ({(df_merged['prcp'] > 0).sum()/len(df_merged)*100:.1f}%)")

# Step 4: Save
print(f"\n[4/4] Saving to: {OUTPUT_FILE}")
df_merged.to_csv(output_file, index=False)

# Make read-only
import stat
os.chmod(output_file, stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH)

file_size_mb = os.path.getsize(output_file) / (1024 * 1024)

print("\n" + "=" * 70)
print("✓ COMPLETE!")
print("=" * 70)
print(f"Input:  {INPUT_FILE}")
print(f"Output: {OUTPUT_FILE}")
print(f"Rows: {len(df_merged):,}")
print(f"Columns: {len(df_merged.columns)}")
print(f"File size: {file_size_mb:.1f} MB")
print(f"✓ File set to read-only")
print("\nWeather columns added:")
print("  temp  = Temperature (°C)")
print("  rhum  = Relative humidity (%)")
print("  prcp  = Precipitation (mm/hour)")
print("  wspd  = Wind speed (km/h)")
print("  wdir  = Wind direction (°)")
print("  pres  = Pressure (hPa)")
print("  coco  = Weather condition code")
print("=" * 70)