"""
22_add_major_events.py
Adds major_event binary feature for big Chicago events
Events: St. Patrick's Day Parade, Pride Parade, Chicago Marathon, Lollapalooza
"""

import pandas as pd
from datetime import datetime, timedelta

def get_st_patricks_parade_date(year):
    """
    St. Patrick's Day Parade: Saturday before or on March 17
    If March 17 is Saturday, parade is that day
    Otherwise, it's the Saturday before
    """
    march_17 = datetime(year, 3, 17)
    day_of_week = march_17.weekday()  # Monday=0, Sunday=6
    
    if day_of_week == 5:  # Saturday
        return march_17.date()
    else:
        # Go back to previous Saturday
        days_back = (day_of_week + 2) % 7
        parade_date = march_17 - timedelta(days=days_back)
        return parade_date.date()

def get_pride_parade_date(year):
    """
    Pride Parade: Last Sunday in June
    """
    # Start from June 30 and work backwards to find last Sunday
    june_30 = datetime(year, 6, 30)
    day_of_week = june_30.weekday()  # Monday=0, Sunday=6
    
    # Calculate days back to last Sunday
    if day_of_week == 6:  # Already Sunday
        return june_30.date()
    else:
        days_back = (day_of_week + 1) % 7
        parade_date = june_30 - timedelta(days=days_back)
        return parade_date.date()

def get_chicago_marathon_date(year):
    """
    Chicago Marathon: 2nd Sunday in October
    """
    # Find first day of October
    oct_1 = datetime(year, 10, 1)
    day_of_week = oct_1.weekday()  # Monday=0, Sunday=6
    
    # Find first Sunday
    if day_of_week == 6:  # Oct 1 is Sunday
        first_sunday = oct_1
    else:
        days_to_sunday = (6 - day_of_week) % 7
        first_sunday = oct_1 + timedelta(days=days_to_sunday)
    
    # Second Sunday is 7 days later
    second_sunday = first_sunday + timedelta(days=7)
    return second_sunday.date()

def get_lollapalooza_dates(year):
    """
    Lollapalooza: First full weekend in August (Thu-Sun, 4 days)
    Typically starts first Thursday after Aug 1
    """
    aug_1 = datetime(year, 8, 1)
    day_of_week = aug_1.weekday()  # Monday=0, Sunday=6
    
    # Find first Thursday (weekday 3)
    if day_of_week <= 3:  # Mon-Thu
        days_to_thursday = 3 - day_of_week
    else:  # Fri-Sun, go to next week's Thursday
        days_to_thursday = (3 - day_of_week) % 7
    
    first_thursday = aug_1 + timedelta(days=days_to_thursday)
    
    # Lollapalooza is Thu-Fri-Sat-Sun (4 days)
    dates = []
    for i in range(4):
        dates.append((first_thursday + timedelta(days=i)).date())
    
    return dates

def is_major_event(check_datetime):
    """
    Check if datetime is during a major Chicago event (with specific hours)
    
    Event hours:
    - St. Patrick's Day: 3pm-3am (15:00-03:00 next day)
    - Pride Parade: 12pm-11pm (12:00-23:00)
    - Chicago Marathon: 7am-4pm (07:00-16:00)
    - Lollapalooza: 11am-10pm (11:00-22:00) for 4 days
    
    Returns: 1 if major event during active hours, 0 if not
    """
    if isinstance(check_datetime, str):
        check_datetime = datetime.strptime(check_datetime, '%Y-%m-%d %H:%M:%S')
    elif not isinstance(check_datetime, datetime):
        check_datetime = pd.to_datetime(check_datetime)
    
    check_date = check_datetime.date()
    check_hour = check_datetime.hour
    year = check_date.year
    
    # Get all event dates for this year
    st_patricks = get_st_patricks_parade_date(year)
    pride = get_pride_parade_date(year)
    marathon = get_chicago_marathon_date(year)
    lolla_dates = get_lollapalooza_dates(year)
    
    # St. Patrick's Day Parade: 3pm-3am (15:00-03:00)
    if check_date == st_patricks:
        if check_hour >= 15:  # 3pm to midnight
            return 1
    # Check next day for 12am-3am hours
    st_patricks_next = st_patricks + timedelta(days=1)
    if check_date == st_patricks_next:
        if check_hour < 3:  # Midnight to 3am
            return 1
    
    # Pride Parade: 12pm-11pm (12:00-23:00)
    if check_date == pride:
        if 12 <= check_hour <= 23:
            return 1
    
    # Chicago Marathon: 7am-4pm (07:00-16:00)
    if check_date == marathon:
        if 7 <= check_hour <= 16:
            return 1
    
    # Lollapalooza: 11am-10pm (11:00-22:00) for 4 days
    if check_date in lolla_dates:
        if 11 <= check_hour <= 22:
            return 1
    
    return 0

def add_major_events_feature(input_file):
    """
    Add major_event feature to crime dataset and overwrite file
    """
    print(f"Loading crime data from: {input_file}")
    df = pd.read_csv(input_file)
    
    print(f"Loaded {len(df):,} rows")
    
    # Parse the Date column
    print("\nParsing dates...")
    df['datetime'] = pd.to_datetime(df['Date'], format='%Y-%m-%d %H:%M:%S')
    
    print("Adding major_event feature (with specific event hours)...")
    df['major_event'] = df['datetime'].apply(is_major_event)
    
    # Statistics
    total_rows = len(df)
    event_days = df['major_event'].sum()
    
    print(f"\n=== Major Events Feature Statistics ===")
    print(f"Total records: {total_rows:,}")
    print(f"Major event days: {event_days:,} ({event_days/total_rows*100:.2f}%)")
    
    # Show which events were found
    print("\n=== Events Detected ===")
    years = df['datetime'].dt.year.unique()
    for year in sorted(years):
        print(f"\n{year}:")
        print(f"  St. Patrick's Parade: {get_st_patricks_parade_date(year)}")
        print(f"  Pride Parade: {get_pride_parade_date(year)}")
        print(f"  Chicago Marathon: {get_chicago_marathon_date(year)}")
        lolla = get_lollapalooza_dates(year)
        print(f"  Lollapalooza: {lolla[0]} to {lolla[-1]} (4 days)")
    
    # Drop the temporary datetime column if it wasn't there originally
    if 'datetime' not in pd.read_csv(input_file, nrows=1).columns:
        df = df.drop('datetime', axis=1)
    
    # Overwrite the original file
    df.to_csv(input_file, index=False)
    print(f"\n✓ Updated file with major_event column: {input_file}")
    
    # Show sample of event days
    event_samples = df[df['major_event'] == 1][['Date', 'major_event']].head(10)
    if len(event_samples) > 0:
        print("\n=== Sample Event Days ===")
        print(event_samples)
    
    return df

if __name__ == "__main__":
    # File path
    INPUT_FILE = 'chicago_crime_2023_2025(working).csv'
    
    print("="*60)
    print("Adding Major Chicago Events Feature")
    print("="*60)
    print()
    
    df = add_major_events_feature(INPUT_FILE)
    
    print("\n" + "="*60)
    print("✓ Complete! Major events feature added successfully.")
    print(f"✓ File updated with new 'major_event' column.")
    print("="*60)