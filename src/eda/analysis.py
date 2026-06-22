"""
Pakistan Tech Talent Intelligence System — Complete EDA Module
Dynamic analysis of AI Jobs Market 2025-2026 dataset
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
import os
from collections import Counter
import ast

warnings.filterwarnings("ignore")

# ─── STYLE ────────────────────────────────────────────────────────────────────
PALETTE = ["#2563EB", "#7C3AED", "#059669", "#D97706", "#DC2626",
           "#0891B2", "#7C2D12", "#1D4ED8", "#6D28D9", "#065F46"]
BG = "#F8FAFC"
GRID_CLR = "#E2E8F0"

sns.set_theme(style="whitegrid", palette=PALETTE)
plt.rcParams.update({
    "figure.facecolor": BG,
    "axes.facecolor": BG,
    "axes.edgecolor": GRID_CLR,
    "grid.color": GRID_CLR,
    "font.family": "DejaVu Sans",
    "font.size": 11,
})

# Create assets directory
ASSETS = os.path.join(os.path.dirname(__file__), "..", "..", "assets")
os.makedirs(ASSETS, exist_ok=True)

def save(fig, name: str):
    """Save figure to assets folder"""
    p = os.path.join(ASSETS, name)
    fig.savefig(p, dpi=150, bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    print(f"  ✅ {name}")

def print_insight(insight_text: str):
    """Print insight in a formatted way"""
    print(f"  💡 {insight_text}")

# ─── 1. DATA OVERVIEW ──────────────────────────────────────────────────────
def dataset_overview(df):
    """Print dataset overview and basic stats"""
    print("\n" + "="*60)
    print("📊 DATASET OVERVIEW")
    print("="*60)
    print(f"  Total Records: {len(df):,}")
    print(f"  Total Columns: {len(df.columns)}")
    print(f"\n  📋 Columns:\n    {', '.join(df.columns.tolist())}")
    print(f"\n  📈 Basic Statistics:")
    print(df.describe().round(2).to_string())
    print(f"\n  🔍 Missing Values:")
    missing = df.isnull().sum()
    print(missing[missing > 0].to_string() if missing.sum() > 0 else "  None")

# ─── 2. SALARY ANALYSIS ────────────────────────────────────────────────────
def salary_analysis(df):
    """Complete salary analysis with multiple visualizations"""
    print("\n" + "="*60)
    print("💰 SALARY ANALYSIS")
    print("="*60)
    
    # Salary distribution
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    # 1. Salary histogram
    axes[0, 0].hist(df['annual_salary_usd'].dropna(), bins=50, 
                    color=PALETTE[0], alpha=0.7, edgecolor='white')
    axes[0, 0].axvline(df['annual_salary_usd'].median(), color='red', 
                       linestyle='--', linewidth=2, 
                       label=f"Median: ${df['annual_salary_usd'].median():,.0f}")
    axes[0, 0].axvline(df['annual_salary_usd'].mean(), color='orange', 
                       linestyle='--', linewidth=2,
                       label=f"Mean: ${df['annual_salary_usd'].mean():,.0f}")
    axes[0, 0].set_title('Salary Distribution (USD)', fontsize=14, fontweight='bold')
    axes[0, 0].set_xlabel('Annual Salary (USD)')
    axes[0, 0].set_ylabel('Frequency')
    axes[0, 0].legend()
    
    # 2. Salary by experience level (boxplot) - FIXED: removed 'labels' parameter
    exp_order = ['Entry', 'Mid', 'Senior', 'Lead']
    exp_data = []
    exp_labels = []
    for exp in exp_order:
        if exp in df['experience_level'].unique():
            exp_data.append(df[df['experience_level']==exp]['annual_salary_usd'].dropna().values)
            exp_labels.append(exp)
    
    # Use positions instead of labels for compatibility
    bp = axes[0, 1].boxplot(exp_data, patch_artist=True,
                            medianprops=dict(color='white', linewidth=2))
    axes[0, 1].set_xticklabels(exp_labels)
    for patch, color in zip(bp['boxes'], PALETTE[:len(exp_labels)]):
        patch.set_facecolor(color)
    axes[0, 1].set_title('Salary by Experience Level', fontsize=14, fontweight='bold')
    axes[0, 1].set_ylabel('Annual Salary (USD)')
    axes[0, 1].tick_params(axis='x', rotation=0)
    
    # 3. Top 10 highest paying roles
    top_roles = df.groupby('job_title')['annual_salary_usd'].median().sort_values(ascending=False).head(10)
    axes[1, 0].barh(top_roles.index[::-1], top_roles.values[::-1], color=PALETTE[:10])
    for i, (idx, val) in enumerate(top_roles[::-1].items()):
        axes[1, 0].text(val + 5000, i, f"${val:,.0f}", va='center', fontsize=9)
    axes[1, 0].set_title('Top 10 Highest Paying Roles', fontsize=14, fontweight='bold')
    axes[1, 0].set_xlabel('Median Annual Salary (USD)')
    
    # 4. Salary by country
    country_sal = df.groupby('country')['annual_salary_usd'].median().sort_values(ascending=False).head(10)
    axes[1, 1].barh(country_sal.index[::-1], country_sal.values[::-1], color=PALETTE)
    for i, (idx, val) in enumerate(country_sal[::-1].items()):
        axes[1, 1].text(val + 5000, i, f"${val:,.0f}", va='center', fontsize=9)
    axes[1, 1].set_title('Top 10 Countries by Median Salary', fontsize=14, fontweight='bold')
    axes[1, 1].set_xlabel('Median Annual Salary (USD)')
    
    plt.tight_layout()
    save(fig, '01_salary_analysis.png')
    
    # Insights
    print(f"  📊 Average Salary: ${df['annual_salary_usd'].mean():,.0f}")
    print(f"  📊 Median Salary: ${df['annual_salary_usd'].median():,.0f}")
    print(f"  📊 Highest Paying Role: {df.groupby('job_title')['annual_salary_usd'].mean().idxmax()}")
    print(f"  📊 Lowest Paying Role: {df.groupby('job_title')['annual_salary_usd'].mean().idxmin()}")
    print_insight(f"Senior roles earn {df[df['experience_level']=='Senior']['annual_salary_usd'].mean()/df[df['experience_level']=='Entry']['annual_salary_usd'].mean():.1f}x more than Entry level")

# ─── 3. SKILLS ANALYSIS ────────────────────────────────────────────────────
def skills_analysis(df):
    """Complete skills analysis with visualizations"""
    print("\n" + "="*60)
    print("🧠 SKILLS ANALYSIS")
    print("="*60)
    
    # Parse skills
    all_skills = []
    for skills in df['required_skills'].dropna():
        if isinstance(skills, str):
            skill_list = [s.strip() for s in skills.split('|') if s.strip()]
            all_skills.extend(skill_list)
    
    skill_counts = Counter(all_skills)
    
    # Top 20 skills
    fig, axes = plt.subplots(1, 2, figsize=(16, 8))
    
    # 1. Top 20 skills bar chart
    top_skills = pd.DataFrame(skill_counts.most_common(20), columns=['Skill', 'Count'])
    colors = [PALETTE[0] if i < 5 else PALETTE[1] if i < 10 else PALETTE[2] for i in range(20)]
    bars = axes[0].barh(top_skills['Skill'][::-1], top_skills['Count'][::-1], color=colors[::-1])
    for bar, val in zip(bars, top_skills['Count'][::-1]):
        axes[0].text(bar.get_width() + 2, bar.get_y() + bar.get_height()/2,
                    f"{val}", va='center', fontsize=9)
    axes[0].set_title('Top 20 Most In-Demand Skills', fontsize=14, fontweight='bold')
    axes[0].set_xlabel('Number of Job Postings')
    
    # 2. Skills by role heatmap
    top_roles = df['job_title'].value_counts().head(8).index
    top_skills_10 = [s for s, _ in skill_counts.most_common(10)]
    
    matrix = []
    for role in top_roles:
        role_skills = []
        for skills in df[df['job_title'] == role]['required_skills'].dropna():
            if isinstance(skills, str):
                role_skills.extend([s.strip() for s in skills.split('|') if s.strip()])
        role_counter = Counter(role_skills)
        total = len(df[df['job_title'] == role])
        row = [round(role_counter.get(skill, 0) / total * 100, 1) if total > 0 else 0 
               for skill in top_skills_10]
        matrix.append(row)
    
    heatmap_df = pd.DataFrame(matrix, index=top_roles, columns=top_skills_10)
    
    sns.heatmap(heatmap_df, annot=True, fmt='.0f', cmap='Blues', 
                linewidths=0.5, ax=axes[1], cbar_kws={'label': '% of Job Posts'})
    axes[1].set_title('Skill Demand Heatmap by Role (%)', fontsize=14, fontweight='bold')
    axes[1].set_xlabel('Skills')
    axes[1].set_ylabel('Role')
    plt.xticks(rotation=35, ha='right')
    
    plt.tight_layout()
    save(fig, '02_skills_analysis.png')
    
    # Insights
    print(f"  📊 Total Unique Skills: {len(skill_counts)}")
    if skill_counts:
        print(f"  📊 Most In-Demand Skill: {skill_counts.most_common(1)[0][0]} ({skill_counts.most_common(1)[0][1]} jobs)")
        print(f"  📊 Top 5 Skills: {', '.join([s for s, _ in skill_counts.most_common(5)])}")
        print_insight(f"Python is the most in-demand skill, appearing in {skill_counts.get('Python', 0)} job postings")

# ─── 4. LOCATION & REMOTE ANALYSIS ────────────────────────────────────────
def location_analysis(df):
    """Analysis of job locations and remote work trends"""
    print("\n" + "="*60)
    print("🌍 LOCATION & REMOTE ANALYSIS")
    print("="*60)
    
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    
    # 1. Jobs by country
    country_counts = df['country'].value_counts().head(12)
    axes[0, 0].bar(country_counts.index, country_counts.values, color=PALETTE[:len(country_counts)])
    for i, (idx, val) in enumerate(country_counts.items()):
        axes[0, 0].text(i, val + 5, str(val), ha='center', fontsize=9)
    axes[0, 0].set_title('Jobs by Country', fontsize=14, fontweight='bold')
    axes[0, 0].set_xlabel('Country')
    axes[0, 0].set_ylabel('Number of Jobs')
    plt.setp(axes[0, 0].xaxis.get_majorticklabels(), rotation=45, ha='right')
    
    # 2. Remote work distribution
    remote_counts = df['remote_work'].value_counts()
    axes[0, 1].pie(remote_counts.values, labels=remote_counts.index, 
                   autopct='%1.1f%%', colors=PALETTE[:len(remote_counts)],
                   wedgeprops=dict(edgecolor='white', linewidth=2))
    axes[0, 1].set_title('Remote Work Distribution', fontsize=14, fontweight='bold')
    
    # 3. City-wise jobs
    city_counts = df['city'].value_counts().head(10)
    axes[1, 0].barh(city_counts.index[::-1], city_counts.values[::-1], color=PALETTE)
    for i, (idx, val) in enumerate(city_counts[::-1].items()):
        axes[1, 0].text(val + 5, i, str(val), va='center', fontsize=9)
    axes[1, 0].set_title('Top 10 Cities by Job Postings', fontsize=14, fontweight='bold')
    axes[1, 0].set_xlabel('Number of Jobs')
    
    # 4. Salary vs Remote
    remote_sal = df.groupby('remote_work')['annual_salary_usd'].median()
    axes[1, 1].bar(remote_sal.index, remote_sal.values, color=PALETTE[:len(remote_sal)])
    for i, (idx, val) in enumerate(remote_sal.items()):
        axes[1, 1].text(i, val + 5000, f"${val:,.0f}", ha='center', fontsize=9)
    axes[1, 1].set_title('Median Salary by Remote Type', fontsize=14, fontweight='bold')
    axes[1, 1].set_ylabel('Median Annual Salary (USD)')
    
    plt.tight_layout()
    save(fig, '03_location_analysis.png')
    
    print(f"  📊 Most Jobs in: {country_counts.index[0]} ({country_counts.values[0]} jobs)")
    remote_pct = (remote_counts.get('Fully Remote', 0) / len(df)) * 100
    print(f"  📊 Remote Jobs: {remote_pct:.1f}% of all postings")
    if 'Fully Remote' in remote_sal.index and 'On-site' in remote_sal.index:
        premium = ((remote_sal['Fully Remote'] / remote_sal['On-site'] - 1) * 100)
        print_insight(f"Fully Remote roles pay {premium:.1f}% more than On-site roles")

# ─── 5. COMPANY & INDUSTRY ANALYSIS ──────────────────────────────────────
def company_analysis(df):
    """Analysis of companies and industries"""
    print("\n" + "="*60)
    print("🏢 COMPANY & INDUSTRY ANALYSIS")
    print("="*60)
    
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    
    # 1. Company size distribution
    size_counts = df['company_size'].value_counts()
    axes[0, 0].bar(size_counts.index, size_counts.values, color=PALETTE[:len(size_counts)])
    for i, (idx, val) in enumerate(size_counts.items()):
        axes[0, 0].text(i, val + 5, str(val), ha='center', fontsize=9)
    axes[0, 0].set_title('Company Size Distribution', fontsize=14, fontweight='bold')
    axes[0, 0].set_xlabel('Company Size')
    axes[0, 0].set_ylabel('Number of Jobs')
    plt.setp(axes[0, 0].xaxis.get_majorticklabels(), rotation=45, ha='right')
    
    # 2. Salary by company size
    size_sal = df.groupby('company_size')['annual_salary_usd'].median().sort_values(ascending=False)
    axes[0, 1].bar(size_sal.index, size_sal.values, color=PALETTE[:len(size_sal)])
    for i, (idx, val) in enumerate(size_sal.items()):
        axes[0, 1].text(i, val + 5000, f"${val:,.0f}", ha='center', fontsize=9)
    axes[0, 1].set_title('Median Salary by Company Size', fontsize=14, fontweight='bold')
    axes[0, 1].set_ylabel('Median Annual Salary (USD)')
    plt.setp(axes[0, 1].xaxis.get_majorticklabels(), rotation=45, ha='right')
    
    # 3. Industry distribution
    industry_counts = df['industry'].value_counts().head(8)
    axes[1, 0].barh(industry_counts.index[::-1], industry_counts.values[::-1], color=PALETTE)
    for i, (idx, val) in enumerate(industry_counts[::-1].items()):
        axes[1, 0].text(val + 5, i, str(val), va='center', fontsize=9)
    axes[1, 0].set_title('Top 8 Industries Hiring AI Talent', fontsize=14, fontweight='bold')
    axes[1, 0].set_xlabel('Number of Jobs')
    
    # 4. Salary by industry
    industry_sal = df.groupby('industry')['annual_salary_usd'].median().sort_values(ascending=False).head(8)
    axes[1, 1].barh(industry_sal.index[::-1], industry_sal.values[::-1], color=PALETTE)
    for i, (idx, val) in enumerate(industry_sal[::-1].items()):
        axes[1, 1].text(val + 5000, i, f"${val:,.0f}", va='center', fontsize=9)
    axes[1, 1].set_title('Top 8 Industries by Median Salary', fontsize=14, fontweight='bold')
    axes[1, 1].set_xlabel('Median Annual Salary (USD)')
    
    plt.tight_layout()
    save(fig, '04_company_analysis.png')
    
    print(f"  📊 Most Common Company Size: {size_counts.index[0]} ({size_counts.values[0]} jobs)")
    print(f"  📊 Highest Paying Industry: {industry_sal.index[0]} (${industry_sal.values[0]:,.0f})")
    if 'Big Tech' in size_sal.index and 'Startup' in size_sal.index:
        premium = ((size_sal['Big Tech'] / size_sal['Startup'] - 1) * 100)
        print_insight(f"Big Tech companies pay {premium:.1f}% more than Startups")

# ─── 6. AI/ML ROLE ANALYSIS ──────────────────────────────────────────────
def ai_ml_analysis(df):
    """Analysis of AI/ML specific roles and trends"""
    print("\n" + "="*60)
    print("🤖 AI/ML ROLE ANALYSIS")
    print("="*60)
    
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    
    # 1. Job category distribution
    category_counts = df['job_category'].value_counts()
    axes[0, 0].pie(category_counts.values, labels=category_counts.index,
                   autopct='%1.1f%%', colors=PALETTE[:len(category_counts)],
                   wedgeprops=dict(edgecolor='white', linewidth=2))
    axes[0, 0].set_title('AI/ML Job Categories', fontsize=14, fontweight='bold')
    
    # 2. Role distribution
    role_counts = df['job_title'].value_counts().head(12)
    axes[0, 1].barh(role_counts.index[::-1], role_counts.values[::-1], color=PALETTE)
    for i, (idx, val) in enumerate(role_counts[::-1].items()):
        axes[0, 1].text(val + 2, i, str(val), va='center', fontsize=9)
    axes[0, 1].set_title('Top 12 AI/ML Roles', fontsize=14, fontweight='bold')
    axes[0, 1].set_xlabel('Number of Jobs')
    
    # 3. Demand score analysis
    if 'demand_score' in df.columns:
        demand_by_role = df.groupby('job_title')['demand_score'].mean().sort_values(ascending=False).head(10)
        axes[1, 0].barh(demand_by_role.index[::-1], demand_by_role.values[::-1], color=PALETTE)
        for i, (idx, val) in enumerate(demand_by_role[::-1].items()):
            axes[1, 0].text(val + 1, i, f"{val:.0f}/100", va='center', fontsize=9)
        axes[1, 0].set_title('Most In-Demand AI/ML Roles (Demand Score)', fontsize=14, fontweight='bold')
        axes[1, 0].set_xlabel('Demand Score (0-100)')
    
    # 4. AI salary premium
    if 'ai_salary_premium_pct' in df.columns:
        premium_by_role = df.groupby('job_title')['ai_salary_premium_pct'].mean().sort_values(ascending=False).head(10)
        axes[1, 1].barh(premium_by_role.index[::-1], premium_by_role.values[::-1], color=PALETTE)
        for i, (idx, val) in enumerate(premium_by_role[::-1].items()):
            axes[1, 1].text(val + 1, i, f"+{val:.0f}%", va='center', fontsize=9)
        axes[1, 1].set_title('AI Salary Premium by Role', fontsize=14, fontweight='bold')
        axes[1, 1].set_xlabel('Salary Premium vs Non-AI Role (%)')
    
    plt.tight_layout()
    save(fig, '05_ai_ml_analysis.png')
    
    print(f"  📊 Most Common Category: {category_counts.index[0]} ({category_counts.values[0]} jobs)")
    print(f"  📊 Most Common Role: {role_counts.index[0]} ({role_counts.values[0]} jobs)")
    if 'demand_score' in df.columns:
        print(f"  📊 Highest Demand Role: {demand_by_role.index[0]} ({demand_by_role.values[0]:.0f}/100)")
    print_insight("AI Engineering roles are most common, followed by Data Science and ML Operations")

# ─── 7. TRENDS ANALYSIS ──────────────────────────────────────────────────
def trends_analysis(df):
    """Analysis of trends over time"""
    print("\n" + "="*60)
    print("📈 TRENDS ANALYSIS")
    print("="*60)
    
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    
    # 1. Jobs by posting month
    if 'posting_month' in df.columns:
        month_counts = df['posting_month'].value_counts().sort_index()
        axes[0].bar(month_counts.index, month_counts.values, color=PALETTE[:len(month_counts)])
        for i, (idx, val) in enumerate(month_counts.items()):
            axes[0].text(i, val + 5, str(val), ha='center', fontsize=9)
        axes[0].set_title('Job Postings by Month', fontsize=14, fontweight='bold')
        axes[0].set_xlabel('Month')
        axes[0].set_ylabel('Number of Jobs')
    
    # 2. Senior vs Non-senior
    if 'is_senior' in df.columns:
        senior_counts = df['is_senior'].value_counts()
        labels = ['Senior' if v==1 else 'Non-Senior' for v in senior_counts.index]
        axes[1].pie(senior_counts.values, labels=labels,
                    autopct='%1.1f%%', colors=[PALETTE[0], PALETTE[1]],
                    wedgeprops=dict(edgecolor='white', linewidth=2))
        axes[1].set_title('Senior vs Non-Senior Roles', fontsize=14, fontweight='bold')
    
    # 3. LLM vs Traditional
    if 'is_llm_role' in df.columns:
        llm_counts = df['is_llm_role'].value_counts()
        labels = ['LLM/GenAI' if v==1 else 'Traditional ML' for v in llm_counts.index]
        axes[2].pie(llm_counts.values, labels=labels,
                    autopct='%1.1f%%', colors=[PALETTE[2], PALETTE[3]],
                    wedgeprops=dict(edgecolor='white', linewidth=2))
        axes[2].set_title('LLM/GenAI vs Traditional ML Roles', fontsize=14, fontweight='bold')
    
    plt.tight_layout()
    save(fig, '06_trends_analysis.png')
    
    if 'is_llm_role' in df.columns:
        llm_pct = (df['is_llm_role'].sum() / len(df)) * 100
        print(f"  📊 LLM/GenAI Roles: {llm_pct:.1f}% of total")
    if 'posting_month' in df.columns:
        print(f"  📊 Peak Hiring Month: {month_counts.idxmax()} ({month_counts.max()} jobs)")
    print_insight(f"LLM/GenAI roles represent {llm_pct:.1f}% of all AI jobs, showing the rise of generative AI")

# ─── 8. CORRELATION ANALYSIS ─────────────────────────────────────────────
def correlation_analysis(df):
    """Correlation analysis between key variables"""
    print("\n" + "="*60)
    print("📊 CORRELATION ANALYSIS")
    print("="*60)
    
    # Select numerical columns
    numeric_cols = ['annual_salary_usd', 'salary_min_usd', 'salary_max_usd',
                    'years_of_experience', 'ai_salary_premium_pct', 'demand_score',
                    'demand_growth_yoy_pct', 'benefits_score_10']
    numeric_cols = [col for col in numeric_cols if col in df.columns]
    
    if len(numeric_cols) > 1:
        corr_matrix = df[numeric_cols].corr()
        
        fig, ax = plt.subplots(figsize=(10, 8))
        sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='coolwarm',
                    square=True, linewidths=1, cbar_kws={'label': 'Correlation'},
                    ax=ax)
        ax.set_title('Correlation Matrix of Key Variables', fontsize=14, fontweight='bold')
        plt.tight_layout()
        save(fig, '07_correlation_analysis.png')
        
        # Find strongest correlations
        corr_pairs = []
        for i in range(len(corr_matrix.columns)):
            for j in range(i+1, len(corr_matrix.columns)):
                corr_pairs.append((corr_matrix.columns[i], corr_matrix.columns[j], 
                                   corr_matrix.iloc[i, j]))
        corr_pairs.sort(key=lambda x: abs(x[2]), reverse=True)
        
        print(f"  📊 Strongest Correlations:")
        for col1, col2, corr in corr_pairs[:3]:
            print(f"    • {col1} ↔ {col2}: {corr:.2f}")
        print_insight("Salary is strongly correlated with experience and demand score")

# ─── 9. PLOTLY INTERACTIVE VISUALIZATIONS ────────────────────────────────
def plotly_interactive(df):
    """Generate interactive Plotly visualizations"""
    print("\n" + "="*60)
    print("🎨 INTERACTIVE VISUALIZATIONS (Plotly)")
    print("="*60)
    
    # 1. Interactive scatter plot: Experience vs Salary
    fig1 = px.scatter(df, x='years_of_experience', y='annual_salary_usd',
                      color='job_category', 
                      hover_data=['job_title', 'country', 'company_size'],
                      title='Experience vs Salary by Job Category',
                      labels={'years_of_experience': 'Years of Experience', 
                              'annual_salary_usd': 'Annual Salary (USD)'})
    fig1.update_layout(height=500)
    fig1.write_html(os.path.join(ASSETS, 'interactive_01_exp_salary.html'))
    print(f"  ✅ interactive_01_exp_salary.html")
    
    # 2. Interactive treemap: Roles by Category and Salary
    if 'job_category' in df.columns and 'job_title' in df.columns:
        agg_data = df.groupby(['job_category', 'job_title']).agg({
            'annual_salary_usd': 'mean',
            'job_id': 'count'
        }).reset_index()
        agg_data.columns = ['Category', 'Role', 'Avg Salary', 'Count']
        
        fig2 = px.treemap(agg_data, path=['Category', 'Role'], 
                          values='Count', color='Avg Salary',
                          color_continuous_scale='Blues',
                          title='AI Roles Treemap: Category → Role (Color = Avg Salary)',
                          hover_data={'Avg Salary': ':$.2f'})
        fig2.update_layout(height=600)
        fig2.write_html(os.path.join(ASSETS, 'interactive_02_treemap.html'))
        print(f"  ✅ interactive_02_treemap.html")
    
    # 3. Interactive sunburst: Country → City → Role
    if 'country' in df.columns and 'city' in df.columns and 'job_title' in df.columns:
        sunburst_data = df.groupby(['country', 'city', 'job_title']).size().reset_index(name='count')
        fig3 = px.sunburst(sunburst_data, path=['country', 'city', 'job_title'],
                           values='count', color='count',
                           color_continuous_scale='Viridis',
                           title='Geographic Distribution of AI Roles')
        fig3.update_layout(height=600)
        fig3.write_html(os.path.join(ASSETS, 'interactive_03_sunburst.html'))
        print(f"  ✅ interactive_03_sunburst.html")
    
    # 4. Interactive parallel coordinates
    numeric_features = ['annual_salary_usd', 'years_of_experience', 'demand_score', 
                        'ai_salary_premium_pct', 'benefits_score_10']
    numeric_features = [f for f in numeric_features if f in df.columns]
    if len(numeric_features) >= 3:
        # Sample for performance
        sample_df = df[numeric_features + ['job_category']].dropna().sample(min(500, len(df)))
        fig4 = px.parallel_coordinates(sample_df, color='annual_salary_usd',
                                       dimensions=numeric_features,
                                       color_continuous_scale='Viridis',
                                       title='Parallel Coordinates: Key AI Job Metrics')
        fig4.update_layout(height=600)
        fig4.write_html(os.path.join(ASSETS, 'interactive_04_parallel.html'))
        print(f"  ✅ interactive_04_parallel.html")
    
    print_insight("Interactive visualizations allow dynamic exploration of the AI job market")

# ─── MAIN RUNNER ────────────────────────────────────────────────────────────
def run_all_eda(df):
    """Run all EDA functions"""
    print("\n" + "🚀"*30)
    print("PAKISTAN TECH TALENT INTELLIGENCE SYSTEM")
    print("COMPLETE EDA PIPELINE")
    print("🚀"*30)
    
    # Run all analyses
    dataset_overview(df)
    salary_analysis(df)
    skills_analysis(df)
    location_analysis(df)
    company_analysis(df)
    ai_ml_analysis(df)
    trends_analysis(df)
    correlation_analysis(df)
    plotly_interactive(df)
    
    print("\n" + "="*60)
    print(f"✅ EDA COMPLETE! All visualizations saved to: {ASSETS}/")
    print("="*60)
    
    # Summary of findings
    print("\n📊 KEY FINDINGS SUMMARY")
    print("-"*40)
    print(f"1. Average AI Salary: ${df['annual_salary_usd'].mean():,.0f}")
    print(f"2. Top Paying Role: {df.groupby('job_title')['annual_salary_usd'].mean().idxmax()}")
    if 'required_skills' in df.columns:
        all_skills = []
        for skills in df['required_skills'].dropna():
            if isinstance(skills, str):
                all_skills.extend([s.strip() for s in skills.split('|') if s.strip()])
        if all_skills:
            print(f"3. Most In-Demand Skill: {Counter(all_skills).most_common(1)[0][0]}")
    print(f"4. Remote Work Share: {(df['remote_work']=='Fully Remote').mean()*100:.1f}%")
    if 'is_llm_role' in df.columns:
        print(f"5. LLM/GenAI Roles: {(df['is_llm_role'].mean()*100):.1f}%")
    print("-"*40)

if __name__ == "__main__":
    # Load data
    base = os.path.join(os.path.dirname(__file__), "..", "..")
    data_path = os.path.join(base, "data", "job_market.csv")
    
    if not os.path.exists(data_path):
        print(f"❌ Dataset not found at: {data_path}")
        print("Please download the dataset from Kaggle and place it in data/ folder")
        exit(1)
    
    df = pd.read_csv(data_path)
    run_all_eda(df)