import pandas as pd
import numpy as np
import joblib
from astral.sun import sun
from astral import Observer
from datetime import datetime, timedelta
import pytz
import math

# ===========================
# CONFIG
# ===========================
MODEL_FILE = 'xgb_crime_model.joblib'
OUTPUT_FILE = '40_powerbi_data_1year.csv'
DAYS_TO_PREDICT = 365  # Full Year
AREAS = list(range(1, 78)) # Areas 1-77

# Chicago Location
city_observer = Observer(latitude=41.8781, longitude=-87.6298, elevation=181)
tz = pytz.timezone('America/Chicago')

def get_solar_features(dt_obj):
    """Calculates sun_altitude and is_night."""
    # Sun Altitude
    try:
        altitude = city_observer.sun_altaz(dt_obj).altitude
    except:
        altitude = 0 # Fallback
    
    # Is Night? (Civil Twilight definition: altitude < -6)
    is_night = 1 if altitude < -6 else 0
    return altitude, is_night

def get_seasonal_weather(month):
    """Returns an estimated temperature (C) based on month for Chicago."""
    # Simple curve: Coldest in Jan (1), Hottest in July (7)
    # Approx: Jan=-5C, Jul=28C
    
    if month in [12, 1, 2]:    # Winter
        temp = -2.0
    elif month in [3, 4]:      # Spring
        temp = 10.0
    elif month in [5, 6, 7, 8, 9]: # Summer/Late Summer
        temp = 25.0
    else:                      # Fall (10, 11)
        temp = 12.0
        
    return temp

def generate_data():
    print("Loading Model...")
    try:
        model = joblib.load(MODEL_FILE)
    except FileNotFoundError:
        print(f"Error: {MODEL_FILE} not found. Run 01_train_model.py first.")
        return

    print(f"Generating simulation for the next {DAYS_TO_PREDICT} days...")
    print("This may take 1-2 minutes...")

    start_date = datetime.now(tz).replace(minute=0, second=0, microsecond=0)
    
    # Pre-calculate time slots to avoid loop overhead
    total_hours = DAYS_TO_PREDICT * 24
    time_slots = [start_date + timedelta(hours=i) for i in range(total_hours)]
    
    # We will build a list of dictionaries (Batch processing is faster)
    data_batch = []
    
    for current_dt in time_slots:
        # 1. Solar/Time Math (Once per hour)
        alt, night = get_solar_features(current_dt)
        temp = get_seasonal_weather(current_dt.month)
        
        # 2. Replicate for all 77 Areas
        # We use list comprehension for speed
        hour_batch = [{
            'datetime': current_dt,
            'Community Area': area,
            'hour': current_dt.hour,
            'day_of_week': current_dt.weekday(),
            'month': current_dt.month,
            'sun_altitude': alt,
            'is_night': night,
            'temperature_2m': temp, 
            'precipitation': 0.0, # Assume dry for baseline
            'rain': 0.0,
            'cloud_cover': 20.0,
            'wind_speed_10m': 12.0
        } for area in AREAS]
        
        data_batch.extend(hour_batch)

        if len(data_batch) % 50000 == 0:
            print(f"Generated {len(data_batch)} rows...")

    print(f"Converting {len(data_batch)} rows to DataFrame...")
    df = pd.DataFrame(data_batch)
    
    # Prepare features for Model
    features = ['Community Area', 'hour', 'day_of_week', 'month', 
                'temperature_2m', 'precipitation', 'rain', 
                'cloud_cover', 'wind_speed_10m', 'sun_altitude', 'is_night']
    
    print("Running XGBoost Predictions...")
    # Inference on 600k+ rows takes a few seconds
    df['Predicted_Risk'] = model.predict(df[features])
    
    # Formatting for Power BI
    print("Formatting for Export...")
    df['Date'] = df['datetime'].dt.date
    df['Time'] = df['datetime'].dt.time
    
    # Drop the complex datetime object to save space (Power BI uses Date/Time cols)
    df = df.drop(columns=['datetime'])
    
    # Save
    print(f"Saving to {OUTPUT_FILE}...")
    df.to_csv(OUTPUT_FILE, index=False)
    print("Done! Ready for Power BI.")

if __name__ == "__main__":
    generate_data()