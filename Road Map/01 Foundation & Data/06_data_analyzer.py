"""
Analyze data types and unique values in each column
Reads from: 05.1_columns_removed.csv
Writes to: 06.1_column_analysis.md
"""

# ============================================================
# FILE PATHS - CONFIGURE HERE
# ============================================================
INPUT_FILE = '05.1_columns_removed.csv'
OUTPUT_FILE = '06.1_column_analysis.md'
# ============================================================

import pandas as pd
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
input_file = os.path.join(script_dir, INPUT_FILE)
output_file = os.path.join(script_dir, OUTPUT_FILE)

print(f"Analyzing columns in: {INPUT_FILE}")
print(f"Writing analysis to: {OUTPUT_FILE}")

df = pd.read_csv(input_file)

# --- BUILD MARKDOWN REPORT ---
lines = []
lines.append("# Column Analysis Report")
lines.append("")
lines.append(f"**Input File:** `{INPUT_FILE}`  ")
lines.append(f"**Analysis Date:** {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}")
lines.append("")
lines.append(f"**Total Rows:** {len(df):,}")
lines.append(f"**Total Columns:** {len(df.columns)}")
lines.append("")
lines.append("---")
lines.append("")

# Analyze each column
for col in df.columns:
    unique_count = df[col].nunique()
    null_count = df[col].isnull().sum()
    null_pct = (null_count / len(df)) * 100

    lines.append(f"## `{col}`")
    lines.append("")
    lines.append(f"| Property | Value |")
    lines.append(f"|----------|-------|")
    lines.append(f"| Unique Values | {unique_count:,} |")
    lines.append(f"| Null Values | {null_count:,} ({null_pct:.1f}%) |")
    lines.append("")

    # SPECIAL HANDLING FOR DESCRIPTION - Show with Primary Type
    if col == 'Description':
        lines.append(f"**Data Type:** CATEGORICAL (large set - {unique_count} categories)")
        lines.append("")
        lines.append(f"### ALL {unique_count} Combinations")
        lines.append("*(Format: PRIMARY TYPE - DESCRIPTION)*")
        lines.append("")
        lines.append("| Combination | Count | Percentage |")
        lines.append("|-------------|-------|------------|")

        # Create combined column
        combined = df['Primary Type'] + ' - ' + df['Description']
        value_counts = combined.value_counts()
        
        for value, count in value_counts.items():
            pct = (count / len(df)) * 100
            lines.append(f"| {value} | {count:,} | {pct:.2f}% |")
        lines.append("")

    # If categorical (< 150 unique values), show them all
    elif unique_count < 150:
        lines.append(f"**Data Type:** CATEGORICAL ({unique_count} categories)")
        lines.append("")
        lines.append("### All Values")
        lines.append("")
        lines.append("| Value | Count | Percentage |")
        lines.append("|-------|-------|------------|")
        
        value_counts = df[col].value_counts()
        for value, count in value_counts.items():
            pct = (count / len(df)) * 100
            lines.append(f"| {str(value)} | {count:,} | {pct:.2f}% |")
        lines.append("")

    # If many unique values, show top 50
    elif unique_count < 1000:
        lines.append(f"**Data Type:** CATEGORICAL (large set - {unique_count} categories)")
        lines.append("")
        lines.append("### Top 50 Most Common Values")
        lines.append("")
        lines.append("| Value | Count | Percentage |")
        lines.append("|-------|-------|------------|")
        
        value_counts = df[col].value_counts().head(50)
        for value, count in value_counts.items():
            pct = (count / len(df)) * 100
            lines.append(f"| {str(value)} | {count:,} | {pct:.2f}% |")
        lines.append("")

    # If tons of unique values, probably continuous or free-text
    else:
        lines.append(f"**Data Type:** CONTINUOUS or FREE-TEXT ({unique_count:,} unique values)")
        lines.append("")
        lines.append("### Sample Values")
        lines.append("")
        samples = df[col].dropna().head(10).tolist()
        for sample in samples:
            lines.append(f"- `{sample}`")
        lines.append("")
    
    lines.append("---")
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