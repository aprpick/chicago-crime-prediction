"""
QUICK XGBoost Training - Get Results Fast!
Optimized for speed - minimal hyperparameter search
Use this to get baseline results quickly, then tune later

Input: 24.1_training_ready.csv
Outputs:
  - Trained model: 01.3_xgboost_model_quick.json
  - Performance report: 01.1_training_results_quick.md
  - Feature importance plot: 01.2_feature_importance_quick.png

Estimated Runtime: 5-10 minutes
"""

import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.utils.class_weight import compute_sample_weight
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# ============================================================
# CONFIGURATION
# ============================================================
INPUT_FILE = '../01 Foundation & Data/24.1_training_ready.csv'

MODEL_OUTPUT = '01.3_xgboost_model_quick.json'
RESULTS_OUTPUT = '01.1_training_results_quick.md'
FEATURE_IMPORTANCE_PLOT = '01.2_feature_importance_quick.png'

# Quick baseline parameters (proven to work well)
QUICK_PARAMS = {
    'max_depth': 6,
    'learning_rate': 0.1,
    'n_estimators': 150,
    'subsample': 0.8,
    'colsample_bytree': 0.8,
    'min_child_weight': 5,
    'objective': 'reg:squarederror',
    'random_state': 42,
    'n_jobs': -1
}

TEST_SIZE = 0.2
RANDOM_STATE = 42
# ============================================================

def print_header(text):
    """Print formatted section header"""
    print("\n" + "="*80)
    print(f"  {text}")
    print("="*80)

def load_data(filepath):
    """Load and prepare data"""
    print_header("LOADING DATA")
    print(f"Reading: {filepath}")
    
    df = pd.read_csv(filepath)
    print(f"✓ Loaded {len(df):,} rows × {len(df.columns)} columns")
    
    # Separate features and target
    X = df.drop('Severity_Score', axis=1)
    y = df['Severity_Score']
    
    print(f"\nFeatures: {list(X.columns)}")
    print(f"Target: Severity_Score")
    
    # Quick stats
    zero_pct = (y == 0).sum() / len(y) * 100
    print(f"\nTarget Statistics:")
    print(f"  Range: {y.min()} to {y.max()}")
    print(f"  Mean: {y.mean():.2f}")
    print(f"  Median: {y.median():.2f}")
    print(f"  Zero-crime blocks: {zero_pct:.1f}%")
    
    return X, y

def split_data(X, y):
    """Split into train/test with stratification"""
    print_header("SPLITTING DATA")
    
    # Bin severity scores for stratified split (handles zero imbalance)
    print("Creating stratified bins to handle 57% zero-severity blocks...")
    y_binned = pd.cut(y, bins=[-1, 0, 3, 8, 15, 200], labels=[0,1,2,3,4])
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=TEST_SIZE,
        random_state=RANDOM_STATE,
        stratify=y_binned
    )
    
    print(f"✓ Train: {len(X_train):,} samples ({(1-TEST_SIZE)*100:.0f}%)")
    print(f"✓ Test:  {len(X_test):,} samples ({TEST_SIZE*100:.0f}%)")
    
    # Check zero distribution
    train_zeros = (y_train == 0).sum() / len(y_train) * 100
    test_zeros = (y_test == 0).sum() / len(y_test) * 100
    print(f"\nZero-severity distribution:")
    print(f"  Train: {train_zeros:.1f}%")
    print(f"  Test:  {test_zeros:.1f}%")
    
    return X_train, X_test, y_train, y_test

def train_model(X_train, y_train, params):
    """Train XGBoost with sample weights for class imbalance"""
    print_header("TRAINING MODEL")
    
    print("Model Configuration:")
    for key, value in params.items():
        if key not in ['random_state', 'n_jobs', 'objective']:
            print(f"  {key:20s} = {value}")
    
    # Compute sample weights (give more importance to rare non-zero blocks)
    print("\n⚖️  Computing sample weights for class imbalance...")
    sample_weights = np.where(y_train == 0, 1.0, 2.5)
    print(f"  Zero blocks: weight = 1.0")
    print(f"  Non-zero blocks: weight = 2.5")
    
    # Train model
    print("\n🚀 Training XGBoost model...")
    start_time = datetime.now()
    
    model = xgb.XGBRegressor(**params)
    model.fit(
        X_train, y_train,
        sample_weight=sample_weights,
        verbose=False
    )
    
    duration = datetime.now() - start_time
    print(f"✓ Training completed in {duration}")
    
    return model

