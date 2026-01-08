"""
Add weather discomfort indices (heat and cold)
Reads from: 15.1_weather_data_added.csv
Writes to: 16.1_weather_DI_added.csv
"""

# ============================================================
# FILE PATHS - CONFIGURE HERE
# ============================================================
INPUT_FILE = '15.1_weather_data_added.csv'
OUTPUT_FILE = '16.1_weather_DI_added.csv'
# ============================================================

import pandas as pd
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
input_file = os.path.join(script_dir, INPUT_FILE)
output_file = os.path.join(script_dir, OUTPUT_FILE)

print("=" * 70)
print("ADDING WEATHER DISCOMFORT INDICES")
print("=" * 70)
print(f"\nInput:  {INPUT_FILE}")
print(f"Output: {OUTPUT_FILE}")

# Load Data
print("\n[1/3] Reading crime + weather data...")
if not os.path.exists(input_file):
    print(f"❌ Error: Could not find {input_file}")
    exit()

df = pd.read_csv(input_file)
print(f"      Rows: {len(df):,}")
print(f"      Current columns: {len(df.columns)}")

print("\n[2/3] Calculating discomfort indices...")

# --- HEAT DISCOMFORT (Thom Index) ---
# Best for predicting irritability/violence spikes in summer
df['heat_DI'] = df['temp'] - 0.55 * (1 - 0.01 * df['rhum']) * (df['temp'] - 14.5)
# We "clip" this at 21 because values below that don't represent heat stress
df['heat_DI'] = df['heat_DI'].clip(lower=21).round(2)

# --- COLD DISCOMFORT (Wind Chill) ---
# Best for predicting "empty streets" and lower crime in winter
# Formula only applies if temp <= 10°C and wind > 4.8 km/h
def get_wind_chill(row):
    t = row['temp']
    v = row['wspd']
    if t <= 10 and v > 4.8:
        return 13.12 + (0.6215 * t) - (11.37 * (v**0.16)) + (0.3965 * t * (v**0.16))
    return t  # If it's warm, the "discomfort" is just the base temp

df['cold_DI'] = df.apply(get_wind_chill, axis=1).round(2)

print("      ✓ Added: heat_DI, cold_DI")

# Statistics
print(f"\n      Heat Discomfort (Thom Index):")
print(f"        Range: {df['heat_DI'].min():.1f}°C to {df['heat_DI'].max():.1f}°C")
print(f"        Average: {df['heat_DI'].mean():.1f}°C")
print(f"        High heat stress (>30°C): {(df['heat_DI'] > 30).sum():,} records ({(df['heat_DI'] > 30).sum()/len(df)*100:.1f}%)")

print(f"\n      Cold Discomfort (Wind Chill):")
print(f"        Range: {df['cold_DI'].min():.1f}°C to {df['cold_DI'].max():.1f}°C")
print(f"        Average: {df['cold_DI'].mean():.1f}°C")
print(f"        Extreme cold (<-10°C): {(df['cold_DI'] < -10).sum():,} records ({(df['cold_DI'] < -10).sum()/len(df)*100:.1f}%)")

# Save the results
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
print("\nDiscomfort indices added:")
print("  heat_DI  = Thom Heat Index (°C) - irritability/violence predictor")
print("  cold_DI  = Wind Chill (°C) - empty streets predictor")
print("=" * 70)

print("\n=== Sample Data ===")
print(df[['Date', 'temp', 'rhum', 'wspd', 'heat_DI', 'cold_DI']].head(10))
print("=" * 70)