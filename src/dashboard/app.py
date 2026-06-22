"""
Pakistan Data Intelligence Dashboard
Dark Mode UI — 10Pearls SHINE Program
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from collections import Counter
import os
import json

# ─── PAGE CONFIG ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Pakistan Data Intelligence",
    page_icon="🌙",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── CUSTOM CSS - DARK MODE ──────────────────────────────────────────────────
CSS = """
<style>
/* ── Reset & Base ─────────────────────────────────────────────────── */
* { box-sizing: border-box; margin: 0; padding: 0; }
html, body, [data-testid="stAppViewContainer"], [data-testid="stMain"] {
    background: #0a0e1a !important;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    color: #e8edf5 !important;
}
[data-testid="stSidebar"] {
    background: #111827 !important;
    border-right: 0.5px solid #1f2937 !important;
    padding: 1rem;
}
[data-testid="stHeader"] { background: transparent !important; }
#MainMenu, footer, header { visibility: hidden; }

/* ── Typography ────────────────────────────────────────────────────── */
h1, h2, h3, h4 { font-family: 'Inter', sans-serif; color: #e8edf5 !important; }
p, span, div { color: #d1d5db !important; }

/* ── Sidebar Brand ───────────────────────────────────────────────── */
.sb-brand {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 8px 0 16px;
    border-bottom: 0.5px solid #1f2937;
}
.sb-brand-icon {
    width: 36px;
    height: 36px;
    border-radius: 8px;
    background: #3266ad;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
}
.sb-brand-icon i { color: #fff; font-size: 16px; }
.sb-brand-title { font-size: 13px; font-weight: 500; color: #e8edf5; margin: 0; }
.sb-brand-sub { font-size: 11px; color: #9ca3af; margin: 0; }

.sb-label {
    font-size: 10px;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: .06em;
    color: #9ca3af;
    margin: 12px 0 6px;
}

.sb-stat {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 8px 10px;
    background: #1f2937;
    border-radius: 8px;
}
.sb-stat i { color: #3266ad; font-size: 14px; width: 16px; }
.sb-stat-val { font-size: 13px; font-weight: 500; color: #e8edf5; }
.sb-stat-lbl { font-size: 11px; color: #9ca3af; margin-left: auto; }

.divider { height: 0.5px; background: #1f2937; margin: 12px 0; }

/* ── Page Header ──────────────────────────────────────────────────── */
.page-header { padding: 4px 0 12px; }
.page-title {
    font-size: 20px;
    font-weight: 600;
    color: #e8edf5 !important;
    margin: 0;
}
.page-sub { font-size: 13px; color: #9ca3af; margin-top: 2px; }

.tag {
    display: inline-flex;
    align-items: center;
    gap: 4px;
    padding: 2px 10px;
    border-radius: 20px;
    font-size: 11px;
    font-weight: 500;
    background: #1a3a2e;
    color: #4ade80;
}

/* ── KPI Cards ────────────────────────────────────────────────────── */
.kpi-grid {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 10px;
    margin: 12px 0;
}
.kpi {
    background: #111827;
    border: 0.5px solid #1f2937;
    border-radius: 12px;
    padding: 14px 16px;
    border-top: 2px solid var(--kc, #3266ad);
}
.kpi:hover {
    border-color: var(--kc, #3266ad);
    box-shadow: 0 0 20px rgba(50, 102, 173, 0.1);
}
.kpi-icon {
    width: 30px;
    height: 30px;
    border-radius: 8px;
    background: var(--kb, rgba(50, 102, 173, 0.15));
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 10px;
}
.kpi-icon i { color: var(--kc, #3266ad); font-size: 14px; }
.kpi-val { font-size: 18px; font-weight: 500; line-height: 1; color: #e8edf5; }
.kpi-lbl { font-size: 11px; color: #9ca3af; margin-top: 3px; }
.kpi-badge {
    display: inline-block;
    margin-top: 6px;
    padding: 2px 8px;
    border-radius: 20px;
    font-size: 10px;
    font-weight: 500;
    background: var(--kb, rgba(50, 102, 173, 0.15));
    color: var(--kc, #3266ad);
}

/* ── Tabs ──────────────────────────────────────────────────────────── */
.tabs {
    display: flex;
    gap: 0;
    background: #111827;
    border: 0.5px solid #1f2937;
    border-radius: 8px;
    padding: 3px;
    flex-wrap: wrap;
    margin: 8px 0 16px;
}
.tab {
    padding: 6px 14px;
    font-size: 12px;
    border-radius: 6px;
    cursor: pointer;
    border: none;
    background: transparent;
    color: #9ca3af;
    font-family: inherit;
    white-space: nowrap;
}
.tab.active { background: #3266ad; color: #fff; }

/* ── Section Header ───────────────────────────────────────────────── */
.sec-hd {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 14px;
}
.sec-hd i { color: #3266ad; font-size: 15px; }
.sec-hd span { font-size: 14px; font-weight: 500; color: #e8edf5; }

/* ── Chart Cards ──────────────────────────────────────────────────── */
.chart-grid {
    display: grid;
    gap: 12px;
}
.g2 { grid-template-columns: repeat(2, 1fr); }
.g3 { grid-template-columns: repeat(3, 1fr); }

.chart-card {
    background: #111827;
    border: 0.5px solid #1f2937;
    border-radius: 12px;
    padding: 16px;
}
.chart-title {
    font-size: 12px;
    font-weight: 500;
    margin-bottom: 12px;
    color: #9ca3af;
}

/* ── Insight Cards ────────────────────────────────────────────────── */
.insight-card {
    background: #111827;
    border: 0.5px solid #1f2937;
    border-radius: 12px;
    padding: 16px;
}
.ins-hd {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 12px;
    font-size: 13px;
    font-weight: 500;
    color: #e8edf5;
}
.ins-hd i { color: #3266ad; }
.ins-item {
    display: flex;
    align-items: flex-start;
    gap: 8px;
    padding: 7px 0;
    border-bottom: 0.5px solid #1f2937;
    font-size: 12px;
    color: #d1d5db;
    line-height: 1.5;
}
.ins-item:last-child { border-bottom: none; }
.ins-item i { color: #4ade80; font-size: 11px; margin-top: 3px; flex-shrink: 0; }
.ins-item strong { color: #e8edf5; }

/* ── Recommendation Cards ────────────────────────────────────────── */
.rec-card {
    background: #111827;
    border: 0.5px solid #1f2937;
    border-radius: 12px;
    padding: 14px;
    margin-bottom: 10px;
}
.rec-card:hover {
    border-color: #3266ad;
}
.rec-title {
    font-size: 13px;
    font-weight: 500;
    display: flex;
    align-items: center;
    gap: 8px;
    color: #e8edf5;
}
.rec-desc {
    font-size: 12px;
    color: #d1d5db;
    margin-top: 6px;
    line-height: 1.5;
}
.badge {
    display: inline-block;
    padding: 2px 10px;
    border-radius: 20px;
    font-size: 10px;
    font-weight: 500;
    margin-top: 8px;
}
.badge-high { background: #1a3a2e; color: #4ade80; }
.badge-med { background: #3a2e1a; color: #fbbf24; }

/* ── Skill Rows ───────────────────────────────────────────────────── */
.skill-row {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 6px 0;
    border-bottom: 0.5px solid #1f2937;
    font-size: 12px;
}
.skill-row:last-child { border-bottom: none; }
.skill-name { min-width: 120px; font-weight: 500; color: #e8edf5; }
.skill-bar-wrap {
    flex: 1;
    height: 6px;
    background: #1f2937;
    border-radius: 3px;
    overflow: hidden;
}
.skill-bar {
    height: 100%;
    border-radius: 3px;
    background: linear-gradient(90deg, #3266ad, #4ade80);
}
.skill-count {
    min-width: 40px;
    text-align: right;
    color: #9ca3af;
}

/* ── Insight Highlight ───────────────────────────────────────────── */
.insight-highlight {
    background: #1a2a3a;
    border-left: 3px solid #4ade80;
    border-radius: 0 8px 8px 0;
    padding: 10px 14px;
    font-size: 12px;
    color: #d1d5db;
    margin-bottom: 8px;
    line-height: 1.5;
}
.insight-highlight i { color: #4ade80; }

/* ── Gap Rows ────────────────────────────────────────────────────── */
.gap-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 8px 0;
    border-bottom: 0.5px solid #1f2937;
    font-size: 12px;
}
.gap-row:last-child { border-bottom: none; }
.gap-row strong { color: #e8edf5; }
.gap-score-high { color: #4ade80; font-weight: 600; }
.gap-score-med { color: #fbbf24; font-weight: 600; }
.gap-score-low { color: #f87171; font-weight: 600; }

/* ── Footer ───────────────────────────────────────────────────────── */
.footer {
    text-align: center;
    font-size: 11px;
    color: #6b7280;
    padding: 12px 0 4px;
    border-top: 0.5px solid #1f2937;
    margin-top: 16px;
}
.footer i { color: #3266ad; }

/* ── Streamlit Overrides ──────────────────────────────────────────── */
[data-testid="stTabs"] [data-baseweb="tab-list"] {
    gap: 0;
    background: #111827;
    border: 0.5px solid #1f2937;
    border-radius: 8px;
    padding: 3px;
    margin: 8px 0 16px;
}
[data-testid="stTabs"] [data-baseweb="tab"] {
    border-radius: 6px;
    padding: 6px 14px;
    font-size: 12px;
    color: #9ca3af;
    background: transparent;
    border: none;
}
[data-testid="stTabs"] [aria-selected="true"] {
    background: #3266ad !important;
    color: #fff !important;
}

/* ── Selectbox Styling ───────────────────────────────────────────── */
[data-testid="stSelectbox"] > div > div {
    background: #1f2937 !important;
    border-color: #1f2937 !important;
    color: #e8edf5 !important;
    border-radius: 8px !important;
}
[data-testid="stSelectbox"] svg {
    color: #9ca3af !important;
}

/* ── Info Box ────────────────────────────────────────────────────── */
.info-box {
    background: #1a2a3a;
    padding: 1rem;
    border-radius: 8px;
    border-left: 3px solid #3266ad;
    margin: 0.5rem 0;
}
.info-box p {
    color: #d1d5db;
    margin: 0;
}
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)


# ─── LOAD DATA ────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    base = os.path.join(os.path.dirname(__file__), "..", "..")
    
    possible_paths = [
        os.path.join(base, "data", "processed", "pakistan_jobs_clean.csv"),
        os.path.join(base, "data", "job_market.csv"),
        os.path.join(base, "data", "ai_jobs_market_2025_2026.csv"),
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            df = pd.read_csv(path)
            if 'required_skills' in df.columns:
                df['skill_list'] = df['required_skills'].apply(
                    lambda x: [s.strip() for s in str(x).split('|') if s.strip()] if pd.notna(x) else []
                )
            elif 'skill_list' not in df.columns:
                df['skill_list'] = [[] for _ in range(len(df))]
            
            if 'is_pakistan' not in df.columns:
                df['is_pakistan'] = df['country'] == 'Pakistan' if 'country' in df.columns else False
            
            return df
    
    st.markdown("""
    <div style='padding: 2rem; text-align: center; background: #1a2a3a; border-radius: 1rem;'>
        <i class='fas fa-database' style='font-size: 3rem; color: #f87171;'></i>
        <h3 style='color: #e8edf5;'>Dataset Not Found</h3>
        <p style='color: #9ca3af;'>Please run data_collector.py first</p>
    </div>
    """, unsafe_allow_html=True)
    return None

@st.cache_data
def load_insights():
    base = os.path.join(os.path.dirname(__file__), "..", "..")
    path = os.path.join(base, "data", "processed", "insights_report.json")
    if os.path.exists(path):
        with open(path, 'r') as f:
            return json.load(f)
    return None

df = load_data()
insights = load_insights()

if df is None:
    st.stop()


# ─── HELPERS ─────────────────────────────────────────────────────────────────
def chart_card(title, fig, height=300):
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Inter', size=11, color='#d1d5db'),
        margin=dict(l=0, r=10, t=30, b=0),
        height=height,
        title_font=dict(size=12, color='#e8edf5'),
        xaxis=dict(gridcolor='#1f2937', linecolor='#1f2937', tickfont=dict(size=10, color='#9ca3af')),
        yaxis=dict(gridcolor='#1f2937', linecolor='#1f2937', tickfont=dict(size=10, color='#9ca3af')),
        showlegend=False,
        coloraxis_showscale=False,
        legend=dict(font=dict(color='#d1d5db'))
    )
    st.markdown(f"<div class='chart-card'><div class='chart-title'>{title}</div>", unsafe_allow_html=True)
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    st.markdown("</div>", unsafe_allow_html=True)


# ─── SIDEBAR ─────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class='sb-brand'>
        <div class='sb-brand-icon'><i class='fas fa-moon'></i></div>
        <div>
            <div class='sb-brand-title'>Pakistan Data Intel</div>
            <div class='sb-brand-sub'>AI-Powered Analytics</div>
        </div>
    </div>
    <div class='divider'></div>
    """, unsafe_allow_html=True)
    
    st.markdown("<div class='sb-label'>Filters</div>", unsafe_allow_html=True)
    
    exp_options = ['All'] + sorted(df['experience_level'].unique().tolist()) if 'experience_level' in df.columns else ['All']
    remote_options = ['All'] + sorted(df['remote_work'].unique().tolist()) if 'remote_work' in df.columns else ['All']
    size_options = ['All'] + sorted(df['company_size'].unique().tolist()) if 'company_size' in df.columns else ['All']
    
    sel_exp = st.selectbox("Experience", exp_options)
    sel_remote = st.selectbox("Work Type", remote_options)
    sel_size = st.selectbox("Company Size", size_options)
    
    fdf = df.copy()
    if sel_exp != 'All' and 'experience_level' in df.columns:
        fdf = fdf[fdf['experience_level'] == sel_exp]
    if sel_remote != 'All' and 'remote_work' in df.columns:
        fdf = fdf[fdf['remote_work'] == sel_remote]
    if sel_size != 'All' and 'company_size' in df.columns:
        fdf = fdf[fdf['company_size'] == sel_size]
    
    pakistan_count = fdf[fdf['is_pakistan'] == True].shape[0] if 'is_pakistan' in fdf.columns else len(fdf)
    
    st.markdown(f"""
    <div class='divider'></div>
    <div class='sb-stat'>
        <i class='fas fa-database'></i>
        <span class='sb-stat-val'>{len(fdf):,}</span>
        <span class='sb-stat-lbl'>Matched jobs</span>
    </div>
    <div class='sb-stat'>
        <i class='fas fa-globe'></i>
        <span class='sb-stat-val'>{fdf['country'].nunique() if 'country' in fdf.columns else 'N/A'}</span>
        <span class='sb-stat-lbl'>Countries</span>
    </div>
    <div class='sb-stat'>
        <i class='fas fa-flag'></i>
        <span class='sb-stat-val'>{pakistan_count:,}</span>
        <span class='sb-stat-lbl'>Pakistan jobs</span>
    </div>
    """, unsafe_allow_html=True)


# ─── MAIN CONTENT ─────────────────────────────────────────────────────────────
st.markdown(f"""
<div class='page-header'>
    <div style='display:flex;align-items:center;gap:10px;flex-wrap:wrap'>
        <div class='page-title'>🌙 Pakistan Data Intelligence System</div>
        <span class='tag'><i class='fas fa-flag' style='font-size:11px'></i> Pakistan focused</span>
    </div>
    <div class='page-sub'>Analyzing {len(fdf):,} AI/ML job postings — {pakistan_count:,} from Pakistan's tech market</div>
</div>
""", unsafe_allow_html=True)

# KPI Cards
avg_sal = fdf['annual_salary_usd'].mean() if 'annual_salary_usd' in fdf.columns else 0
max_sal = fdf['annual_salary_usd'].max() if 'annual_salary_usd' in fdf.columns else 0
rem_pct = (fdf['remote_work'] == 'Fully Remote').mean() * 100 if 'remote_work' in fdf.columns else 0
top_role = fdf['job_title'].mode()[0] if not fdf.empty and 'job_title' in fdf.columns else 'N/A'
role_count = fdf['job_title'].nunique() if 'job_title' in fdf.columns else 0

st.markdown(f"""
<div class='kpi-grid'>
    <div class='kpi' style='--kc:#60a5fa;--kb:rgba(96,165,250,0.15)'>
        <div class='kpi-icon'><i class='fas fa-briefcase'></i></div>
        <div class='kpi-val'>{len(fdf):,}</div>
        <div class='kpi-lbl'>Total jobs</div>
        <div class='kpi-badge'>{role_count} roles</div>
    </div>
    <div class='kpi' style='--kc:#4ade80;--kb:rgba(74,222,128,0.15)'>
        <div class='kpi-icon'><i class='fas fa-dollar-sign'></i></div>
        <div class='kpi-val'>${avg_sal:,.0f}</div>
        <div class='kpi-lbl'>Avg annual salary</div>
        <div class='kpi-badge'>USD</div>
    </div>
    <div class='kpi' style='--kc:#fbbf24;--kb:rgba(251,191,36,0.15)'>
        <div class='kpi-icon'><i class='fas fa-crown'></i></div>
        <div class='kpi-val'>${max_sal:,.0f}</div>
        <div class='kpi-lbl'>Max salary</div>
        <div class='kpi-badge'>Top band</div>
    </div>
    <div class='kpi' style='--kc:#a78bfa;--kb:rgba(167,139,250,0.15)'>
        <div class='kpi-icon'><i class='fas fa-home'></i></div>
        <div class='kpi-val'>{rem_pct:.1f}%</div>
        <div class='kpi-lbl'>Fully remote</div>
        <div class='kpi-badge'>Of listings</div>
    </div>
    <div class='kpi' style='--kc:#f87171;--kb:rgba(248,113,113,0.15)'>
        <div class='kpi-icon'><i class='fas fa-medal'></i></div>
        <div class='kpi-val' style='font-size:13px;padding-top:4px'>{top_role[:18]}</div>
        <div class='kpi-lbl'>Most listed role</div>
        <div class='kpi-badge'>Top demand</div>
    </div>
</div>
""", unsafe_allow_html=True)


# ─── TABS ─────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "Overview", "Salary Analysis", "Skills", "Location", "AI/ML Trends", "Business Insights"
])


# ─── TAB 1: OVERVIEW ──────────────────────────────────────────────────────────
with tab1:
    col1, col2 = st.columns(2)
    
    with col1:
        if 'job_category' in fdf.columns:
            cat = fdf['job_category'].value_counts().head(8)
            fig = px.pie(values=cat.values, names=cat.index, hole=0.4,
                         color_discrete_sequence=['#60a5fa','#4ade80','#fbbf24','#f87171','#a78bfa','#34d399','#f472b6'])
            fig.update_traces(textposition='outside', textfont_size=11, textfont_color='#d1d5db')
            chart_card("Job Distribution by Category", fig, 280)
    
    with col2:
        if 'job_title' in fdf.columns:
            roles = fdf['job_title'].value_counts().head(8)
            fig = go.Figure(go.Bar(
                x=roles.values, y=roles.index, orientation='h',
                marker=dict(color='#60a5fa', line=dict(width=0)),
                text=roles.values, textposition='outside', textfont=dict(size=11, color='#d1d5db')
            ))
            fig.update_layout(xaxis_title='', yaxis_title='', yaxis=dict(autorange='reversed'))
            chart_card("Top 8 AI/ML Roles", fig, 280)
    
    col1, col2 = st.columns(2)
    
    with col1:
        if 'company_size' in fdf.columns:
            sz = fdf['company_size'].value_counts()
            fig = go.Figure(go.Bar(
                x=sz.index, y=sz.values,
                marker=dict(color=['#93c5fd','#60a5fa','#2563eb'], line=dict(width=0)),
                text=sz.values, textposition='outside', textfont=dict(size=11, color='#d1d5db')
            ))
            fig.update_layout(xaxis_title='', yaxis_title='Listings')
            chart_card("Jobs by Company Size", fig, 250)
    
    with col2:
        if 'industry' in fdf.columns:
            ind = fdf['industry'].value_counts().head(8)
            fig = go.Figure(go.Bar(
                x=ind.values, y=ind.index, orientation='h',
                marker=dict(color='#60a5fa', line=dict(width=0)),
                text=ind.values, textposition='outside', textfont=dict(size=11, color='#d1d5db')
            ))
            fig.update_layout(xaxis_title='Listings', yaxis_title='', yaxis=dict(autorange='reversed'))
            chart_card("Top Industries", fig, 250)


# ─── TAB 2: SALARY ANALYSIS ──────────────────────────────────────────────────
with tab2:
    col1, col2 = st.columns(2)
    
    with col1:
        if 'annual_salary_usd' in fdf.columns:
            med = fdf['annual_salary_usd'].median()
            mean_ = fdf['annual_salary_usd'].mean()
            fig = px.histogram(fdf, x='annual_salary_usd', nbins=35, color_discrete_sequence=['#60a5fa'])
            fig.add_vline(x=med, line_dash='dash', line_color='#f87171', line_width=1.5,
                          annotation_text=f"Median ${med:,.0f}", annotation_position="top right",
                          annotation_font=dict(color='#f87171'))
            fig.add_vline(x=mean_, line_dash='dot', line_color='#fbbf24', line_width=1.5,
                          annotation_text=f"Mean ${mean_:,.0f}", annotation_position="bottom right",
                          annotation_font=dict(color='#fbbf24'))
            fig.update_layout(bargap=0.05, xaxis_title='Annual Salary (USD)', yaxis_title='Frequency')
            chart_card("Salary Distribution", fig, 300)
    
    with col2:
        if 'experience_level' in fdf.columns:
            exp_order = [e for e in ['Entry', 'Mid', 'Senior', 'Lead'] if e in fdf['experience_level'].unique()]
            fig = go.Figure()
            colors = ['#93c5fd','#60a5fa','#2563eb','#1e40af']
            for i, exp in enumerate(exp_order):
                vals = fdf[fdf['experience_level'] == exp]['annual_salary_usd']
                fig.add_trace(go.Box(y=vals, name=exp, marker_color=colors[i % len(colors)],
                                     line_color=colors[i % len(colors)],
                                     fillcolor=colors[i % len(colors)] + '33'))
            fig.update_layout(yaxis_title='Annual Salary (USD)', showlegend=False)
            chart_card("Salary by Experience Level", fig, 300)
    
    if 'is_pakistan' in fdf.columns:
        comp_df = fdf.groupby('is_pakistan')['annual_salary_usd'].mean().reset_index()
        comp_df['region'] = ['Pakistan' if v else 'International' for v in comp_df['is_pakistan']]
        fig = go.Figure(go.Bar(
            x=comp_df['region'], y=comp_df['annual_salary_usd'],
            marker=dict(color=['#4ade80', '#60a5fa'], line=dict(width=0)),
            text=[f"${v:,.0f}" for v in comp_df['annual_salary_usd']],
            textposition='outside', textfont=dict(size=11, color='#d1d5db')
        ))
        fig.update_layout(xaxis_title='', yaxis_title='Average Salary (USD)', showlegend=False)
        chart_card("Pakistan vs International — Average Salary", fig, 250)
    
    if 'job_title' in fdf.columns:
        top_sal = fdf.groupby('job_title')['annual_salary_usd'].median().sort_values(ascending=False).head(10)
        fig = go.Figure(go.Bar(
            x=top_sal.values, y=top_sal.index, orientation='h',
            marker=dict(color='#4ade80', line=dict(width=0)),
            text=[f"${v:,.0f}" for v in top_sal.values],
            textposition='outside', textfont=dict(size=11, color='#d1d5db')
        ))
        fig.update_layout(xaxis_title='Median Salary (USD)', yaxis_title='', yaxis=dict(autorange='reversed'))
        chart_card("Top 10 Highest-Paying Roles (Median USD)", fig, 300)


# ─── TAB 3: SKILLS ────────────────────────────────────────────────────────────
with tab3:
    all_skills = []
    for s in fdf['skill_list']:
        if isinstance(s, list):
            all_skills.extend(s)
    
    if all_skills:
        skill_counts = Counter(all_skills)
        skill_df = pd.DataFrame(skill_counts.most_common(15), columns=['Skill', 'Count'])
        
        max_count = skill_df['Count'].max()
        st.markdown("<div class='chart-card'><div class='chart-title'>Top 15 In-Demand Skills</div>", unsafe_allow_html=True)
        for _, row in skill_df.iterrows():
            pct = (row['Count'] / max_count) * 100
            st.markdown(f"""
            <div class='skill-row'>
                <span class='skill-name'>{row['Skill']}</span>
                <div class='skill-bar-wrap'>
                    <div class='skill-bar' style='width:{pct:.0f}%'></div>
                </div>
                <span class='skill-count'>{row['Count']:,}</span>
            </div>
            """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            base = fdf['annual_salary_usd'].median() if 'annual_salary_usd' in fdf.columns else 0
            premiums = []
            for skill, _ in skill_counts.most_common(10):
                if 'required_skills' in fdf.columns:
                    mask = fdf['required_skills'].str.contains(skill, case=False, na=False)
                    if mask.sum() > 0 and base > 0:
                        premium = ((fdf[mask]['annual_salary_usd'].median() - base) / base) * 100
                        premiums.append({'Skill': skill, 'Premium': premium})
            if premiums:
                prem_df = pd.DataFrame(premiums).sort_values('Premium', ascending=False)
                colors_bar = ['#4ade80' if v >= 0 else '#f87171' for v in prem_df['Premium']]
                fig = go.Figure(go.Bar(
                    x=prem_df['Premium'], y=prem_df['Skill'], orientation='h',
                    marker=dict(color=colors_bar, line=dict(width=0)),
                    text=[f"{v:+.1f}%" for v in prem_df['Premium']],
                    textposition='outside', textfont=dict(size=11, color='#d1d5db')
                ))
                fig.update_layout(xaxis_title='Salary Premium vs Median (%)', yaxis_title='',
                                  yaxis=dict(autorange='reversed'))
                chart_card("Salary Premium by Skill", fig, 350)
        
        with col2:
            if 'job_title' in fdf.columns:
                top_roles = fdf['job_title'].value_counts().head(5).index
                top_skills = [s for s, _ in skill_counts.most_common(8)]
                matrix = []
                for role in top_roles:
                    role_df = fdf[fdf['job_title'] == role]
                    total = len(role_df)
                    if total == 0:
                        continue
                    role_skills = []
                    for sk in role_df['skill_list']:
                        if isinstance(sk, list):
                            role_skills.extend(sk)
                    rc = Counter(role_skills)
                    matrix.append([round(rc.get(sk, 0) / total * 100, 1) for sk in top_skills])
                if matrix:
                    hm_df = pd.DataFrame(matrix, index=top_roles[:len(matrix)], columns=top_skills)
                    fig = px.imshow(hm_df, text_auto='.1f', aspect='auto',
                                    color_continuous_scale=[[0,'#1f2937'],[.5,'#60a5fa'],[1,'#2563eb']],
                                    labels=dict(color='% of Jobs'))
                    fig.update_traces(textfont_size=10, textfont_color='#e8edf5')
                    fig.update_layout(height=350)
                    chart_card("Skill Demand by Role (%)", fig, 350)


# ─── TAB 4: LOCATION ──────────────────────────────────────────────────────────
with tab4:
    col1, col2 = st.columns(2)
    
    with col1:
        if 'country' in fdf.columns:
            cc = fdf['country'].value_counts().head(10)
            colors = ['#4ade80' if c == 'Pakistan' else '#60a5fa' for c in cc.index]
            fig = go.Figure(go.Bar(
                x=cc.index, y=cc.values,
                marker=dict(color=colors, line=dict(width=0)),
                text=cc.values, textposition='outside', textfont=dict(size=11, color='#d1d5db')
            ))
            fig.update_layout(xaxis_title='', yaxis_title='Job Listings')
            chart_card("Jobs by Country", fig, 280)
    
    with col2:
        if 'country' in fdf.columns and 'annual_salary_usd' in fdf.columns:
            cs = fdf.groupby('country')['annual_salary_usd'].median().sort_values(ascending=False).head(10)
            colors = ['#4ade80' if c == 'Pakistan' else '#60a5fa' for c in cs.index]
            fig = go.Figure(go.Bar(
                x=cs.index, y=cs.values,
                marker=dict(color=colors, line=dict(width=0)),
                text=[f"${v:,.0f}" for v in cs.values],
                textposition='outside', textfont=dict(size=11, color='#d1d5db')
            ))
            fig.update_layout(xaxis_title='', yaxis_title='Median Salary (USD)')
            chart_card("Median Salary by Country (USD)", fig, 280)
    
    if 'city' in fdf.columns and 'is_pakistan' in fdf.columns:
        pakistan_df = fdf[fdf['is_pakistan'] == True]
        if not pakistan_df.empty:
            col1, col2 = st.columns(2)
            with col1:
                city_counts = pakistan_df['city'].value_counts().head(6)
                fig = go.Figure(go.Bar(
                    x=city_counts.values, y=city_counts.index, orientation='h',
                    marker=dict(color='#4ade80', line=dict(width=0)),
                    text=city_counts.values, textposition='outside', textfont=dict(size=11, color='#d1d5db')
                ))
                fig.update_layout(xaxis_title='Listings', yaxis_title='', yaxis=dict(autorange='reversed'))
                chart_card("Pakistan — Jobs by City", fig, 250)
    
    if 'remote_work' in fdf.columns:
        col1, col2 = st.columns(2)
        with col1:
            rc = fdf['remote_work'].value_counts()
            fig = px.pie(values=rc.values, names=rc.index, hole=0.4,
                         color_discrete_sequence=['#60a5fa','#a78bfa','#93c5fd'])
            fig.update_traces(textposition='outside', textfont_size=11, textfont_color='#d1d5db')
            chart_card("Remote Work Distribution", fig, 250)


# ─── TAB 5: AI/ML TRENDS ─────────────────────────────────────────────────────
with tab5:
    col1, col2 = st.columns(2)
    
    with col1:
        if 'is_llm_role' in fdf.columns:
            lc = fdf['is_llm_role'].value_counts()
            labels = ['LLM / GenAI' if v == 1 else 'Traditional ML' for v in lc.index]
            fig = px.pie(values=lc.values, names=labels, hole=0.4,
                         color_discrete_sequence=['#60a5fa','#93c5fd'])
            fig.update_traces(textposition='outside', textfont_size=11, textfont_color='#d1d5db')
            chart_card("LLM / GenAI vs Traditional ML", fig, 260)
    
    with col2:
        if 'is_senior' in fdf.columns:
            sc = fdf['is_senior'].value_counts()
            labels = ['Senior' if v == 1 else 'Non-Senior' for v in sc.index]
            fig = px.pie(values=sc.values, names=labels, hole=0.4,
                         color_discrete_sequence=['#4ade80','#86efac'])
            fig.update_traces(textposition='outside', textfont_size=11, textfont_color='#d1d5db')
            chart_card("Senior vs Non-Senior Roles", fig, 260)
    
    if 'demand_score' in fdf.columns:
        col1, col2 = st.columns(2)
        with col1:
            dr = fdf.groupby('job_title')['demand_score'].mean().sort_values(ascending=False).head(8)
            fig = go.Figure(go.Bar(
                x=dr.values, y=dr.index, orientation='h',
                marker=dict(color='#fbbf24', line=dict(width=0)),
                text=[f"{v:.0f}" for v in dr.values],
                textposition='outside', textfont=dict(size=11, color='#d1d5db')
            ))
            fig.update_layout(xaxis_title='Demand Score (0-100)', yaxis_title='', yaxis=dict(autorange='reversed'))
            chart_card("Most In-Demand Roles by Score", fig, 280)
    
    if 'education_required' in fdf.columns:
        edu = fdf['education_required'].value_counts()
        fig = px.pie(values=edu.values, names=edu.index, hole=0.4,
                     color_discrete_sequence=['#60a5fa','#4ade80','#fbbf24','#93c5fd'])
        fig.update_traces(textposition='outside', textfont_size=11, textfont_color='#d1d5db')
        fig.update_layout(height=280)
        chart_card("Education Requirements", fig, 280)


# ─── TAB 6: BUSINESS INSIGHTS ────────────────────────────────────────────────
with tab6:
    st.markdown("<div class='sec-hd'><i class='fas fa-lightbulb'></i><span>Business Insights & Recommendations</span></div>", unsafe_allow_html=True)
    
    if insights:
        st.markdown("<div style='font-size:13px;font-weight:500;margin-bottom:10px;color:#e8edf5'>Key takeaways</div>", unsafe_allow_html=True)
        summary = insights.get('summary', {})
        for insight in summary.get('top_insights', []):
            st.markdown(f"""
            <div class='insight-highlight'>
                <i class='fas fa-lightbulb' style='color:#4ade80;margin-right:6px'></i>
                {insight}
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<div style='font-size:13px;font-weight:500;margin:14px 0 10px;color:#e8edf5'>Actionable recommendations</div>", unsafe_allow_html=True)
        for rec in insights.get('recommendations', []):
            priority = rec.get('priority', 'Medium')
            badge_class = 'badge-high' if priority == 'High' else 'badge-med'
            icon = 'fa-circle-check' if priority == 'High' else 'fa-clock'
            st.markdown(f"""
            <div class='rec-card'>
                <div class='rec-title'>
                    <i class='fas {icon}' style='color:#4ade80'></i>
                    {rec.get('title')}
                </div>
                <div class='rec-desc'>{rec.get('description')}</div>
                <span class='badge {badge_class}'>{priority} priority</span>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<div style='font-size:13px;font-weight:500;margin:14px 0 10px;color:#e8edf5'>Skill gap analysis</div>", unsafe_allow_html=True)
        skill_gap = insights.get('skill_gap', {})
        for analysis in skill_gap.get('skill_gap_analysis', []):
            score = analysis.get('supply_score', 0)
            score_class = 'gap-score-high' if score >= 70 else 'gap-score-med' if score >= 50 else 'gap-score-low'
            st.markdown(f"""
            <div class='gap-row'>
                <span><strong>{analysis['skill']}</strong></span>
                <span>Demand: {analysis['demand']} | Supply score: <span class='{score_class}'>{analysis['supply_score']}/100</span></span>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class='info-box'>
            <p><i class='fas fa-info-circle' style='color:#60a5fa'></i> Run insights generator: <code style='background:#1f2937;padding:2px 8px;border-radius:4px;color:#e8edf5'>python src/eda/insights_generator.py</code></p>
        </div>
        """, unsafe_allow_html=True)


# ─── INSIGHTS STRIP ──────────────────────────────────────────────────────────
st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
st.markdown("<div class='sec-hd'><i class='fas fa-lightbulb'></i><span>Key Insights</span></div>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class='insight-card'>
        <div class='ins-hd'><i class='fas fa-chart-line'></i>Salary trends</div>
        <div class='ins-item'><i class='fas fa-check-circle'></i>Senior roles earn <strong>2.3×</strong> more than entry</div>
        <div class='ins-item'><i class='fas fa-check-circle'></i>Top 10% earn <strong>$300,000+</strong></div>
        <div class='ins-item'><i class='fas fa-check-circle'></i>Remote roles carry <strong>8% salary premium</strong></div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class='insight-card'>
        <div class='ins-hd'><i class='fas fa-microchip'></i>Skill premium</div>
        <div class='ins-item'><i class='fas fa-check-circle'></i>LLM/GenAI skills command <strong>highest premium</strong></div>
        <div class='ins-item'><i class='fas fa-check-circle'></i><strong>Python + Cloud</strong> = higher pay</div>
        <div class='ins-item'><i class='fas fa-check-circle'></i><strong>MLOps</strong> fastest-growing demand</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class='insight-card'>
        <div class='ins-hd'><i class='fas fa-globe'></i>Market insights</div>
        <div class='ins-item'><i class='fas fa-check-circle'></i>US has <strong>highest salaries</strong></div>
        <div class='ins-item'><i class='fas fa-check-circle'></i><strong>AI Engineering</strong> most posted</div>
        <div class='ins-item'><i class='fas fa-check-circle'></i>Enterprises pay <strong>35% more</strong></div>
    </div>
    """, unsafe_allow_html=True)
