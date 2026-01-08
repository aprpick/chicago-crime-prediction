"""
Remove rare PRIMARY TYPE + DESCRIPTION combinations (< 100 crimes)
Reads from: 09.1_severity_analyzed.csv
Writes to: 10.1_rare_combos_removed.csv
"""

# ============================================================
# FILE PATHS - CONFIGURE HERE
# ============================================================
INPUT_FILE = '08.1_enforcement_crimes_removed.csv'
OUTPUT_FILE = '10.1_rare_combos_removed.csv'
THRESHOLD = 100  # Minimum crimes per combination to keep
# ============================================================

import pandas as pd
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
input_file = os.path.join(script_dir, INPUT_FILE)
output_file = os.path.join(script_dir, OUTPUT_FILE)

print("=" * 80)
print(f"REMOVING RARE PRIMARY TYPE + DESCRIPTION COMBINATIONS (< {THRESHOLD} crimes)")
print("=" * 80)
print(f"\nInput:  {INPUT_FILE}")
print(f"Output: {OUTPUT_FILE}")

# Read data
print("\n[1/4] Reading data...")
df = pd.read_csv(input_file)
print(f"      Original rows: {len(df):,}")
print(f"      Original unique combinations: {df.groupby(['Primary Type', 'Description']).ngroups}")

# Get combination counts (Primary Type + Description)
print("\n[2/4] Identifying rare combinations...")
combo_counts = df.groupby(['Primary Type', 'Description']).size()

# Identify rare combinations (< threshold crimes)
rare_combos = combo_counts[combo_counts < THRESHOLD]
keep_combos = combo_counts[combo_counts >= THRESHOLD]

print(f"      Threshold: {THRESHOLD} crimes")
print(f"      Combinations to REMOVE: {len(rare_combos)}")
print(f"      Combinations to KEEP: {len(keep_combos)}")

# Show what we're removing - grouped by Primary Type
print(f"\n      Rare combinations being removed ({len(rare_combos)} total):")
print()

for primary_type in sorted(rare_combos.index.get_level_values(0).unique()):
    primary_rares = rare_combos[rare_combos.index.get_level_values(0) == primary_type]
    
    if len(primary_rares) > 0:
        print(f"      {primary_type}:")
        for (p_type, description), count in primary_rares.items():
            pct = (count / len(df)) * 100
            print(f"        - {description:50s}: {count:5,} ({pct:5.2f}%)")
        print()

# Calculate impact
total_rare_crimes = rare_combos.sum()
total_rare_pct = (total_rare_crimes / len(df)) * 100

print("=" * 80)
print(f"IMPACT SUMMARY:")
print(f"  Total crimes in rare combinations: {total_rare_crimes:,} ({total_rare_pct:.2f}%)")
print(f"  Crimes to keep: {len(df) - total_rare_crimes:,} ({100-total_rare_pct:.2f}%)")
print("=" * 80)

# Filter out rare combinations
print(f"\n[3/4] Filtering data...")
mask = df.apply(
    lambda row: combo_counts.get((row['Primary Type'], row['Description']), 0) >= THRESHOLD,
    axis=1
)
df_filtered = df[mask].copy()

removed = len(df) - len(df_filtered)
removed_pct = (removed / len(df)) * 100

print(f"      Rows removed: {removed:,} ({removed_pct:.2f}%)")
print(f"      Rows remaining: {len(df_filtered):,} ({100-removed_pct:.2f}%)")

# Count unique combinations remaining
remaining_combos = df_filtered.groupby(['Primary Type', 'Description']).ngroups
print(f"      Unique combinations remaining: {remaining_combos}")

# Show what's left per Primary Type
print(f"\n      Subcategories remaining per Primary Type:")
subcats_remaining = df_filtered.groupby('Primary Type')['Description'].nunique().sort_values(ascending=False)
for primary, count in subcats_remaining.items():
    original_count = df[df['Primary Type'] == primary]['Description'].nunique()
    print(f"        {primary:30s}: {count:2d} (was {original_count})")

# Save to new file
print(f"\n[4/4] Saving to: {OUTPUT_FILE}")
df_filtered.to_csv(output_file, index=False)

file_size_mb = os.path.getsize(output_file) / (1024 * 1024)

print("\n" + "=" * 80)
print("✓ COMPLETE!")
print("=" * 80)
print(f"Input:  {INPUT_FILE}")
print(f"Output: {OUTPUT_FILE}")
print(f"Rows: {len(df_filtered):,}")
print(f"Unique combinations: {remaining_combos}")
print(f"File size: {file_size_mb:.1f} MB")
print(f"Data retained: {100-removed_pct:.2f}%")
print("=" * 80)