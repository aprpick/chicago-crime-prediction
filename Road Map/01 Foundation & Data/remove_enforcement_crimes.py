"""
Remove enforcement-driven and non-predictable crimes
Edits the file directly (overwrites it)
"""

import pandas as pd
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
input_file = os.path.join(script_dir, 'chicago_crime_2023_2025_7_rows_(working).csv')

print("=" * 70)
print("REMOVING ENFORCEMENT-DRIVEN AND NON-PREDICTABLE CRIMES")
print("=" * 70)
print(f"\nFile: {input_file}")
print("\n⚠️  WARNING: This will overwrite the file directly!")

# Read data
print("\n[1/4] Reading data...")
df = pd.read_csv(input_file)
print(f"      Original rows: {len(df):,}")

# Crime types to remove
remove_list = [
    # Enforcement-driven (only found when police present)
    'NARCOTICS',
    'WEAPONS VIOLATION',
    'CONCEALED CARRY LICENSE VIOLATION',
    'LIQUOR LAW VIOLATION',
    'PROSTITUTION',
    'GAMBLING',
    'PUBLIC INDECENCY',
    'INTERFERENCE WITH PUBLIC OFFICER',
    'OTHER NARCOTIC VIOLATION',
    'NON-CRIMINAL',
    'HUMAN TRAFFICKING',

    # Too vague or problematic
    'OTHER OFFENSE',
    'OBSCENITY',
    
    # Not time/place predictable
    'STALKING',              # Long-process crime, follows victim
    'DECEPTIVE PRACTICE',    # Fraud/scams, no spatial pattern
    'OFFENSE INVOLVING CHILDREN'  # Vague, privacy concerns
]

# Show breakdown before removal
print(f"\n[2/4] Crime types to remove:")
print("      " + "-" * 66)
total_to_remove = 0
for crime in remove_list:
    count = len(df[df['Primary Type'] == crime])
    pct = (count / len(df)) * 100 if len(df) > 0 else 0
    if count > 0:
        print(f"      {crime:45s}: {count:7,} ({pct:5.2f}%)")
        total_to_remove += count

print("      " + "-" * 66)
print(f"      {'TOTAL TO REMOVE':45s}: {total_to_remove:7,} ({total_to_remove/len(df)*100:5.2f}%)")

# Filter out unwanted crimes
print(f"\n[3/4] Filtering crimes...")
df_filtered = df[~df['Primary Type'].isin(remove_list)].copy()

removed = len(df) - len(df_filtered)
print(f"      Removed: {removed:,} rows")
print(f"      Remaining: {len(df_filtered):,} rows")

# Show what's left
print(f"\n      Remaining crime types ({df_filtered['Primary Type'].nunique()}):")
remaining_crimes = df_filtered['Primary Type'].value_counts()
for crime, count in remaining_crimes.items():
    pct = (count / len(df_filtered)) * 100
    print(f"      {crime:45s}: {count:7,} ({pct:5.2f}%)")

# Save back to same file
print(f"\n[4/4] Saving to: {input_file}")
df_filtered.to_csv(input_file, index=False)

file_size_mb = os.path.getsize(input_file) / (1024 * 1024)

print("\n" + "=" * 70)
print("✓ COMPLETE!")
print("=" * 70)
print(f"Rows: {len(df_filtered):,}")
print(f"File size: {file_size_mb:.1f} MB")
print(f"Crime types removed: {len(remove_list)}")
print(f"Crime types remaining: {df_filtered['Primary Type'].nunique()}")
print(f"Total rows removed: {removed:,} ({removed/len(df)*100:.1f}%)")
print("=" * 70)