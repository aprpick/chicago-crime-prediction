import pandas as pd
import os

# Setup paths
script_dir = os.path.dirname(os.path.abspath(__file__))
input_file = os.path.join(script_dir, '17_chicago_weather_2023_2025_truncated.csv')
output_file = os.path.join(script_dir, '18_chicago_weather_6hr_grouped.csv')

# 1. Load the data
if os.path.exists(input_file):
    df = pd.read_csv(input_file)
    
    # 2. Convert datetime column to actual datetime objects
    df['datetime'] = pd.to_datetime(df['datetime'])
    
    # 3. Group into 6-hour blocks
    # '6H' resamples the data into blocks (00:00, 06:00, 12:00, 18:00)
    # We take the mean (average) of the DI scores for those 6 hours
    df_6hr = df.resample('6H', on='datetime').agg({
        'heat_DI': 'mean',
        'cold_DI': 'mean'
    }).reset_index()
    
    # 4. Round for cleanliness
    df_6hr['heat_DI'] = df_6hr['heat_DI'].round(2)
    df_6hr['cold_DI'] = df_6hr['cold_DI'].round(2)
    
    # 5. Save the new CSV
    df_6hr.to_csv(output_file, index=False)
    
    print(f"✅ Success! Created grouped weather file: {output_file}")
    print("\nPreview of the 6-hour blocks:")
    print(df_6hr.head(8))
else:
    print(f"❌ Error: Could not find {input_file}")