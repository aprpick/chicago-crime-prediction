"""
Generate Predictions for Power BI Dashboard
Loads trained model and generates predictions for all combinations of:
- 77 Community Areas
- 365 days (full year)
- 8 time blocks per day

Output: CSV file ready for Power BI import
"""

import pandas as pd
import numpy as np
import xgboost as xgb
from datetime import datetime, timedelta
import os

# ============================================================
# CONFIGURATION
# ============================================================
MODEL_FILE = '01.3_xgboost_model_final.json'
TRAINING_DATA = '../01 Foundation & Data/24.1_training_ready.csv'
OUTPUT_FILE = '02.1_predictions_2026.csv'

# Prediction period
START_DATE = '2026-01-01'
END_DATE = '2026-12-31'

# Chicago community areas (1-77)
COMMUNITY_AREAS = list(range(1, 78))

# Time blocks (0-7 representing 3-hour periods)
TIME_BLOCKS = list(range(8))
TIME_BLOCK_LABELS = {
    0: '00:00-03:00 (Midnight-3am)',
    1: '03:00-06:00 (3am-6am)',
    2: '06:00-09:00 (6am-9am)',
    3: '09:00-12:00 (9am-Noon)',
    4: '12:00-15:00 (Noon-3pm)',
    5: '15:00-18:00 (3pm-6pm)',
    6: '18:00-21:00 (6pm-9pm)',
    7: '21:00-00:00 (9pm-Midnight)'
}

# ============================================================

def load_model():
    """Load the trained XGBoost model"""
    print(f"Loading model: {MODEL_FILE}")
    model = xgb.XGBRegressor()
    model.load_model(MODEL_FILE)
    print(f"✓ Model loaded successfully")
    return model

def load_feature_template():
    """Load training data to get feature names and typical values"""
    print(f"\nLoading training data template: {TRAINING_DATA}")
    df = pd.read_csv(TRAINING_DATA)
    
    # Get feature columns (exclude target)
    features = [col for col in df.columns if col != 'Severity_Score']
    print(f"✓ Features to predict with: {features}")
    
    return features, df

def generate_date_features(date):
    """Generate date-related features for a given date"""
    return {
        'day_of_week': date.weekday(),  # 0=Monday, 6=Sunday
        'month': date.month,
        'weekend_night_peak': 1 if (date.weekday() in [4, 5]) else 0,  # Simplified
    }

def generate_prediction_data(features, template_df):
    """Generate all combinations of area × date × time for predictions"""
    print("\n" + "="*70)
    print("GENERATING PREDICTION DATA")
    print("="*70)
    
    # Generate date range
    start = pd.to_datetime(START_DATE)
    end = pd.to_datetime(END_DATE)
    dates = pd.date_range(start, end, freq='D')
    
    print(f"\nDate range: {START_DATE} to {END_DATE}")
    print(f"Days: {len(dates)}")
    print(f"Community areas: {len(COMMUNITY_AREAS)}")
    print(f"Time blocks per day: {len(TIME_BLOCKS)}")
    print(f"Total predictions: {len(dates) * len(COMMUNITY_AREAS) * len(TIME_BLOCKS):,}")
    
    # Create all combinations
    data = []
    
    for date in dates:
        month = date.month
        dow = date.weekday()
        
        # Generate for each area and time block
        for area in COMMUNITY_AREAS:
            for time_block in TIME_BLOCKS:
                row = {
                    'Date': date.strftime('%Y-%m-%d'),
                    'Community_Area': area,
                    'time_block': time_block,
                    'time_block_label': TIME_BLOCK_LABELS[time_block],
                    'day_of_week': dow,
                    'month': month,
                    'Year': date.year,
                    'Week': date.isocalendar()[1],
                    'DayName': date.strftime('%A'),
                }
                
                # Adjust weekend_night_peak based on day and time
                # Fri/Sat during blocks 6,7,0 (6pm-3am)
                if dow in [4, 5] and time_block in [6, 7, 0]:
                    row['weekend_night_peak'] = 1
                else:
                    row['weekend_night_peak'] = 0
                
                data.append(row)
    
    df = pd.DataFrame(data)
    print(f"\n✓ Generated {len(df):,} prediction rows")
    print(f"\nFeatures used (5 total):")
    print(f"  - Community_Area (1-77)")
    print(f"  - time_block (0-7)")
    print(f"  - day_of_week (0-6)")
    print(f"  - month (1-12)")
    print(f"  - weekend_night_peak (0/1) [auto-calculated]")
    print(f"\n✓ ALL features calculated automatically from date!")
    
    return df)
                row['major_event'] = 0
                
                data.append(row)
    
    df = pd.DataFrame(data)
    print(f"\n✓ Generated {len(df):,} prediction rows")
    print(f"\nFeatures used:")
    print(f"  - Community_Area (1-77)")
    print(f"  - time_block (0-7)")
    print(f"  - day_of_week (0-6)")
    print(f"  - month (1-12)")
    print(f"  - weekend_night_peak (0/1)")
    print(f"  - major_event (0/1) [set manually for known events]")
    
    return df

