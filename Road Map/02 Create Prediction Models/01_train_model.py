import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error
import os

# --- CONFIGURATION ---
script_dir = os.path.dirname(os.path.abspath(__file__))
# Go up one level (..), then down into '01 Foundation & Data'
INPUT_FILE = os.path.join(script_dir, "..", "01 Foundation & Data", "28_training_data_with_zeros.csv")
MODEL_FILE = os.path.join(script_dir, "chicago_crime_model.json")

# --- 1. LOAD DATA ---
print(f"Loading data from: {os.path.abspath(INPUT_FILE)}")
if not os.path.exists(INPUT_FILE):
    print("ERROR: File not found!")
    exit()

df = pd.read_csv(INPUT_FILE)

# --- 2. PREPARE FEATURES ---
target_col = 'Total_Severity_Load'
drop_cols = ['Date', target_col]

X = df.drop(columns=drop_cols)
y = df[target_col]

print(f"Training on {len(X)} rows with {len(X.columns)} features.")

# --- 3. SPLIT ---
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# --- 4. DEFINE MODEL ---
model = xgb.XGBRegressor(
    objective='reg:squarederror',
    n_estimators=1000,
    learning_rate=0.05,
    max_depth=6,
    subsample=0.8,
    colsample_bytree=0.8,
    n_jobs=-1,
    random_state=42,
    early_stopping_rounds=50 # Stop if it doesn't get better for 50 trees
)

# --- 5. TRAIN ---
print("\nTraining XGBoost Model...")
model.fit(
    X_train, y_train,
    eval_set=[(X_test, y_test)],
    verbose=100
)

# --- 6. EVALUATE ---
print("\n--- RESULTS ---")
predictions = model.predict(X_test)
mae = mean_absolute_error(y_test, predictions)
avg_severity = y.mean()

print(f"Mean Absolute Error (MAE): {mae:.2f}")
print(f"Average Severity Load: {avg_severity:.2f}")

# --- 7. SAVE (THE FIX IS HERE) ---
print(f"Saving model to {MODEL_FILE}...")
# We use .get_booster() to bypass the bug in the wrapper
model.get_booster().save_model(MODEL_FILE)
print("Done. The brain is saved.")