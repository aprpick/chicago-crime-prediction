import pandas as pd
from datetime import datetime
import meteostat as ms  # New style import
import os

print("=" * 70)
print("DOWNLOADING CHICAGO WEATHER DATA (2023-2025)")
print("=" * 70)

script_dir = os.path.dirname(os.path.abspath(__file__))
output_file = os.path.join(script_dir, '15_chicago_weather_2023_2025.csv')

print("\n[1/2] Fetching data from Meteostat...")
print("      Station: Chicago O'Hare (72530 / KORD)")
print("      Period: 2023-2025")

# Chicago O'Hare station ID
station = ms.Station(id='72530')  # New way to specify station

# Date range
start = datetime(2023, 1, 1)
end = datetime(2025, 12, 31, 23, 59)

# Fetch hourly data (new lowercase function)
ts = ms.hourly(station, start, end)
weather = ts.fetch()

if weather is None or weather.empty:
    print("      ✗ No data returned!")
    print("        - Check internet")
    print("        - Delete cache: C:\\Users\\14037\\.meteostat\\cache")
    print("        - Test shorter range first")
    exit()

print(f"      ✓ Downloaded {len(weather):,} hourly records")

# Make datetime a column
weather = weather.reset_index()
weather = weather.rename(columns={'time': 'datetime'})

print("\n      Available columns:")
for col in weather.columns:
    print(f"        - {col}")

print("\n[2/2] Saving to CSV...")
weather.to_csv(output_file, index=False)

file_size_mb = os.path.getsize(output_file) / (1024 * 1024)

print("\n" + "=" * 70)
print("✓ COMPLETE!")
print("=" * 70)
print(f"File: {output_file}")
print(f"Rows: {len(weather):,}")
print(f"Columns: {len(weather.columns)}")
print(f"Size: {file_size_mb:.1f} MB")
print(f"Date range: {weather['datetime'].min()} to {weather['datetime'].max()}")
print("=" * 70)

print("\nColumns explanation:")
print("  temp  = Temperature (°C)")
print("  dwpt  = Dew point (°C)")
print("  rhum  = Relative humidity (%)")
print("  prcp  = Precipitation (mm/hour)")
print("  wspd  = Wind speed (km/h)")
print("  wdir  = Wind direction (°)")
print("  pres  = Pressure (hPa)")
print("  coco  = Weather condition code")
print("\nNote: Missing values appear as NaN")
print("=" * 70)