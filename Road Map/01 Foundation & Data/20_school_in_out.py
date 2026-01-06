"""
21_add_school_calendar.py
Adds school_in_session binary feature to crime dataset based on CPS calendar
School hours: 8am-3pm on school days only
"""

import pandas as pd
from datetime import datetime, date

# Chicago Public Schools Calendar Data (2023-2025)
# Based on official CPS calendars

SCHOOL_BREAKS = {
    # 2023 (School Year 2022-2023 and start of 2023-2024)
    '2023': {
        'winter_break_2022': ('2022-12-19', '2023-01-02'),  # Winter 2022-2023
        'spring_break': ('2023-03-27', '2023-03-31'),
        'summer_break': ('2023-06-09', '2023-08-20'),  # Ends June 8, starts Aug 21
        'thanksgiving': ('2023-11-20', '2023-11-24'),
        'winter_break_2023': ('2023-12-22', '2024-01-07'),  # Winter 2023-2024
    },
    
    # 2024 (School Year 2023-2024 and start of 2024-2025)
    '2024': {
        'spring_break': ('2024-03-25', '2024-03-29'),  # Week in late March
        'summer_break': ('2024-06-07', '2024-08-25'),  # Ends June 6, starts Aug 26
        'thanksgiving': ('2024-11-25', '2024-11-29'),
        'winter_break': ('2024-12-23', '2025-01-03'),  # 2 weeks
    },
    
    # 2025 (School Year 2024-2025 and start of 2025-2026)
    '2025': {
        'spring_break': ('2025-03-24', '2025-03-28'),  # Week in late March
        'summer_break': ('2025-06-13', '2025-08-17'),  # Ends June 12, starts Aug 18
        'thanksgiving': ('2025-11-24', '2025-11-28'),
        'winter_break': ('2025-12-22', '2026-01-02'),
    }
}

# Additional single-day holidays/breaks (not school days)
SINGLE_DAY_BREAKS = {
    '2023': [
        '2023-01-16',  # MLK Day
        '2023-02-20',  # Presidents Day
        '2023-09-04',  # Labor Day
        '2023-10-09',  # Indigenous Peoples Day
        '2023-11-10',  # Veterans Day
    ],
    '2024': [
        '2024-01-15',  # MLK Day
        '2024-02-19',  # Presidents Day
        '2024-09-02',  # Labor Day
        '2024-09-27',  # Professional Development Day
        '2024-10-14',  # Indigenous Peoples Day
        '2024-10-28',  # Parent-Teacher Conference
        '2024-11-11',  # Veterans Day
    ],
    '2025': [
        '2025-01-20',  # MLK Day
        '2025-02-17',  # Presidents Day
        '2025-09-01',  # Labor Day
        '2025-09-26',  # Professional Development Day
        '2025-10-13',  # Indigenous Peoples Day
        '2025-10-27',  # Parent-Teacher Conference
        '2025-11-11',  # Veterans Day
    ]
}

def is_school_in_session(check_datetime):
    """
    Determine if school is in session at a given datetime
    School hours: 8am-3pm on school days
    Returns: 1 if in session, 0 if not
    """
    if isinstance(check_datetime, str):
        check_datetime = datetime.strptime(check_datetime, '%Y-%m-%d %H:%M:%S')
    elif not isinstance(check_datetime, datetime):
        check_datetime = pd.to_datetime(check_datetime)
    
    check_date = check_datetime.date()
    check_hour = check_datetime.hour
    year = str(check_date.year)
    
    # Check if date is in a break period
    if year in SCHOOL_BREAKS:
        for break_name, (start, end) in SCHOOL_BREAKS[year].items():
            start_date = datetime.strptime(start, '%Y-%m-%d').date()
            end_date = datetime.strptime(end, '%Y-%m-%d').date()
            
            if start_date <= check_date <= end_date:
                return 0  # School not in session
    
    # Check single-day breaks
    if year in SINGLE_DAY_BREAKS:
        date_str = check_date.strftime('%Y-%m-%d')
        if date_str in SINGLE_DAY_BREAKS[year]:
            return 0  # School not in session
    
    # Check if weekend
    if check_date.weekday() >= 5:  # Saturday = 5, Sunday = 6
        return 0  # School not in session
    
    # Check if during school hours (8am-3pm)
    if 8 <= check_hour < 15:  # 8am to 2:59pm
        return 1  # School in session
    
    # School day but outside school hours
    return 0

def add_school_calendar_feature(input_file):
    """
    Add school_in_session feature to crime dataset and overwrite file
    """
    print(f"Loading crime data from: {input_file}")
    df = pd.read_csv(input_file)
    
    print(f"Loaded {len(df):,} rows")
    print(f"Columns: {df.columns.tolist()}")
    
    # Parse the Date column (format: 2025-12-27 00:00:00)
    print("\nParsing dates...")
    df['datetime'] = pd.to_datetime(df['Date'], format='%Y-%m-%d %H:%M:%S')
    
    print("Adding school_in_session feature (8am-3pm on school days only)...")
    df['school_in_session'] = df['datetime'].apply(is_school_in_session)
    
    # Statistics
    total_rows = len(df)
    in_session = df['school_in_session'].sum()
    not_in_session = total_rows - in_session
    
    print(f"\n=== School Calendar Feature Statistics ===")
    print(f"Total records: {total_rows:,}")
    print(f"School in session (8am-3pm): {in_session:,} ({in_session/total_rows*100:.1f}%)")
    print(f"School NOT in session: {not_in_session:,} ({not_in_session/total_rows*100:.1f}%)")
    
    # Drop the temporary datetime column if it wasn't there originally
    if 'datetime' not in pd.read_csv(input_file, nrows=1).columns:
        df = df.drop('datetime', axis=1)
    
    # Overwrite the original file
    df.to_csv(input_file, index=False)
    print(f"\n✓ Updated file with school_in_session column: {input_file}")
    
    # Show sample
    print("\n=== Sample Data (first 10 rows) ===")
    sample_cols = ['Date', 'hour', 'school_in_session']
    print(df[sample_cols].head(10))
    
    return df

if __name__ == "__main__":
    # File path
    INPUT_FILE = 'chicago_crime_2023_2025(working).csv'
        
    print("="*60)
    print("Adding School Calendar Feature (Hourly: 8am-3pm)")
    print("="*60)
    print()
    
    df = add_school_calendar_feature(INPUT_FILE)
    
    print("\n" + "="*60)
    print("✓ Complete! School calendar feature added successfully.")
    print(f"✓ File updated with new 'school_in_session' column.")
    print("="*60)