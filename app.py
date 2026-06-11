"""
M&E DASHBOARD - Nagaland State Budget Initiatives 2026-27
Run with: streamlit run app.py
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime
import os

import os
import sys

# For Cloud deployment - get the current directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def load_budget_data():
    """Load budget and initiatives data from Excel"""
    try:
        file_path = os.path.join(BASE_DIR, 'data', 'budget_initiatives.xlsx')
        df = pd.read_excel(file_path)
        df.columns = df.columns.str.strip()
        return df
    except FileNotFoundError:
        st.error(f"❌ File not found: data/budget_initiatives.xlsx")
        return None

def load_financial_data():
    """Load financial tracking data from Excel"""
    try:
        file_path = os.path.join(BASE_DIR, 'data', 'financial_tracking.xlsx')
        df = pd.read_excel(file_path)
        df.columns = df.columns.str.strip()
        
        date_columns = ['Funds Released Date', 'Funds Received Date', 'Funds Utilisation Date']
        for col in date_columns:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], errors='coerce')
        return df
    except FileNotFoundError:
        st.warning("⚠️ financial_tracking.xlsx not found. Using sample data.")
        return create_sample_financial_data()
    
# SIMPLE LOGIN - Add at the very top of app.py

import streamlit as st

# Initialize session state
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

# Login check at the very beginning
if not st.session_state.authenticated:
    st.set_page_config(page_title="Login", page_icon="🔐", layout="centered")
    
    st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
    }
    </style>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image("https://cdn-icons-png.flaticon.com/512/5087/5087579.png", width=100)
        st.title("Dashboard Login")
        st.markdown("### Nagaland State Budget")
        
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        
        if st.button("Login", use_container_width=True):
            if username == "Finance" and password == "Finance@123":
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("Invalid credentials. Access denied.")
    
    st.stop()  # Stop execution if not authenticated

# If authenticated, continue with normal page config
st.set_page_config(
    page_title="Nagaland M&E Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Add logout button in sidebar
with st.sidebar:
    st.markdown("---")
    if st.button("🚪 Logout", use_container_width=True):
        st.session_state.authenticated = False
        st.rerun()
# ============================================
# YOUR EXISTING DASHBOARD CODE CONTINUES HERE
# ============================================

# Page configuration
st.set_page_config(
    page_title="Nagaland M&E Dashboard",
    page_icon="map.jpg",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    /* Center align the main title */
    .stTitle {
        text-align: center !important;
    }
    
    /* Or if using st.markdown for title */
    h1 {
        text-align: center !important;
    }
</style>
""", unsafe_allow_html=True)

