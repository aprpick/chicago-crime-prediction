Data acquired 

    https://data.cityofchicago.org/Public-Safety/Crimes-2001-to-Present/ijzp-q8t2/about_data
    created - chicago_crime_2001_2025_(raw).csv

Unique Identifiers Added to Each Row

    01_unique_identifier.py
    edited - chicago_crime_2001_2025_(raw).csv

Data Previewed

    02_preview_data.py
    created - preview_data_100.csv

Date Sorting Confirmed

    03_sorting_checker.py

Data Rows Truncated to 2021-2025

    04_data_row_truncator_2023_2025.py
    created - chicago_crime_2023_2025.csv

Data Columns Truncated to Date,Primary Type,Description,Community Area,Domestic,Latitude,Longitude

    05_data_column_truncator.py
    created - chicago_crime_2023_2025_7_rows.csv

Data Analyzed 

    06_data_analyzer.py

"Domestic = True" Removed

    07_domestic_remove.py
    created - chicago_crime_2023_2025_7_rows_(working).csv

"Primary Type"s Removed -'NARCOTICS', 'WEAPONS VIOLATION', 'CONCEALED CARRY LICENSE VIOLATION', 'LIQUOR LAW VIOLATION', 'PROSTITUTION', 'GAMBLING', 'PUBLIC INDECENCY', 'INTERFERENCE WITH PUBLIC OFFICER', 'OTHER NARCOTIC VIOLATION', 'NON-CRIMINAL', 'OTHER OFFENSE', 'OBSCENITY', 'STALKING','DECEPTIVE PRACTICE','OFFENSE INVOLVING CHILDREN'

    08_remove_enforcement_crimes.py
    edited - chicago_crime_2023_2025_7_rows_(working).csv


Analyze "Primary Type" + "Description" for Severity Scoring

    09_severity_analyzer.py

Remove rare "Primary Type" + "Description" Combinations for severity calculation

    10_remove_rare_combinations.py
    edited - chicago_crime_2023_2025_7_rows_(working).csv

Add Severity Score Column

    11_add_severity_scores.py
    edited - chicago_crime_2023_2025_7_rows_(working).csv

Removing Unecessary Columns - Description, Domestic, Latitude, Longitude 

    12_unnecessary_columns_remove.py
    edited - chicago_crime_2023_2025_7_rows_(working).csv

Adding Weekend Features - weekend_night_peak (Fri 8pm-Sat 3am, Sat 8pm-Sun 3am) weekend_regular (Fri 6-8pm, Sat/Sun) 

    13_adding_weekends.py
    edited - chicago_crime_2023_2025_7_rows_(working).csv

Adding Holidays - theft/violence prone occasions

    14_adding_holidays.py
    edited - chicago_crime_2023_2025_7_rows_(working).csv

Downloading Weather Data

    15_download_weather_data.py
    created - 15_chicago_weather_2023_2025.csv

Truncating weather data 

    16_weather_data_column_truncator.py
    edited - 15_chicago_weather_2023_2025.csv

Weather Columns Truncated

    17_weather_data_column_truncator.py
    created - 17_chicago_weather_2023_2025_truncated.csv

Weather DI Values averaged out over 6 hour periods

    18_adding_DI_to_working.py
    created - 18_chicago_weather_6hr_grouped.csv

Weather DI Added to Working CSV

    19_DI_added_to_working.py
    edited - 15_chicago_weather_2023_2025.csv
    
School in/out

    20_school_in_out.py
    edited - 15_chicago_weather_2023_2025.csv

Adding big events - Lollapalooza, Chicago Marathon, Pride Parade, St. Patrick's Day Parade

    21_big_events.py
    edited - 15_chicago_weather_2023_2025.csv

Adding moon illumation 

    22_moon_illumination.py
    edited - 15_chicago_weather_2023_2025.csv

Adding sun brightness
    
    23_add_solar_altitude.py
    23_solar_altitude.csv