def evaluate_model(model, X_train, y_train, X_test, y_test):
    """Evaluate model performance"""
    print_header("MODEL EVALUATION")
    
    # Predictions
    y_train_pred = model.predict(X_train)
    y_test_pred = model.predict(X_test)
    
    # Metrics
    def calc_metrics(y_true, y_pred, dataset_name):
        mse = mean_squared_error(y_true, y_pred)
        rmse = np.sqrt(mse)
        mae = mean_absolute_error(y_true, y_pred)
        r2 = r2_score(y_true, y_pred)
        
        print(f"\n{dataset_name} Performance:")
        print(f"  RMSE: {rmse:.4f}  (avg error ±{rmse:.2f} severity points)")
        print(f"  MAE:  {mae:.4f}  (typical error {mae:.2f} severity points)")
        print(f"  R²:   {r2:.4f}  (explains {r2*100:.1f}% of variance)")
        
        return {'mse': mse, 'rmse': rmse, 'mae': mae, 'r2': r2}
    
    train_metrics = calc_metrics(y_train, y_train_pred, "TRAINING SET")
    test_metrics = calc_metrics(y_test, y_test_pred, "TEST SET")
    
    # Overfitting check
    overfit_ratio = train_metrics['rmse'] / test_metrics['rmse']
    print(f"\nGeneralization Check:")
    print(f"  Train/Test RMSE ratio: {overfit_ratio:.2f}")
    if overfit_ratio < 0.85:
        print("  ⚠️  Model may be overfitting")
    elif overfit_ratio > 1.15:
        print("  ⚠️  Model may be underfitting")
    else:
        print("  ✓ Good generalization!")
    
    # Analyze predictions on zero vs non-zero blocks
    print(f"\nPrediction Analysis:")
    zero_mask = y_test == 0
    nonzero_mask = y_test > 0
    
    if zero_mask.sum() > 0:
        zero_mae = mean_absolute_error(y_test[zero_mask], y_test_pred[zero_mask])
        print(f"  Zero-severity blocks MAE: {zero_mae:.4f}")
    
    if nonzero_mask.sum() > 0:
        nonzero_mae = mean_absolute_error(y_test[nonzero_mask], y_test_pred[nonzero_mask])
        print(f"  Non-zero blocks MAE: {nonzero_mae:.4f}")
    
    return {
        'train': train_metrics,
        'test': test_metrics,
        'predictions': y_test_pred
    }

def analyze_feature_importance(model, feature_names, output_file):
    """Create feature importance plot"""
    print_header("FEATURE IMPORTANCE")
    
    # Get importances
    importance = model.feature_importances_
    feature_df = pd.DataFrame({
        'feature': feature_names,
        'importance': importance
    }).sort_values('importance', ascending=False)
    
    print("\nFeature Importance Ranking:")
    for i, row in feature_df.iterrows():
        rank = feature_df.index.get_loc(i) + 1
        bar = "█" * int(row['importance'] * 50)
        print(f"  {rank:2d}. {row['feature']:25s} {row['importance']:.4f} {bar}")
    
    # Plot
    plt.figure(figsize=(10, 8))
    colors = plt.cm.viridis(np.linspace(0.3, 0.9, len(feature_df)))
    plt.barh(feature_df['feature'], feature_df['importance'], color=colors)
    plt.xlabel('Importance Score', fontsize=12, fontweight='bold')
    plt.ylabel('Feature', fontsize=12, fontweight='bold')
    plt.title('XGBoost Feature Importance (Quick Baseline)', fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"\n✓ Plot saved: {output_file}")
    
    return feature_df

