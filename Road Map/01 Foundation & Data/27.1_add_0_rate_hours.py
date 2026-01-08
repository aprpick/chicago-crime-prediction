import pandas as pd
import numpy as np
import os

# --- CONFIGURATION ---
INPUT_FILE = "27_shift_data_for_model.csv"
OUTPUT_FILE = "28_training_data_with_zeros.csv"

# RATIO = 3
# For every 1 row of crime, we create 3 rows of "Silence".
# This creates a dataset that is 75% Safe / 25% Dangerous.
RATIO = 3 

def main():
    if not os.path.exists(INPUT_FILE):
        print(f"ERROR: {INPUT_FILE} not found.")
        return

    print(f"Loading {INPUT_FILE}...")
    df_real = pd.read_csv(INPUT_FILE)
    n_real = len(df_real)
    
    print(f"Original Active Shifts: {n_real:,}")
    print(f"Injecting Zeros (Ratio 1:{RATIO})...")
    print("Strategy: Spatial Cloning (Copying weather/time to random quiet areas)")

    # --- 1. CREATE GHOST ROWS ---
    # We duplicate the real data X times.
    # This guarantees the "Ghost" rows have valid Dates, Hours, Solar, and Weather
    # that actually happened in Chicago history.
    df_zeros = pd.concat([df_real] * RATIO, ignore_index=True)
    
    # --- 2. MODIFY THE GHOSTS ---
    # Set Severity to 0 (Quiet)
    df_zeros['Total_Severity_Load'] = 0
    
    # Randomize Location
    # We assign these quiet moments to random Community Areas (1-77)
    print("Randomizing locations for quiet rows...")
    df_zeros['Community Area'] = np.random.randint(1, 78, size=len(df_zeros))

    # --- 3. COMBINE & SHUFFLE ---
    print("Merging Real and Ghost data...")
    df_final = pd.concat([df_real, df_zeros], ignore_index=True)
    
    # Shuffle the deck so the model doesn't get clumps of zeros
    df_final = df_final.sample(frac=1, random_state=42).reset_index(drop=True)

    # --- 4. STATS & VERIFICATION ---
    print("-" * 30)
    print(f"Total Training Rows: {len(df_final):,}")
    
    avg_old = df_real['Total_Severity_Load'].mean()
    avg_new = df_final['Total_Severity_Load'].mean()
    
    print(f"Avg Severity (Before): {avg_old:.2f} (Bias: Too High)")
    print(f"Avg Severity (After):  {avg_new:.2f} (Realistic)")
    print("-" * 30)

    # --- 5. SAVE ---
    print(f"Saving to {OUTPUT_FILE}...")
    df_final.to_csv(OUTPUT_FILE, index=False)
    print("Done. Ready for training.")

if __name__ == "__main__":
    main()