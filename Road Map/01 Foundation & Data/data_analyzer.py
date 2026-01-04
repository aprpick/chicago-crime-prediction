"""
Analyze data types and unique values in each column
Modified to show Primary Type with Description
"""

import pandas as pd
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
input_file = os.path.join(script_dir, 'chicago_crime_2023_2025_7_rows_(working).csv')

print("=" * 70)
print("DATA TYPE ANALYSIS")
print("=" * 70)

df = pd.read_csv(input_file)

print(f"\nTotal rows: {len(df):,}\n")

# Analyze each column
for col in df.columns:
    unique_count = df[col].nunique()
    null_count = df[col].isnull().sum()
    null_pct = (null_count / len(df)) * 100
    
    print("=" * 70)
    print(f"COLUMN: {col}")
    print("=" * 70)
    print(f"Unique values: {unique_count:,}")
    print(f"Null values: {null_count:,} ({null_pct:.1f}%)")
    
    # SPECIAL HANDLING FOR DESCRIPTION - Show with Primary Type
    if col == 'Description':
        print(f"\nData type: CATEGORICAL (large set - {unique_count} categories)")
        print("\nTop 20 most common (showing as 'PRIMARY TYPE - DESCRIPTION'):")
        
        # Create combined column
        combined = df['Primary Type'] + ' - ' + df['Description']
        value_counts = combined.value_counts().head(20)
        
        for value, count in value_counts.items():
            pct = (count / len(df)) * 100
            print(f"  {value:60s}: {count:7,} ({pct:5.2f}%)")
    
    # If categorical (< 100 unique values), show them all
    elif unique_count < 100:
        print(f"\nData type: CATEGORICAL ({unique_count} categories)")
        print("\nAll values with counts:")
        value_counts = df[col].value_counts()
        for value, count in value_counts.items():
            pct = (count / len(df)) * 100
            print(f"  {str(value):50s}: {count:7,} ({pct:5.2f}%)")
    
    # If many unique values, show top 20
    elif unique_count < 1000:
        print(f"\nData type: CATEGORICAL (large set - {unique_count} categories)")
        print("\nTop 20 most common values:")
        value_counts = df[col].value_counts().head(20)
        for value, count in value_counts.items():
            pct = (count / len(df)) * 100
            print(f"  {str(value):50s}: {count:7,} ({pct:5.2f}%)")
    
    # If tons of unique values, probably continuous or free-text
    else:
        print(f"\nData type: CONTINUOUS or FREE-TEXT ({unique_count:,} unique values)")
        print("\nSample values:")
        print(df[col].dropna().head(10).to_string(index=False))
    
    print()

print("=" * 70)
print("ANALYSIS COMPLETE")
print("=" * 70)