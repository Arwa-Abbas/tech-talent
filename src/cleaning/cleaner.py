"""
Pakistan Tech Talent Intelligence System — Data Cleaning Pipeline
Handles: duplicates, missing values, title standardisation, skill normalisation, text cleaning.
"""

import pandas as pd
import numpy as np
import re
import os
import logging
from typing import Tuple

logging.basicConfig(level=logging.INFO, format="%(levelname)s | %(message)s")
log = logging.getLogger(__name__)

# ─── MAPS ─────────────────────────────────────────────────────────────────────
TITLE_MAP = {
    "data science engineer":          "Data Scientist",
    "data science specialist":        "Data Scientist",
    "senior data scientist":          "Data Scientist",
    "junior data scientist":          "Data Scientist",
    "ml engineer":                    "Machine Learning Engineer",
    "machine learning developer":     "Machine Learning Engineer",
    "ai engineer":                    "Machine Learning Engineer",
    "artificial intelligence engineer":"Machine Learning Engineer",
    "fullstack developer":            "Full Stack Developer",
    "full-stack developer":           "Full Stack Developer",
    "full stack engineer":            "Full Stack Developer",
    "business data analyst":          "Data Analyst",
    "junior data analyst":            "Data Analyst",
    "senior data analyst":            "Data Analyst",
    "bi developer":                   "Business Intelligence Developer",
    "business intelligence analyst":  "Business Intelligence Developer",
    "power bi developer":             "Business Intelligence Developer",
}

SKILL_MAP = {
    "ml":                  "Machine Learning",
    "machine learning":    "Machine Learning",
    "dl":                  "Deep Learning",
    "deep learning":       "Deep Learning",
    "nlp":                 "NLP",
    "natural language processing": "NLP",
    "cv":                  "Computer Vision",
    "computer vision":     "Computer Vision",
    "tensorflow":          "TensorFlow",
    "tf":                  "TensorFlow",
    "pytorch":             "PyTorch",
    "torch":               "PyTorch",
    "scikit-learn":        "Scikit-learn",
    "sklearn":             "Scikit-learn",
    "postgres":            "PostgreSQL",
    "postgresql":          "PostgreSQL",
    "mysql":               "SQL",
    "mssql":               "SQL",
    "ms sql":              "SQL",
    "sql server":          "SQL",
    "js":                  "JavaScript",
    "javascript":          "JavaScript",
    "ts":                  "TypeScript",
    "typescript":          "TypeScript",
    "node":                "Node.js",
    "nodejs":              "Node.js",
    "reactjs":             "React",
    "react.js":            "React",
    "nextjs":              "Next.js",
    "next.js":             "Next.js",
    "power bi":            "Power BI",
    "powerbi":             "Power BI",
    "aws":                 "Cloud (AWS/GCP)",
    "gcp":                 "Cloud (AWS/GCP)",
    "azure":               "Cloud (AWS/GCP)",
    "cloud":               "Cloud (AWS/GCP)",
    "docker":              "Docker",
    "kubernetes":          "Kubernetes",
    "k8s":                 "Kubernetes",
    "airflow":             "Airflow",
    "apache airflow":      "Airflow",
    "mlflow":              "MLflow",
    "fastapi":             "FastAPI",
    "rest api":            "REST API",
    "restful api":         "REST API",
    "llm":                 "LLMs",
    "large language model": "LLMs",
    "bert":                "BERT",
    "hugging face":        "Hugging Face",
    "huggingface":         "Hugging Face",
}

STOPWORDS = {"and", "or", "the", "a", "an", "in", "of", "to", "for",
             "with", "on", "at", "by", "from", "is", "are", "has",
             "have", "be", "been", "will", "we", "you", "your", "our",
             "this", "that", "as", "it", "its", "also", "which", "who"}

# ─── HELPERS ──────────────────────────────────────────────────────────────────
def _clean_text(text: str) -> str:
    if not isinstance(text, str):
        return ""
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    tokens = [t for t in text.split() if t not in STOPWORDS]
    return " ".join(tokens)

def _normalise_title(title: str) -> str:
    if not isinstance(title, str):
        return "Other"
    return TITLE_MAP.get(title.strip().lower(), title.strip())

def _normalise_skills(skills_str: str) -> str:
    if not isinstance(skills_str, str):
        return ""
    skills = [s.strip() for s in skills_str.split(",") if s.strip()]
    normalised = []
    seen = set()
    for s in skills:
        key = s.lower()
        mapped = SKILL_MAP.get(key, s)
        if mapped.lower() not in seen:
            seen.add(mapped.lower())
            normalised.append(mapped)
    return ", ".join(normalised)

def _extract_skill_list(skills_str: str) -> list:
    if not isinstance(skills_str, str):
        return []
    return [s.strip() for s in skills_str.split(",") if s.strip()]

