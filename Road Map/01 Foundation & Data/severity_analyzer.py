"""
Analyze Primary Types with their Description subcategories
Shows hierarchical structure for severity assessment
"""

import pandas as pd
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
input_file = os.path.join(script_dir, 'chicago_crime_2023_2025_7_rows_(working).csv')

print("=" * 80)
print("PRIMARY TYPES AND THEIR DESCRIPTION SUBCATEGORIES")
print("=" * 80)

df = pd.read_csv(input_file)

print(f"\nTotal crimes: {len(df):,}")
print(f"Unique Primary Types: {df['Primary Type'].nunique()}")
print(f"Unique Descriptions: {df['Description'].nunique()}")

# Get Primary Type totals
primary_totals = df['Primary Type'].value_counts()

# Group by Primary Type, then show all descriptions
for primary_type in sorted(primary_totals.index):
    primary_count = primary_totals[primary_type]
    primary_pct = (primary_count / len(df)) * 100
    
    print("\n" + "=" * 80)
    print(f"{primary_type}")
    print(f"TOTAL: {primary_count:,} crimes ({primary_pct:.2f}%)")
    print("=" * 80)
    
    # Get all descriptions for this primary type
    descriptions = df[df['Primary Type'] == primary_type]['Description'].value_counts()
    
    print(f"Subcategories: {len(descriptions)}")
    print()
    
    for desc, count in descriptions.items():
        desc_pct = (count / primary_count) * 100  # Percentage within this primary type
        overall_pct = (count / len(df)) * 100      # Percentage of all crimes
        print(f"  {desc:55s} : {count:7,} ({desc_pct:5.1f}% of {primary_type:20s}, {overall_pct:5.2f}% overall)")

print("\n" + "=" * 80)
print("ANALYSIS COMPLETE")
print("=" * 80)

# Summary statistics
print("\nSUMMARY:")
print(f"Total Primary Types: {df['Primary Type'].nunique()}")

# Count subcategories per primary type
subcats_per_primary = df.groupby('Primary Type')['Description'].nunique()
print(f"\nSubcategories per Primary Type:")
print(f"  Minimum: {subcats_per_primary.min()} subcategories")
print(f"  Maximum: {subcats_per_primary.max()} subcategories")
print(f"  Average: {subcats_per_primary.mean():.1f} subcategories")

print("\nPrimary Types with most subcategories:")
top_subcats = subcats_per_primary.sort_values(ascending=False).head(5)
for primary, count in top_subcats.items():
    print(f"  {primary:30s}: {count} subcategories")