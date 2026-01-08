"""
Analyze dataset and write statistics to text file
Reads from: 24.1_training_ready.csv
Writes to: 25.1_dataset_analysis.txt
"""

# ============================================================
# FILE PATHS - CONFIGURE HERE
# ============================================================
INPUT_FILE = '24.1_training_ready.csv'
OUTPUT_FILE = '25.1_dataset_analysis.md'
# ============================================================

import pandas as pd
import numpy as np
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
input_file = os.path.join(script_dir, INPUT_FILE)
output_file = os.path.join(script_dir, OUTPUT_FILE)

def main():
    if not os.path.exists(input_file):
        print(f"ERROR: {input_file} not found.")
        return

    print(f"Scanning {INPUT_FILE} for training estimation...")
    print(f"Writing analysis to: {OUTPUT_FILE}")
    
    # Load data
    df = pd.read_csv(input_file)
    
    # --- METRICS ---
    num_rows = len(df)
    num_cols = len(df.columns)
    memory_usage = df.memory_usage(deep=True).sum() / (1024 * 1024)  # in MB
    
    # Count Numeric vs Text columns
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    text_cols = df.select_dtypes(exclude=[np.number]).columns.tolist()

    # --- BUILD REPORT IN MARKDOWN ---
    lines = []
    lines.append("# Dataset Analysis Report")
    lines.append("")
    lines.append(f"**Input File:** `{INPUT_FILE}`  ")
    lines.append(f"**Analysis Date:** {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## Dataset Overview")
    lines.append("")
    lines.append(f"| Metric | Value |")
    lines.append(f"|--------|-------|")
    lines.append(f"| **Total Rows** | {num_rows:,} |")
    lines.append(f"| **Total Features** | {num_cols} |")
    lines.append(f"| **Memory Usage** | {memory_usage:.2f} MB |")
    lines.append("")
    
    lines.append("## Feature Types")
    lines.append("")
    lines.append(f"### ✅ Numeric Features (Ready to Train): {len(numeric_cols)}")
    lines.append("")
    if len(numeric_cols) > 0:
        for col in numeric_cols:
            lines.append(f"- `{col}`")
    lines.append("")

    lines.append(f"### ⚠️ Text/Object Features: {len(text_cols)}")
    lines.append("")
    if len(text_cols) > 0:
        lines.append("**WARNING:** XGBoost cannot read these directly. Must be encoded first:")
        lines.append("")
        for col in text_cols:
            lines.append(f"- `{col}`")
        lines.append("")
        lines.append("> You must One-Hot Encode or Label Encode these before training")
    else:
        lines.append("✅ **Great!** All data is numeric.")
    lines.append("")

    # --- ESTIMATION MATH ---
    complexity_factor = num_rows * num_cols
    
    lines.append("---")
    lines.append("")
    lines.append("## Estimated Training Time")
    lines.append("*Standard Laptop CPU (8-16GB RAM, 4-8 cores)*")
    lines.append("")
    
    if len(text_cols) > 0:
        lines.append("❌ **CANNOT ESTIMATE** - Text columns must be fixed first")
    else:
        estimated_seconds = (complexity_factor / 200000) 
        
        if estimated_seconds < 60:
            lines.append(f"🚀 **FAST:** ~{estimated_seconds:.1f} seconds")
        else:
            lines.append(f"⏳ **NORMAL:** ~{estimated_seconds/60:.1f} minutes")
    lines.append("")        
    lines.append("> Assumes standard model (100-500 trees). Grid Search multiply by 50x.")
    lines.append("")
    
    lines.append("---")
    lines.append("")
    lines.append("## Column Details")
    lines.append("")
    
    for col in df.columns:
        dtype = df[col].dtype
        null_count = df[col].isnull().sum()
        null_pct = (null_count / num_rows) * 100
        unique_vals = df[col].nunique()
        
        lines.append(f"### `{col}`")
        lines.append("")
        lines.append(f"| Property | Value |")
        lines.append(f"|----------|-------|")
        lines.append(f"| Type | `{dtype}` |")
        lines.append(f"| Null Values | {null_count:,} ({null_pct:.2f}%) |")
        lines.append(f"| Unique Values | {unique_vals:,} |")
        
        if dtype in ['int64', 'float64']:
            lines.append(f"| Min | {df[col].min():.2f} |")
            lines.append(f"| Max | {df[col].max():.2f} |")
            lines.append(f"| Mean | {df[col].mean():.2f} |")
            lines.append(f"| Std Dev | {df[col].std():.2f} |")
        
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

if __name__ == "__main__":
    main()