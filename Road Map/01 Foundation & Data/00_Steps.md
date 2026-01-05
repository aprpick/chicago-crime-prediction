Data acquired 

    https://data.cityofchicago.org/Public-Safety/Crimes-2001-to-Present/ijzp-q8t2/about_data
    created - chicago_crime_2001_2025_(raw).csv

Unique Identifiers Added to Each Row

    unique_identifier.py
    edited - chicago_crime_2001_2025_(raw).csv

Data Previewed

    preview_data.py
    created - preview_data_100.csv

Date Sorting Confirmed

    sorting_checker.py

Data Rows Truncated to 2021-2025

    data_row_truncator_2023_2025.py
    created - chicago_crime_2023_2025.csv

Data Columns Truncated to Date,Primary Type,Description,Community Area,Domestic,Latitude,Longitude

    data_column_truncator.py
    created - chicago_crime_2023_2025_7_rows.csv

Data Analyzed 

    data_analyzer.py

"Domestic = True" Removed

    domestic_remove.py
    created - chicago_crime_2023_2025_7_rows_(working).csv

"Primary Type"s Removed -'NARCOTICS', 'WEAPONS VIOLATION', 'CONCEALED CARRY LICENSE VIOLATION', 'LIQUOR LAW VIOLATION', 'PROSTITUTION', 'GAMBLING', 'PUBLIC INDECENCY', 'INTERFERENCE WITH PUBLIC OFFICER', 'OTHER NARCOTIC VIOLATION', 'NON-CRIMINAL', 'OTHER OFFENSE', 'OBSCENITY', 'STALKING','DECEPTIVE PRACTICE','OFFENSE INVOLVING CHILDREN'

    remove_enforcement_crimes.py
    edited - chicago_crime_2023_2025_7_rows_(working).csv


Analyze "Primary Type" + "Description" for Severity Scoring

    severity_analyzer.py

Remove rare "Primary Type" + "Description" Combinations for severity calculation

    remove_rare_combinations.py
    edited - chicago_crime_2023_2025_7_rows_(working).csv

Add Severity Score Column

    add_severity_scores.py
    edited - chicago_crime_2023_2025_7_rows_(working).csv

Removing Unecessary Columns - Description, Domestic, Latitude, Longitude 

    12_unnecessary_columns_remove.py
    edited - chicago_crime_2023_2025_7_rows_(working).csv