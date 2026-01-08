"""
Add severity scores using complete mapping of all 88 combinations
Reads from: 10.1_rare_combos_removed.csv
Writes to: 11.1_severity_added.csv
"""

# ============================================================
# FILE PATHS - CONFIGURE HERE
# ============================================================
INPUT_FILE = '10.1_rare_combos_removed.csv'
OUTPUT_FILE = '11.1_severity_added.csv'
# ============================================================

import pandas as pd
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
input_file = os.path.join(script_dir, INPUT_FILE)
output_file = os.path.join(script_dir, OUTPUT_FILE)

print("=" * 80)
print("ADDING SEVERITY SCORES (Complete 88-combination mapping)")
print("=" * 80)
print(f"\nInput:  {INPUT_FILE}")
print(f"Output: {OUTPUT_FILE}")

# ============================================================================
# COMPLETE SEVERITY MAPPING (Primary Type, Description) -> Severity Score
# ============================================================================
severity_mapping = {
    # HOMICIDE (10) - Maximum severity
    ('HOMICIDE', 'FIRST DEGREE MURDER'): 10,
    
    # ASSAULT - Grouped by weapon type
    ('ASSAULT', 'AGGRAVATED - HANDGUN'): 9,
    ('ASSAULT', 'AGGRAVATED - OTHER FIREARM'): 9,
    ('ASSAULT', 'AGGRAVATED PROTECTED EMPLOYEE - HANDGUN'): 9,
    ('ASSAULT', 'AGGRAVATED - KNIFE / CUTTING INSTRUMENT'): 8,
    ('ASSAULT', 'AGGRAVATED - OTHER DANGEROUS WEAPON'): 8,
    ('ASSAULT', 'AGGRAVATED PROTECTED EMPLOYEE - OTHER DANGEROUS WEAPON'): 8,
    ('ASSAULT', 'AGGRAVATED POLICE OFFICER - OTHER DANGEROUS WEAPON'): 8,
    ('ASSAULT', 'SIMPLE'): 5,
    ('ASSAULT', 'PROTECTED EMPLOYEE - HANDS, FISTS, FEET, NO / MINOR INJURY'): 6,
    ('ASSAULT', 'AGGRAVATED POLICE OFFICER - HANDS, FISTS, FEET, NO INJURY'): 6,
    
    # BATTERY - Grouped by weapon/aggravation
    ('BATTERY', 'AGGRAVATED - HANDGUN'): 9,
    ('BATTERY', 'AGGRAVATED - KNIFE / CUTTING INSTRUMENT'): 8,
    ('BATTERY', 'AGGRAVATED - OTHER DANGEROUS WEAPON'): 8,
    ('BATTERY', 'AGGRAVATED POLICE OFFICER - OTHER DANGEROUS WEAPON'): 8,
    ('BATTERY', 'AGGRAVATED PROTECTED EMPLOYEE - OTHER DANGEROUS WEAPON'): 8,
    ('BATTERY', 'AGGRAVATED OF A SENIOR CITIZEN'): 7,
    ('BATTERY', 'AGGRAVATED OF A CHILD'): 7,
    ('BATTERY', 'AGGRAVATED - HANDS, FISTS, FEET, SERIOUS INJURY'): 7,
    ('BATTERY', 'AGGRAVATED P.O. - HANDS, FISTS, FEET, SERIOUS INJURY'): 7,
    ('BATTERY', 'AGG. PROTECTED EMPLOYEE - HANDS, FISTS, FEET, SERIOUS INJURY'): 7,
    ('BATTERY', 'AGGRAVATED - HANDS, FISTS, FEET, NO / MINOR INJURY'): 5,
    ('BATTERY', 'AGGRAVATED P.O. - HANDS, FISTS, FEET, NO / MINOR INJURY'): 5,
    ('BATTERY', 'PROTECTED EMPLOYEE - HANDS, FISTS, FEET, NO / MINOR INJURY'): 5,
    ('BATTERY', 'SIMPLE'): 4,
    
    # ROBBERY - Grouped by weapon
    ('ROBBERY', 'ARMED - HANDGUN'): 10,
    ('ROBBERY', 'ATTEMPT ARMED - HANDGUN'): 9,
    ('ROBBERY', 'ARMED - OTHER FIREARM'): 10,
    ('ROBBERY', 'AGGRAVATED VEHICULAR HIJACKING'): 10,
    ('ROBBERY', 'VEHICULAR HIJACKING'): 9,
    ('ROBBERY', 'ARMED - KNIFE / CUTTING INSTRUMENT'): 9,
    ('ROBBERY', 'ATTEMPT ARMED - KNIFE / CUTTING INSTRUMENT'): 8,
    ('ROBBERY', 'ARMED - OTHER DANGEROUS WEAPON'): 9,
    ('ROBBERY', 'ATTEMPT ARMED - OTHER DANGEROUS WEAPON'): 8,
    ('ROBBERY', 'AGGRAVATED'): 8,
    ('ROBBERY', 'ATTEMPT AGGRAVATED'): 7,
    ('ROBBERY', 'STRONG ARM - NO WEAPON'): 6,
    ('ROBBERY', 'ATTEMPT STRONG ARM - NO WEAPON'): 5,
    
    # CRIMINAL SEXUAL ASSAULT - Grouped by aggravation
    ('CRIMINAL SEXUAL ASSAULT', 'AGGRAVATED - HANDGUN'): 10,
    ('CRIMINAL SEXUAL ASSAULT', 'PREDATORY'): 10,
    ('CRIMINAL SEXUAL ASSAULT', 'AGGRAVATED - OTHER'): 9,
    ('CRIMINAL SEXUAL ASSAULT', 'NON-AGGRAVATED'): 8,
    ('CRIMINAL SEXUAL ASSAULT', 'ATTEMPT NON-AGGRAVATED'): 7,
    
    # ARSON
    ('ARSON', 'BY FIRE'): 7,
    ('ARSON', 'ATTEMPT ARSON'): 6,
    
    # SEX OFFENSE
    ('SEX OFFENSE', 'AGGRAVATED CRIMINAL SEXUAL ABUSE'): 8,
    ('SEX OFFENSE', 'CRIMINAL SEXUAL ABUSE'): 7,
    ('SEX OFFENSE', 'OTHER'): 6,
    ('SEX OFFENSE', 'NON-CONSENSUAL DISSEMINATION OF PRIVATE SEXUAL IMAGES'): 5,
    ('SEX OFFENSE', 'PUBLIC INDECENCY'): 3,
    
    # BURGLARY - Grouped by force
    ('BURGLARY', 'HOME INVASION'): 6,
    ('BURGLARY', 'FORCIBLE ENTRY'): 5,
    ('BURGLARY', 'UNLAWFUL ENTRY'): 4,
    ('BURGLARY', 'ATTEMPT FORCIBLE ENTRY'): 4,
    ('BURGLARY', 'BURGLARY FROM MOTOR VEHICLE'): 3,
    
    # MOTOR VEHICLE THEFT - Mostly same
    ('MOTOR VEHICLE THEFT', 'AUTOMOBILE'): 4,
    ('MOTOR VEHICLE THEFT', 'TRUCK, BUS, MOTOR HOME'): 4,
    ('MOTOR VEHICLE THEFT', 'CYCLE, SCOOTER, BIKE WITH VIN'): 3,
    ('MOTOR VEHICLE THEFT', 'CYCLE, SCOOTER, BIKE NO VIN'): 3,
    ('MOTOR VEHICLE THEFT', 'ATTEMPT - AUTOMOBILE'): 3,
    ('MOTOR VEHICLE THEFT', 'THEFT / RECOVERY - AUTOMOBILE'): 2,
    
    # CRIMINAL DAMAGE - All similar
    ('CRIMINAL DAMAGE', 'TO VEHICLE'): 3,
    ('CRIMINAL DAMAGE', 'TO PROPERTY'): 3,
    ('CRIMINAL DAMAGE', 'CRIMINAL DEFACEMENT'): 3,
    ('CRIMINAL DAMAGE', 'TO CITY OF CHICAGO PROPERTY'): 3,
    ('CRIMINAL DAMAGE', 'TO STATE SUPPORTED PROPERTY'): 3,
    
    # THEFT - Minor variation by value
    ('THEFT', 'OVER $500'): 2,
    ('THEFT', '$500 AND UNDER'): 2,
    ('THEFT', 'RETAIL THEFT'): 2,
    ('THEFT', 'FROM BUILDING'): 2,
    ('THEFT', 'THEFT FROM MOTOR VEHICLE'): 2,
    ('THEFT', 'POCKET-PICKING'): 3,
    ('THEFT', 'PURSE-SNATCHING'): 3,
    ('THEFT', 'ATTEMPT THEFT'): 1,
    ('THEFT', 'DELIVERY CONTAINER THEFT'): 1,
    
    # CRIMINAL TRESPASS - All similar
    ('CRIMINAL TRESPASS', 'TO LAND'): 2,
    ('CRIMINAL TRESPASS', 'TO RESIDENCE'): 3,
    ('CRIMINAL TRESPASS', 'TO VEHICLE'): 2,
    ('CRIMINAL TRESPASS', 'TO STATE SUP LAND'): 2,
    
    # INTIMIDATION
    ('INTIMIDATION', 'INTIMIDATION'): 3,
    ('INTIMIDATION', 'EXTORTION'): 4,
    
    # PUBLIC PEACE VIOLATION - Varied
    ('PUBLIC PEACE VIOLATION', 'BOMB THREAT'): 5,
    ('PUBLIC PEACE VIOLATION', 'ARSON THREAT'): 4,
    ('PUBLIC PEACE VIOLATION', 'RECKLESS CONDUCT'): 2,
    ('PUBLIC PEACE VIOLATION', 'OTHER VIOLATION'): 2,
    ('PUBLIC PEACE VIOLATION', 'FALSE POLICE REPORT'): 1,
    ('PUBLIC PEACE VIOLATION', 'TIRE DEFLATION DEVICE DEPLOYMENT'): 2,
    ('PUBLIC PEACE VIOLATION', 'PEEPING TOM'): 3,
}

