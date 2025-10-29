"""
Professional Bundle Analyzer - Enterprise Edition
Supersession-Enhanced Bundle Analysis Tool
Southeastern Equipment Co. | v2.9
FINAL FIXED VERSION - Ready to Upload
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import io

# ==============================================================================
# PAGE CONFIGURATION
# ==============================================================================
st.set_page_config(
    page_title="SE Bundle Analyzer Pro | Southeastern Equipment",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
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
    }
    
    .block-container {
        padding-top: 2rem;
        max-width: 1400px;
    }
    
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
    }
    
    .metric-card {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.07);
        border-left: 4px solid #3B82F6;
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        box-shadow: 0 8px 15px rgba(0, 0, 0, 0.1);
        transform: translateY(-2px);
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1E3A8A;
    }
    
    .metric-label {
        font-size: 0.95rem;
        color: #64748B;
        font-weight: 500;
        text-transform: uppercase;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #F1F5F9;
        padding: 0.5rem;
        border-radius: 10px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: white;
        border-radius: 8px;
        font-weight: 600;
        padding: 0 2rem;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #1E3A8A 0%, #3B82F6 100%) !important;
        color: white !important;
    }
    
    .bundle-card {
        background: white;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 0.75rem 0;
        border: 2px solid #E2E8F0;
        transition: all 0.3s ease;
    }
    
    .bundle-card:hover {
        border-color: #3B82F6;
        transform: translateY(-2px);
    }
    
    .conf-perfect { background: #10B981; color: white; padding: 0.4rem 1rem; border-radius: 20px; display: inline-block; }
    .conf-high { background: #3B82F6; color: white; padding: 0.4rem 1rem; border-radius: 20px; display: inline-block; }
    .conf-medium { background: #F59E0B; color: white; padding: 0.4rem 1rem; border-radius: 20px; display: inline-block; }
    .conf-low { background: #94A3B8; color: white; padding: 0.4rem 1rem; border-radius: 20px; display: inline-block; }
    
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
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# SESSION STATE
# ==============================================================================
if 'bundles_df' not in st.session_state:
    st.session_state.bundles_df = None

# ==============================================================================
# HELPER FUNCTIONS
# ==============================================================================

@st.cache_data
def load_data_from_file():
    """Load pre-uploaded data from data folder"""
    try:
        df = pd.read_csv('data/COMPLETE_BUNDLE_ANALYSIS_20251029_084720.csv')
        if 'Enhanced_Confidence_%' in df.columns:
            df['Confidence_Score'] = df['Enhanced_Confidence_%'] / 100.0
        elif 'Base_Confidence_%' in df.columns:
            df['Confidence_Score'] = df['Base_Confidence_%'] / 100.0
        return df
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return None

def get_confidence_badge(confidence):
    if confidence >= 1.0:
        return '<span class="conf-perfect">🌟 100%</span>'
    elif confidence >= 0.7:
        return f'<span class="conf-high">✓ {confidence:.0%}</span>'
    elif confidence >= 0.4:
        return f'<span class="conf-medium">○ {confidence:.0%}</span>'
    else:
        return f'<span class="conf-low">◌ {confidence:.0%}</span>'

def format_currency(value):
    return f"${value:,.0f}"

def format_number(value):
    if value >= 1_000_000:
        return f"{value/1_000_000:.1f}M"
    elif value >= 1_000:
        return f"{value/1_000:.1f}K"
    return f"{value:.0f}"

def create_metric_card(icon, value, label):
    return f"""
    <div class="metric-card">
        <div style="font-size: 2rem;">{icon}</div>
        <div class="metric-value">{value}</div>
        <div class="metric-label">{label}</div>
    </div>
    """

# ==============================================================================
# HEADER
# ==============================================================================
st.markdown("""
<div class="main-header">
    <h1>🚀 SE Bundle Analyzer Pro</h1>
    <p>Supersession-Enhanced Bundle Analysis & Revenue Optimization Platform</p>
    <div style="display: inline-block; background: rgba(255,255,255,0.2); padding: 0.3rem 1rem; border-radius: 20px; margin-top: 0.5rem;">
        Southeastern Equipment Co. | v2.9
    </div>
