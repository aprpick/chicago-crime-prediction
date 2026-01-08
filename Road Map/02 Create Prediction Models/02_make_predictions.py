import pandas as pd
import xgboost as xgb
from astral import LocationInfo
from astral.sun import elevation
import pytz
import os

# --- CONFIGURATION ---
TARGET_DATE = "2026-06-20"  # Saturday
TARGET_HOUR = 23            # 11 PM

# Paths
script_dir = os.path.dirname(os.path.abspath(__file__))
MODEL_FILE = os.path.join(script_dir, "chicago_crime_model.json")
OUTPUT_CSV = os.path.join(script_dir, "prediction_results_full.csv")

# Solar Settings
CITY_LAT = 41.8781
CITY_LON = -87.6298
city = LocationInfo("Chicago", "USA", "America/Chicago", CITY_LAT, CITY_LON)
chicago_tz = pytz.timezone("America/Chicago")

def main():
    if not os.path.exists(MODEL_FILE):
        print(f"ERROR: Model file {MODEL_FILE} not found.")
        return

    print(f"--- GENERATING PREDICTION ---")
    print(f"Target: {TARGET_DATE} @ {TARGET_HOUR}:00")

    # --- 1. GENERATE FEATURES ---
    print("Creating virtual rows for all 77 Community Areas...")
    future_data = []
    
    dt = pd.to_datetime(TARGET_DATE)
    day_of_week = dt.dayofweek
    month = dt.month
    
    is_weekend = 1 if day_of_week >= 5 else 0
    weekend_night_peak = 1 if (is_weekend and (TARGET_HOUR >= 20 or TARGET_HOUR <= 4)) else 0
    
    # Calculate Solar Altitude
    temp_dt = dt.replace(hour=0, minute=0, second=0, microsecond=0)
    target_time = temp_dt + pd.Timedelta(hours=TARGET_HOUR, minutes=30)
    local_dt = chicago_tz.localize(target_time)
    solar_alt = float(elevation(city.observer, local_dt))

    # Build rows
    for area in range(1, 78):
        future_data.append({
            'hour': TARGET_HOUR,
            'Community Area': area,
            'day_of_week': day_of_week,
            'month': month,
            'weekend_night_peak': weekend_night_peak,
            'weekend_regular': is_weekend,
            'is_violent_holiday': 0, 
            'is_theft_holiday': 0,
            'school_in_session': 0, 
            'major_event': 0,
            'moon_illumination': 50,
            'solar_altitude': solar_alt
        })

    df_future = pd.DataFrame(future_data)

    # --- 2. PREDICT ---
    model = xgb.Booster()
    model.load_model(MODEL_FILE)
    dtest = xgb.DMatrix(df_future)
    
    df_future['Predicted_Risk'] = model.predict(dtest)

    # --- 3. SHOW ALL 77 RESULTS ---
    # Sort by Risk (Highest to Lowest)
    sorted_df = df_future.sort_values(by='Predicted_Risk', ascending=False)

    print("\n--- FULL RANKING (ALL 77 AREAS) ---")
    print(f"{'RANK':<5} | {'AREA':<5} | {'RISK SCORE':<10}")
    print("-" * 35)
    
    rank = 1
    for index, row in sorted_df.iterrows():
        print(f"{rank:<5} | {int(row['Community Area']):<5} | {row['Predicted_Risk']:.2f}")
        rank += 1

    # --- 4. SAVE TO CSV ---
    sorted_df.to_csv(OUTPUT_CSV, index=False)
    print(f"\nSaved full list to: {OUTPUT_CSV}")

if __name__ == "__main__":
    main()