# ============================================================================
# READ DATA AND APPLY
# ============================================================================
print("\n[1/3] Reading data...")
df = pd.read_csv(input_file)
print(f"      Rows: {len(df):,}")

print("\n[2/3] Applying severity scores...")

# Apply severity mapping
df['Severity_Score'] = df.apply(
    lambda row: severity_mapping.get((row['Primary Type'], row['Description']), None),
    axis=1
)

# Check for unmapped combinations
unmapped = df[df['Severity_Score'].isnull()]
if len(unmapped) > 0:
    print(f"\n      ⚠️  WARNING: {len(unmapped):,} rows have no severity score!")
    print("      Unmapped combinations:")
    unmapped_combos = unmapped.groupby(['Primary Type', 'Description']).size()
    for (p_type, desc), count in unmapped_combos.items():
        print(f"        {p_type} - {desc}: {count:,} crimes")
else:
    print("      ✓ All combinations successfully mapped!")

# Show severity distribution
print("\n      Severity score distribution:")
severity_dist = df['Severity_Score'].value_counts().sort_index()
for severity, count in severity_dist.items():
    if not pd.isna(severity):
        pct = (count / len(df)) * 100
        print(f"        Severity {int(severity):2d}: {count:7,} crimes ({pct:5.2f}%)")

