"""
Pakistan Tech Talent Intelligence System — ML Salary Predictor
Trains and evaluates models for salary prediction
"""

import pandas as pd
import numpy as np
import os
import pickle
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
import xgboost as xgb
import mlflow
import mlflow.sklearn
import warnings
warnings.filterwarnings("ignore")

class SalaryPredictor:
    def __init__(self):
        self.models = {
            'linear': LinearRegression(),
            'random_forest': RandomForestRegressor(n_estimators=100, random_state=42),
            'xgboost': xgb.XGBRegressor(n_estimators=100, random_state=42)
        }
        self.label_encoders = {}
        self.feature_columns = None
        self.results = {}
        
    def prepare_features(self, df):
        """Prepare features for ML model"""
        # Copy dataframe
        data = df.copy()
        
        # Encode categorical variables
        categorical_cols = ['job_title_clean', 'experience_level', 'company_tier']
        for col in categorical_cols:
            le = LabelEncoder()
            data[f'{col}_encoded'] = le.fit_transform(data[col].astype(str))
            self.label_encoders[col] = le
            
        # Skill count feature
        data['skill_count'] = data['skill_list'].apply(
            lambda x: len(x) if isinstance(x, list) else 0
        )
        
        # Is AI/ML role
        data['is_ai_ml_role'] = data['is_ai_ml_role'].astype(int)
        
        # Features for model
        self.feature_columns = [
            'job_title_clean_encoded',
            'experience_level_encoded',
            'company_tier_encoded',
            'skill_count',
            'is_ai_ml_role'
        ]
        
        # Handle missing values
        X = data[self.feature_columns].fillna(0)
        y = data['salary_pkr_k'].fillna(data['salary_pkr_k'].median())
        
        return X, y
        
    def train_and_evaluate(self, df):
        """Train all models and evaluate"""
        X, y = self.prepare_features(df)
        
        # Train-test split
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        print("\n🤖 Training ML Models...")
        print("─" * 40)
        
        for name, model in self.models.items():
            print(f"\n  Training {name}...")
            
            # Train model
            model.fit(X_train, y_train)
            
            # Predictions
            y_pred = model.predict(X_test)
            
            # Metrics
            r2 = r2_score(y_test, y_pred)
            mae = mean_absolute_error(y_test, y_pred)
            rmse = np.sqrt(mean_squared_error(y_test, y_pred))
            
            self.results[name] = {
                'model': model,
                'r2': r2,
                'mae': mae,
                'rmse': rmse
            }
            
            print(f"    R² Score: {r2:.4f}")
            print(f"    MAE: {mae:.2f} PKR")
            print(f"    RMSE: {rmse:.2f} PKR")
        
        return self.results
    
    def save_models(self, path='models/'):
        """Save trained models"""
        os.makedirs(path, exist_ok=True)
        
        for name, result in self.results.items():
            with open(f"{path}{name}_model.pkl", 'wb') as f:
                pickle.dump(result['model'], f)
        
        # Save label encoders
        with open(f"{path}label_encoders.pkl", 'wb') as f:
            pickle.dump(self.label_encoders, f)
            
        print(f"\n✅ Models saved to {path}")
    
    def predict_salary(self, job_title, experience_level, company_tier, skills, is_ai_ml):
        """Predict salary for new job posting"""
        # Encode features
        data = {
            'job_title_clean_encoded': self.label_encoders['job_title_clean'].transform([job_title])[0],
            'experience_level_encoded': self.label_encoders['experience_level'].transform([experience_level])[0],
            'company_tier_encoded': self.label_encoders['company_tier'].transform([company_tier])[0],
            'skill_count': len(skills) if isinstance(skills, list) else 0,
            'is_ai_ml_role': int(is_ai_ml)
        }
        
        X_pred = pd.DataFrame([data])
        
        # Use best model (xgboost usually)
        best_model = self.results['xgboost']['model']
        prediction = best_model.predict(X_pred)[0]
        
        return round(prediction, 2)

def main():
    # Load clean data
    base = os.path.join(os.path.dirname(__file__), "..", "..")
    path = os.path.join(base, "data", "processed", "pk_tech_jobs_clean.csv")
    
    if not os.path.exists(path):
        print("❌ Clean data not found. Run cleaner.py first.")
        return
    
    df = pd.read_csv(path)
    
    # Parse skill_list
    import ast
    df['skill_list'] = df['skill_list'].apply(
        lambda x: ast.literal_eval(x) if isinstance(x, str) and x.startswith('[') 
        else ([s.strip() for s in x.split(',')] if isinstance(x, str) else [])
    )
    
    # Initialize and train
    predictor = SalaryPredictor()
    results = predictor.train_and_evaluate(df)
    
    # Save models
    predictor.save_models()
    
    # Print summary
    print("\n📊 Model Performance Summary")
    print("─" * 40)
    for name, result in results.items():
        print(f"\n{name.upper()}:")
        print(f"  R² Score: {result['r2']:.4f}")
        print(f"  MAE: {result['mae']:.2f} PKR")
        print(f"  RMSE: {result['rmse']:.2f} PKR")

if __name__ == "__main__":
    main()