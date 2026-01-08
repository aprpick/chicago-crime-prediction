import pandas as pd
import numpy as np
import os

# --- CONFIG ---
INPUT_FILE = "00_chicago_crime_2023_2025(working).csv"

def main():
    if not os.path.exists(INPUT_FILE):
        print(f"ERROR: {INPUT_FILE} not found.")
        return

    print(f"Scanning {INPUT_FILE} for training estimation...\n")
    
    # Load data
    df = pd.read_csv(INPUT_FILE)
    
    # --- METRICS ---
    num_rows = len(df)
    num_cols = len(df.columns)
    memory_usage = df.memory_usage(deep=True).sum() / (1024 * 1024) # in MB
    
    # Count Numeric vs Text columns
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    text_cols = df.select_dtypes(exclude=[np.number]).columns.tolist()

    # --- THE REPORT ---
    print("="*40)
    print("      DATASET VITAL SIGNS")
    print("="*40)
    print(f"TOTAL ROWS:      {num_rows:,}")
    print(f"TOTAL FEATURES:  {num_cols}")
    print(f"MEMORY USAGE:    {memory_usage:.2f} MB")
    print("-" * 40)
    
    print(f"\nNUMERIC FEATURES (Ready to Train): {len(numeric_cols)}")
    # Print first 5 to verify
    print(f"Examples: {numeric_cols[:5]}...")

    print(f"\nTEXT/OBJECT FEATURES (Must be encoded): {len(text_cols)}")
    if len(text_cols) > 0:
        print(f"⚠️  WARNING: XGBoost cannot read these directly:")
        print(f"   {text_cols}")
        print("   (You must One-Hot Encode or Label Encode these before training)")
    else:
        print("✅  Great! All data is numeric.")

    # --- ESTIMATION MATH ---
    # Benchmark: A standard modern laptop (8-16GB RAM, 4-8 Cores)
    # XGBoost processes roughly 100,000 rows x 20 cols in ~3-5 seconds depending on depth.
    
    complexity_factor = num_rows * num_cols
    
    print("\n" + "="*40)
    print("      ESTIMATED TRAINING TIME")
    print("      (Standard Laptop CPU)")
    print("="*40)
    
    if len(text_cols) > 0:
        print("❌ CANNOT ESTIMATE: You have text columns.")
        print("   Fix those first, or the training will crash immediately.")
    else:
        # Very rough heuristic for XGBoost (100 trees)
        # This varies wildly based on CPU, but gives you an order of magnitude.
        estimated_seconds = (complexity_factor / 200000) 
        
        if estimated_seconds < 60:
            print(f"🚀 FAST: ~{estimated_seconds:.1f} seconds")
        else:
            print(f"⏳ NORMAL: ~{estimated_seconds/60:.1f} minutes")
            
    print("\nNOTE: This assumes you are training a standard model (100-500 trees).")
    print("If you run a Grid Search (optimization), multiply this by 50x.")

if __name__ == "__main__":
    main()