import pandas as pd
import os

# 1. Setup paths
script_dir = os.path.dirname(os.path.abspath(__file__))
input_file = os.path.join(script_dir, '15_chicago_weather_2023_2025.csv')
output_file = os.path.join(script_dir, '16_chicago_weather_with_DI.csv')

# 2. Load Data
if os.path.exists(input_file):
    df = pd.read_csv(input_file)
    
    # --- HEAT DISCOMFORT (Thom Index) ---
    # Best for predicting irritability/violence spikes in summer
    df['heat_DI'] = df['temp'] - 0.55 * (1 - 0.01 * df['rhum']) * (df['temp'] - 14.5)
    # We "clip" this at 21 because values below that don't represent heat stress
    df['heat_DI'] = df['heat_DI'].clip(lower=21).round(2)

    # --- COLD DISCOMFORT (Wind Chill) ---
    # Best for predicting "empty streets" and lower crime in winter
    # Formula only applies if temp <= 10°C and wind > 4.8 km/h
    def get_wind_chill(row):
        t = row['temp']
        v = row['wspd']
        if t <= 10 and v > 4.8:
            return 13.12 + (0.6215 * t) - (11.37 * (v**0.16)) + (0.3965 * t * (v**0.16))
        return t # If it's warm, the "discomfort" is just the base temp

    df['cold_DI'] = df.apply(get_wind_chill, axis=1).round(2)

    # 3. Save the results
    df.to_csv(output_file, index=False)
    
    print(f"✅ Success! New columns 'heat_DI' and 'cold_DI' added.")
    print(df[['temp', 'rhum', 'wspd', 'heat_DI', 'cold_DI']].head())
else:
    print(f"❌ Error: Could not find {input_file}")