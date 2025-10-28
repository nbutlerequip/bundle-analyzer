"""
Supersession-Enhanced Bundle Analyzer - Simplified Version
Pre-loaded data - Users just click "Run Analysis"
"""

import streamlit as st
import pandas as pd
import os
from datetime import datetime
from collections import defaultdict
import io
import glob

# Page config
st.set_page_config(
    page_title="Bundle Analyzer",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #003366 0%, #0055AA 100%);
        padding: 30px;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 30px;
    }
    .stat-box {
        background: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        border-left: 4px solid #003366;
    }
    .stat-value {
        font-size: 2rem;
        font-weight: bold;
        color: #003366;
    }
    .stat-label {
        font-size: 0.9rem;
        color: #666;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1>🚀 Supersession-Enhanced Bundle Analyzer</h1>
    <p>Discover hidden opportunities with 22+ years of historical purchasing intelligence</p>
    <p style="font-size: 0.8rem; opacity: 0.9;">Southeastern Equipment Co. | v2.0</p>
</div>
""", unsafe_allow_html=True)

# Initialize session state
if 'analysis_complete' not in st.session_state:
    st.session_state.analysis_complete = False
if 'results_df' not in st.session_state:
    st.session_state.results_df = None
if 'stats' not in st.session_state:
    st.session_state.stats = None

# Helper functions
@st.cache_data
def load_supersession_data_from_folder():
    """Load supersession files from data folder"""
    all_supersessions = []
    data_folder = 'data'
    
    if not os.path.exists(data_folder):
        st.error(f"⚠️ Data folder not found. Please create a 'data' folder with your Excel files.")
        return pd.DataFrame(columns=['current', 'old'])
    
    # Find all Excel files with supersession-related names
    pattern = os.path.join(data_folder, '*')
    files = glob.glob(pattern)
    excel_files = [f for f in files if f.endswith(('.xlsx', '.xls'))]
    supersession_files = [f for f in excel_files if 'supercede' in f.lower() or 'supersede' in f.lower()]
    
    st.info(f"📂 Found {len(supersession_files)} supersession files in data folder")
    
    for file_path in supersession_files:
        try:
            df = pd.read_excel(file_path)
            df.columns = df.columns.str.strip().str.upper()
            
            current_col = None
            supersedes_col = None
            
            for col in df.columns:
                col_clean = str(col).upper()
                if 'CURRENT' in col_clean or 'NEW' in col_clean:
                    current_col = col
                elif 'SUPERSEDE' in col_clean or 'OLD' in col_clean or 'REPLACE' in col_clean:
                    supersedes_col = col
            
            if current_col and supersedes_col:
                temp_df = df[[current_col, supersedes_col]].copy()
                temp_df.columns = ['current', 'old']
                temp_df = temp_df.dropna()
                temp_df['current'] = temp_df['current'].astype(str).str.strip().str.replace('.0', '', regex=False)
                temp_df['old'] = temp_df['old'].astype(str).str.strip().str.replace('.0', '', regex=False)
                temp_df = temp_df[temp_df['current'] != 'nan']
                temp_df = temp_df[temp_df['old'] != 'nan']
                temp_df = temp_df[temp_df['current'] != temp_df['old']]
                all_supersessions.append(temp_df)
                st.success(f"✅ Loaded {os.path.basename(file_path)}: {len(temp_df):,} mappings")
        except Exception as e:
            st.warning(f"⚠️ Could not read {os.path.basename(file_path)}: {str(e)}")
    
    if all_supersessions:
        return pd.concat(all_supersessions, ignore_index=True).drop_duplicates()
    return pd.DataFrame(columns=['current', 'old'])

@st.cache_data
def load_bundle_data_from_folder():
    """Load bundle analysis file from data folder"""
    data_folder = 'data'
    
    if not os.path.exists(data_folder):
        return None
    
    # Find bundle analysis file
    pattern = os.path.join(data_folder, '*')
    files = glob.glob(pattern)
    excel_files = [f for f in files if f.endswith(('.xlsx', '.xls'))]
    
    # Look for bundle file
    bundle_file = None
    for f in excel_files:
        fname_lower = f.lower()
        if 'bundle' in fname_lower or 'analysis' in fname_lower:
            if 'part_type' not in fname_lower:  # Exclude part_type files
                bundle_file = f
                break
    
    if bundle_file:
        st.info(f"📊 Using bundle file: {os.path.basename(bundle_file)}")
        return pd.read_excel(bundle_file)
    else:
        st.error("⚠️ No bundle analysis file found in data folder")
        return None

def build_predecessor_map(supersession_df):
    """Build predecessor chains"""
    pred_map = defaultdict(list)
    for _, row in supersession_df.iterrows():
        pred_map[row['current']].append(row['old'])
    
    def get_all_predecessors(part, visited=None):
        if visited is None:
            visited = set()
        if part in visited:
            return []
        visited.add(part)
        all_preds = []
        if part in pred_map:
            for pred in pred_map[part]:
                all_preds.append(pred)
                all_preds.extend(get_all_predecessors(pred, visited))
        return all_preds
    
    predecessor_master = {}
    for part in pred_map.keys():
        preds = get_all_predecessors(part)
        if preds:
            predecessor_master[part] = list(set(preds))
    
    return predecessor_master

def process_bundles(bundle_df, predecessor_master):
    """Process bundle data with supersession enhancement"""
    results = []
    
    for _, row in bundle_df.iterrows():
        part1 = None
        part2 = None
        
        for col in bundle_df.columns:
            col_str = str(col).lower().replace(' ', '').replace('_', '')
            if 'part1' in col_str or 'item1' in col_str:
                part1 = str(row[col]).strip().replace('.0', '')
            elif 'part2' in col_str or 'item2' in col_str:
                part2 = str(row[col]).strip().replace('.0', '')
        
        if not part1 or not part2 or part1 == 'nan' or part2 == 'nan':
            continue
        
        frequency = 0
        confidence = 0
        
        for col in bundle_df.columns:
            col_lower = str(col).lower()
            if 'frequency' in col_lower or 'count' in col_lower:
                try:
                    frequency = int(row[col])
                except:
                    pass
            if 'confidence' in col_lower:
                try:
                    conf = row[col]
                    confidence = float(str(conf).replace('%', '')) if isinstance(conf, str) else float(conf)
                except:
                    pass
        
        desc1 = desc2 = ''
        for col in bundle_df.columns:
            col_str = str(col).lower()
            if 'description1' in col_str or 'desc1' in col_str:
                desc1 = str(row[col])[:50]
            elif 'description2' in col_str or 'desc2' in col_str:
                desc2 = str(row[col])[:50]
        
        preds1 = predecessor_master.get(part1, [])
        preds2 = predecessor_master.get(part2, [])
        total_preds = len(preds1) + len(preds2)
        
        boost = min(total_preds * 5, 40)
        enhanced_confidence = min(confidence + boost, 99)
        
        avg_price = 50
        for col in bundle_df.columns:
            if 'price' in str(col).lower() or 'cost' in str(col).lower():
                try:
                    price = row[col]
                    avg_price = float(str(price).replace('$', '').replace(',', '')) if isinstance(price, str) else float(price)
                    break
                except:
                    pass
        
        revenue = frequency * avg_price * 2 if frequency > 0 else 0
        
        results.append({
            'Part_1': part1,
            'Part_2': part2,
            'Description_1': desc1,
            'Description_2': desc2,
            'Frequency': int(frequency),
            'Confidence_Original': round(confidence, 1),
            'Confidence_Enhanced': round(enhanced_confidence, 1),
            'Confidence_Boost': round(boost, 1),
            'Has_History': 'YES' if total_preds > 0 else 'NO',
            'Predecessors_Part1': len(preds1),
            'Predecessors_Part2': len(preds2),
            'Total_Predecessors': total_preds,
            'Revenue': round(revenue, 2),
            'Actionable': 'YES' if enhanced_confidence >= 50 else 'NO'
        })
    
    return pd.DataFrame(results).sort_values('Confidence_Enhanced', ascending=False)

# Main UI
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    st.markdown("### 📊 Ready to Analyze")
    st.info("Your supersession and bundle data files are pre-loaded. Click the button below to run the analysis!")
    
    if st.button("🚀 Run Analysis", type="primary", use_container_width=True):
        with st.spinner("🔄 Processing data... This may take 1-2 minutes..."):
            
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            status_text.text("📂 Loading supersession data...")
            progress_bar.progress(20)
            supersession_df = load_supersession_data_from_folder()
            
            status_text.text("🔗 Building predecessor chains...")
            progress_bar.progress(40)
            predecessor_master = build_predecessor_map(supersession_df)
            
            status_text.text("📊 Loading bundle data...")
            progress_bar.progress(60)
            bundle_df = load_bundle_data_from_folder()
            
            if bundle_df is None:
                st.error("❌ Could not load bundle data. Please check your data folder.")
                st.stop()
            
            status_text.text("🧮 Analyzing bundles...")
            progress_bar.progress(80)
            results_df = process_bundles(bundle_df, predecessor_master)
            
            with_history = len(results_df[results_df['Has_History'] == 'YES'])
            pct_with_history = (with_history / len(results_df) * 100) if len(results_df) > 0 else 0
            
            stats = {
                'total_bundles': len(results_df),
                'with_history': with_history,
                'pct_with_history': pct_with_history,
                'avg_boost': results_df['Confidence_Boost'].mean(),
                'total_revenue': results_df['Revenue'].sum(),
                'actionable': len(results_df[results_df['Actionable'] == 'YES'])
            }
            
            status_text.text("✅ Complete!")
            progress_bar.progress(100)
            
            st.session_state.results_df = results_df
            st.session_state.stats = stats
            st.session_state.analysis_complete = True
            
            st.success("✅ Analysis complete! See results below.")
            st.rerun()

# Display results
if st.session_state.analysis_complete and st.session_state.results_df is not None:
    
    st.header("📊 Analysis Summary")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="stat-box">
            <div class="stat-value">{st.session_state.stats['total_bundles']:,}</div>
            <div class="stat-label">Total Bundles</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="stat-box">
            <div class="stat-value">{st.session_state.stats['with_history']:,}</div>
            <div class="stat-label">With Supersession History</div>
            <div style="color: #10B981; font-weight: 600; margin-top: 5px;">
                {st.session_state.stats['pct_with_history']:.1f}%
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="stat-box">
            <div class="stat-value">+{st.session_state.stats['avg_boost']:.1f}%</div>
            <div class="stat-label">Avg Confidence Boost</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="stat-box">
            <div class="stat-value">${st.session_state.stats['total_revenue']/1000000:.1f}M</div>
            <div class="stat-label">Revenue Potential</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.divider()
    
    st.header("🔍 Filter & Explore Results")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        min_confidence = st.slider("Minimum Enhanced Confidence", 0, 100, 50)
    
    with col2:
        history_filter = st.selectbox("Supersession History", ["All", "With History Only", "Without History Only"])
    
    with col3:
        actionable_filter = st.selectbox("Actionable Status", ["All", "Actionable Only (≥50%)", "Not Actionable"])
    
    filtered_df = st.session_state.results_df.copy()
    filtered_df = filtered_df[filtered_df['Confidence_Enhanced'] >= min_confidence]
    
    if history_filter == "With History Only":
        filtered_df = filtered_df[filtered_df['Has_History'] == 'YES']
    elif history_filter == "Without History Only":
        filtered_df = filtered_df[filtered_df['Has_History'] == 'NO']
    
    if actionable_filter == "Actionable Only (≥50%)":
        filtered_df = filtered_df[filtered_df['Actionable'] == 'YES']
    elif actionable_filter == "Not Actionable":
        filtered_df = filtered_df[filtered_df['Actionable'] == 'NO']
    
    search_term = st.text_input("🔍 Search by part number or description", "")
    if search_term:
        mask = (
            filtered_df['Part_1'].str.contains(search_term, case=False, na=False) |
            filtered_df['Part_2'].str.contains(search_term, case=False, na=False) |
            filtered_df['Description_1'].str.contains(search_term, case=False, na=False) |
            filtered_df['Description_2'].str.contains(search_term, case=False, na=False)
        )
        filtered_df = filtered_df[mask]
    
    st.info(f"📊 Showing {len(filtered_df):,} bundles (filtered from {len(st.session_state.results_df):,})")
    
    tab1, tab2, tab3 = st.tabs(["📋 Top 50", "📊 All Results", "📥 Download"])
    
    with tab1:
        st.subheader("🏆 Top 50 Opportunities")
        top_50 = filtered_df.head(50)
        
        st.write("**Top 10 Detailed View:**")
        for idx, row in top_50.head(10).iterrows():
            with st.container():
                col1, col2, col3 = st.columns([2, 2, 1])
                
                with col1:
                    st.markdown(f"**{row['Part_1']}** + **{row['Part_2']}**")
                    st.caption(f"{row['Description_1']} | {row['Description_2']}")
                
                with col2:
                    st.metric("Enhanced Confidence", f"{row['Confidence_Enhanced']:.1f}%", f"+{row['Confidence_Boost']:.1f}%")
                
                with col3:
                    st.metric("Revenue", f"${row['Revenue']/1000:.1f}K")
                    if row['Has_History'] == 'YES':
                        st.success(f"🔗 {row['Total_Predecessors']} preds")
        
        st.divider()
        st.write("**Complete Top 50 Table:**")
        st.dataframe(
            top_50[['Part_1', 'Part_2', 'Frequency', 'Confidence_Original', 
                    'Confidence_Enhanced', 'Confidence_Boost', 'Has_History', 
                    'Total_Predecessors', 'Revenue']],
            use_container_width=True,
            height=400
        )
    
    with tab2:
        st.subheader("📊 All Filtered Results")
        st.dataframe(
            filtered_df[['Part_1', 'Part_2', 'Frequency', 'Confidence_Original', 
                        'Confidence_Enhanced', 'Confidence_Boost', 'Has_History', 
                        'Total_Predecessors', 'Revenue']],
            use_container_width=True,
            height=600
        )
    
    with tab3:
        st.subheader("📥 Download Results")
        
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            summary_data = {
                'Metric': [
                    'Total Bundles', 'With Supersession History', '% with History',
                    'Avg Confidence (Original)', 'Avg Confidence (Enhanced)',
                    'Avg Boost', 'Total Revenue', 'Actionable Bundles'
                ],
                'Value': [
                    st.session_state.stats['total_bundles'],
                    st.session_state.stats['with_history'],
                    f"{st.session_state.stats['pct_with_history']:.1f}%",
                    f"{st.session_state.results_df['Confidence_Original'].mean():.1f}%",
                    f"{st.session_state.results_df['Confidence_Enhanced'].mean():.1f}%",
                    f"+{st.session_state.stats['avg_boost']:.1f}%",
                    f"${st.session_state.stats['total_revenue']:,.2f}",
                    st.session_state.stats['actionable']
                ]
            }
            pd.DataFrame(summary_data).to_excel(writer, sheet_name='Summary', index=False)
            filtered_df.head(50).to_excel(writer, sheet_name='Top 50', index=False)
            filtered_df.to_excel(writer, sheet_name='All Results', index=False)
        
        excel_data = output.getvalue()
        
        st.download_button(
            label="📊 Download Excel File",
            data=excel_data,
            file_name=f"Bundle_Analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )
        
        st.success("✅ Click the button above to download your results as Excel")

else:
    # Welcome screen with instructions
    st.markdown("### 📚 Setup Instructions")
    
    st.info("""
    **For Admin: How to Add Data Files**
    
    1. In your GitHub repository, create a folder called `data`
    2. Upload your Excel files to this folder:
       - All Supercedes files (Supercedes 1, 2, 3, 4, CONSOLIDATED, etc.)
       - Bundle Analysis file (Bundle_Analysis_20250926.xlsx or similar)
    3. Commit the changes
    4. Streamlit will auto-update in 2 minutes
    5. Users can then just click "Run Analysis"!
    """)
    
    st.markdown("### ✨ For Users")
    st.success("""
    Once files are loaded by admin:
    - Just click the **"Run Analysis"** button above
    - No file uploads needed
    - Results appear in 1-2 minutes
    - Download Excel report when done
    """)
