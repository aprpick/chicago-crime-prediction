"""
23_add_moon_phase.py
Adds moon_illumination feature (0-100%) to crime dataset
Moon illumination represents the percentage of the moon's surface that is lit
"""

# ============================================================
# FILE PATHS - CONFIGURE HERE
# ============================================================
INPUT_FILE = 'chicago_crime_2023_2025(working).csv'
# Note: This script overwrites the input file with the new column added

# ============================================================

import pandas as pd
from datetime import datetime
import math

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
    # 0 = new moon, 0.5 = full moon, 1 = new moon again
    phase = (days_since_new % synodic_month) / synodic_month
    
    # Convert phase to illumination percentage
    # Formula: illumination peaks at phase 0.5 (full moon)
    # and is minimum at phase 0 and 1 (new moon)
    illumination = (1 - math.cos(2 * math.pi * phase)) / 2
    
    # Return as percentage (0-100)
    return round(illumination * 100, 2)

def get_moon_phase_name(illumination):
    """
    Convert illumination percentage to moon phase name
    For debugging/verification purposes
    """
    if illumination < 6.25:
        return "New Moon"
    elif illumination < 43.75:
        return "Waxing Crescent"
    elif illumination < 56.25:
        return "First Quarter"
    elif illumination < 93.75:
        return "Waxing Gibbous"
    elif illumination < 106.25:  # Allow for rounding
        return "Full Moon"
    elif illumination < 143.75:
        return "Waning Gibbous"
    elif illumination < 156.25:
        return "Last Quarter"
    else:
        return "Waning Crescent"

def add_moon_illumination_feature(input_file):
    """
    Add moon_illumination feature to crime dataset and overwrite file
    """
    print(f"Loading crime data from: {input_file}")
    df = pd.read_csv(input_file)
    
    print(f"Loaded {len(df):,} rows")
    
    # Parse the Date column
    print("\nParsing dates...")
    df['datetime'] = pd.to_datetime(df['Date'], format='%Y-%m-%d %H:%M:%S')
    
    print("Calculating moon illumination for each record...")
    df['moon_illumination'] = df['datetime'].apply(get_moon_illumination)
    
    # Statistics
    total_rows = len(df)
    avg_illumination = df['moon_illumination'].mean()
    min_illumination = df['moon_illumination'].min()
    max_illumination = df['moon_illumination'].max()
    
    # Count records during different moon phases
    new_moon_count = len(df[df['moon_illumination'] < 25])
    full_moon_count = len(df[df['moon_illumination'] > 75])
    
    print(f"\n=== Moon Illumination Statistics ===")
    print(f"Total records: {total_rows:,}")
    print(f"Average illumination: {avg_illumination:.1f}%")
    print(f"Range: {min_illumination:.1f}% to {max_illumination:.1f}%")
    print(f"\nRecords during new moon (<25%): {new_moon_count:,} ({new_moon_count/total_rows*100:.1f}%)")
    print(f"Records during full moon (>75%): {full_moon_count:,} ({full_moon_count/total_rows*100:.1f}%)")
    
    # Show sample moon phases across the dataset
    print("\n=== Sample Moon Phases ===")
    sample = df[['Date', 'moon_illumination']].head(20).copy()
    sample['moon_phase'] = sample['moon_illumination'].apply(get_moon_phase_name)
    print(sample[['Date', 'moon_illumination', 'moon_phase']])
    
    # Drop the temporary datetime column if it wasn't there originally
    if 'datetime' not in pd.read_csv(input_file, nrows=1).columns:
        df = df.drop('datetime', axis=1)
    
    # Overwrite the original file
    df.to_csv(input_file, index=False)
    print(f"\n✓ Updated file with moon_illumination column: {input_file}")
    
    return df

if __name__ == "__main__":
    print("="*60)
    print("Adding Moon Illumination Feature")
    print("="*60)
    print()
    
    df = add_moon_illumination_feature(INPUT_FILE)
    
    print("\n" + "="*60)
    print("✓ Complete! Moon illumination feature added successfully.")
    print(f"✓ File updated with new 'moon_illumination' column (0-100%).")
    print("="*60)