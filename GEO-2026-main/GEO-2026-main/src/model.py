import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
import joblib

class TailorOracle:
    def __init__(self):
        self.model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.feature_cols = None
        self.is_trained = False

    def _prepare_data(self, df):
        """Cleans data and calculates target rates."""
        # Standardize strings
        df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
        # Ensure we have valid time data
        df = df[df['Time Needed (in days)'] > 0].copy()
        
        # Target: Pieces per Day
        df['Actual_Rate'] = df['Clothes Assigned'] / df['Time Needed (in days)']
        
        features = ['Name', 'Clothes Type', 'Specialist', 'Clothes Assigned']
        X = pd.get_dummies(df[features])
        y = df['Actual_Rate']
        
        return X, y, df['Time Needed (in days)']

    def fit(self, df):
        """
        Trains the model on 100% of the provided data.
        """
        X, y, _ = self._prepare_data(df)
        self.feature_cols = X.columns
        
        # Train on everything
        self.model.fit(X, y)
        self.is_trained = True
        return {"status": "success", "samples_trained": len(df)}

    def predict(self, df_input: pd.DataFrame) -> np.ndarray:
        """
        Predicts 'Days Taken' for a DataFrame of multiple assignments.
        Expects columns: ['Name', 'Clothes Type', 'Specialist', 'Clothes Assigned']
        """
        if not self.is_trained:
            raise RuntimeError("Oracle must be trained before calling predict.")

        # 1. Standardize and Encode
        # Ensure we handle the dummy variables correctly based on training columns
        X_input = pd.get_dummies(df_input).reindex(columns=self.feature_cols, fill_value=0)
        
        # 2. Predict Daily Rate
        pred_rates = np.clip(self.model.predict(X_input), 0.1, None)
        
        # 3. Calculate Days: W = Qty / Rate
        # Extract quantities from input to perform vector math
        qtys = df_input['Clothes Assigned'].values
        pred_days = qtys / pred_rates
        
        return pred_days

    def predict_one(self, tailor_name: str, clothes_type: str, qty: int, specialist_status: str) -> float:
        """Helper for the Optimizer to predict a single case."""
        single_row = pd.DataFrame([{
            'Name': tailor_name,
            'Clothes Type': clothes_type,
            'Specialist': specialist_status,
            'Clothes Assigned': qty
        }])
        return self.predict(single_row)[0]

    def evaluate(self, df_test: pd.DataFrame):
        """
        Evaluates the model against a separate testing set.
        """
        # Prepare test data
        X_test, y_test, actual_days = self._prepare_data(df_test)
        
        # Align columns
        X_test = X_test.reindex(columns=self.feature_cols, fill_value=0)
        
        # Predict
        pred_rate = np.clip(self.model.predict(X_test), 0.1, None)
        qty_test = df_test['Clothes Assigned'].values
        pred_days = qty_test / pred_rate
        
        return {
            "mae_days": mean_absolute_error(actual_days, pred_days),
            "r2": r2_score(actual_days, pred_days)
        }

    def save(self, path):
        joblib.dump({'m': self.model, 'f': self.feature_cols}, path)

    def load(self, path):
        data = joblib.load(path)
        self.model, self.feature_cols = data['m'], data['f']
        self.is_trained = True