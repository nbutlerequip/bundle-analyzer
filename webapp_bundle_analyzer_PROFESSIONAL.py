"""
Professional Bundle Analyzer - Enterprise Edition
Supersession-Enhanced Bundle Analysis Tool
Southeastern Equipment Co. | v2.9
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime
import io

# ==============================================================================
# PAGE CONFIGURATION
# ==============================================================================
st.set_page_config(
    page_title="SE Bundle Analyzer Pro | Southeastern Equipment",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'About': "# SE Bundle Analyzer Pro\nProfessional Bundle Analysis & Revenue Optimization Platform"
    }
)

# ==============================================================================
# PROFESSIONAL STYLING
# ==============================================================================
st.markdown("""
<style>
    /* Main Theme Colors */
    :root {
        --primary-color: #1E3A8A;
        --secondary-color: #3B82F6;
        --accent-color: #10B981;
        --warning-color: #F59E0B;
        --danger-color: #EF4444;
        --dark-bg: #0F172A;
        --light-bg: #F8FAFC;
    }
    
    /* Remove default Streamlit padding */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1400px;
    }
    
    /* Professional Header */
    .main-header {
        background: linear-gradient(135deg, #1E3A8A 0%, #3B82F6 100%);
        padding: 2.5rem 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(30, 58, 138, 0.3);
    }
    
    .main-header h1 {
        font-size: 2.8rem;
        font-weight: 700;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
    }
    
    .main-header p {
        font-size: 1.1rem;
        margin-top: 0.5rem;
        opacity: 0.95;
    }
    
    .company-badge {
        display: inline-block;
        background: rgba(255,255,255,0.2);
        padding: 0.3rem 1rem;
        border-radius: 20px;
        font-size: 0.9rem;
        margin-top: 0.5rem;
    }
    
    /* Professional Metric Cards */
    .metric-card {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.07);
        border-left: 4px solid #3B82F6;
        transition: all 0.3s ease;
        height: 100%;
    }
    
    .metric-card:hover {
        box-shadow: 0 8px 15px rgba(0, 0, 0, 0.1);
        transform: translateY(-2px);
    }
    
    .metric-icon {
        font-size: 2rem;
        margin-bottom: 0.5rem;
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1E3A8A;
        line-height: 1;
        margin: 0.5rem 0;
    }
    
    .metric-label {
        font-size: 0.95rem;
        color: #64748B;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .metric-change {
        font-size: 0.85rem;
        color: #10B981;
        margin-top: 0.5rem;
    }
    
    /* Professional Tab Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #F1F5F9;
        padding: 0.5rem;
        border-radius: 10px;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 3.5rem;
        padding: 0 2rem;
        background-color: white;
        border-radius: 8px;
        font-weight: 600;
        font-size: 1rem;
        color: #475569;
        border: 2px solid transparent;
        transition: all 0.3s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background-color: #E0F2FE;
        color: #1E3A8A;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #1E3A8A 0%, #3B82F6 100%) !important;
        color: white !important;
        border-color: #1E3A8A !important;
    }
    
    /* Professional Data Tables */
    .dataframe {
        border: none !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        border-radius: 8px;
        overflow: hidden;
    }
    
    .dataframe thead tr th {
        background: linear-gradient(135deg, #1E3A8A 0%, #3B82F6 100%) !important;
        color: white !important;
        font-weight: 600 !important;
        padding: 1rem !important;
        border: none !important;
    }
    
    .dataframe tbody tr:hover {
        background-color: #F0F9FF !important;
    }
    
    /* Professional Cards */
    .info-card {
        background: linear-gradient(135deg, #EFF6FF 0%, #DBEAFE 100%);
        border-left: 4px solid #3B82F6;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    
    .success-card {
        background: linear-gradient(135deg, #ECFDF5 0%, #D1FAE5 100%);
        border-left: 4px solid #10B981;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    
    .warning-card {
        background: linear-gradient(135deg, #FFFBEB 0%, #FEF3C7 100%);
        border-left: 4px solid #F59E0B;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    
    /* Professional Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #1E3A8A 0%, #3B82F6 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        font-size: 1rem;
        font-weight: 600;
        border-radius: 8px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px rgba(59, 130, 246, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(59, 130, 246, 0.4);
    }
    
    /* Professional Download Buttons */
    .stDownloadButton > button {
        background: linear-gradient(135deg, #10B981 0%, #059669 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        font-size: 1rem;
        font-weight: 600;
        border-radius: 8px;
        transition: all 0.3s ease;
    }
    
    .stDownloadButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(16, 185, 129, 0.4);
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #F8FAFC 0%, #EFF6FF 100%);
        border-right: 1px solid #E2E8F0;
    }
    
    [data-testid="stSidebar"] .element-container {
        padding: 0.5rem 0;
    }
    
    /* Professional Confidence Badges */
    .conf-perfect {
        background: linear-gradient(135deg, #10B981 0%, #059669 100%);
        color: white;
        padding: 0.4rem 1rem;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.9rem;
        display: inline-block;
        box-shadow: 0 2px 4px rgba(16, 185, 129, 0.3);
    }
    
    .conf-high {
        background: linear-gradient(135deg, #3B82F6 0%, #2563EB 100%);
        color: white;
        padding: 0.4rem 1rem;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.9rem;
        display: inline-block;
        box-shadow: 0 2px 4px rgba(59, 130, 246, 0.3);
    }
    
    .conf-medium {
        background: linear-gradient(135deg, #F59E0B 0%, #D97706 100%);
        color: white;
        padding: 0.4rem 1rem;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.9rem;
        display: inline-block;
        box-shadow: 0 2px 4px rgba(245, 158, 11, 0.3);
    }
    
    .conf-low {
        background: linear-gradient(135deg, #94A3B8 0%, #64748B 100%);
        color: white;
        padding: 0.4rem 1rem;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.9rem;
        display: inline-block;
        box-shadow: 0 2px 4px rgba(148, 163, 184, 0.3);
    }
    
    /* Loading Animation */
    .stSpinner > div {
        border-top-color: #3B82F6 !important;
    }
    
    /* Professional Section Headers */
    .section-header {
        font-size: 1.8rem;
        font-weight: 700;
        color: #1E3A8A;
        margin: 2rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 3px solid #3B82F6;
    }
    
    /* Bundle Card Styling */
    .bundle-card {
        background: white;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 0.75rem 0;
        border: 2px solid #E2E8F0;
        transition: all 0.3s ease;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    
    .bundle-card:hover {
        border-color: #3B82F6;
        box-shadow: 0 6px 12px rgba(59, 130, 246, 0.15);
        transform: translateY(-2px);
    }
    
    .bundle-parts {
        font-size: 1.2rem;
        font-weight: 600;
        color: #1E3A8A;
        margin-bottom: 0.5rem;
    }
    
    .bundle-stats {
        color: #64748B;
        font-size: 0.95rem;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 2rem 0;
        margin-top: 3rem;
        border-top: 2px solid #E2E8F0;
        color: #64748B;
    }
    
    /* Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Scrollbar Styling */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: #F1F5F9;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #CBD5E1;
        border-radius: 5px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #94A3B8;
    }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# INITIALIZE SESSION STATE
# ==============================================================================
if 'bundles_df' not in st.session_state:
    st.session_state.bundles_df = None
if 'supersession_df' not in st.session_state:
    st.session_state.supersession_df = None
if 'search_history' not in st.session_state:
    st.session_state.search_history = []
if 'analysis_run' not in st.session_state:
    st.session_state.analysis_run = False

# ==============================================================================
# HELPER FUNCTIONS
# ==============================================================================

@st.cache_data
def load_data_from_repo():
    """Load pre-uploaded data from GitHub repository"""
    try:
        # Try to load the bundle analysis file
        df = pd.read_csv('data/COMPLETE_BUNDLE_ANALYSIS_20251029_084720.csv')
        return df
    except FileNotFoundError:
        try:
            # Try alternative filename
            df = pd.read_csv('data/Bundle_Analysis_20250926.xlsx')
            return df
        except:
            return None
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return None

def get_confidence_badge(confidence):
    """Return HTML for confidence badge"""
    if confidence >= 1.0:
        return '<span class="conf-perfect">🌟 100%</span>'
    elif confidence >= 0.7:
        return f'<span class="conf-high">✓ {confidence:.0%}</span>'
    elif confidence >= 0.4:
        return f'<span class="conf-medium">○ {confidence:.0%}</span>'
    else:
        return f'<span class="conf-low">◌ {confidence:.0%}</span>'

def format_currency(value):
    """Format value as currency"""
    return f"${value:,.0f}"

def format_number(value):
    """Format large numbers with K, M suffixes"""
    if value >= 1_000_000:
        return f"{value/1_000_000:.1f}M"
    elif value >= 1_000:
        return f"{value/1_000:.1f}K"
    else:
        return f"{value:.0f}"

def create_metric_card(icon, value, label, change=None):
    """Create a professional metric card"""
    change_html = f'<div class="metric-change">↑ {change}</div>' if change else ''
    return f"""
    <div class="metric-card">
        <div class="metric-icon">{icon}</div>
        <div class="metric-value">{value}</div>
        <div class="metric-label">{label}</div>
        {change_html}
    </div>
    """

# ==============================================================================
# PROFESSIONAL HEADER
# ==============================================================================
st.markdown("""
<div class="main-header">
    <h1>🚀 SE Bundle Analyzer Pro</h1>
    <p>Supersession-Enhanced Bundle Analysis & Revenue Optimization Platform</p>
    <div class="company-badge">Southeastern Equipment Co. | v2.9</div>
</div>
""", unsafe_allow_html=True)

# ==============================================================================
# SIDEBAR CONFIGURATION
# ==============================================================================
with st.sidebar:
    st.markdown("### ⚙️ Analysis Configuration")
    
    # Auto-load data section
    st.markdown("#### 📊 Data Loading")
    
    if st.session_state.bundles_df is None:
        if st.button("🚀 Load Bundle Data", type="primary", use_container_width=True):
            with st.spinner("Loading bundle analysis data..."):
                st.session_state.bundles_df = load_data_from_repo()
                if st.session_state.bundles_df is not None:
                    # Convert percentage columns to 0-1 scale if needed
                    if 'Enhanced_Confidence_%' in st.session_state.bundles_df.columns:
                        st.session_state.bundles_df['Confidence_Score'] = (
                            st.session_state.bundles_df['Enhanced_Confidence_%'] / 100
                        )
                    st.session_state.analysis_run = True
                    st.success(f"✅ Loaded {len(st.session_state.bundles_df):,} bundles!")
                    st.rerun()
                else:
                    st.error("⚠️ Could not load data. Please upload files manually.")
    else:
        st.success(f"✅ {len(st.session_state.bundles_df):,} bundles loaded")
        if st.button("🔄 Reload Data", use_container_width=True):
            st.session_state.bundles_df = None
            st.session_state.analysis_run = False
            st.rerun()
    
    st.markdown("---")
    
    # Manual upload option
    with st.expander("📁 Manual Upload (Optional)"):
        uploaded_file = st.file_uploader(
            "Upload Bundle Analysis CSV",
            type=['csv'],
            help="Upload if auto-load doesn't work"
        )
        
        if uploaded_file:
            try:
                df = pd.read_csv(uploaded_file)
                if 'Enhanced_Confidence_%' in df.columns:
                    df['Confidence_Score'] = df['Enhanced_Confidence_%'] / 100
                st.session_state.bundles_df = df
                st.success("✅ File uploaded successfully!")
                st.rerun()
            except Exception as e:
                st.error(f"Error: {str(e)}")
    
    st.markdown("---")
    
    # Filters (only show if data is loaded)
    if st.session_state.bundles_df is not None:
        st.markdown("#### 🔍 Analysis Filters")
        
        min_confidence = st.slider(
            "Minimum Confidence",
            0.0, 1.0, 0.4, 0.05,
            help="Filter bundles by minimum confidence score"
        )
        
        min_customers = st.number_input(
            "Minimum Customers",
            min_value=1,
            value=10,
            step=5,
            help="Filter bundles by minimum customer count"
        )
        
        # Apply filters
        df_filtered = st.session_state.bundles_df[
            (st.session_state.bundles_df['Confidence_Score'] >= min_confidence) &
            (st.session_state.bundles_df['Customer_Count'] >= min_customers)
        ].copy()
        
        st.info(f"📊 {len(df_filtered):,} bundles match filters")
        
        st.markdown("---")
        
        # Show supersession filter
        if 'Has_Supersession' in st.session_state.bundles_df.columns:
            show_supersession_only = st.checkbox(
                "🔗 Supersession Enhanced Only",
                help="Show only bundles with supersession data"
            )
            
            if show_supersession_only:
                df_filtered = df_filtered[df_filtered['Has_Supersession'] == 'Yes']
                st.info(f"🔗 {len(df_filtered):,} with supersession")
    else:
        df_filtered = None
        st.info("👆 Load data to enable filters")
    
    st.markdown("---")
    st.markdown("### 📖 Quick Guide")
    st.markdown("""
    **Steps:**
    1. Click "Load Bundle Data"
    2. Adjust filters if needed
    3. Explore the dashboard
    4. Export your results
    
    **Need Help?**
    Check the documentation in your GitHub repo.
    """)

# ==============================================================================
# MAIN CONTENT
# ==============================================================================

if st.session_state.bundles_df is None:
    # Welcome screen with professional design
    st.markdown('<div class="info-card">', unsafe_allow_html=True)
    st.markdown("### 👋 Welcome to SE Bundle Analyzer Pro")
    st.markdown("""
    This professional platform helps you analyze and optimize your parts bundling strategy using
    advanced supersession intelligence and customer purchasing patterns.
    
    **✨ Key Features:**
    - 📊 **Interactive Dashboards** - Visual insights into bundling opportunities
    - 🔍 **Smart Search** - Find bundles by part number instantly
    - 📈 **Revenue Projections** - Quantify your opportunities
    - 🔗 **Supersession Integration** - 22+ years of historical intelligence
    - 📥 **Professional Reports** - Export presentation-ready insights
    
    **🚀 Get Started:**
    Click the **"Load Bundle Data"** button in the sidebar to begin your analysis.
    """)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Show data requirements
    with st.expander("📋 Data Requirements & Format"):
        st.markdown("""
        **Required Columns:**
        - `Part_1` - First part number
        - `Part_2` - Second part number
        - `Customer_Count` - Number of customers
        - `Enhanced_Confidence_%` or `Confidence_Score` - Confidence percentage/score
        
        **Optional Columns:**
        - `Has_Supersession` - Supersession flag
        - `Annual_Revenue_Potential_$` - Revenue estimate
        - `Part1_Predecessors`, `Part2_Predecessors` - Historical data
        """)

else:
    # Main analysis interface
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Executive Dashboard",
        "🔍 Search & Analyze",
        "🏆 Top Opportunities",
        "🔗 Supersession Intel",
        "📥 Reports & Export"
    ])
    
    # ==============================================================================
    # TAB 1: EXECUTIVE DASHBOARD
    # ==============================================================================
    with tab1:
        st.markdown('<h2 class="section-header">📊 Executive Dashboard</h2>', unsafe_allow_html=True)
        
        # Key metrics row
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_bundles = len(df_filtered)
            st.markdown(
                create_metric_card("📦", f"{total_bundles:,}", "Total Bundles"),
                unsafe_allow_html=True
            )
        
        with col2:
            total_customers = df_filtered['Customer_Count'].sum()
            st.markdown(
                create_metric_card("👥", format_number(total_customers), "Customer Base"),
                unsafe_allow_html=True
            )
        
        with col3:
            avg_conf = df_filtered['Confidence_Score'].mean()
            st.markdown(
                create_metric_card("📈", f"{avg_conf:.0%}", "Avg Confidence"),
                unsafe_allow_html=True
            )
        
        with col4:
            if 'Annual_Revenue_Potential_$' in df_filtered.columns:
                total_revenue = df_filtered['Annual_Revenue_Potential_$'].sum()
                st.markdown(
                    create_metric_card("💰", format_currency(total_revenue), "Revenue Potential"),
                    unsafe_allow_html=True
                )
            else:
                high_conf = len(df_filtered[df_filtered['Confidence_Score'] >= 0.7])
                st.markdown(
                    create_metric_card("🌟", f"{high_conf:,}", "High Confidence"),
                    unsafe_allow_html=True
                )
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Charts row
        col_left, col_right = st.columns(2)
        
        with col_left:
            st.markdown("#### Confidence Distribution")
            
            # Create bins for confidence
            df_filtered['Confidence_Tier'] = pd.cut(
                df_filtered['Confidence_Score'],
                bins=[0, 0.4, 0.5, 0.7, 1.0],
                labels=['<40%', '40-50%', '50-70%', '70-100%']
            )
            
            tier_counts = df_filtered['Confidence_Tier'].value_counts().sort_index()
            
            fig = go.Figure(data=[
                go.Bar(
                    x=tier_counts.index,
                    y=tier_counts.values,
                    marker=dict(
                        color=['#94A3B8', '#F59E0B', '#3B82F6', '#10B981'],
                        line=dict(color='white', width=2)
                    ),
                    text=tier_counts.values,
                    textposition='auto',
                    textfont=dict(size=14, color='white', family='Arial Black')
                )
            ])
            
            fig.update_layout(
                height=350,
                margin=dict(l=20, r=20, t=20, b=20),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                xaxis=dict(title="Confidence Tier", titlefont=dict(size=14)),
                yaxis=dict(title="Number of Bundles", titlefont=dict(size=14)),
                font=dict(family="Arial", size=12)
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        with col_right:
            st.markdown("#### Revenue by Confidence Tier")
            
            if 'Annual_Revenue_Potential_$' in df_filtered.columns:
                revenue_by_tier = df_filtered.groupby('Confidence_Tier')['Annual_Revenue_Potential_$'].sum().sort_index()
                
                fig = go.Figure(data=[
                    go.Bar(
                        x=revenue_by_tier.index,
                        y=revenue_by_tier.values,
                        marker=dict(
                            color=['#94A3B8', '#F59E0B', '#3B82F6', '#10B981'],
                            line=dict(color='white', width=2)
                        ),
                        text=[format_currency(v) for v in revenue_by_tier.values],
                        textposition='auto',
                        textfont=dict(size=12, color='white', family='Arial Black')
                    )
                ])
                
                fig.update_layout(
                    height=350,
                    margin=dict(l=20, r=20, t=20, b=20),
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    xaxis=dict(title="Confidence Tier", titlefont=dict(size=14)),
                    yaxis=dict(title="Revenue Potential ($)", titlefont=dict(size=14)),
                    font=dict(family="Arial", size=12)
                )
                
                st.plotly_chart(fig, use_container_width=True)
            else:
                # Customer count by tier
                customers_by_tier = df_filtered.groupby('Confidence_Tier')['Customer_Count'].sum().sort_index()
                
                fig = go.Figure(data=[
                    go.Bar(
                        x=customers_by_tier.index,
                        y=customers_by_tier.values,
                        marker=dict(
                            color=['#94A3B8', '#F59E0B', '#3B82F6', '#10B981'],
                            line=dict(color='white', width=2)
                        ),
                        text=customers_by_tier.values,
                        textposition='auto',
                        textfont=dict(size=14, color='white', family='Arial Black')
                    )
                ])
                
                fig.update_layout(
                    height=350,
                    margin=dict(l=20, r=20, t=20, b=20),
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    xaxis=dict(title="Confidence Tier", titlefont=dict(size=14)),
                    yaxis=dict(title="Total Customers", titlefont=dict(size=14)),
                    font=dict(family="Arial", size=12)
                )
                
                st.plotly_chart(fig, use_container_width=True)
        
        # Top 10 bundles preview
        st.markdown('<h3 class="section-header">🏆 Top 10 High-Value Bundles</h3>', unsafe_allow_html=True)
        
        top_10 = df_filtered.nlargest(10, 'Customer_Count')
        
        for idx, row in top_10.iterrows():
            conf_badge = get_confidence_badge(row['Confidence_Score'])
            supersession = " 🔗" if row.get('Has_Supersession') == 'Yes' else ""
            
            st.markdown(f"""
            <div class="bundle-card">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div class="bundle-parts">
                        <strong>{row['Part_1']}</strong> + <strong>{row['Part_2']}</strong>{supersession}
                    </div>
                    <div>{conf_badge}</div>
                </div>
                <div class="bundle-stats">
                    👥 {row['Customer_Count']:,} customers
                    {f" | 💰 {format_currency(row['Annual_Revenue_Potential_$'])}" if 'Annual_Revenue_Potential_$' in row else ""}
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # ==============================================================================
    # TAB 2: SEARCH & ANALYZE
    # ==============================================================================
    with tab2:
        st.markdown('<h2 class="section-header">🔍 Search & Analyze Bundles</h2>', unsafe_allow_html=True)
        
        search_col1, search_col2 = st.columns([3, 1])
        
        with search_col1:
            search_term = st.text_input(
                "🔎 Search by Part Number",
                placeholder="Enter part number (e.g., 87682999)",
                help="Search for bundles containing this part"
            )
        
        with search_col2:
            st.markdown("<br>", unsafe_allow_html=True)
            search_button = st.button("🔍 Search", type="primary", use_container_width=True)
        
        if search_button and search_term:
            # Perform search
            search_results = df_filtered[
                (df_filtered['Part_1'].astype(str).str.contains(search_term, case=False)) |
                (df_filtered['Part_2'].astype(str).str.contains(search_term, case=False))
            ].sort_values('Customer_Count', ascending=False)
            
            if len(search_results) > 0:
                st.markdown(f'<div class="success-card">✅ Found <strong>{len(search_results):,}</strong> bundles containing "{search_term}"</div>', unsafe_allow_html=True)
                
                # Metrics
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Bundles Found", f"{len(search_results):,}")
                with col2:
                    st.metric("Total Customers", f"{search_results['Customer_Count'].sum():,}")
                with col3:
                    st.metric("Avg Confidence", f"{search_results['Confidence_Score'].mean():.0%}")
                
                st.markdown("---")
                
                # Display results
                for idx, row in search_results.head(20).iterrows():
                    conf_badge = get_confidence_badge(row['Confidence_Score'])
                    supersession = " 🔗" if row.get('Has_Supersession') == 'Yes' else ""
                    
                    st.markdown(f"""
                    <div class="bundle-card">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <div class="bundle-parts">
                                <strong>{row['Part_1']}</strong> + <strong>{row['Part_2']}</strong>{supersession}
                            </div>
                            <div>{conf_badge}</div>
                        </div>
                        <div class="bundle-stats">
                            👥 {row['Customer_Count']:,} customers
                            {f" | 💰 {format_currency(row['Annual_Revenue_Potential_$'])}" if 'Annual_Revenue_Potential_$' in row else ""}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Export option
                st.markdown("---")
                csv = search_results.to_csv(index=False)
                st.download_button(
                    label="📥 Download Search Results",
                    data=csv,
                    file_name=f"bundle_search_{search_term}_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv"
                )
            else:
                st.markdown(f'<div class="warning-card">⚠️ No bundles found containing "{search_term}"</div>', unsafe_allow_html=True)
    
    # ==============================================================================
    # TAB 3: TOP OPPORTUNITIES
    # ==============================================================================
    with tab3:
        st.markdown('<h2 class="section-header">🏆 Top Bundle Opportunities</h2>', unsafe_allow_html=True)
        
        col1, col2 = st.columns([1, 3])
        with col1:
            top_n = st.selectbox("Show Top", [10, 20, 50, 100], index=1)
        with col2:
            sort_by = st.radio(
                "Sort By",
                ['Customer_Count', 'Confidence_Score', 'Annual_Revenue_Potential_$'] if 'Annual_Revenue_Potential_$' in df_filtered.columns else ['Customer_Count', 'Confidence_Score'],
                horizontal=True,
                format_func=lambda x: {'Customer_Count': 'Customer Count', 'Confidence_Score': 'Confidence', 'Annual_Revenue_Potential_$': 'Revenue'}.get(x, x)
            )
        
        top_bundles = df_filtered.nlargest(top_n, sort_by)
        
        # Create professional table
        display_df = top_bundles[['Part_1', 'Part_2', 'Customer_Count', 'Confidence_Score']].copy()
        display_df['Confidence_Score'] = display_df['Confidence_Score'].apply(lambda x: f"{x:.0%}")
        
        if 'Has_Supersession' in top_bundles.columns:
            display_df['Supersession'] = top_bundles['Has_Supersession'].apply(lambda x: '✓' if x == 'Yes' else '')
        
        if 'Annual_Revenue_Potential_$' in top_bundles.columns:
            display_df['Revenue'] = top_bundles['Annual_Revenue_Potential_$'].apply(format_currency)
        
        st.dataframe(display_df, use_container_width=True, hide_index=True, height=600)
        
        # Export
        st.markdown("---")
        csv = top_bundles.to_csv(index=False)
        st.download_button(
            label=f"📥 Download Top {top_n} Bundles",
            data=csv,
            file_name=f"top_{top_n}_bundles_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv",
            type="primary"
        )
    
    # ==============================================================================
    # TAB 4: SUPERSESSION INTELLIGENCE
    # ==============================================================================
    with tab4:
        st.markdown('<h2 class="section-header">🔗 Supersession Intelligence</h2>', unsafe_allow_html=True)
        
        if 'Has_Supersession' in df_filtered.columns:
            supersession_bundles = df_filtered[df_filtered['Has_Supersession'] == 'Yes']
            
            if len(supersession_bundles) > 0:
                # Metrics
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.markdown(
                        create_metric_card(
                            "🔗",
                            f"{len(supersession_bundles):,}",
                            "Enhanced Bundles",
                            f"{len(supersession_bundles)/len(df_filtered)*100:.1f}%"
                        ),
                        unsafe_allow_html=True
                    )
                
                with col2:
                    if 'Confidence_Improvement_%' in supersession_bundles.columns:
                        avg_improvement = supersession_bundles['Confidence_Improvement_%'].mean()
                        st.markdown(
                            create_metric_card("📈", f"+{avg_improvement:.1f}%", "Avg Boost"),
                            unsafe_allow_html=True
                        )
                
                with col3:
                    enhanced_customers = supersession_bundles['Customer_Count'].sum()
                    st.markdown(
                        create_metric_card("👥", format_number(enhanced_customers), "Customer Base"),
                        unsafe_allow_html=True
                    )
                
                with col4:
                    if 'Total_Predecessors' in supersession_bundles.columns:
                        total_predecessors = supersession_bundles['Total_Predecessors'].sum()
                        st.markdown(
                            create_metric_card("📜", format_number(total_predecessors), "Historical Parts"),
                            unsafe_allow_html=True
                        )
                
                st.markdown("<br>", unsafe_allow_html=True)
                
                # Top improved bundles
                st.markdown("#### 🚀 Top 20 Most Improved Bundles")
                
                if 'Confidence_Improvement_%' in supersession_bundles.columns:
                    top_improved = supersession_bundles.nlargest(20, 'Confidence_Improvement_%')
                    
                    for idx, row in top_improved.iterrows():
                        conf_badge = get_confidence_badge(row['Confidence_Score'])
                        improvement = row['Confidence_Improvement_%']
                        
                        st.markdown(f"""
                        <div class="bundle-card">
                            <div style="display: flex; justify-content: space-between; align-items: center;">
                                <div class="bundle-parts">
                                    <strong>{row['Part_1']}</strong> + <strong>{row['Part_2']}</strong> 🔗
                                </div>
                                <div>{conf_badge}</div>
                            </div>
                            <div class="bundle-stats">
                                👥 {row['Customer_Count']:,} customers | 📈 +{improvement:.1f}% improvement
                                {f" | 📜 {row['Total_Predecessors']} predecessors" if 'Total_Predecessors' in row else ""}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
            else:
                st.info("No supersession data available in filtered results")
        else:
            st.markdown('<div class="info-card">', unsafe_allow_html=True)
            st.markdown("""
            ### 🔗 Supersession Intelligence Not Available
            
            Your dataset doesn't include supersession data. To unlock this powerful feature:
            
            1. Run the supersession integration script
            2. Upload the enhanced CSV file
            3. Get insights from 22+ years of historical data
            
            **Benefits:**
            - Discover hidden purchase patterns
            - Boost confidence scores by 10-30%
            - Validate bundles with decades of proof
            """)
            st.markdown('</div>', unsafe_allow_html=True)
    
    # ==============================================================================
    # TAB 5: REPORTS & EXPORT
    # ==============================================================================
    with tab5:
        st.markdown('<h2 class="section-header">📥 Professional Reports & Export</h2>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 🎯 High-Value Bundles Report")
            
            export_threshold = st.slider(
                "Confidence Threshold",
                0.0, 1.0, 0.7, 0.05,
                key="export_threshold"
            )
            
            exportable = df_filtered[df_filtered['Confidence_Score'] >= export_threshold]
            
            st.markdown(f'<div class="success-card">📊 <strong>{len(exportable):,}</strong> bundles meet criteria</div>', unsafe_allow_html=True)
            
            if len(exportable) > 0:
                csv = exportable.to_csv(index=False)
                st.download_button(
                    label="📥 Download High-Value Report",
                    data=csv,
                    file_name=f"high_value_bundles_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv",
                    type="primary",
                    use_container_width=True
                )
        
        with col2:
            st.markdown("### 📊 Executive Summary")
            
            summary = f"""
# Bundle Analysis Executive Summary
**Generated:** {datetime.now().strftime('%B %d, %Y %I:%M %p')}
**Southeastern Equipment Co.**

## Key Findings

### Overall Opportunity
- **Total Bundles Identified:** {len(df_filtered):,}
- **Total Customer Base:** {df_filtered['Customer_Count'].sum():,}
- **Average Confidence:** {df_filtered['Confidence_Score'].mean():.1%}

### High-Confidence Opportunities (≥70%)
- **Bundle Count:** {len(df_filtered[df_filtered['Confidence_Score'] >= 0.7]):,}
- **Customer Base:** {df_filtered[df_filtered['Confidence_Score'] >= 0.7]['Customer_Count'].sum():,}

### Top 5 Recommended Bundles
"""
            top_5 = df_filtered.nlargest(5, 'Customer_Count')
            for idx, row in top_5.iterrows():
                summary += f"\n### {row['Part_1']} + {row['Part_2']}\n"
                summary += f"- **Confidence:** {row['Confidence_Score']:.1%}\n"
                summary += f"- **Customers:** {row['Customer_Count']:,}\n"
            
            st.download_button(
                label="📥 Download Executive Summary",
                data=summary,
                file_name=f"executive_summary_{datetime.now().strftime('%Y%m%d')}.md",
                mime="text/markdown",
                type="primary",
                use_container_width=True
            )
        
        st.markdown("---")
        
        # Full dataset exports
        st.markdown("### 📋 Complete Dataset Export")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            csv_full = df_filtered.to_csv(index=False)
            st.download_button(
                label="📥 Export CSV",
                data=csv_full,
                file_name=f"complete_analysis_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv",
                use_container_width=True
            )
        
        with col2:
            # Excel export
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df_filtered.to_excel(writer, index=False, sheet_name='Bundle Analysis')
            
            st.download_button(
                label="📥 Export Excel",
                data=output.getvalue(),
                file_name=f"complete_analysis_{datetime.now().strftime('%Y%m%d')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )
        
        with col3:
            json_data = df_filtered.to_json(orient='records', indent=2)
            st.download_button(
                label="📥 Export JSON",
                data=json_data,
                file_name=f"complete_analysis_{datetime.now().strftime('%Y%m%d')}.json",
                mime="application/json",
                use_container_width=True
            )

# ==============================================================================
# PROFESSIONAL FOOTER
# ==============================================================================
st.markdown("---")
st.markdown("""
<div class="footer">
    <strong>SE Bundle Analyzer Pro v2.9</strong><br>
    Professional Bundle Analysis & Revenue Optimization Platform<br>
    Southeastern Equipment Co. | Powered by Advanced Analytics
</div>
""", unsafe_allow_html=True)
