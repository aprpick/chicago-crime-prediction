import pandas as pd
import os

# ==========================================
#        USER CONFIGURATION SECTION
# ==========================================

# 1. FILE SETTINGS
INPUT_FILE  = "00_chicago_crime_2023_2025(working).csv"
OUTPUT_FILE = "25_training_script.csv"

# 2. COLUMNS TO REMOVE (Vertical Filters)
# Add any column names here that you want to DROP entirely.
# For training, we definitely want to drop the raw 'Date' string.
DROP_COLUMNS = [
    "Date", 
    # "Case Number",  # Example: You can uncomment these to drop them too
    # "Updated On"
]

# 3. ROWS TO REMOVE (Horizontal Filters) - Advanced
# Set this to True if you want to apply row filtering logic below
FILTER_ROWS = False

# ==========================================

def main():
    # --- 1. SETUP ---
    if not os.path.exists(INPUT_FILE):
        print(f"ERROR: Could not find {INPUT_FILE}")
        return

    print(f"Loading {INPUT_FILE}...")
    df = pd.read_csv(INPUT_FILE)
    original_rows = len(df)
    original_cols = len(df.columns)

    # --- 2. REMOVE COLUMNS ---
    print(f"Removing columns: {DROP_COLUMNS}")
    # We use errors='ignore' so the script doesn't crash if the column is already gone
    df.drop(columns=DROP_COLUMNS, inplace=True, errors='ignore')

    # --- 3. REMOVE ROWS (Optional) ---
    if FILTER_ROWS:
        print("Applying row filters...")
        
        # --- EXAMPLE FILTERS (Edit these as needed) ---
        
        # Example A: Drop rows where 'Crime_ID' is missing
        # df = df.dropna(subset=['Crime_ID'])
        
        # Example B: Drop rows where 'Severity_Score' is 0
        # df = df[df['Severity_Score'] > 0]
        
        # Example C: Keep only 2024 data (if you had a year column)
        # df = df[df['year'] == 2024]
        
        pass # 'pass' does nothing, it's just here to prevent errors if empty

    # --- 4. REPORT CHANGES ---
    new_rows = len(df)
    new_cols = len(df.columns)
    
    print("\n--- SUMMARY OF CHANGES ---")
    print(f"Rows:    {original_rows} -> {new_rows}")
    print(f"Columns: {original_cols} -> {new_cols}")
    print(f"Dropped: {original_cols - new_cols} columns")

    # --- 5. SAVE ---
    print(f"\nSaving to {OUTPUT_FILE}...")
    df.to_csv(OUTPUT_FILE, index=False)
    print("Done.")

if __name__ == "__main__":
    main()