</div>
""", unsafe_allow_html=True)

# ==============================================================================
# SIDEBAR
# ==============================================================================
with st.sidebar:
    st.markdown("### ⚙️ Analysis Configuration")
    st.markdown("#### 📊 Data Loading")
    
    if st.session_state.bundles_df is None:
        if st.button("🚀 Load Bundle Data", type="primary", use_container_width=True):
            with st.spinner("Loading..."):
                st.session_state.bundles_df = load_data_from_file()
                if st.session_state.bundles_df is not None:
                    st.success(f"✅ Loaded {len(st.session_state.bundles_df):,} bundles!")
                    st.rerun()
                else:
                    st.error("⚠️ Data file not found!")
    else:
        st.success(f"✅ {len(st.session_state.bundles_df):,} bundles loaded")
        if st.button("🔄 Reload", use_container_width=True):
            st.session_state.bundles_df = None
            st.rerun()
    
    st.markdown("---")
    
    with st.expander("📁 Manual Upload"):
        uploaded_file = st.file_uploader("Upload CSV", type=['csv'])
        if uploaded_file:
            try:
                df = pd.read_csv(uploaded_file)
                if 'Enhanced_Confidence_%' in df.columns:
                    df['Confidence_Score'] = df['Enhanced_Confidence_%'] / 100
                elif 'Base_Confidence_%' in df.columns:
                    df['Confidence_Score'] = df['Base_Confidence_%'] / 100
                st.session_state.bundles_df = df
                st.success("✅ Uploaded!")
                st.rerun()
            except Exception as e:
                st.error(f"Error: {str(e)}")
    
    if st.session_state.bundles_df is not None:
        st.markdown("---")
        st.markdown("#### 🔍 Filters")
        
        min_confidence = st.slider("Min Confidence", 0.0, 1.0, 0.4, 0.05)
        min_customers = st.number_input("Min Customers", 1, value=10, step=5)
        
        df_filtered = st.session_state.bundles_df[
            (st.session_state.bundles_df['Confidence_Score'] >= min_confidence) &
            (st.session_state.bundles_df['Customer_Count'] >= min_customers)
        ].copy()
        
        st.info(f"📊 {len(df_filtered):,} bundles")
        
        if 'Has_Supersession' in st.session_state.bundles_df.columns:
            show_super = st.checkbox("🔗 Supersession Only")
            if show_super:
                df_filtered = df_filtered[df_filtered['Has_Supersession'] == 'Yes']
    else:
        df_filtered = None

# ==============================================================================
# MAIN CONTENT
# ==============================================================================

if st.session_state.bundles_df is None:
    st.markdown('<div class="info-card">', unsafe_allow_html=True)
    st.markdown("""
    ### 👋 Welcome to SE Bundle Analyzer Pro
    
    **✨ Key Features:**
    - 📊 Interactive Dashboards
    - 🔍 Smart Search
    - 📈 Revenue Projections
    - 🔗 Supersession Integration
    - 📥 Professional Reports
    
    **🚀 Get Started:**
    Click "Load Bundle Data" in the sidebar.
    """)
    st.markdown('</div>', unsafe_allow_html=True)

else:
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Dashboard",
        "🔍 Search",
        "🏆 Top Bundles",
        "🔗 Supersession",
        "📥 Export"
    ])
    
    # TAB 1: DASHBOARD
    with tab1:
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(create_metric_card("📦", f"{len(df_filtered):,}", "Bundles"), unsafe_allow_html=True)
        with col2:
            st.markdown(create_metric_card("👥", format_number(df_filtered['Customer_Count'].sum()), "Customers"), unsafe_allow_html=True)
        with col3:
            st.markdown(create_metric_card("📈", f"{df_filtered['Confidence_Score'].mean():.0%}", "Avg Confidence"), unsafe_allow_html=True)
        with col4:
            if 'Annual_Revenue_Potential_$' in df_filtered.columns:
                st.markdown(create_metric_card("💰", format_currency(df_filtered['Annual_Revenue_Potential_$'].sum()), "Revenue"), unsafe_allow_html=True)
            else:
                st.markdown(create_metric_card("🌟", f"{len(df_filtered[df_filtered['Confidence_Score']>=0.7]):,}", "High Conf"), unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Charts
        col_left, col_right = st.columns(2)
        
        with col_left:
            st.markdown("#### Confidence Distribution")
            df_filtered['Tier'] = pd.cut(
                df_filtered['Confidence_Score'],
                bins=[0, 0.4, 0.5, 0.7, 1.0],
                labels=['<40%', '40-50%', '50-70%', '70-100%']
            )
            tier_counts = df_filtered['Tier'].value_counts().sort_index()
            
            fig = go.Figure(data=[go.Bar(
                x=tier_counts.index,
                y=tier_counts.values,
                marker=dict(color=['#94A3B8', '#F59E0B', '#3B82F6', '#10B981']),
                text=tier_counts.values,
                textposition='auto'
            )])
            fig.update_layout(height=350, showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
        
        with col_right:
            st.markdown("#### Top 10 Bundles")
            top_10 = df_filtered.nlargest(10, 'Customer_Count')
            for _, row in top_10.iterrows():
                badge = get_confidence_badge(row['Confidence_Score'])
                super_icon = " 🔗" if row.get('Has_Supersession') == 'Yes' else ""
                st.markdown(f"""
                <div class="bundle-card">
                    <div style="display: flex; justify-content: space-between;">
                        <strong>{row['Part_1']} + {row['Part_2']}</strong>{super_icon}
                        <div>{badge}</div>
                    </div>
                    <div style="color: #64748B; font-size: 0.9rem;">
                        👥 {row['Customer_Count']:,} customers
                    </div>
                </div>
                """, unsafe_allow_html=True)
    
    # TAB 2: SEARCH
    with tab2:
        st.markdown("### 🔍 Search Bundles")
        
        col1, col2 = st.columns([3, 1])
        with col1:
            search_term = st.text_input("Search by part number", placeholder="e.g., 87682999")
        with col2:
            st.markdown("<br>", unsafe_allow_html=True)
            search_btn = st.button("Search", type="primary", use_container_width=True)
        
        if search_btn and search_term:
            results = df_filtered[
                (df_filtered['Part_1'].astype(str).str.contains(search_term, case=False)) |
                (df_filtered['Part_2'].astype(str).str.contains(search_term, case=False))
            ].sort_values('Customer_Count', ascending=False)
            
            if len(results) > 0:
                st.markdown(f'<div class="success-card">✅ Found {len(results):,} bundles</div>', unsafe_allow_html=True)
                
                for _, row in results.head(20).iterrows():
                    badge = get_confidence_badge(row['Confidence_Score'])
                    st.markdown(f"""
                    <div class="bundle-card">
                        <div style="display: flex; justify-content: space-between;">
                            <strong>{row['Part_1']} + {row['Part_2']}</strong>
                            <div>{badge}</div>
                        </div>
                        <div style="color: #64748B;">👥 {row['Customer_Count']:,} customers</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                csv = results.to_csv(index=False)
                st.download_button("📥 Download Results", csv, f"search_{search_term}.csv")
            else:
                st.warning(f"No bundles found containing '{search_term}'")
    
    # TAB 3: TOP BUNDLES
    with tab3:
        st.markdown("### 🏆 Top Opportunities")
        
        col1, col2 = st.columns([1, 3])
        with col1:
            top_n = st.selectbox("Show Top", [10, 20, 50, 100], index=1)
        with col2:
            sort_options = ['Customer_Count', 'Confidence_Score']
            if 'Annual_Revenue_Potential_$' in df_filtered.columns:
                sort_options.append('Annual_Revenue_Potential_$')
            sort_by = st.radio("Sort By", sort_options, horizontal=True)
        
        top_bundles = df_filtered.nlargest(top_n, sort_by)
        
        display_df = top_bundles[['Part_1', 'Part_2', 'Customer_Count', 'Confidence_Score']].copy()
        display_df['Confidence_Score'] = display_df['Confidence_Score'].apply(lambda x: f"{x:.0%}")
        st.dataframe(display_df, use_container_width=True, height=600)
        
        csv = top_bundles.to_csv(index=False)
        st.download_button(f"📥 Download Top {top_n}", csv, f"top_{top_n}_bundles.csv", type="primary")
    
    # TAB 4: SUPERSESSION
    with tab4:
        st.markdown("### 🔗 Supersession Intelligence")
        
        if 'Has_Supersession' in df_filtered.columns:
            super_bundles = df_filtered[df_filtered['Has_Supersession'] == 'Yes']
            if len(super_bundles) > 0:
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Enhanced Bundles", f"{len(super_bundles):,}")
                with col2:
                    st.metric("Enhanced Customers", f"{super_bundles['Customer_Count'].sum():,}")
                with col3:
                    if 'Confidence_Improvement_%' in super_bundles.columns:
                        st.metric("Avg Improvement", f"+{super_bundles['Confidence_Improvement_%'].mean():.1f}%")
                
                st.markdown("#### Top Improved Bundles")
                if 'Confidence_Improvement_%' in super_bundles.columns:
                    top_improved = super_bundles.nlargest(20, 'Confidence_Improvement_%')
                    for _, row in top_improved.iterrows():
                        badge = get_confidence_badge(row['Confidence_Score'])
                        st.markdown(f"""
                        <div class="bundle-card">
                            <div style="display: flex; justify-content: space-between;">
                                <strong>{row['Part_1']} + {row['Part_2']}</strong> 🔗
                                <div>{badge}</div>
                            </div>
                            <div style="color: #64748B;">
                                👥 {row['Customer_Count']:,} | 📈 +{row['Confidence_Improvement_%']:.1f}%
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
        else:
            st.info("Supersession data not available in this dataset")
    
    # TAB 5: EXPORT
    with tab5:
        st.markdown("### 📥 Export Reports")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### High-Value Report")
            threshold = st.slider("Confidence Threshold", 0.0, 1.0, 0.7, 0.05)
            exportable = df_filtered[df_filtered['Confidence_Score'] >= threshold]
            st.info(f"{len(exportable):,} bundles meet criteria")
            if len(exportable) > 0:
                csv = exportable.to_csv(index=False)
                st.download_button("📥 Download Report", csv, "high_value_bundles.csv", type="primary")
        
        with col2:
            st.markdown("#### Executive Summary")
            summary = f"""# Bundle Analysis Summary
**Generated:** {datetime.now().strftime('%B %d, %Y')}

## Key Findings
- **Total Bundles:** {len(df_filtered):,}
- **Total Customers:** {df_filtered['Customer_Count'].sum():,}
- **Average Confidence:** {df_filtered['Confidence_Score'].mean():.1%}

## Top 5 Bundles
"""
            for _, row in df_filtered.nlargest(5, 'Customer_Count').iterrows():
                summary += f"- {row['Part_1']} + {row['Part_2']}: {row['Customer_Count']:,} customers ({row['Confidence_Score']:.0%})\n"
            
            st.download_button("📥 Download Summary", summary, "executive_summary.md", type="primary")
        
        st.markdown("---")
        st.markdown("#### Complete Dataset")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.download_button("CSV", df_filtered.to_csv(index=False), "complete_analysis.csv")
        with col2:
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df_filtered.to_excel(writer, index=False)
            st.download_button("Excel", output.getvalue(), "complete_analysis.xlsx")
        with col3:
            st.download_button("JSON", df_filtered.to_json(orient='records'), "complete_analysis.json")

# ==============================================================================
# FOOTER
# ==============================================================================
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #64748B; padding: 2rem 0;">
    <strong>SE Bundle Analyzer Pro v2.9</strong><br>
    Southeastern Equipment Co. | Powered by Advanced Analytics
</div>
""", unsafe_allow_html=True)
