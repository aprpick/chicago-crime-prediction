"""
Major Events Crime Impact Analyzer
Analyzes historical crime data (2023-2025) to determine actual impact multipliers
for major Chicago events using severity scores.

Input: 11.1_severity_added.csv
Output: Event impact report with recommended multipliers
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# ============================================================
# FILE PATHS
# ============================================================
SEVERITY_DATA = '../01 Foundation & Data/11.1_severity_added.csv'
OUTPUT_REPORT = '04.1_event_impact_analysis.md'

# ============================================================
# MAJOR CHICAGO EVENTS (2023-2025)
# ============================================================

EVENTS = {
    'Lollapalooza': {
        'dates': [
            ('2023-08-03', '2023-08-06'),
            ('2024-08-01', '2024-08-04'),
            ('2025-07-31', '2025-08-03'),
        ],
        'areas': [33, 8, 32],  # Grant Park, Near North, Loop
        'description': 'Music festival in Grant Park',
        'late_night': False  # Ends before midnight
    },
    'St_Patricks_Day': {
        'dates': [
            ('2023-03-17', '2023-03-17'),
            ('2024-03-17', '2024-03-17'),
            ('2025-03-17', '2025-03-17'),
        ],
        'areas': [8, 32, 28],  # Near North, Loop, Near West
        'description': 'River dyeing and parades downtown',
        'late_night': True  # Bars close at 2-4am, spillover to next morning
    },
    'New_Years_Eve': {
        'dates': [
            ('2022-12-31', '2022-12-31'),  # For 2023 data
            ('2023-12-31', '2023-12-31'),
            ('2024-12-31', '2024-12-31'),
        ],
        'areas': list(range(1, 78)),  # Citywide
        'description': 'New Year celebrations (9pm-3am spike)',
        'late_night': True  # Midnight spike extends to next morning
    },
    'Fourth_of_July': {
        'dates': [
            ('2023-07-04', '2023-07-04'),
            ('2024-07-04', '2024-07-04'),
            ('2025-07-04', '2025-07-04'),
        ],
        'areas': list(range(1, 78)),  # Citywide
        'description': 'Independence Day celebrations',
        'late_night': True  # Fireworks and parties until late
    },
    'Taste_of_Chicago': {
        'dates': [
            ('2023-07-07', '2023-07-16'),
            ('2024-07-05', '2024-07-14'),
            ('2025-07-11', '2025-07-20'),
        ],
        'areas': [33, 32, 8],  # Grant Park area
        'description': 'Food festival in Grant Park',
        'late_night': False  # Closes at 9pm
    },
    'Pride_Parade': {
        'dates': [
            ('2023-06-25', '2023-06-25'),
            ('2024-06-30', '2024-06-30'),
            ('2025-06-29', '2025-06-29'),
        ],
        'areas': [6, 7],  # Lakeview
        'description': 'Pride Parade in Lakeview',
        'late_night': True  # Bars and parties until 2-4am
    },
    'Chicago_Marathon': {
        'dates': [
            ('2023-10-08', '2023-10-08'),
            ('2024-10-13', '2024-10-13'),
            ('2025-10-12', '2025-10-12'),
        ],
        'areas': [8, 28, 32, 33, 7, 6],  # Marathon route
        'description': 'Chicago Marathon route',
        'late_night': False  # Morning event
    },
    'Air_Water_Show': {
        'dates': [
            ('2023-08-12', '2023-08-13'),
            ('2024-08-10', '2024-08-11'),
            ('2025-08-09', '2025-08-10'),
        ],
        'areas': [3, 77, 7, 8],  # Lakefront
        'description': 'Air & Water Show on lakefront',
        'late_night': False  # Daytime event
    },
    'Halloween': {
        'dates': [
            ('2023-10-31', '2023-10-31'),
            ('2024-10-31', '2024-10-31'),
            ('2025-10-31', '2025-10-31'),
        ],
        'areas': list(range(1, 78)),  # Citywide
        'description': 'Halloween (6pm-3am spike)',
        'late_night': True  # Party/bar spillover until 2-4am
    },
}

# ============================================================

def load_data():
    """Load raw crime data"""
    print("="*70)
    print("LOADING CRIME DATA")
    print("="*70)
    
    print(f"\nReading: {RAW_DATA}")
    df = pd.read_csv(RAW_DATA)
    
    print(f"✓ Loaded {len(df):,} crime records")
    print(f"  Date range: {df['Date'].min()} to {df['Date'].max()}")
    
    # Parse dates
    df['Date'] = pd.to_datetime(df['Date'], format='%m/%d/%Y %I:%M:%S %p', errors='coerce')
    df['date_only'] = df['Date'].dt.date
    
    # Filter to 2023-2025
    df = df[(df['Year'] >= 2023) & (df['Year'] <= 2025)]
    
    print(f"✓ Filtered to 2023-2025: {len(df):,} records")
    
    return df

def load_data():
    """Load crime data with severity scores"""
    print("="*70)
    print("LOADING CRIME DATA WITH SEVERITY")
    print("="*70)
    
    print(f"\nReading: {SEVERITY_DATA}")
    df = pd.read_csv(SEVERITY_DATA)
    
    print(f"✓ Loaded {len(df):,} crime records")
    print(f"  Date range: {df['Date'].min()} to {df['Date'].max()}")
    
    # Parse dates
    df['Date'] = pd.to_datetime(df['Date'], format='%m/%d/%Y %I:%M:%S %p', errors='coerce')
    df['date_only'] = df['Date'].dt.date
    
    # Filter to 2023-2025
    df = df[(df['Year'] >= 2023) & (df['Year'] <= 2025)]
    
    print(f"✓ Filtered to 2023-2025: {len(df):,} records")
    print(f"  Total severity: {df['Severity_Score'].sum():,.0f}")
    print(f"  Average severity per crime: {df['Severity_Score'].mean():.2f}")
    
    return df

def get_baseline_severity(df, event_dates, areas):
    """Calculate baseline severity for comparison dates (1 week before/after)"""
    # Get dates 1 week before and 1 week after event (but not during event)
    baseline_dates = []
    
    for start_str, end_str in event_dates:
        start = pd.to_datetime(start_str).date()
        end = pd.to_datetime(end_str).date()
        
        # 1 week before
        week_before_start = start - timedelta(days=14)
        week_before_end = start - timedelta(days=7)
        
        # 1 week after
        week_after_start = end + timedelta(days=7)
        week_after_end = end + timedelta(days=14)
        
        baseline_dates.extend([
            (week_before_start, week_before_end),
            (week_after_start, week_after_end)
        ])
    
    # Get baseline severity
    baseline_mask = pd.Series(False, index=df.index)
    for start, end in baseline_dates:
        baseline_mask |= (df['date_only'] >= start) & (df['date_only'] <= end)
    
    if len(areas) < 77:  # Not citywide
        baseline_mask &= df['Community Area'].isin(areas)
    
    baseline_df = df[baseline_mask]
    
    if len(baseline_df) == 0:
        return 0, 0
    
    baseline_severity_per_day = baseline_df.groupby('date_only')['Severity_Score'].sum().mean()
    baseline_crimes_per_day = baseline_df.groupby('date_only').size().mean()
    
    return baseline_severity_per_day, baseline_crimes_per_day

def analyze_event(df, event_name, event_info):
    """Analyze crime impact for a specific event"""
    print(f"\n{'='*70}")
    print(f"ANALYZING: {event_name.replace('_', ' ')}")
    print(f"{'='*70}")
    print(f"Description: {event_info['description']}")
    print(f"Areas affected: {len(event_info['areas'])} areas")
    print(f"Late-night spillover: {'Yes (extends to next morning)' if event_info.get('late_night', False) else 'No'}")
    
    results = []
    
    for start_str, end_str in event_info['dates']:
        start = pd.to_datetime(start_str).date()
        end = pd.to_datetime(end_str).date()
        
        # Extend by 1 day for late-night events (to capture midnight-6am spillover)
        if event_info.get('late_night', False):
            end = end + timedelta(days=1)
        
        year = pd.to_datetime(start_str).year
        
        print(f"\n  {year}: {start} to {end}{' (+ morning spillover)' if event_info.get('late_night', False) else ''}")
        
        # Get event severity
        event_mask = (df['date_only'] >= start) & (df['date_only'] <= end)
        if len(event_info['areas']) < 77:  # Not citywide
            event_mask &= df['Community Area'].isin(event_info['areas'])
        
        event_df = df[event_mask]
        
        if len(event_df) == 0:
            print(f"    ⚠️  No data found")
            continue
        
        event_days = (end - start).days + 1
        event_severity_per_day = event_df['Severity_Score'].sum() / event_days
        event_crimes_per_day = len(event_df) / event_days
        
        # Get baseline
        baseline_severity_per_day, baseline_crimes_per_day = get_baseline_severity(
            df, [(start_str, end_str)], event_info['areas']
        )
        
        if baseline_severity_per_day == 0:
            print(f"    ⚠️  No baseline data")
            continue
        
        # Calculate multipliers
        severity_multiplier = event_severity_per_day / baseline_severity_per_day
        crime_count_multiplier = event_crimes_per_day / baseline_crimes_per_day
        
        print(f"    Event severity/day:    {event_severity_per_day:,.0f}")
        print(f"    Baseline severity/day: {baseline_severity_per_day:,.0f}")
        print(f"    Severity multiplier:   {severity_multiplier:.2f}x")
        print(f"    Crime count multiplier: {crime_count_multiplier:.2f}x")
        
        results.append({
            'year': year,
            'event_severity': event_severity_per_day,
            'baseline_severity': baseline_severity_per_day,
            'severity_multiplier': severity_multiplier,
            'crime_multiplier': crime_count_multiplier,
            'crimes_per_day': event_crimes_per_day
        })
    
    if results:
        avg_severity_mult = np.mean([r['severity_multiplier'] for r in results])
        avg_crime_mult = np.mean([r['crime_multiplier'] for r in results])
        
        print(f"\n  📊 AVERAGE ACROSS {len(results)} YEARS:")
        print(f"     Severity multiplier: {avg_severity_mult:.2f}x")
        print(f"     Crime count multiplier: {avg_crime_mult:.2f}x")
        
        return {
            'event': event_name,
            'description': event_info['description'],
            'areas': event_info['areas'],
            'late_night': event_info.get('late_night', False),
            'years_analyzed': len(results),
            'avg_severity_multiplier': avg_severity_mult,
            'avg_crime_multiplier': avg_crime_mult,
            'yearly_results': results
        }
    
    return None

def save_report(event_results):
    """Save analysis report"""
    print(f"\n{'='*70}")
    print("SAVING REPORT")
    print(f"{'='*70}")
    
    lines = []
    lines.append("# Major Events Crime Impact Analysis")
    lines.append("")
    lines.append(f"**Analysis Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append(f"**Data Period:** 2023-2025")
    lines.append(f"**Events Analyzed:** {len(event_results)}")
    lines.append("")
    lines.append("---")
    lines.append("")
    
    # Sort by severity multiplier
    event_results_sorted = sorted(event_results, key=lambda x: x['avg_severity_multiplier'], reverse=True)
    
    lines.append("## Summary: Recommended Multipliers")
    lines.append("")
    lines.append("| Event | Severity Multiplier | Crime Count Multiplier | Areas Affected |")
    lines.append("|-------|---------------------|------------------------|----------------|")
    
    for result in event_results_sorted:
        event_name = result['event'].replace('_', ' ')
        areas_str = 'Citywide' if len(result['areas']) > 50 else f"{len(result['areas'])} areas"
        lines.append(
            f"| {event_name} | **{result['avg_severity_multiplier']:.2f}x** | "
            f"{result['avg_crime_multiplier']:.2f}x | {areas_str} |"
        )
    
    lines.append("")
    lines.append("---")
    lines.append("")
    
    # Detailed results
    lines.append("## Detailed Analysis by Event")
    lines.append("")
    
    for result in event_results_sorted:
        event_name = result['event'].replace('_', ' ')
        lines.append(f"### {event_name}")
        lines.append("")
        lines.append(f"**Description:** {result['description']}")
        lines.append(f"**Areas:** {result['areas'][:10]}{'...' if len(result['areas']) > 10 else ''}")
        lines.append(f"**Years Analyzed:** {result['years_analyzed']}")
        lines.append("")
        lines.append(f"**Average Severity Multiplier:** {result['avg_severity_multiplier']:.2f}x")
        lines.append(f"**Average Crime Count Multiplier:** {result['avg_crime_multiplier']:.2f}x")
        lines.append("")
        
        lines.append("| Year | Event Severity/Day | Baseline Severity/Day | Multiplier |")
        lines.append("|------|-------------------|----------------------|------------|")
        for yr in result['yearly_results']:
            lines.append(
                f"| {yr['year']} | {yr['event_severity']:,.0f} | "
                f"{yr['baseline_severity']:,.0f} | {yr['severity_multiplier']:.2f}x |"
            )
        lines.append("")
        lines.append("---")
        lines.append("")
    
    # Save
    with open(OUTPUT_REPORT, 'w') as f:
        f.write('\n'.join(lines))
    
    print(f"✓ Report saved: {OUTPUT_REPORT}")

def main():
    print("="*70)
    print("     MAJOR EVENTS CRIME IMPACT ANALYZER")
    print("="*70)
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Load data
    df = load_data()
    
    # Analyze each event
    event_results = []
    
    for event_name, event_info in EVENTS.items():
        result = analyze_event(df, event_name, event_info)
        if result:
            event_results.append(result)
    
    # Save report
    if event_results:
        save_report(event_results)
    
    print(f"\n{'='*70}")
    print("✅ ANALYSIS COMPLETE!")
    print(f"{'='*70}")
    print(f"\nAnalyzed {len(event_results)} events")
    print(f"Report: {OUTPUT_REPORT}")
    print(f"\n💡 Use these multipliers to adjust your Power BI predictions!")
    print(f"{'='*70}")

if __name__ == "__main__":
    main()