# ─── MAIN PIPELINE ────────────────────────────────────────────────────────────
def load_raw(path: str) -> pd.DataFrame:
    log.info(f"Loading raw data from {path}")
    df = pd.read_csv(path)
    log.info(f"  Shape: {df.shape}")
    return df

def remove_duplicates(df: pd.DataFrame) -> Tuple[pd.DataFrame, int]:
    n_before = len(df)
    df = df.drop_duplicates(subset=["job_title", "company", "city", "experience_level"], keep="first")
    n_removed = n_before - len(df)
    log.info(f"  Duplicates removed: {n_removed}")
    return df.reset_index(drop=True), n_removed

def handle_missing(df: pd.DataFrame) -> pd.DataFrame:
    # Salary: median per role + exp level
    df["salary_pkr_k"] = pd.to_numeric(df["salary_pkr_k"], errors="coerce")
    median_sal = df.groupby(["job_title", "experience_level"])["salary_pkr_k"].transform("median")
    df["salary_pkr_k"] = df["salary_pkr_k"].fillna(median_sal)
    # Remaining NaN → overall median
    df["salary_pkr_k"] = df["salary_pkr_k"].fillna(df["salary_pkr_k"].median())
    
    # Other cols
    df["city"]          = df["city"].fillna("Unknown")
    df["job_type"]      = df["job_type"].fillna("Full-time")
    df["education"]     = df["education"].fillna("Not Specified")
    df["benefits"]      = df["benefits"].fillna("Not Specified")
    df["job_description"]= df["job_description"].fillna("")

    log.info(f"  Missing values handled")
    return df

def standardise_titles(df: pd.DataFrame) -> pd.DataFrame:
    df["job_title_clean"] = df["job_title"].apply(_normalise_title)
    changed = (df["job_title"] != df["job_title_clean"]).sum()
    log.info(f"  Titles standardised: {changed} changed")
    return df

def normalise_skills(df: pd.DataFrame) -> pd.DataFrame:
    df["required_skills_clean"] = df["required_skills"].apply(_normalise_skills)
    df["skill_list"]            = df["required_skills_clean"].apply(_extract_skill_list)
    df["skill_count"]           = df["skill_list"].apply(len)
    log.info("  Skills normalised")
    return df

def clean_text_fields(df: pd.DataFrame) -> pd.DataFrame:
    df["description_clean"] = df["job_description"].apply(_clean_text)
    log.info("  Text fields cleaned")
    return df

def feature_engineering(df: pd.DataFrame) -> pd.DataFrame:
    # Date features
    df["date_posted"] = pd.to_datetime(df["date_posted"], errors="coerce")
    df["year_posted"]  = df["date_posted"].dt.year
    df["month_posted"] = df["date_posted"].dt.month
    df["quarter"]      = df["date_posted"].dt.quarter

    # Location type
    def loc_type(c):
        if isinstance(c, str):
            if "remote" in c.lower(): return "Remote"
            if "hybrid" in c.lower(): return "Hybrid"
        return "On-site"
    df["location_type"] = df["city"].apply(loc_type)

    # City clean (strip Hybrid prefix)
    df["city_clean"] = df["city"].str.replace(r"Hybrid \(|\)", "", regex=True).str.strip()

    # Salary band
    def sal_band(s):
        if s < 80:   return "Entry (<80k)"
        elif s < 150: return "Mid (80–150k)"
        elif s < 220: return "Senior (150–220k)"
        else:         return "Lead (220k+)"
    df["salary_band"] = df["salary_pkr_k"].apply(sal_band)

    # Is AI/ML role?
    AI_ROLES = {"Data Scientist", "Machine Learning Engineer", "NLP Engineer",
                "Computer Vision Engineer", "AI Research Engineer", "MLOps Engineer"}
    df["is_ai_ml_role"] = df["job_title_clean"].isin(AI_ROLES)

    log.info("  Feature engineering complete")
    return df

def run_pipeline(raw_path: str, out_path: str) -> pd.DataFrame:
    log.info("═" * 50)
    log.info("STARTING DATA CLEANING PIPELINE")
    log.info("═" * 50)

    df = load_raw(raw_path)
    df, _ = remove_duplicates(df)
    df = handle_missing(df)
    df = standardise_titles(df)
    df = normalise_skills(df)
    df = clean_text_fields(df)
    df = feature_engineering(df)

    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    df.to_csv(out_path, index=False)
    log.info(f"  Clean data saved → {out_path}  Shape: {df.shape}")
    log.info("═" * 50)
    return df

if __name__ == "__main__":
    base = os.path.join(os.path.dirname(__file__), "..", "..")
    raw = os.path.join(base, "data", "raw", "pk_tech_jobs.csv")
    out = os.path.join(base, "data", "processed", "pk_tech_jobs_clean.csv")
    run_pipeline(raw, out)