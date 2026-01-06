import pandas as pd
import os

# ==========================================
#              USER CONFIGURATION
# ==========================================

# 1. The Main File (Your "Master" list of crimes)
MAIN_CSV = "00_chicago_crime_2023_2025(working).csv"

# 2. The Feature File (The one with the new data)
FEATURE_CSV = "23_solar_altitude.csv"

# 3. The ID Column (Must exist in BOTH files)
ID_COLUMN = "Crime_ID"

# 4. Which columns do you want to grab from the Feature file?
#    (Do NOT include the ID column here, just the new data columns)
COLUMNS_TO_ADD = [
    "solar_altitude" 
    # You can add more here later: "temperature", "weather_code", etc.
]

# 5. Output File Name
OUTPUT_CSV = "00_chicago_crime_2023_2025(working).csv"

# ==========================================

def main():
    # --- 1. SETUP ---
    if not os.path.exists(MAIN_CSV):
        print(f"Error: {MAIN_CSV} not found.")
        return
    if not os.path.exists(FEATURE_CSV):
        print(f"Error: {FEATURE_CSV} not found.")
        return

    print(f"Loading Main Data: {MAIN_CSV}...")
    df_main = pd.read_csv(MAIN_CSV)
    original_row_count = len(df_main)

    print(f"Loading Feature Data: {FEATURE_CSV}...")
    # Load ONLY the ID and the columns you requested (Saves memory)
    cols_to_load = [ID_COLUMN] + COLUMNS_TO_ADD
    try:
        df_feature = pd.read_csv(FEATURE_CSV, usecols=cols_to_load)
    except ValueError as e:
        print(f"\nERROR: One of your requested columns doesn't exist in {FEATURE_CSV}.")
        print(f"Details: {e}")
        return

    # --- 2. CLEANUP ---
    # If the column already exists in Main (e.g. you ran this twice), remove the old one
    # so we don't end up with 'solar_altitude_x' and 'solar_altitude_y'
    for col in COLUMNS_TO_ADD:
        if col in df_main.columns:
            print(f"Removing old version of '{col}' from main file...")
            df_main.drop(columns=[col], inplace=True)

    # --- 3. THE MERGE ---
    print(f"Merging {COLUMNS_TO_ADD} to the right of the main data...")
    
    # 'how=left' ensures we keep EVERY row from your Main file.
    # If the feature file is missing an ID, it will just leave the cell blank.
    df_merged = df_main.merge(df_feature, on=ID_COLUMN, how='left')

    # --- 4. SAFETY CHECKS ---
    # Verify we didn't accidentally multiply rows (common merge error)
    if len(df_merged) != original_row_count:
        print(f"\nWARNING: Row count changed!")
        print(f"Original: {original_row_count}")
        print(f"New:      {len(df_merged)}")
        print("This means your Feature CSV has duplicate Crime_IDs. Check that file.")
    else:
        print(f"Success: Row count verified ({original_row_count}).")

    # --- 5. SAVE ---
    print(f"Saving to {OUTPUT_CSV}...")
    df_merged.to_csv(OUTPUT_CSV, index=False)
    print("Done.")

if __name__ == "__main__":
    main()