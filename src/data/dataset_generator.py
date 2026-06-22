"""
Pakistan Tech Talent Intelligence System - Dataset Generator
Generates realistic synthetic dataset for Pakistan tech job market
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os

# ─── CONSTANTS ──────────────────────────────────────────────────────────────────

ROLES = {
    "Data Scientist": {
        "base_salary": (180, 350),
        "exp_multiplier": 1.15,
        "typical_skills": ["Python", "SQL", "Machine Learning", "Statistics", "Data Visualization"],
        "companies": ["Systems Ltd", "Techlogix", "Netsol", "10Pearls", "Folio3"]
    },
    "Machine Learning Engineer": {
        "base_salary": (200, 380),
        "exp_multiplier": 1.20,
        "typical_skills": ["Python", "PyTorch", "TensorFlow", "MLOps", "Docker"],
        "companies": ["Systems Ltd", "10Pearls", "Netsol", "Techlogix", "Arbisoft"]
    },
    "Data Analyst": {
        "base_salary": (120, 220),
        "exp_multiplier": 1.10,
        "typical_skills": ["SQL", "Python", "Power BI", "Excel", "Data Visualization"],
        "companies": ["Systems Ltd", "Techlogix", "Netsol", "Folio3", "Contour"]
    },
    "Full Stack Developer": {
        "base_salary": (150, 280),
        "exp_multiplier": 1.12,
        "typical_skills": ["JavaScript", "React", "Node.js", "Python", "SQL"],
        "companies": ["Systems Ltd", "Techlogix", "Arbisoft", "10Pearls", "Netsol"]
    },
    "DevOps Engineer": {
        "base_salary": (170, 320),
        "exp_multiplier": 1.18,
        "typical_skills": ["Docker", "Kubernetes", "AWS", "Linux", "CI/CD"],
        "companies": ["Systems Ltd", "10Pearls", "Techlogix", "Netsol", "Arbisoft"]
    },
    "NLP Engineer": {
        "base_salary": (220, 400),
        "exp_multiplier": 1.25,
        "typical_skills": ["Python", "NLP", "LLMs", "Hugging Face", "PyTorch"],
        "companies": ["Systems Ltd", "10Pearls", "Netsol", "Techlogix"]
    },
    "AI Research Engineer": {
        "base_salary": (240, 420),
        "exp_multiplier": 1.30,
        "typical_skills": ["Python", "PyTorch", "Deep Learning", "MLflow", "BERT"],
        "companies": ["10Pearls", "Systems Ltd", "Netsol", "Techlogix"]
    },
    "Business Intelligence Developer": {
        "base_salary": (130, 230),
        "exp_multiplier": 1.08,
        "typical_skills": ["SQL", "Power BI", "ETL", "Data Warehouse", "Excel"],
        "companies": ["Systems Ltd", "Techlogix", "Netsol", "Folio3"]
    }
}

CITIES = [
    "Karachi", "Lahore", "Islamabad", "Hybrid (Karachi)", 
    "Hybrid (Lahore)", "Remote", "Hybrid (Islamabad)", 
    "Rawalpindi", "Faisalabad", "Multan"
]

JOB_TYPES = ["Full-time", "Contract", "Freelance"]
EDUCATION = ["Bachelors", "Masters", "PhD", "Not Specified"]
EXPERIENCE_LEVELS = ["Junior", "Mid", "Senior"]

COMPANY_TIERS = {
    "MNC": ["Systems Ltd", "10Pearls", "Netsol"],
    "Tier1": ["Techlogix", "Arbisoft", "Folio3"],
    "Tier2": ["Contour", "Gaditek", "Tkxel"],
    "Startup": ["smaller startup", "emerging tech firm"]
}

BENEFITS_LIST = [
    "Health Insurance", "Annual Bonus", "Stock Options", "Flexible Hours",
    "Professional Development", "Food Allowance", "Transport Allowance",
    "Performance Bonus", "Medical Coverage", "Remote Work"
]

# Generate 3000 synthetic job postings
def generate_jobs(n=3000, seed=42):
    np.random.seed(seed)
    random.seed(seed)
    
    jobs = []
    start_date = datetime(2024, 1, 1)
    end_date = datetime(2025, 3, 31)
    
    for _ in range(n):
        # Pick a role
        role = random.choice(list(ROLES.keys()))
        role_config = ROLES[role]
        
        # Experience level
        exp_level = np.random.choice(
            EXPERIENCE_LEVELS, 
            p=[0.3, 0.45, 0.25]
        )
        
        # Experience years
        if exp_level == "Junior":
            exp_years = np.random.uniform(0, 2)
        elif exp_level == "Mid":
            exp_years = np.random.uniform(2, 5)
        else:
            exp_years = np.random.uniform(5, 10)
        
        # Salary based on role, experience, and randomness
        base_min, base_max = role_config["base_salary"]
        exp_factor = 1 + (exp_years / 10) * role_config["exp_multiplier"]
        salary_base = np.random.uniform(base_min, base_max) * exp_factor
        # Add randomness
        salary = salary_base * np.random.uniform(0.85, 1.15)
        salary = int(round(salary / 5) * 5)  # Round to nearest 5
        
        # City
        city = random.choice(CITIES)
        
        # Company
        company = random.choice(role_config["companies"])
        
        # Skills
        num_skills = random.randint(4, 8)
        skills = random.sample(role_config["typical_skills"], 
                              min(num_skills, len(role_config["typical_skills"])))
        # Add some extra random skills
        extra_skills = ["Docker", "AWS", "Git", "React", "Node.js", "PostgreSQL", 
                        "MongoDB", "FastAPI", "Flask", "Kubernetes", "MLflow",
                        "Airflow", "LLMs", "BERT", "PyTorch", "TensorFlow"]
        if len(skills) < 8:
            additional = random.sample(extra_skills, min(8 - len(skills), 5))
            skills.extend(additional)
        skills = list(set(skills))[:8]  # Ensure max 8 skills
        
        # Job title (with some variation)
        title = role
        if random.random() < 0.15:
            prefixes = ["Senior", "Lead", "Junior", "Associate"]
            title = f"{random.choice(prefixes)} {title}"
        
        # Date
        date = start_date + timedelta(days=random.randint(0, (end_date - start_date).days))
        
        # Description
        description = f"""
        We are hiring a {title} to join our team. 
        Required skills: {', '.join(skills)}.
        Experience required: {exp_years:.1f}+ years.
        This is a {random.choice(JOB_TYPES)} position.
        Education: {random.choice(EDUCATION)} preferred.
        """
        
        # Benefits
        benefits = random.sample(BENEFITS_LIST, random.randint(2, 5))
        
        # Company tier
        company_tier = "Tier2"
        for tier, companies in COMPANY_TIERS.items():
            if any(c in company for c in companies) or company == "startup":
                company_tier = tier
                break
        
        jobs.append({
            "job_title": title,
            "company": company,
            "city": city,
            "job_type": random.choice(JOB_TYPES),
            "experience_level": exp_level,
            "min_experience_years": round(exp_years, 1),
            "salary_pkr_k": salary,
            "required_skills": ", ".join(skills),
            "education": random.choice(EDUCATION),
            "job_description": description.strip(),
            "benefits": ", ".join(benefits),
            "date_posted": date,
            "company_tier": company_tier,
            "is_ai_ml_role": role in ["Data Scientist", "Machine Learning Engineer", 
                                      "NLP Engineer", "AI Research Engineer"]
        })
    
    return pd.DataFrame(jobs)

def main():
    # Create directories
    os.makedirs("data/raw", exist_ok=True)
    os.makedirs("data/processed", exist_ok=True)
    
    # Generate dataset
    print("Generating Pakistan tech job dataset...")
    df = generate_jobs(3000)
    
    # Save raw
    raw_path = "data/raw/pk_tech_jobs.csv"
    df.to_csv(raw_path, index=False)
    print(f"Dataset saved to {raw_path}")
    print(f"   Shape: {df.shape}")
    print(f"   Columns: {list(df.columns)}")
    print(f"   Jobs per role:\n{df['job_title'].value_counts().head(10)}")
    
    return df

if __name__ == "__main__":
    main()