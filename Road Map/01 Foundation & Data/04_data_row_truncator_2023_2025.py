"""
Filter raw crime data to extract only 2023, 2024, 2025 rows
"""

# ============================================================
# FILE PATHS - CONFIGURE HERE
# ============================================================
INPUT_FILE = '00_chicago_crime_2001_2025_(raw).csv'
OUTPUT_FILE = '04.1_chicago_crime_2023_2025_(raw).csv'
# ============================================================

import pandas as pd
from datetime import datetime

def filter_crime_data_by_year(input_file, output_file, years=[2023, 2024, 2025]):
    """
    Filter crime data to only include specified years
    """
    print(f"Loading raw crime data from: {input_file}")
    print("This may take a moment for large files...")
    
    # Read CSV
    df = pd.read_csv(input_file)
    print(f"Loaded {len(df):,} total rows")
    
    # Parse the Date column (format: 12/27/2025 12:00:00 AM)
    print("\nParsing dates...")
    df['parsed_date'] = pd.to_datetime(df['Date'], format='%m/%d/%Y %I:%M:%S %p')
    df['year'] = df['parsed_date'].dt.year
    
    # Filter for specified years
    print(f"\nFiltering for years: {years}")
    filtered_df = df[df['year'].isin(years)].copy()
    
    # Drop the temporary columns
    filtered_df = filtered_df.drop(['parsed_date', 'year'], axis=1)
    
    # Statistics
    print(f"\n=== Filtering Results ===")
    print(f"Original rows: {len(df):,}")
    print(f"Filtered rows: {len(filtered_df):,}")
    print(f"Rows removed: {len(df) - len(filtered_df):,}")
    print(f"Percentage kept: {len(filtered_df)/len(df)*100:.1f}%")
    
    # Show year breakdown
    print("\n=== Year Breakdown ===")
    year_counts = df.groupby(df['parsed_date'].dt.year).size()
    for year in years:
        if year in year_counts.index:
            count = year_counts[year]
            print(f"{year}: {count:,} rows")
    
    # Save filtered data
    print(f"\nSaving filtered data to: {output_file}")
    filtered_df.to_csv(output_file, index=False)
    print(f"✓ Saved {len(filtered_df):,} rows to {output_file}")
    
    return filtered_df

if __name__ == "__main__":
    print("="*60)
    print("Filter Raw Crime Data: 2023-2025")
    print("="*60)
    print()
    
    df = filter_crime_data_by_year(INPUT_FILE, OUTPUT_FILE, years=[2023, 2024, 2025])
    
    print("\n" + "="*60)
    print("✓ Complete! Filtered data saved successfully.")
    print("="*60)