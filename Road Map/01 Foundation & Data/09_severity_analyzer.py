"""
Analyze Primary Types with their Description subcategories
Shows hierarchical structure for severity assessment
Reads from: 08.1_enforcement_crimes_removed.csv
Writes to: 09.1_severity_hierarchy.md
"""

# ============================================================
# FILE PATHS - CONFIGURE HERE
# ============================================================
INPUT_FILE = '08.1_enforcement_crimes_removed.csv'
OUTPUT_FILE = '09.1_severity_hierarchy.md'
# ============================================================

import pandas as pd
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
input_file = os.path.join(script_dir, INPUT_FILE)
output_file = os.path.join(script_dir, OUTPUT_FILE)

print(f"Analyzing crime hierarchy in: {INPUT_FILE}")
print(f"Writing analysis to: {OUTPUT_FILE}")

df = pd.read_csv(input_file)

# --- BUILD MARKDOWN REPORT ---
lines = []
lines.append("# Crime Severity Hierarchy Analysis")
lines.append("")
lines.append(f"**Input File:** `{INPUT_FILE}`  ")
lines.append(f"**Analysis Date:** {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}")
lines.append("")
lines.append("---")
lines.append("")
lines.append("## Overview")
lines.append("")
lines.append(f"| Metric | Value |")
lines.append(f"|--------|-------|")
lines.append(f"| Total Crimes | {len(df):,} |")
lines.append(f"| Unique Primary Types | {df['Primary Type'].nunique()} |")
lines.append(f"| Unique Descriptions | {df['Description'].nunique()} |")
lines.append("")
lines.append("---")
lines.append("")

# Get Primary Type totals
primary_totals = df['Primary Type'].value_counts()

# Group by Primary Type, then show all descriptions
for primary_type in sorted(primary_totals.index):
    primary_count = primary_totals[primary_type]
    primary_pct = (primary_count / len(df)) * 100
    
    lines.append(f"## {primary_type}")
    lines.append("")
    lines.append(f"**Total:** {primary_count:,} crimes ({primary_pct:.2f}%)")
    lines.append("")
    
    # Get all descriptions for this primary type
    descriptions = df[df['Primary Type'] == primary_type]['Description'].value_counts()
    
    lines.append(f"**Subcategories:** {len(descriptions)}")
    lines.append("")
    lines.append("| Description | Count | % of Type | % Overall |")
    lines.append("|-------------|-------|-----------|-----------|")
    
    for desc, count in descriptions.items():
        desc_pct = (count / primary_count) * 100
        overall_pct = (count / len(df)) * 100
        lines.append(f"| {desc} | {count:,} | {desc_pct:.1f}% | {overall_pct:.2f}% |")
    
    lines.append("")
    lines.append("---")
    lines.append("")

# Summary statistics
lines.append("## Summary Statistics")
lines.append("")
lines.append(f"**Total Primary Types:** {df['Primary Type'].nunique()}")
lines.append("")

# Count subcategories per primary type
subcats_per_primary = df.groupby('Primary Type')['Description'].nunique()

lines.append("### Subcategories per Primary Type")
lines.append("")
lines.append(f"| Statistic | Value |")
lines.append(f"|-----------|-------|")
lines.append(f"| Minimum | {subcats_per_primary.min()} subcategories |")
lines.append(f"| Maximum | {subcats_per_primary.max()} subcategories |")
lines.append(f"| Average | {subcats_per_primary.mean():.1f} subcategories |")
lines.append("")

lines.append("### Primary Types with Most Subcategories")
lines.append("")
lines.append("| Primary Type | Subcategories |")
lines.append("|--------------|---------------|")

top_subcats = subcats_per_primary.sort_values(ascending=False).head(5)
for primary, count in top_subcats.items():
    lines.append(f"| {primary} | {count} |")

lines.append("")
lines.append("---")
lines.append("")
lines.append("> **Note:** Use this analysis to assign severity scores in the next step.")
lines.append("")
lines.append("*End of Report*")

# --- WRITE TO FILE ---
with open(output_file, 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines))

# Make read-only
import stat
os.chmod(output_file, stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH)

print(f"\n✓ Analysis complete!")
print(f"✓ Report saved to: {OUTPUT_FILE}")
print(f"✓ File set to read-only")