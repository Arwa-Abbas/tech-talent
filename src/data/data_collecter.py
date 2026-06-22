"""
Pakistan Data Intelligence System - Data Collector
Collects and combines data from multiple sources
"""

import pandas as pd
import numpy as np
import os
import json
import requests
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PakistanDataCollector:
    def __init__(self):
        self.data_sources = {}
        self.combined_data = None
        
    def load_kaggle_dataset(self, filepath):
        """Load the AI Jobs Market dataset"""
        try:
            df = pd.read_csv(filepath)
            logger.info(f"Loaded Kaggle dataset: {len(df)} rows")
            
            # Add Pakistan-specific data if available
            # Filter or augment with Pakistan data
            df['source'] = 'Kaggle'
            return df
        except Exception as e:
            logger.error(f"Error loading Kaggle dataset: {e}")
            return None
    
    def create_pakistan_synthetic_data(self, n_samples=200):
        """Create synthetic Pakistan-specific job data"""
        np.random.seed(42)
        
        roles = [
            'Data Scientist', 'ML Engineer', 'Software Engineer', 
            'Data Analyst', 'DevOps Engineer', 'Full Stack Developer',
            'AI Engineer', 'NLP Engineer', 'Computer Vision Engineer'
        ]
        
        pakistan_cities = ['Karachi', 'Lahore', 'Islamabad', 'Rawalpindi', 
                          'Faisalabad', 'Multan', 'Hyderabad', 'Peshawar']
        
        companies = ['Systems Ltd', 'Techlogix', 'Netsol', '10Pearls', 'Folio3',
                    'Arbisoft', 'Gaditek', 'Contour', 'Tkxel']
        
        skills_pool = [
            'Python', 'SQL', 'Machine Learning', 'Deep Learning', 'NLP',
            'Computer Vision', 'Docker', 'Kubernetes', 'AWS', 'GCP',
            'React', 'Node.js', 'Django', 'Flask', 'FastAPI',
            'TensorFlow', 'PyTorch', 'Scikit-learn', 'Pandas', 'NumPy'
        ]
        
        data = []
        for _ in range(n_samples):
            role = np.random.choice(roles)
            experience = np.random.choice(['Junior', 'Mid', 'Senior', 'Lead'])
            
            # Salary ranges in PKR (converted to USD for consistency)
            base_salary = {
                'Junior': np.random.randint(80000, 150000),
                'Mid': np.random.randint(150000, 250000),
                'Senior': np.random.randint(250000, 400000),
                'Lead': np.random.randint(350000, 600000)
            }[experience]
            
            # Skills for this role
            num_skills = np.random.randint(4, 8)
            skills = np.random.choice(skills_pool, num_skills, replace=False)
            
            # City
            city = np.random.choice(pakistan_cities)
            company = np.random.choice(companies)
            
            data.append({
                'job_id': f'PKJOB{_:04d}',
                'job_title': role,
                'job_category': 'AI Engineering' if any(x in role for x in ['Data Scientist', 'ML', 'AI', 'NLP', 'Computer Vision']) else 'Software Development',
                'experience_level': experience,
                'years_of_experience': np.random.uniform(0, 10),
                'education_required': np.random.choice(['Bachelor\'s', 'Master\'s', 'PhD']),
                'annual_salary_usd': round(base_salary / 280),  # Rough PKR to USD conversion
                'salary_min_usd': round(base_salary / 300),
                'salary_max_usd': round(base_salary / 260),
                'city': city,
                'country': 'Pakistan',
                'remote_work': np.random.choice(['On-site', 'Hybrid', 'Fully Remote'], p=[0.4, 0.35, 0.25]),
                'company_size': np.random.choice(['Startup', 'Mid-size', 'Enterprise', 'Big Tech']),
                'industry': np.random.choice(['Technology', 'Finance', 'Healthcare', 'Education']),
                'required_skills': '|'.join(skills),
                'ai_salary_premium_pct': np.random.uniform(0, 30),
                'demand_score': np.random.uniform(60, 100),
                'demand_growth_yoy_pct': np.random.uniform(0, 50),
                'posting_month': np.random.randint(1, 13),
                'posting_year': np.random.choice([2025, 2026]),
                'is_senior': 1 if experience in ['Senior', 'Lead'] else 0,
                'is_llm_role': 1 if any(x in role for x in ['NLP', 'AI']) else 0,
                'source': 'Pakistan_Synthetic'
            })
        
        return pd.DataFrame(data)
    
    def combine_datasets(self, kaggle_df, pakistan_df):
        """Combine datasets and add Pakistan-specific features"""
        if kaggle_df is None:
            return pakistan_df
        
        # Combine
        combined = pd.concat([kaggle_df, pakistan_df], ignore_index=True)
        
        # Add Pakistan-specific flags
        combined['is_pakistan'] = combined['country'] == 'Pakistan'
        combined['region'] = 'Pakistan' if combined['country'] == 'Pakistan' else 'International'
        
        # Add economy indicators (simplified)
        combined['tech_maturity_score'] = np.where(
            combined['is_pakistan'],
            np.random.uniform(50, 70, len(combined)),
            np.random.uniform(70, 95, len(combined))
        )
        
        logger.info(f"Combined dataset: {len(combined)} rows")
        return combined
    
    def save_data(self, df, filepath='data/raw/pakistan_jobs_data.csv'):
        """Save combined dataset"""
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        df.to_csv(filepath, index=False)
        logger.info(f"Saved combined data to {filepath}")
        return filepath

def main():
    # Initialize collector
    collector = PakistanDataCollector()
    
    # Load Kaggle dataset
    base = os.path.join(os.path.dirname(__file__), "..", "..")
    kaggle_path = os.path.join(base, "data", "job_market.csv")
    
    kaggle_df = None
    if os.path.exists(kaggle_path):
        kaggle_df = collector.load_kaggle_dataset(kaggle_path)
    
    # Create Pakistan data
    pakistan_df = collector.create_pakistan_synthetic_data(300)
    
    # Combine
    combined = collector.combine_datasets(kaggle_df, pakistan_df)
    
    # Save
    output_path = os.path.join(base, "data", "raw", "pakistan_jobs_data.csv")
    collector.save_data(combined, output_path)
    
    print("\nData Collection Complete!")
    print(f"Total Records: {len(combined)}")
    print(f"Pakistan Records: {len(combined[combined['is_pakistan']])}")
    print(f"Columns: {list(combined.columns)}")

if __name__ == "__main__":
    main()