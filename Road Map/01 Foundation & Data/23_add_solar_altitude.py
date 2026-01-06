import pandas as pd
from astral import LocationInfo
from astral.sun import elevation
import pytz
import os

# --- CONFIGURATION ---
INPUT_FILE = "00_chicago_crime_2023_2025(working).csv"
OUTPUT_FILE = "23_solar_altitude.csv"  # The lookup file

# Chicago Coordinates
CITY_LAT = 41.8781
CITY_LON = -87.6298
city = LocationInfo("Chicago", "USA", "America/Chicago", CITY_LAT, CITY_LON)
chicago_tz = pytz.timezone("America/Chicago")

def main():
    if not os.path.exists(INPUT_FILE):
        print(f"ERROR: {INPUT_FILE} not found.")
        return

    print(f"Loading {INPUT_FILE}...")
    # OPTIMIZATION: We only load the columns we actually need for the math
    # This makes the script run much faster and uses less RAM.
    df = pd.read_csv(INPUT_FILE, usecols=['Crime_ID', 'Date', 'hour'])

    # --- THE VERIFIED SAFE MATH ---
    def get_solar_altitude(row):
        try:
            # 1. Convert Date string to Temp Object
            temp_dt = pd.to_datetime(row['Date'])
            
            # 2. Force to Midnight (Safety measure)
            temp_dt = temp_dt.replace(hour=0, minute=0, second=0, microsecond=0)
            
            # 3. Add Hour + 30 mins
            target_time = temp_dt + pd.Timedelta(hours=int(row['hour']), minutes=30)
            
            # 4. Localize and Calculate
            local_dt = chicago_tz.localize(target_time)
            alt = elevation(city.observer, local_dt)
            return float(alt)
            
        except Exception:
            return -999.0

    print("Calculating Solar Altitude...")
    df['solar_altitude'] = df.apply(get_solar_altitude, axis=1)

    # --- CREATE THE LOOKUP TABLE ---
    print("Creating final output with ONLY Crime_ID and solar_altitude...")
    
    # Select only the two columns you asked for
    final_df = df[['Crime_ID', 'solar_altitude']]

    # --- SAVE ---
    print(f"Saving to {OUTPUT_FILE}...")
    final_df.to_csv(OUTPUT_FILE, index=False)
    
    # Verification Print
    print("\nDone. Preview of the new file:")
    print(final_df.head())

if __name__ == "__main__":
    main()