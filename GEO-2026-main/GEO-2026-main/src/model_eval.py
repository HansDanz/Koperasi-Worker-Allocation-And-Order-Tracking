import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score
from model import TailorOracle # Importing your class

def run_visual_comparison(csv_path):
    # 1. LOAD AND PREPARE
    df = pd.read_csv(csv_path)
    df['Project Start'] = pd.to_datetime(df['Project Start'], dayfirst=True)
    df = df.sort_values('Project Start').reset_index(drop=True)
    
    # 2. CHRONOLOGICAL SPLIT (80/20)
    split_idx = int(len(df) * 0.8)
    train_df = df.iloc[:split_idx]
    test_df = df.iloc[split_idx:]
    
    # 3. TRAIN RANDOM FOREST (Your Oracle)
    oracle = TailorOracle()
    oracle.fit(train_df)
    
    # 4. TRAIN LINEAR REGRESSION (The Baseline)
    # We must replicate the same encoding for the baseline to be fair
    features = ['Name', 'Clothes Type', 'Specialist', 'Clothes Assigned']
    X_train_lr = pd.get_dummies(train_df[features])
    y_train_lr = train_df['Clothes Assigned'] / train_df['Time Needed (in days)']
    
    lr_baseline = LinearRegression()
    lr_baseline.fit(X_train_lr, y_train_lr)
    
    # 5. EVALUATE BOTH ON THE 'FUTURE' TEST SET
    # Random Forest Predictions
    rf_days = oracle.predict(test_df)
    
    # Linear Regression Predictions
    X_test_lr = pd.get_dummies(test_df[features]).reindex(columns=X_train_lr.columns, fill_value=0)
    lr_rates = np.clip(lr_baseline.predict(X_test_lr), 0.1, None)
    lr_days = test_df['Clothes Assigned'].values / lr_rates
    
    actual_days = np.array(test_df['Time Needed (in days)'].values)
    
    # 6. CALCULATE METRICS
    rf_metrics = oracle.evaluate(test_df)
    lr_metrics = {
        "mae_days": mean_absolute_error(actual_days, lr_days),
        "r2": r2_score(actual_days, lr_days)
    }
    
    # 7. VISUALIZATION
    sns.set_style("whitegrid")
    fig, axes = plt.subplots(1, 2, figsize=(15, 6))
    
    # --- Plot 1: Actual vs Predicted ---
    # Random Forest
    axes[0].scatter(actual_days, rf_days, color='#2ecc71', alpha=0.7, label=f"RF (R²: {rf_metrics['r2']:.2f})")
    # Linear Regression
    axes[0].scatter(actual_days, lr_days, color='#e74c3c', alpha=0.4, label=f"LR (R²: {lr_metrics['r2']:.2f})")
    
    # Perfect Prediction Line
    lims = [0, max(actual_days.max(), rf_days.max()) + 2]
    axes[0].plot(lims, lims, 'k--', alpha=0.5, zorder=0, label="Perfect Prediction")
    
    axes[0].set_title("Actual vs. Predicted Completion Time", fontsize=14)
    axes[0].set_xlabel("Actual Days Taken")
    axes[0].set_ylabel("Predicted Days Taken")
    axes[0].legend()

    # --- Plot 2: Error Distribution (Residuals) ---
    rf_errors = rf_days - actual_days
    lr_errors = lr_days - actual_days
    
    sns.kdeplot(rf_errors, ax=axes[1], fill=True, color='#2ecc71', label="Random Forest")
    sns.kdeplot(lr_errors, ax=axes[1], fill=True, color='#e74c3c', label="Linear Regression")
    
    axes[1].axvline(0, color='k', linestyle='--', alpha=0.6)
    axes[1].set_title("Distribution of Prediction Errors (Residuals)", fontsize=14)
    axes[1].set_xlabel("Error in Days (Predicted - Actual)")
    axes[1].set_ylabel("Density")
    axes[1].legend()

    plt.tight_layout()
    plt.show()

    # Print Summary Table
    print("\n" + "="*45)
    print(f"{'Metric':<20} | {'Random Forest':<12} | {'Linear Reg'}")
    print("-" * 45)
    print(f"{'MAE (Error Days)':<20} | {rf_metrics['mae_days']:>12.2f} | {lr_metrics['mae_days']:>10.2f}")
    print(f"{'R2 (Confidence)':<20} | {rf_metrics['r2']:>12.2f} | {lr_metrics['r2']:>10.2f}")
    print("="*45)

if __name__ == "__main__":
    run_visual_comparison("./data/data.csv")