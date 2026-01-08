"""
Remove unnecessary columns to prepare data for XGBoost training
Reads from: 23.1_solar_altitude_added.csv
Writes to: 24.1_training_ready.csv
"""

# ============================================================
# FILE PATHS - CONFIGURE HERE
# ============================================================
INPUT_FILE = '23.1_solar_altitude_added.csv'
OUTPUT_FILE = '24.1_training_ready.csv'

# Columns to remove (not needed for training)
DROP_COLUMNS = [
    'block_datetime',  # Already encoded in other features
    'time_block',      # Redundant with time-based features
    'crime_count',     # Not a feature (just for reference)
]
# ============================================================

import pandas as pd
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
input_file = os.path.join(script_dir, INPUT_FILE)
output_file = os.path.join(script_dir, OUTPUT_FILE)

print("=" * 70)
print("PREPARING DATA FOR TRAINING")
print("=" * 70)
print(f"\nInput:  {INPUT_FILE}")
print(f"Output: {OUTPUT_FILE}")

# Load data
print("\n[1/3] Reading data...")
df = pd.read_csv(input_file)
original_rows = len(df)
original_cols = len(df.columns)

print(f"      Rows: {original_rows:,}")
print(f"      Original columns: {original_cols}")

print(f"\n      Current columns:")
for i, col in enumerate(df.columns, 1):
    print(f"        {i:2d}. {col}")

# Remove columns
print(f"\n[2/3] Removing columns...")
print(f"      Columns to drop: {DROP_COLUMNS}")

# Drop columns (ignore if they don't exist)
df = df.drop(columns=DROP_COLUMNS, errors='ignore')

new_cols = len(df.columns)
dropped = original_cols - new_cols

print(f"      Dropped: {dropped} columns")
print(f"      Remaining: {new_cols} columns")

print(f"\n      Final columns:")
for i, col in enumerate(df.columns, 1):
    marker = " ← TARGET" if col == 'Severity_Score' else ""
    print(f"        {i:2d}. {col}{marker}")

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
print(f"Original columns: {original_cols}")
print(f"Final columns: {new_cols}")
print(f"Columns dropped: {dropped}")
print(f"File size: {file_size_mb:.1f} MB")
print(f"✓ File set to read-only")
print("\nReady for XGBoost training!")
print("  Features (X): 14 columns")
print("  Target (y): Severity_Score")
print("=" * 70)