# Show examples by severity level
print("\n      Example crimes by severity:")
for severity in sorted(df['Severity_Score'].dropna().unique()):
    examples = df[df['Severity_Score'] == severity][['Primary Type', 'Description']].drop_duplicates().head(3)
    print(f"\n      Severity {int(severity):2d}:")
    for idx, row in examples.iterrows():
        print(f"        - {row['Primary Type']} - {row['Description']}")

# Save to new file
print(f"\n[3/3] Saving to: {OUTPUT_FILE}")
df.to_csv(output_file, index=False)

file_size_mb = os.path.getsize(output_file) / (1024 * 1024)

print("\n" + "=" * 80)
print("✓ COMPLETE!")
print("=" * 80)
print(f"Input:  {INPUT_FILE}")
print(f"Output: {OUTPUT_FILE}")
print(f"Rows: {len(df):,}")
print(f"Columns: {len(df.columns)}")
print(f"File size: {file_size_mb:.1f} MB")
print(f"New column: Severity_Score (1-10)")
if len(df[df['Severity_Score'].notna()]) > 0:
    print(f"Severity range: {int(df['Severity_Score'].min())}-{int(df['Severity_Score'].max())}")
    print(f"Average severity: {df['Severity_Score'].mean():.2f}")
print("=" * 80)