def save_results(metrics, params, feature_importance, output_file):
    """Save markdown report"""
    lines = []
    lines.append("# XGBoost Training Results - QUICK BASELINE")
    lines.append("")
    lines.append(f"**Training Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append(f"**Purpose:** Quick baseline model - faster training, tune later")
    lines.append(f"**Runtime:** ~5-10 minutes")
    lines.append("")
    lines.append("---")
    lines.append("")
    
    lines.append("## Model Configuration")
    lines.append("")
    lines.append("| Parameter | Value |")
    lines.append("|-----------|-------|")
    for key, value in params.items():
        if key not in ['random_state', 'n_jobs', 'objective']:
            lines.append(f"| {key} | {value} |")
    lines.append("")
    lines.append("**Note:** Sample weights used (non-zero blocks weighted 2.5x)")
    lines.append("")
    lines.append("---")
    lines.append("")
    
    lines.append("## Performance Metrics")
    lines.append("")
    lines.append("### Training Set")
    lines.append("| Metric | Value |")
    lines.append("|--------|-------|")
    lines.append(f"| RMSE | {metrics['train']['rmse']:.4f} |")
    lines.append(f"| MAE | {metrics['train']['mae']:.4f} |")
    lines.append(f"| R² Score | {metrics['train']['r2']:.4f} |")
    lines.append("")
    
    lines.append("### Test Set")
    lines.append("| Metric | Value |")
    lines.append("|--------|-------|")
    lines.append(f"| RMSE | {metrics['test']['rmse']:.4f} |")
    lines.append(f"| MAE | {metrics['test']['mae']:.4f} |")
    lines.append(f"| R² Score | {metrics['test']['r2']:.4f} |")
    lines.append("")
    
    lines.append("### Interpretation")
    lines.append(f"- **Average prediction error:** ±{metrics['test']['rmse']:.2f} severity points")
    lines.append(f"- **Typical error:** {metrics['test']['mae']:.2f} severity points")
    lines.append(f"- **Variance explained:** {metrics['test']['r2']*100:.1f}%")
    lines.append("")
    lines.append("---")
    lines.append("")
    
    lines.append("## Feature Importance")
    lines.append("")
    lines.append("| Rank | Feature | Importance | Notes |")
    lines.append("|------|---------|------------|-------|")
    for i, row in feature_importance.iterrows():
        rank = feature_importance.index.get_loc(i) + 1
        notes = ""
        if row['importance'] < 0.01:
            notes = "⚠️ Low importance - consider removing"
        elif rank <= 3:
            notes = "🌟 Top predictor"
        lines.append(f"| {rank} | {row['feature']} | {row['importance']:.4f} | {notes} |")
    lines.append("")
    lines.append("---")
    lines.append("")
    
    lines.append("## Next Steps for Optimization")
    lines.append("")
    lines.append("1. **Remove low-importance features** (importance < 0.01) and retrain")
    lines.append("2. **Hyperparameter tuning:** Try different max_depth, learning_rate, n_estimators")
    lines.append("3. **Advanced techniques:**")
    lines.append("   - Two-stage model (predict zero vs. non-zero, then predict severity)")
    lines.append("   - Try LightGBM or CatBoost")
    lines.append("   - Add interaction features (e.g., Community_Area × weekend_night_peak)")
    lines.append("4. **Temporal validation:** Train on 2023-2024, test on 2025")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("**Files Generated:**")
    lines.append(f"- Model: `{MODEL_OUTPUT}`")
    lines.append(f"- Report: `{RESULTS_OUTPUT}`")
    lines.append(f"- Plot: `{FEATURE_IMPORTANCE_PLOT}`")
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    
    print(f"✓ Report saved: {output_file}")

def main():
    print("\n" + "="*80)
    print("     QUICK XGBOOST TRAINING - CHICAGO CRIME PREDICTION")
    print("="*80)
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("Estimated runtime: 5-10 minutes")
    
    # Load data
    X, y = load_data(INPUT_FILE)
    
    # Split data
    X_train, X_test, y_train, y_test = split_data(X, y)
    
    # Train model
    model = train_model(X_train, y_train, QUICK_PARAMS)
    
    # Evaluate
    results = evaluate_model(model, X_train, y_train, X_test, y_test)
    
    # Feature importance
    feature_importance = analyze_feature_importance(
        model, X.columns, FEATURE_IMPORTANCE_PLOT
    )
    
    # Save model
    print_header("SAVING OUTPUTS")
    # Use get_booster() to access the underlying XGBoost model
    model.get_booster().save_model(MODEL_OUTPUT)
    print(f"✓ Model saved: {MODEL_OUTPUT}")
    
    # Save report
    save_results(results, QUICK_PARAMS, feature_importance, RESULTS_OUTPUT)
    
    # Final summary
    print_header("✅ QUICK TRAINING COMPLETE!")
    print(f"\nTest Set Performance:")
    print(f"  RMSE: {results['test']['rmse']:.4f} (±{results['test']['rmse']:.2f} severity points)")
    print(f"  MAE:  {results['test']['mae']:.4f} ({results['test']['mae']:.2f} severity points avg error)")
    print(f"  R²:   {results['test']['r2']:.4f} ({results['test']['r2']*100:.1f}% variance explained)")
    
    print(f"\nTop 3 Most Important Features:")
    for i, row in feature_importance.head(3).iterrows():
        print(f"  {i+1}. {row['feature']} ({row['importance']:.4f})")
    
    print(f"\n📁 Output Files:")
    print(f"  1. {MODEL_OUTPUT}")
    print(f"  2. {RESULTS_OUTPUT}")
    print(f"  3. {FEATURE_IMPORTANCE_PLOT}")
    
    print("\n💡 Next: Review results, then run full hyperparameter search for optimization")
    print("="*80)

if __name__ == "__main__":
    main()