# Custom CSS for bold white text everywhere
st.markdown("""
<style>
    /* Make all text bold and white */
    .stMarkdown, .stMetric, .stText, .stSubheader, .stTitle {
        color: white !important;
        font-weight: bold !important;
    }
    
    /* Metric labels and values */
    [data-testid="stMetricLabel"] {
        color: white !important;
        font-weight: bold !important;
    }
    
    [data-testid="stMetricValue"] {
        color: white !important;
        font-weight: bold !important;
        font-size: 28px !important;
    }
    
    /* Subheaders */
    h1, h2, h3, h4, h5, h6 {
        color: white !important;
        font-weight: bold !important;
    }
    
    /* Plotly charts - make axis text white and bold */
    .main-svg, .g-title, .g-xtick, .g-ytick {
        fill: white !important;
        font-weight: bold !important;
    }
    
    /* Sidebar text */
    .css-1d391kg, .stSidebar {
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# DATA LOADING FUNCTIONS
# ============================================

@st.cache_data(ttl=3600)  # Cache data for 1 hour
def load_budget_data():
    """Load budget and initiatives data from Excel"""
    try:    
        df = pd.read_excel('budget_initiatives.xlsx')
        # Clean column names
        df.columns = df.columns.str.strip()
        return df
    except FileNotFoundError:
        st.error("❌ File not found: data/budget_initiatives.xlsx")
        st.info("Please ensure the file exists at: data/budget_initiatives.xlsx")
        return None
    except Exception as e:
        st.error(f"Error loading budget data: {e}")
        return None

@st.cache_data(ttl=3600)
def load_financial_data():
    """Load financial tracking data from Excel"""
    try:
        df = pd.read_excel('financial_tracking.xlsx')
        df.columns = df.columns.str.strip()
        
        # Convert date columns
        date_columns = ['Funds Released Date', 'Funds Received Date', 'Funds Utilisation Date']
        for col in date_columns:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], errors='coerce')
        
        return df
    except FileNotFoundError:
        st.warning("⚠️ financial_tracking.xlsx not found. Using sample data.")
        return create_sample_financial_data()
    except Exception as e:
        st.error(f"Error loading financial data: {e}")
        return None

def create_sample_financial_data():
    """Create sample financial data for demonstration"""
    initiatives = [
        'CM Sports Advancement Initiative-B',
        'Nagaland Cleanliness Performance Incentive for Local Bodies-B',
        'Nagaland Weavers Advancement & Market Formalisation-B'
    ]
    data = []
    for init in initiatives:
        data.append({
            'Initiative': init,
            'Component': 'Various',
            'Amount Released': np.random.uniform(1000000, 5000000),
            'Amount Received': np.random.uniform(1000000, 5000000),
            'Amount Utilised': np.random.uniform(500000, 3000000),
            'Physical Progress %': np.random.uniform(30, 80),
            'Financial Progress %': np.random.uniform(25, 75),
            'Timeline Status': np.random.choice(['On Track', 'At Risk', 'Delayed'], p=[0.6, 0.3, 0.1])
        })
    return pd.DataFrame(data)

# ============================================
# KPI CALCULATIONS
# ============================================

def calculate_financial_metrics(budget_df, financial_df):
    """Calculate overall financial metrics"""
    total_budget = budget_df['Allocation'].sum() if budget_df is not None else 0
    
    if financial_df is not None and not financial_df.empty:
        total_released = financial_df['Amount Released'].sum() if 'Amount Released' in financial_df.columns else 0
        total_utilised = financial_df['Amount Utilised'].sum() if 'Amount Utilised' in financial_df.columns else 0
    else:
        total_released = 0
        total_utilised = 0
    
    utilisation_efficiency = (total_utilised / total_released * 100) if total_released > 0 else 0
    
    return {
        'total_budget': total_budget,
        'total_released': total_released,
        'total_utilised': total_utilised,
        'utilisation_efficiency': utilisation_efficiency,
        'financial_progress': (total_utilised / total_budget * 100) if total_budget > 0 else 0
    }

def calculate_physical_progress(budget_df, financial_df):
    """Calculate physical progress based on KPIs"""
    # This would ideally come from actual achievement data
    # For demo, we'll calculate from financial progress
    if financial_df is not None and not financial_df.empty:
        avg_financial = financial_df['Financial Progress %'].mean() if 'Financial Progress %' in financial_df.columns else 0
        avg_physical = financial_df['Physical Progress %'].mean() if 'Physical Progress %' in financial_df.columns else 50
    else:
        avg_financial = 0
        avg_physical = 0
    
    return {
        'physical_progress': avg_physical,
        'financial_progress': avg_financial,
        'overall_progress': (avg_physical + avg_financial) / 2
    }

# ============================================
# VISUALIZATION FUNCTIONS
# ============================================

def create_budget_pie_chart(budget_df):
    """Create pie chart for budget distribution by initiative"""
    if budget_df is None or budget_df.empty:
        return None
    
    initiative_budget = budget_df.groupby('Initiative')['Allocation'].sum().reset_index()
    initiative_budget = initiative_budget.sort_values('Allocation', ascending=False).head(10)
    initiative_budget['Allocation_Cr'] = initiative_budget['Allocation'] / 10000000
    
    fig = px.pie(initiative_budget, 
                 values='Allocation', 
                 names='Initiative',
                 title='Budget Distribution by Initiative (Top 10)',
                 hole=0.4,
                 color_discrete_sequence=px.colors.qualitative.Set2)
    
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(height=500)
    return fig

def create_department_chart(budget_df):
    """Create bar chart for department budgets"""
    if budget_df is None or budget_df.empty:
        return None
    
    dept_budget = budget_df.groupby('Primary Department')['Allocation'].sum().reset_index()
    dept_budget = dept_budget.sort_values('Allocation', ascending=True)
    dept_budget['Allocation_Cr'] = dept_budget['Allocation'] / 10000000  # Convert to Crore
    
    fig = px.bar(dept_budget, 
                 y='Primary Department', 
                 x='Allocation_Cr',
                 title='Budget by Department (₹ Crore)',
                 orientation='h',
                 color='Allocation_Cr',
                 color_continuous_scale='Blues',
                 labels={'Allocation_Cr': 'Budget (₹ Crore)', 'Primary Department': 'Department'})
    
    # Force tick format to show "Cr" instead of "M"
    fig.update_layout(
        height=500,
        xaxis=dict(
            tickformat='.1f',  # Show 1 decimal place
            ticksuffix=' Cr'    # Add "Cr" suffix to every tick
        )
    )
    
    return fig

def create_sdg_funding_chart(budget_df):
    """Create chart showing funding by SDG"""
    if budget_df is None or budget_df.empty:
        return None
    
    sdg_funding = budget_df.groupby('Core SDG Indicator')['Allocation'].sum().reset_index()
    sdg_funding = sdg_funding[sdg_funding['Core SDG Indicator'].notna()]
    sdg_funding = sdg_funding[sdg_funding['Core SDG Indicator'] != '-']
    sdg_funding['Allocation_Cr'] = sdg_funding['Allocation'] / 10000000
    
    fig = px.bar(sdg_funding, 
                 x='Core SDG Indicator', 
                 y='Allocation_Cr',
                 title='Budget Allocation by SDG Goal (₹ Crore)',
                 color='Allocation_Cr',
                 color_continuous_scale='Viridis',
                 labels={'Allocation_Cr': 'Budget (₹ Crore)', 'Core SDG Indicator': 'SDG Goal'})
    
    fig.update_layout(
        height=450, 
        xaxis_tickangle=-45,
        yaxis=dict(
            tickformat='.1f',
            ticksuffix=' Cr'
        )
    )
    return fig
def create_financial_progress_gauge(metrics):
    """Create gauge chart for financial progress"""
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=metrics['financial_progress'],
        title={'text': "Financial Progress (%)"},
        domain={'x': [0, 1], 'y': [0, 1]},
        gauge={
            'axis': {'range': [0, 100]},
            'bar': {'color': "#2ecc71"},
            'steps': [
                {'range': [0, 30], 'color': "lightgray"},
                {'range': [30, 70], 'color': "gray"},
                {'range': [70, 100], 'color': "darkgray"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 90
            }
        }
    ))
    fig.update_layout(height=300)
    return fig

def create_initiative_table(budget_df, financial_df):
    """Create detailed initiatives table with SDG and progress"""
    if budget_df is None or budget_df.empty:
        return pd.DataFrame()
    
    # Aggregate by initiative
    initiative_summary = budget_df.groupby(['Primary Department', 'Initiative', 'Core SDG Indicator']).agg({
        'Allocation': 'sum',
        'Component': 'count'
    }).rename(columns={'Component': 'Component_Count'})
    
    initiative_summary = initiative_summary.reset_index()
    initiative_summary['Allocation_Cr'] = initiative_summary['Allocation'] / 10000000
    
    # Add progress if financial data available
    if financial_df is not None and not financial_df.empty:
        # Map progress to initiatives
        progress_map = financial_df.groupby('Initiative')['Financial Progress %'].mean().to_dict()
        initiative_summary['Progress %'] = initiative_summary['Initiative'].map(progress_map).fillna(0)
        
        # Add status based on progress
        def get_status(progress):
            if progress >= 70:
                return "🟢 On Track"
            elif progress >= 40:
                return "🟡 At Risk"
            else:
                return "🔴 Delayed"
        
        initiative_summary['Status'] = initiative_summary['Progress %'].apply(get_status)
    else:
        initiative_summary['Progress %'] = 0
        initiative_summary['Status'] = "⚪ Not Started"
    
    return initiative_summary

def create_progress_timeline(financial_df):
    """Create timeline chart for financial progress"""
    if financial_df is None or financial_df.empty:
        return None
    
    if 'Funds Utilisation Date' not in financial_df.columns:
        return None
    
    # Aggregate by date
    timeline_data = financial_df.groupby(pd.Grouper(key='Funds Utilisation Date', freq='ME')).agg({
        'Amount Utilised': 'sum'
    }).reset_index()
    
    # Convert to Crore
    timeline_data['Amount Utilised_Cr'] = timeline_data['Amount Utilised'] / 10000000
    
    timeline_data = timeline_data.dropna()
    
    if timeline_data.empty:
        return None
    
    fig = px.line(timeline_data, 
                  x='Funds Utilisation Date', 
                  y='Amount Utilised_Cr',
                  title='Monthly Funds Utilisation Trend (₹ Crore)',
                  markers=True,
                  labels={'Amount Utilised_Cr': 'Amount Utilised (₹ Crore)', 'Funds Utilisation Date': 'Month'})
    
    # Update y-axis to show Cr instead of M
    fig.update_layout(
        height=400,
        yaxis=dict(
            tickformat='.1f',
            ticksuffix=' Cr',
            title_font=dict(color='white', size=12),
            tickfont=dict(color='white', size=11)
        ),
        xaxis=dict(
            title_font=dict(color='white', size=12),
            tickfont=dict(color='white', size=11)
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(255,255,255,0.05)'
    )
    
    # Make line and markers stand out
    fig.update_traces(line_color='#a8ff78', line_width=3, marker_size=10, marker_color='#667eea')
    
    return fig

# ============================================
# MAIN DASHBOARD
# ============================================

def main():
# ============================================
# HEADER WITH IMAGE AT TOP RIGHT
# ============================================

# Create two columns: one for title, one for image
    col_title, col_image = st.columns([3, 1])

    with col_title:
        st.markdown("""
        <div style='text-align: center;'>
            <h1 style='margin-bottom: 0;'>📊 Nagaland State Budget Monitoring Dashboard</h1>
            <h3 style='margin-top: 0; color: #a8ff78;'>(Financial Year 2026-27)</h3>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("##### ***Monitored by CM Office***")

    with col_image:
# Load and display the image
        from PIL import Image
        import os
        import base64
    
        image_path = "CM PIC.png"
    
        if os.path.exists(image_path):
            with open(image_path, "rb") as img_file:
                img_data = base64.b64encode(img_file.read()).decode()
            
            st.markdown(f"""
            <div style="display: flex; justify-content: flex-end;">
                <div style="margin-left: auto; text-align: right;">
                    <img src="data:image/png;base64,{img_data}" 
                         style="width: 150px; height: auto; border-radius: 20px; 
                            border: 2px solid #667eea;">
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.warning("⚠️ CM image not found")

    st.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    st.markdown("---")

    
    # Load data
    with st.spinner("Loading data..."):
        budget_df = load_budget_data()
        financial_df = load_financial_data()
    
    if budget_df is None:
        st.stop()
    
    # Calculate metrics
    financial_metrics = calculate_financial_metrics(budget_df, financial_df)
    progress_metrics = calculate_physical_progress(budget_df, financial_df)
    
    # ============================================
    # TOP METRICS ROW - IMPROVED VISIBILITY
    # ============================================
    st.subheader("📈 Key Performance Indicators")

    # Create a more attractive metrics row with custom styling
    col1, col2, col3, col4, col5 = st.columns(5)

    # Custom CSS for better visibility
    st.markdown("""
    <style>
        .metric-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 15px;
            border-radius: 15px;
            text-align: center;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
            transition: transform 0.3s;
        }
        .metric-card:hover {
            transform: translateY(-5px);
        }
        .metric-label {
            color: white;
            font-size: 14px;
            font-weight: 500;
            margin-bottom: 10px;
            opacity: 0.9;
        }
        .metric-value {
            color: white;
            font-size: 28px;
            font-weight: bold;
            margin-bottom: 5px;
        }
        .metric-delta {
            color: #a8ff78;
            font-size: 12px;
            font-weight: 500;
        }
        .card-1 { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }
        .card-2 { background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); }
        .card-3 { background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); }
        .card-4 { background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%); }
        .card-5 { background: linear-gradient(135deg, #fa709a 0%, #fee140 100%); }
    </style>
    """, unsafe_allow_html=True)

    # Calculate metrics
    total_budget_cr = financial_metrics['total_budget'] / 10000000
    total_released_cr = financial_metrics['total_released'] / 10000000
    total_utilised_cr = financial_metrics['total_utilised'] / 10000000
    util_efficiency = financial_metrics['utilisation_efficiency']
    financial_progress = financial_metrics['financial_progress']

    with col1:
        st.markdown(f"""
        <div class="metric-card card-1">
            <div class="metric-label"> ₹ Total Budget</div>
            <div class="metric-value">₹{total_budget_cr:.1f} Cr</div>
            <div class="metric-delta">FY 2026-27</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="metric-card card-2">
            <div class="metric-label">📤 Total Released</div>
            <div class="metric-value">₹{total_released_cr:.1f} Cr</div>
            <div class="metric-delta">{ (total_released_cr/total_budget_cr*100) if total_budget_cr > 0 else 0:.1f}% of budget</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="metric-card card-3">
            <div class="metric-label">✅ Total Utilised</div>
            <div class="metric-value">₹{total_utilised_cr:.1f} Cr</div>
            <div class="metric-delta">{ (total_utilised_cr/total_released_cr*100) if total_released_cr > 0 else 0:.1f}% of released</div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        # Color based on efficiency
        efficiency_color = "#a8ff78" if util_efficiency >= 70 else "#ffeb3b" if util_efficiency >= 40 else "#ff6b6b"
        st.markdown(f"""
        <div class="metric-card card-4">
            <div class="metric-label">⚡ Utilisation Efficiency</div>
            <div class="metric-value" style="color: {efficiency_color};">{util_efficiency:.1f}%</div>
            <div class="metric-delta">Target: 80%</div>
        </div>
        """, unsafe_allow_html=True)

    with col5:
        # Color based on progress
        progress_color = "#a8ff78" if financial_progress >= 70 else "#ffeb3b" if financial_progress >= 40 else "#ff6b6b"
        st.markdown(f"""
        <div class="metric-card card-5">
            <div class="metric-label">₹ Financial Progress</div>
            <div class="metric-value" style="color: {progress_color};">{financial_progress:.1f}%</div>
            <div class="metric-delta">Overall completion</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    
    # ============================================
    # PROGRESS ROW
    # ============================================
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("💰 Financial Progress")
        financial_gauge = create_financial_progress_gauge(financial_metrics)
        st.plotly_chart(financial_gauge, use_container_width=True)
    
    with col2:
        st.subheader("📊 Physical Progress")
        # Physical progress gauge
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=progress_metrics['physical_progress'],
            title={'text': "Physical Progress (%)"},
            gauge={
                'axis': {'range': [0, 100]},
                'bar': {'color': "#3498db"},
                'steps': [
                    {'range': [0, 30], 'color': "lightgray"},
                    {'range': [30, 70], 'color': "gray"},
                    {'range': [70, 100], 'color': "darkgray"}
                ]
            }
        ))
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # ============================================
    # CHARTS ROW
    # ============================================
    col1, col2 = st.columns(2)
    
    with col1:
        budget_pie = create_budget_pie_chart(budget_df)
        if budget_pie:
            st.plotly_chart(budget_pie, use_container_width=True)
    
    with col2:
        dept_chart = create_department_chart(budget_df)
        if dept_chart:
            st.plotly_chart(dept_chart, use_container_width=True)
    
    # ============================================
    # SDG FUNDING
    # ============================================
    st.subheader("🎯 SDG Alignment & Funding")
    col1, col2 = st.columns([2, 1])
    
    with col1:
        sdg_chart = create_sdg_funding_chart(budget_df)
        if sdg_chart:
            st.plotly_chart(sdg_chart, use_container_width=True)
    
    with col2:
        # SDG Summary Cards
        if budget_df is not None:
            sdg_summary = budget_df.groupby('Core SDG Indicator')['Allocation'].sum().reset_index()
            sdg_summary = sdg_summary[sdg_summary['Core SDG Indicator'].notna()]
            sdg_summary = sdg_summary[sdg_summary['Core SDG Indicator'] != '-']
            
            for _, row in sdg_summary.iterrows():
                st.markdown(f"""
                <div class="card">
                    <strong>{row['Core SDG Indicator']}</strong><br>
                    Budget: ₹{row['Allocation']/10000000:.1f} Cr
                </div>
                """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # ============================================
    # INITIATIVES TABLE
    # ============================================
    st.subheader("📋 Initiatives & SDG Linkage")
    
    initiative_table = create_initiative_table(budget_df, financial_df)
    
    if not initiative_table.empty:
        # Add filters
        col1, col2, col3 = st.columns(3)
        with col1:
            dept_filter = st.multiselect(
                "Filter by Department",
                options=initiative_table['Primary Department'].unique(),
                default=[]
            )
        with col2:
            sdg_filter = st.multiselect(
                "Filter by SDG",
                options=initiative_table['Core SDG Indicator'].unique(),
                default=[]
            )
        with col3:
            status_filter = st.multiselect(
                "Filter by Status",
                options=initiative_table['Status'].unique(),
                default=[]
            )
        
        # Apply filters
        filtered_df = initiative_table.copy()
        if dept_filter:
            filtered_df = filtered_df[filtered_df['Primary Department'].isin(dept_filter)]
        if sdg_filter:
            filtered_df = filtered_df[filtered_df['Core SDG Indicator'].isin(sdg_filter)]
        if status_filter:
            filtered_df = filtered_df[filtered_df['Status'].isin(status_filter)]
        
        # Display table
        display_cols = ['Primary Department', 'Initiative', 'Allocation_Cr', 'Core SDG Indicator', 'Progress %', 'Status']
        st.dataframe(
            filtered_df[display_cols].rename(columns={
                'Primary Department': 'Department',
                'Allocation_Cr': 'Budget (₹ Cr)',
                'Core SDG Indicator': 'SDG Goal',
                'Progress %': 'Progress'
            }),
            use_container_width=True,
            hide_index=True
        )
    
    st.markdown("---")
    
    # ============================================
    # TIMELINE & ALERTS
    # ============================================
    col1, col2 = st.columns(2)
    
    with col1:
        timeline = create_progress_timeline(financial_df)
        if timeline:
            st.plotly_chart(timeline, use_container_width=True)
    
    with col2:
        st.subheader("Alerts & Recommendations")
        
        # Identify at-risk initiatives
        at_risk = initiative_table[initiative_table['Progress %'] < 40] if not initiative_table.empty else pd.DataFrame()
        
        if not at_risk.empty:
            st.warning(f"🔴 {len(at_risk)} initiatives are at risk (Progress < 40%)")
            for _, row in at_risk.head(5).iterrows():
                st.write(f"• **{row['Initiative']}** - Progress: {row['Progress %']:.0f}%")
        else:
            st.success("✅ All initiatives are on track!")
        
        # Poor M&E indicators
        if budget_df is not None:
            poor_me = budget_df[budget_df['Monitoring and Performance Indicators'].isna() | 
                                (budget_df['Monitoring and Performance Indicators'] == '-') |
                                (budget_df['Monitoring and Performance Indicators'] == '')]
            
            if not poor_me.empty:
                st.info(f"📋 {len(poor_me)} components have undefined M&E indicators")
        
        st.markdown("---")
        st.caption("**Recommendations:**\n"
                   "• Prioritize M&E for high-budget initiatives\n"
                   "• Define SMART indicators for all components\n"
                   "• Conduct quarterly reviews for at-risk initiatives")
    
    # ============================================
    # EXPORT OPTIONS
    # ============================================
    st.markdown("---")
    st.subheader("📎 Export Options")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📊 Export Dashboard as HTML"):
            st.info("Use browser 'Save as' or print to save as PDF")
    
    with col2:
        if st.button("📄 Export Data as CSV"):
            if not initiative_table.empty:
                csv = initiative_table.to_csv(index=False)
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name=f"me_dashboard_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv"
                )
    
    with col3:
        st.caption(f"Data refreshed: {datetime.now().strftime('%Y-%m-%d %H:%M')}")

if __name__ == "__main__":
    main()
