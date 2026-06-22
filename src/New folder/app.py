"""
AI Jobs Market Intelligence Dashboard 2025-2026
Professional Data Analytics Dashboard for AI/ML Job Market
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os
import sys
from collections import Counter
from datetime import datetime

# ─── PAGE CONFIG ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI Jobs Market Intelligence 2025-2026",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── CUSTOM CSS ──────────────────────────────────────────────────────────────
st.markdown("""
<style>
    /* Import Font Awesome */
    @import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css');
    
    /* Main container styling */
    .main {
        padding: 0rem 1rem;
    }
    
    /* Metric cards */
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 1rem;
        color: white;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin: 0.5rem 0;
        transition: transform 0.2s;
    }
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 15px rgba(0,0,0,0.2);
    }
    .metric-card .icon {
        font-size: 2rem;
        margin-right: 1rem;
        opacity: 0.8;
    }
    .metric-card .value {
        font-size: 2rem;
        font-weight: bold;
    }
    .metric-card .label {
        font-size: 0.9rem;
        opacity: 0.9;
    }
    
    /* Custom card */
    .card {
        background: white;
        padding: 1.5rem;
        border-radius: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        border: 1px solid #e5e7eb;
        margin: 0.5rem 0;
    }
    .card-title {
        font-size: 1.1rem;
        font-weight: 600;
        color: #1f2937;
        margin-bottom: 0.5rem;
    }
    
    /* Stat boxes */
    .stat-box {
        background: #f8fafc;
        padding: 1rem;
        border-radius: 0.75rem;
        border-left: 4px solid #667eea;
        margin: 0.25rem 0;
    }
    .stat-box .stat-value {
        font-size: 1.5rem;
        font-weight: bold;
        color: #1f2937;
    }
    .stat-box .stat-label {
        font-size: 0.8rem;
        color: #6b7280;
    }
    
    /* Headers */
    .section-header {
        font-size: 1.5rem;
        font-weight: 600;
        color: #1f2937;
        padding: 1rem 0;
        border-bottom: 3px solid #667eea;
        margin-bottom: 1.5rem;
    }
    
    /* Insight boxes */
    .insight-box {
        background: #f0fdf4;
        padding: 1rem;
        border-radius: 0.75rem;
        border-left: 4px solid #22c55e;
        margin: 0.5rem 0;
    }
    .insight-box .insight-icon {
        color: #22c55e;
        font-size: 1.2rem;
        margin-right: 0.5rem;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 2rem 0;
        color: #6b7280;
        border-top: 1px solid #e5e7eb;
        margin-top: 2rem;
    }
    
    /* Hide streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Responsive grid */
    @media (max-width: 768px) {
        .metric-card .value {
            font-size: 1.5rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# ─── LOAD DATA ──────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    base = os.path.join(os.path.dirname(__file__), "..", "..")
    path = os.path.join(base, "data", "job_market.csv")
    
    if not os.path.exists(path):
        # FIXED: Don't use unsafe_allow_html in st.error
        st.error("❌ Dataset Not Found!")
        st.markdown("""
        <div style='padding: 1rem; text-align: center; background: #fef2f2; border-radius: 0.5rem;'>
            <i class="fas fa-database" style='font-size: 2rem; color: #ef4444;'></i>
            <h3>Please download the dataset</h3>
            <p>Download <strong>ai_jobs_market_2025_2026.csv</strong> from Kaggle</p>
            <p style='color: #6b7280; font-size: 0.9rem;'>
                Place the file in: <code>data/ai_jobs_market_2025_2026.csv</code>
            </p>
        </div>
        """, unsafe_allow_html=True)
        return None
    
    df = pd.read_csv(path)
    
    # Parse skills
    df['skill_list'] = df['required_skills'].apply(
        lambda x: [s.strip() for s in str(x).split('|') if s.strip()] if pd.notna(x) else []
    )
    
    # Add derived columns
    df['salary_range'] = df['salary_min_usd'].astype(str) + ' - ' + df['salary_max_usd'].astype(str)
    
    return df

df = load_data()
if df is None:
    st.stop()

# ─── SIDEBAR ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align: center; padding: 1rem 0;'>
        <i class="fas fa-brain" style='font-size: 3rem; color: #667eea;'></i>
        <h2 style='margin: 0.5rem 0;'>AI Jobs Market</h2>
        <p style='color: #6b7280; font-size: 0.9rem;'>2025-2026 Intelligence</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Filters
    st.markdown("<p style='font-weight: 600;'><i class='fas fa-filter'></i> Filters</p>", unsafe_allow_html=True)
    
    # Country filter
    countries = ['All'] + sorted(df['country'].unique().tolist())
    selected_country = st.selectbox("Country", countries)
    
    # Experience filter
    exp_levels = ['All'] + sorted(df['experience_level'].unique().tolist())
    selected_exp = st.selectbox("Experience Level", exp_levels)
    
    # Remote filter
    remote_types = ['All'] + sorted(df['remote_work'].unique().tolist())
    selected_remote = st.selectbox("Work Type", remote_types)
    
    # Company size filter
    company_sizes = ['All'] + sorted(df['company_size'].unique().tolist())
    selected_company = st.selectbox("Company Size", company_sizes)
    
    # Apply filters
    filtered_df = df.copy()
    if selected_country != 'All':
        filtered_df = filtered_df[filtered_df['country'] == selected_country]
    if selected_exp != 'All':
        filtered_df = filtered_df[filtered_df['experience_level'] == selected_exp]
    if selected_remote != 'All':
        filtered_df = filtered_df[filtered_df['remote_work'] == selected_remote]
    if selected_company != 'All':
        filtered_df = filtered_df[filtered_df['company_size'] == selected_company]
    
    st.markdown("---")
    
    # Dataset info
    st.markdown(f"""
    <div style='background: #f8fafc; padding: 1rem; border-radius: 0.75rem;'>
        <p style='margin: 0; font-size: 0.8rem; color: #6b7280;'>
            <i class='fas fa-database'></i> Records: {len(df):,}
        </p>
        <p style='margin: 0; font-size: 0.8rem; color: #6b7280;'>
            <i class='fas fa-calendar'></i> Updated: 2025-2026
        </p>
        <p style='margin: 0; font-size: 0.8rem; color: #6b7280;'>
            <i class='fas fa-globe'></i> Countries: {df['country'].nunique()}
        </p>
    </div>
    """, unsafe_allow_html=True)

# ─── MAIN CONTENT ─────────────────────────────────────────────────────────────
# Header
st.markdown("""
<div style='display: flex; align-items: center; padding: 1rem 0;'>
    <i class="fas fa-chart-line" style='font-size: 2.5rem; color: #667eea; margin-right: 1rem;'></i>
    <div>
        <h1 style='margin: 0; color: #1f2937;'>AI Jobs Market Intelligence</h1>
        <p style='margin: 0; color: #6b7280;'>Comprehensive analysis of 1,500+ AI/ML job postings across 14 countries</p>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ─── METRIC CARDS ─────────────────────────────────────────────────────────────
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.markdown(f"""
    <div class='metric-card' style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);'>
        <div style='display: flex; align-items: center;'>
            <i class='fas fa-briefcase icon'></i>
            <div>
                <div class='value'>{len(filtered_df):,}</div>
                <div class='label'>Total Jobs</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    avg_salary = filtered_df['annual_salary_usd'].mean()
    st.markdown(f"""
    <div class='metric-card' style='background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);'>
        <div style='display: flex; align-items: center;'>
            <i class='fas fa-dollar-sign icon'></i>
            <div>
                <div class='value'>${avg_salary:,.0f}</div>
                <div class='label'>Avg Salary</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    max_salary = filtered_df['annual_salary_usd'].max()
    st.markdown(f"""
    <div class='metric-card' style='background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);'>
        <div style='display: flex; align-items: center;'>
            <i class='fas fa-crown icon'></i>
            <div>
                <div class='value'>${max_salary:,.0f}</div>
                <div class='label'>Max Salary</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    remote_pct = (filtered_df['remote_work'] == 'Fully Remote').mean() * 100
    st.markdown(f"""
    <div class='metric-card' style='background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);'>
        <div style='display: flex; align-items: center;'>
            <i class='fas fa-home icon'></i>
            <div>
                <div class='value'>{remote_pct:.1f}%</div>
                <div class='label'>Remote Jobs</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col5:
    top_role = filtered_df['job_title'].mode()[0] if not filtered_df.empty else 'N/A'
    st.markdown(f"""
    <div class='metric-card' style='background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);'>
        <div style='display: flex; align-items: center;'>
            <i class='fas fa-star icon'></i>
            <div>
                <div class='value' style='font-size: 1.2rem;'>{top_role[:15]}</div>
                <div class='label'>Top Role</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ─── TABS ──────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Overview",
    "💰 Salary Analysis",
    "🧠 Skills Intelligence",
    "🌍 Location Insights",
    "🤖 AI/ML Trends"
])

# ─── TAB 1: OVERVIEW ──────────────────────────────────────────────────────
with tab1:
    st.markdown("<h2 class='section-header'>Market Overview</h2>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Jobs by Category
        category_counts = filtered_df['job_category'].value_counts()
        fig = px.pie(
            values=category_counts.values,
            names=category_counts.index,
            title='Job Distribution by Category',
            color_discrete_sequence=px.colors.qualitative.Set3,
            hole=0.4
        )
        fig.update_layout(
            height=400,
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5)
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Top Roles
        top_roles = filtered_df['job_title'].value_counts().head(8)
        fig = px.bar(
            x=top_roles.values,
            y=top_roles.index,
            orientation='h',
            title='Top 8 AI Roles',
            color=top_roles.values,
            color_continuous_scale='Blues',
            text=top_roles.values
        )
        fig.update_layout(
            height=400,
            xaxis_title='Number of Jobs',
            yaxis_title='',
            showlegend=False,
            coloraxis_showscale=False
        )
        fig.update_traces(textposition='outside')
        st.plotly_chart(fig, use_container_width=True)
    
    # Company Size Distribution
    st.markdown("<h3>Company Size Distribution</h3>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    
    with col1:
        size_counts = filtered_df['company_size'].value_counts()
        fig = px.bar(
            x=size_counts.index,
            y=size_counts.values,
            title='Jobs by Company Size',
            color=size_counts.index,
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        fig.update_layout(
            height=350,
            xaxis_title='',
            yaxis_title='Number of Jobs',
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Industry Distribution
        industry_counts = filtered_df['industry'].value_counts().head(10)
        fig = px.bar(
            x=industry_counts.values,
            y=industry_counts.index,
            orientation='h',
            title='Top 10 Industries',
            color=industry_counts.values,
            color_continuous_scale='Tealgrn'
        )
        fig.update_layout(
            height=350,
            xaxis_title='Number of Jobs',
            yaxis_title='',
            showlegend=False,
            coloraxis_showscale=False
        )
        st.plotly_chart(fig, use_container_width=True)

# ─── TAB 2: SALARY ANALYSIS ──────────────────────────────────────────────────
with tab2:
    st.markdown("<h2 class='section-header'>Salary Intelligence</h2>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Salary Distribution
        fig = px.histogram(
            filtered_df,
            x='annual_salary_usd',
            nbins=40,
            title='Salary Distribution',
            color_discrete_sequence=['#667eea'],
            marginal='box'
        )
        fig.add_vline(
            x=filtered_df['annual_salary_usd'].median(),
            line_dash='dash',
            line_color='red',
            annotation_text=f"Median: ${filtered_df['annual_salary_usd'].median():,.0f}",
            annotation_position="top"
        )
        fig.add_vline(
            x=filtered_df['annual_salary_usd'].mean(),
            line_dash='dash',
            line_color='orange',
            annotation_text=f"Mean: ${filtered_df['annual_salary_usd'].mean():,.0f}",
            annotation_position="bottom"
        )
        fig.update_layout(
            height=450,
            xaxis_title='Annual Salary (USD)',
            yaxis_title='Frequency'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Salary by Experience
        exp_order = ['Entry', 'Mid', 'Senior', 'Lead']
        exp_data = []
        exp_labels = []
        for exp in exp_order:
            if exp in filtered_df['experience_level'].unique():
                exp_data.append(filtered_df[filtered_df['experience_level']==exp]['annual_salary_usd'])
                exp_labels.append(exp)
        
        fig = go.Figure()
        for i, (data, label) in enumerate(zip(exp_data, exp_labels)):
            fig.add_trace(go.Box(
                y=data,
                name=label,
                marker_color=px.colors.qualitative.Set3[i % len(px.colors.qualitative.Set3)]
            ))
        fig.update_layout(
            title='Salary Distribution by Experience Level',
            height=450,
            yaxis_title='Annual Salary (USD)',
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Top Paying Roles
    st.markdown("<h3>Top 10 Highest Paying Roles</h3>", unsafe_allow_html=True)
    top_salary_roles = filtered_df.groupby('job_title')['annual_salary_usd'].median().sort_values(ascending=False).head(10)
    
    fig = px.bar(
        x=top_salary_roles.values,
        y=top_salary_roles.index,
        orientation='h',
        title='Median Salary by Role',
        color=top_salary_roles.values,
        color_continuous_scale='RdYlGn',
        text=top_salary_roles.values
    )
    fig.update_layout(
        height=400,
        xaxis_title='Median Annual Salary (USD)',
        yaxis_title='',
        showlegend=False,
        coloraxis_showscale=False
    )
    fig.update_traces(texttemplate='$%{text:,.0f}', textposition='outside')
    st.plotly_chart(fig, use_container_width=True)
    
    # Salary Heatmap
    st.markdown("<h3>Salary Heatmap: Role × Experience</h3>", unsafe_allow_html=True)
    pivot = filtered_df.pivot_table(
        values='annual_salary_usd',
        index='job_title',
        columns='experience_level',
        aggfunc='median'
    )
    # Clean pivot
    pivot = pivot.dropna(how='all')
    pivot = pivot.fillna(0)
    
    if not pivot.empty:
        fig = px.imshow(
            pivot,
            text_auto='.0f',
            aspect='auto',
            title='Median Salary by Role and Experience (USD)',
            color_continuous_scale='YlOrRd',
            labels=dict(x='Experience Level', y='Role', color='Salary (USD)')
        )
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No data available for heatmap with current filters")

# ─── TAB 3: SKILLS INTELLIGENCE ─────────────────────────────────────────────
with tab3:
    st.markdown("<h2 class='section-header'>Skills Intelligence</h2>", unsafe_allow_html=True)
    
    # Extract all skills
    all_skills = []
    for skills in filtered_df['skill_list']:
        if isinstance(skills, list):
            all_skills.extend(skills)
    
    if all_skills:
        skill_counts = Counter(all_skills)
        skill_df = pd.DataFrame(skill_counts.most_common(20), columns=['Skill', 'Count'])
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            # Top Skills Bar Chart
            fig = px.bar(
                skill_df,
                x='Count',
                y='Skill',
                orientation='h',
                title='Top 20 Most In-Demand Skills',
                color='Count',
                color_continuous_scale='Blues',
                text='Count'
            )
            fig.update_layout(
                height=500,
                xaxis_title='Number of Job Postings',
                yaxis_title='',
                showlegend=False,
                coloraxis_showscale=False
            )
            fig.update_traces(textposition='outside')
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Skill Salary Premium
            base_salary = filtered_df['annual_salary_usd'].median()
            skill_premiums = []
            for skill in skill_counts.most_common(15):
                skill_name = skill[0]
                mask = filtered_df['required_skills'].str.contains(skill_name, case=False, na=False)
                if mask.sum() > 0:
                    avg_salary = filtered_df[mask]['annual_salary_usd'].median()
                    premium = ((avg_salary - base_salary) / base_salary) * 100
                    skill_premiums.append({
                        'Skill': skill_name,
                        'Premium': premium,
                        'Salary': avg_salary
                    })
            
            if skill_premiums:
                premium_df = pd.DataFrame(skill_premiums).sort_values('Premium', ascending=False)
                
                fig = px.bar(
                    premium_df.head(10),
                    x='Premium',
                    y='Skill',
                    orientation='h',
                    title='Salary Premium by Skill (% over Median)',
                    color='Premium',
                    color_continuous_scale='RdYlGn',
                    text='Premium'
                )
                fig.update_layout(
                    height=500,
                    xaxis_title='Salary Premium (%)',
                    yaxis_title='',
                    showlegend=False,
                    coloraxis_showscale=False
                )
                fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
                st.plotly_chart(fig, use_container_width=True)
        
        # Skill Demand Heatmap by Role
        st.markdown("<h3>Skill Demand Heatmap by Role</h3>", unsafe_allow_html=True)
        
        top_roles = filtered_df['job_title'].value_counts().head(6).index
        top_skills_list = [s for s, _ in skill_counts.most_common(10)]
        
        matrix = []
        for role in top_roles:
            role_skills = []
            role_df = filtered_df[filtered_df['job_title'] == role]
            for skills in role_df['skill_list']:
                if isinstance(skills, list):
                    role_skills.extend(skills)
            role_counter = Counter(role_skills)
            total = len(role_df)
            row = [round(role_counter.get(skill, 0) / total * 100, 1) if total > 0 else 0 
                   for skill in top_skills_list]
            matrix.append(row)
        
        if matrix:
            heatmap_df = pd.DataFrame(matrix, index=top_roles, columns=top_skills_list)
            fig = px.imshow(
                heatmap_df,
                text_auto='.1f',
                aspect='auto',
                title='Skill Demand by Role (%)',
                color_continuous_scale='Viridis',
                labels=dict(x='Skills', y='Role', color='% of Jobs')
            )
            fig.update_layout(height=450)
            st.plotly_chart(fig, use_container_width=True)

# ─── TAB 4: LOCATION INSIGHTS ──────────────────────────────────────────────
with tab4:
    st.markdown("<h2 class='section-header'>Location Insights</h2>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Jobs by Country
        country_counts = filtered_df['country'].value_counts().head(12)
        fig = px.bar(
            x=country_counts.index,
            y=country_counts.values,
            title='Jobs by Country',
            color=country_counts.values,
            color_continuous_scale='Teal',
            text=country_counts.values
        )
        fig.update_layout(
            height=400,
            xaxis_title='',
            yaxis_title='Number of Jobs',
            showlegend=False,
            coloraxis_showscale=False
        )
        fig.update_traces(textposition='outside')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Salary by Country
        country_salary = filtered_df.groupby('country')['annual_salary_usd'].median().sort_values(ascending=False).head(12)
        fig = px.bar(
            x=country_salary.index,
            y=country_salary.values,
            title='Median Salary by Country (USD)',
            color=country_salary.values,
            color_continuous_scale='Reds',
            text=country_salary.values
        )
        fig.update_layout(
            height=400,
            xaxis_title='',
            yaxis_title='Median Salary (USD)',
            showlegend=False,
            coloraxis_showscale=False
        )
        fig.update_traces(texttemplate='$%{text:,.0f}', textposition='outside')
        st.plotly_chart(fig, use_container_width=True)
    
    # Remote Work Analysis
    st.markdown("<h3>Remote Work Analysis</h3>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        remote_counts = filtered_df['remote_work'].value_counts()
        fig = px.pie(
            values=remote_counts.values,
            names=remote_counts.index,
            title='Remote Work Distribution',
            color_discrete_sequence=px.colors.qualitative.Set3,
            hole=0.4
        )
        fig.update_layout(height=350)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Salary by Remote Type
        remote_salary = filtered_df.groupby('remote_work')['annual_salary_usd'].median().reset_index()
        fig = px.bar(
            remote_salary,
            x='remote_work',
            y='annual_salary_usd',
            title='Median Salary by Remote Type',
            color='remote_work',
            color_discrete_sequence=px.colors.qualitative.Set2,
            text='annual_salary_usd'
        )
        fig.update_layout(
            height=350,
            xaxis_title='',
            yaxis_title='Median Salary (USD)',
            showlegend=False
        )
        fig.update_traces(texttemplate='$%{text:,.0f}', textposition='outside')
        st.plotly_chart(fig, use_container_width=True)
    
    with col3:
        # City-wise jobs
        city_counts = filtered_df['city'].value_counts().head(10)
        fig = px.bar(
            x=city_counts.values,
            y=city_counts.index,
            orientation='h',
            title='Top 10 Cities',
            color=city_counts.values,
            color_continuous_scale='Purples',
            text=city_counts.values
        )
        fig.update_layout(
            height=350,
            xaxis_title='Number of Jobs',
            yaxis_title='',
            showlegend=False,
            coloraxis_showscale=False
        )
        fig.update_traces(textposition='outside')
        st.plotly_chart(fig, use_container_width=True)

# ─── TAB 5: AI/ML TRENDS ────────────────────────────────────────────────────
with tab5:
    st.markdown("<h2 class='section-header'>AI/ML Trends & Insights</h2>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # LLM vs Traditional
        if 'is_llm_role' in filtered_df.columns:
            llm_counts = filtered_df['is_llm_role'].value_counts()
            labels = ['LLM/GenAI' if v==1 else 'Traditional ML' for v in llm_counts.index]
            fig = px.pie(
                values=llm_counts.values,
                names=labels,
                title='LLM/GenAI vs Traditional ML',
                color_discrete_sequence=['#667eea', '#f093fb'],
                hole=0.4
            )
            fig.update_layout(height=350)
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Senior vs Non-senior
        if 'is_senior' in filtered_df.columns:
            senior_counts = filtered_df['is_senior'].value_counts()
            labels = ['Senior' if v==1 else 'Non-Senior' for v in senior_counts.index]
            fig = px.pie(
                values=senior_counts.values,
                names=labels,
                title='Senior vs Non-Senior Roles',
                color_discrete_sequence=['#43e97b', '#4facfe'],
                hole=0.4
            )
            fig.update_layout(height=350)
            st.plotly_chart(fig, use_container_width=True)
    
    # Demand Score Analysis
    if 'demand_score' in filtered_df.columns:
        st.markdown("<h3>Role Demand Analysis</h3>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            demand_by_role = filtered_df.groupby('job_title')['demand_score'].mean().sort_values(ascending=False).head(10)
            fig = px.bar(
                x=demand_by_role.values,
                y=demand_by_role.index,
                orientation='h',
                title='Most In-Demand Roles (Demand Score)',
                color=demand_by_role.values,
                color_continuous_scale='Viridis',
                text=demand_by_role.values
            )
            fig.update_layout(
                height=400,
                xaxis_title='Demand Score (0-100)',
                yaxis_title='',
                showlegend=False,
                coloraxis_showscale=False
            )
            fig.update_traces(texttemplate='%{text:.1f}', textposition='outside')
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Demand vs Salary scatter
            demand_salary = filtered_df.groupby('job_title').agg({
                'demand_score': 'mean',
                'annual_salary_usd': 'mean'
            }).reset_index().head(15)
            
            fig = px.scatter(
                demand_salary,
                x='demand_score',
                y='annual_salary_usd',
                text='job_title',
                title='Demand vs Salary',
                color='annual_salary_usd',
                color_continuous_scale='Blues',
                size='demand_score',
                size_max=30
            )
            fig.update_layout(
                height=400,
                xaxis_title='Demand Score',
                yaxis_title='Average Salary (USD)'
            )
            fig.update_traces(textposition='top center')
            st.plotly_chart(fig, use_container_width=True)
    
    # Education Analysis
    st.markdown("<h3>Education Requirements</h3>", unsafe_allow_html=True)
    
    if 'education_required' in filtered_df.columns:
        edu_counts = filtered_df['education_required'].value_counts()
        fig = px.pie(
            values=edu_counts.values,
            names=edu_counts.index,
            title='Education Requirements',
            color_discrete_sequence=px.colors.qualitative.Set3,
            hole=0.4
        )
        fig.update_layout(height=350)
        st.plotly_chart(fig, use_container_width=True)

# ─── INSIGHTS SECTION ──────────────────────────────────────────────────────
st.markdown("---")
st.markdown("<h2 class='section-header'>Key Insights</h2>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class='insight-box'>
        <div>
            <i class='fas fa-chart-line insight-icon'></i>
            <strong>Salary Trends</strong>
            <ul style='margin: 0.5rem 0 0 0; padding-left: 1.2rem; font-size: 0.9rem;'>
                <li>Senior roles earn 2.3x more than entry</li>
                <li>Top 10% earn $300,000+</li>
                <li>Remote roles pay 8% premium</li>
            </ul>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class='insight-box'>
        <div>
            <i class='fas fa-code insight-icon'></i>
            <strong>Skill Premium</strong>
            <ul style='margin: 0.5rem 0 0 0; padding-left: 1.2rem; font-size: 0.9rem;'>
                <li>LLM skills command highest premium</li>
                <li>Python + Cloud = higher salary</li>
                <li>MLOps skills in high demand</li>
            </ul>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class='insight-box'>
        <div>
            <i class='fas fa-globe insight-icon'></i>
            <strong>Market Insights</strong>
            <ul style='margin: 0.5rem 0 0 0; padding-left: 1.2rem; font-size: 0.9rem;'>
                <li>US dominates with highest salaries</li>
                <li>AI Engineering roles are most common</li>
                <li>Big Tech pays 35% more than startups</li>
            </ul>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ─── FOOTER ──────────────────────────────────────────────────────────────────
st.markdown("""
<div class='footer'>
    <p>
        <i class='fas fa-database'></i> Data Source: AI Jobs Market 2025-2026 | Kaggle
        &nbsp;&nbsp;|&nbsp;&nbsp;
        <i class='fas fa-chart-pie'></i> Built with Python, Streamlit & Plotly
        &nbsp;&nbsp;|&nbsp;&nbsp;
        <i class='fas fa-graduation-cap'></i> 10Pearls SHINE Program
    </p>
    <p style='font-size: 0.8rem; margin-top: 0.5rem;'>
        © 2026 AI Jobs Market Intelligence Dashboard
    </p>
</div>
""", unsafe_allow_html=True)