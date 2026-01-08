
exit("deprecated")

import pandas as pd
import os

# Setup paths
script_dir = os.path.dirname(os.path.abspath(__file__))
crime_path = os.path.join(script_dir, 'chicago_crime_2023_2025(working).csv')
weather_grouped_path = os.path.join(script_dir, '18_chicago_weather_6hr_grouped.csv')
output_path = os.path.join(script_dir, '19_crime_Data_Working.csv')

# 1. Load the data
df_crime = pd.read_csv(crime_path)
df_weather = pd.read_csv(weather_grouped_path)

# 2. Convert date columns to actual datetime objects
df_crime['Date'] = pd.to_datetime(df_crime['Date'])
df_weather['datetime'] = pd.to_datetime(df_weather['datetime'])

# 3. Create a helper column in Crime data to match the Weather blocks
# 'dt.floor('6H')' turns 14:32:00 into 12:00:00 (the start of that 6-hour window)
df_crime['weather_merge_key'] = df_crime['Date'].dt.floor('6H')

# 4. Merge the two dataframes
# We use 'left' join so we keep all crimes even if weather data is missing for some reason
df_final = pd.merge(
    df_crime, 
    df_weather, 
    left_on='weather_merge_key', 
    right_on='datetime', 
    how='left'
)

# 5. Cleanup: remove the helper columns used for merging
df_final = df_final.drop(columns=['weather_merge_key', 'datetime'])

# 6. Save the results
df_final.to_csv(output_path, index=False)

print(f"✅ Merge Complete!")
print(f"Original Crime Rows: {len(df_crime)}")
print(f"Final Merged Rows: {len(df_final)}")
print("\nPreview of mapped data:")
print(df_final[['Date', 'heat_DI', 'cold_DI']].head())