def make_predictions(model, df, features):
    """Generate predictions using the trained model"""
    print("\n" + "="*70)
    print("MAKING PREDICTIONS")
    print("="*70)
    
    # Prepare feature matrix (match training feature order)
    X = df[features].copy()
    
    print(f"\nFeature matrix shape: {X.shape}")
    print(f"Features: {list(X.columns)}")
    
    # Make predictions
    print("\nGenerating predictions...")
    predictions = model.predict(X)
    
    # Add predictions to dataframe
    df['Predicted_Severity'] = predictions
    df['Predicted_Severity'] = df['Predicted_Severity'].clip(lower=0).round(2)
    
    print(f"✓ Predictions complete")
    print(f"\nPrediction statistics:")
    print(f"  Min:    {predictions.min():.2f}")
    print(f"  Max:    {predictions.max():.2f}")
    print(f"  Mean:   {predictions.mean():.2f}")
    print(f"  Median: {np.median(predictions):.2f}")
    
    return df

def add_summary_columns(df):
    """Add helpful summary columns for Power BI"""
    print("\n" + "="*70)
    print("ADDING SUMMARY COLUMNS")
    print("="*70)
    
    # Risk level categories
    def categorize_risk(severity):
        if severity < 1:
            return 'Very Low'
        elif severity < 2:
            return 'Low'
        elif severity < 4:
            return 'Moderate'
        elif severity < 7:
            return 'High'
        else:
            return 'Very High'
    
    df['Risk_Level'] = df['Predicted_Severity'].apply(categorize_risk)
    
    # Relative to annual max (for each area)
    annual_max = df.groupby('Community_Area')['Predicted_Severity'].transform('max')
    df['Relative_to_Max'] = (df['Predicted_Severity'] / annual_max * 100).round(1)
    
    # Weekend flag
    df['Is_Weekend'] = df['day_of_week'].isin([5, 6]).astype(int)
    
    # Time period label
    def time_period(block):
        if block in [0, 1]:
            return 'Night (Midnight-6am)'
        elif block in [2, 3]:
            return 'Morning (6am-Noon)'
        elif block in [4, 5]:
            return 'Afternoon (Noon-6pm)'
        else:
            return 'Evening (6pm-Midnight)'
    
    df['Time_Period'] = df['time_block'].apply(time_period)
    
    print("✓ Summary columns added:")
    print("  - Risk_Level (Very Low to Very High)")
    print("  - Relative_to_Max (% of annual max per area)")
    print("  - Is_Weekend (0/1)")
    print("  - Time_Period (4 categories)")
    
    return df

def save_predictions(df, output_file):
    """Save predictions to CSV"""
    print("\n" + "="*70)
    print("SAVING PREDICTIONS")
    print("="*70)
    
    # Select columns for Power BI (remove feature columns, keep useful ones)
    output_cols = [
        'Date', 'Year', 'Month', 'Week', 'DayName', 'Is_Weekend',
        'Community_Area', 
        'time_block', 'time_block_label', 'Time_Period',
        'Predicted_Severity', 'Risk_Level', 'Relative_to_Max'
    ]
    
    df_output = df[output_cols].copy()
    
    # Sort by date, area, time
    df_output = df_output.sort_values(['Date', 'Community_Area', 'time_block'])
    
    print(f"\nSaving to: {output_file}")
    df_output.to_csv(output_file, index=False)
    
    file_size_mb = os.path.getsize(output_file) / (1024 * 1024)
    print(f"✓ Saved {len(df_output):,} rows")
    print(f"  File size: {file_size_mb:.1f} MB")
    print(f"  Columns: {len(df_output.columns)}")
    
    return df_output

def print_summary(df):
    """Print summary statistics"""
    print("\n" + "="*70)
    print("PREDICTION SUMMARY")
    print("="*70)
    
    print("\nTop 10 Highest Risk Predictions:")
    top10 = df.nlargest(10, 'Predicted_Severity')[
        ['Date', 'Community_Area', 'time_block_label', 'Predicted_Severity', 'Risk_Level']
    ]
    print(top10.to_string(index=False))
    
    print("\n\nAverage Severity by Time Block:")
    by_time = df.groupby('time_block_label')['Predicted_Severity'].mean().sort_values(ascending=False)
    for label, severity in by_time.items():
        print(f"  {label:30s}: {severity:.2f}")
    
    print("\n\nAverage Severity by Day of Week:")
    day_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    by_day = df.groupby('day_of_week')['Predicted_Severity'].mean()
    for dow, severity in by_day.items():
        print(f"  {day_names[dow]:10s}: {severity:.2f}")
    
    print("\n\nRisk Level Distribution:")
    risk_dist = df['Risk_Level'].value_counts(normalize=True) * 100
    for level, pct in risk_dist.sort_index().items():
        print(f"  {level:12s}: {pct:.1f}%")

def main():
    print("="*70)
    print("      POWER BI PREDICTION GENERATOR")
    print("      Chicago Crime Severity Predictions")
    print("="*70)
    print(f"\nStarted: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Load model and template
    model = load_model()
    features, template_df = load_feature_template()
    
    # Generate prediction data
    df = generate_prediction_data(features, template_df)
    
    # Make predictions
    df = make_predictions(model, df, features)
    
    # Add summary columns
    df = add_summary_columns(df)
    
    # Save to CSV
    df_output = save_predictions(df, OUTPUT_FILE)
    
    # Print summary
    print_summary(df_output)
    
    print("\n" + "="*70)
    print("✅ PREDICTIONS COMPLETE!")
    print("="*70)
    print(f"\nOutput file: {OUTPUT_FILE}")
    print(f"Ready for Power BI import")
    print(f"\nNext steps:")
    print("  1. Open Power BI Desktop")
    print("  2. Import this CSV file")
    print("  3. Create visualizations using the prediction data")
    print("="*70)

if __name__ == "__main__":
    main()