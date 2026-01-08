import pandas as pd
import os

# --- CONFIGURATION ---
INPUT_FILE = "00_chicago_crime_2023_2025(working).csv"
OUTPUT_FILE = "28_shift_data_for_model.csv"

def main():
    if not os.path.exists(INPUT_FILE):
        print(f"ERROR: {INPUT_FILE} not found.")
        return

    print(f"Loading {INPUT_FILE}...")
    df = pd.read_csv(INPUT_FILE)
    
    print(f"Original Crime Rows: {len(df)}")

    # 1. DEFINE GROUPING
    # We group by Date + Hour + Area to isolate a specific "Shift"
    group_cols = ['Date', 'hour', 'Community Area']

    # 2. DEFINE AGGREGATION RULES
    # Target = SUM (How much total work is there?)
    # Features = FIRST (They are the same for the whole hour)
    agg_rules = {
        'Severity_Score': 'sum',
        
        # Features
        'day_of_week': 'first',
        'month': 'first',
        'weekend_night_peak': 'first',
        'weekend_regular': 'first',
        'is_violent_holiday': 'first',
        'is_theft_holiday': 'first',
        'school_in_session': 'first',
        'major_event': 'first',
        'moon_illumination': 'first',
        'solar_altitude': 'first'
    }

    print("Aggregating individual crimes into 'Shift Loads'...")
    
    # 3. PERFORM THE GROUPING
    df_shifts = df.groupby(group_cols).agg(agg_rules).reset_index()

    # 4. RENAME THE TARGET
    # Change 'Severity_Score' to 'Total_Severity_Load' so it's clear this is a Volume metric
    df_shifts.rename(columns={'Severity_Score': 'Total_Severity_Load'}, inplace=True)

    # 5. STATS
    print("-" * 30)
    print(f"Original Rows (Crimes): {len(df)}")
    print(f"New Rows (Hourly Shifts): {len(df_shifts)}")
    print(f"Data compressed by: {len(df) - len(df_shifts)} rows")
    print("-" * 30)
    
    # 6. SAVE
    print(f"Saving training data to {OUTPUT_FILE}...")
    df_shifts.to_csv(OUTPUT_FILE, index=False)
    print("Done! This is the file you will use to train the model.")

if __name__ == "__main__":
    main()