import pandas as pd
import matplotlib.pyplot as plt

# 1. Load the data
# We use the filename you provided, assuming it is formatted as a CSV
file_name = '02.1_predictions_2026.csv'

try:
    df = pd.read_csv(file_name)
    print(f"✅ Successfully loaded {len(df)} rows.")
except Exception as e:
    print(f"❌ Error loading file: {e}")
    exit()

# 2. Check if 'Community_Area' exists before proceeding
if 'Community_Area' not in df.columns:
    print("❌ Column 'Community_Area' not found in the CSV headers.")
    print(f"Found headers: {list(df.columns)}")
    exit()

# 3. Create the Aggregated Table
# We group by Community_Area and calculate the 4 metrics you asked for
summary_table = df.groupby('Community_Area').agg(
    Total_Rows=('Community_Area', 'size'),           # Count of rows
    Unique_Months=('month', 'nunique'),              # Count of unique months
    Unique_Days=('DayName', 'nunique'),              # Count of unique days
    Unique_Time_Blocks=('time_block_label', 'nunique') # Count of unique time blocks
).reset_index()

# 4. Print the Data Table to the Console
print("\n--- DATA SUMMARY TABLE ---")
print(summary_table.to_string(index=False))
print(f"\nTotal Communities Found: {len(summary_table)}")

# 5. Create the "Visual Table" (Bar Charts)
# We will create a figure with 2 subplots to visualize the data distribution
plt.figure(figsize=(15, 8))

# Subplot 1: Total Rows per Community Area
plt.subplot(2, 1, 1) # 2 rows, 1 column, position 1
plt.bar(summary_table['Community_Area'].astype(str), summary_table['Total_Rows'], color='skyblue')
plt.xlabel('Community Area')
plt.ylabel('Total Rows (Count)')
plt.title('Row Count by Community Area')
plt.xticks(rotation=90, fontsize=8) # Rotate labels so they fit

# Subplot 2: Check for Completeness (Unique Months count)
# This checks if some communities are missing months of data
plt.subplot(2, 1, 2) # 2 rows, 1 column, position 2
plt.bar(summary_table['Community_Area'].astype(str), summary_table['Unique_Months'], color='salmon')
plt.xlabel('Community Area')
plt.ylabel('Unique Months Found')
plt.title('Unique Months per Community (Completeness Check)')
plt.xticks(rotation=90, fontsize=8)

plt.tight_layout()
plt.show()