import pandas as pd
from astral import LocationInfo
from astral.sun import elevation  # <--- THIS IS THE FIX
import pytz
import os

# --- CONFIGURATION ---
INPUT_FILE = "00_chicago_crime_2023_2025(working).csv"
OUTPUT_FILE = "01_chicago_crime_with_solar.csv"

# Chicago Coordinates
CITY_LAT = 41.8781
CITY_LON = -87.6298
city = LocationInfo("Chicago", "USA", "America/Chicago", CITY_LAT, CITY_LON)
chicago_tz = pytz.timezone("America/Chicago")

def main():
    if not os.path.exists(INPUT_FILE):
        print(f"ERROR: Could not find {INPUT_FILE}")
        return

    print(f"Loading {INPUT_FILE}...")
    df = pd.read_csv(INPUT_FILE)

    print("Converting timestamps...")
    # 1. Convert to Datetime and Normalize to Midnight
    df['Date'] = pd.to_datetime(df['Date']).dt.normalize()
    
    # 2. Ensure Hour is Integer
    df['hour'] = df['hour'].fillna(0).astype(int)

    # --- THE MATH ---
    def get_solar_altitude(row):
        try:
            # Create timestamp: Date + Hour + 30 mins
            target_time = row['Date'] + pd.Timedelta(hours=row['hour'], minutes=30)
            
            # Localize to Chicago Time
            local_dt = chicago_tz.localize(target_time)
            
            # Calculate Elevation (This is the fixed line)
            # Returns the angle of the sun in degrees
            alt = elevation(city.observer, local_dt)
            return float(alt)
            
        except Exception as e:
            # STOP AND PRINT THE ERROR if it fails
            print(f"CRASH on row: {row}")
            print(f"ERROR DETAILS: {e}")
            return -999.0

    print("Calculating Solar Altitude...")
    df['solar_altitude'] = df.apply(get_solar_altitude, axis=1)

    # --- CHECK RESULTS ---
    print("\n--- SAMPLE DATA ---")
    print(df[['Date', 'hour', 'solar_altitude']].head(5))

    # --- SAVE ---
    print(f"\nSaving to {OUTPUT_FILE}...")
    df.to_csv(OUTPUT_FILE, index=False)
    print("Done.")

if __name__ == "__main__":
    main()