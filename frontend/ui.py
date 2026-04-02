"""
Ultimate AI Excel Agent - All Features
By Syed Rafay

Features:
- Data Cleaning (Duplicates, Nulls, Types)
- Charts & Graphs
- Export (Excel, CSV, PDF)
- Multiple Files Support
- Beautiful UI
"""

import sys
import io
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except:
        pass

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import sys
import base64
from io import BytesIO
sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))
from agent_gemini import create_agent

# =============================================================================
# Page Configuration & Custom CSS
# =============================================================================

st.set_page_config(
    page_title="AI Excel Agent - By Syed Rafay",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Modern CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
    
    :root {
        --primary-gradient: linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #d946ef 100%);
        --secondary-gradient: linear-gradient(135deg, #06b6d4 0%, #0ea5e9 100%);
        --success-gradient: linear-gradient(135deg, #10b981 0%, #059669 100%);
    }
    
    .stApp {
        font-family: 'Inter', sans-serif;
        background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 25%, #ddd6fe 50%, #fce7f3 75%, #fef3c7 100%);
        background-size: 400% 400%;
        animation: gradientFlow 15s ease infinite;
    }
    
    @keyframes gradientFlow {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .main-header {
        background: var(--primary-gradient);
        padding: 4rem 3rem;
        border-radius: 2rem;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 10px 40px rgba(99, 102, 241, 0.4);
    }
    
    .main-header h1 {
        color: white;
        font-size: 3.5rem;
        font-weight: 900;
        margin: 0;
        text-shadow: 0 4px 20px rgba(0,0,0,0.3);
    }
    
    .main-header p {
        color: rgba(255,255,255,0.95);
        font-size: 1.3rem;
        margin-top: 0.8rem;
    }
    
    .metric-card {
        background: white;
        padding: 2.5rem;
        border-radius: 1.5rem;
        text-align: center;
        box-shadow: 8px 8px 16px rgba(163, 177, 198, 0.3), -8px -8px 16px rgba(255, 255, 255, 0.9);
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }
    
    .metric-card:hover {
        transform: translateY(-10px);
    }
    
    .metric-value {
        font-size: 3rem;
        font-weight: 900;
        background: var(--primary-gradient);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .metric-label {
        font-size: 0.85rem;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        font-weight: 700;
    }
    
    .chat-user {
        background: var(--primary-gradient);
        color: white;
        padding: 1.5rem 2rem;
        border-radius: 2rem 2rem 0.5rem 2rem;
        margin: 1.5rem 0;
        box-shadow: 0 8px 30px rgba(99, 102, 241, 0.4);
    }
    
    .chat-ai {
        background: white;
        color: #1e293b;
        padding: 1.5rem 2rem;
        border-radius: 2rem 2rem 2rem 0.5rem;
        margin: 1.5rem 0;
        border-left: 5px solid #6366f1;
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.12);
    }
    
    .stButton > button {
        background: var(--primary-gradient);
        color: white;
        border: none;
        padding: 1rem 2rem;
        border-radius: 1rem;
        font-weight: 700;
        transition: all 0.3s ease;
        box-shadow: 0 8px 25px rgba(99, 102, 241, 0.4);
    }
    
    .stButton > button:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 35px rgba(99, 102, 241, 0.5);
    }
    
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, rgba(99, 102, 241, 0.95) 0%, rgba(139, 92, 246, 0.95) 100%);
    }
    
    [data-testid="stSidebar"] * {
        color: white !important;
    }
    
    .feature-card {
        background: white;
        padding: 2.5rem;
        border-radius: 1.5rem;
        text-align: center;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }
    
    .feature-card:hover {
        transform: translateY(-15px) rotateY(5deg);
    }
    
    .feature-icon {
        font-size: 4rem;
        margin-bottom: 1.5rem;
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# =============================================================================
# Session State
# =============================================================================

if "file_uploaded" not in st.session_state:
    st.session_state.file_uploaded = False
if "loaded_data" not in st.session_state:
    st.session_state.loaded_data = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "current_file_name" not in st.session_state:
    st.session_state.current_file_name = None
if "multiple_files" not in st.session_state:
    st.session_state.multiple_files = {}

# =============================================================================
# Sidebar
# =============================================================================

with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 2rem 0; border-bottom: 2px solid rgba(255,255,255,0.2);">
        <h2 style="color: white; margin: 0;">⚙️ Control Panel</h2>
        <p style="color: rgba(255,255,255,0.8); margin-top: 0.5rem;">by Syed Rafay</p>
    </div>
    """, unsafe_allow_html=True)
    
    # File Upload
    st.markdown("### 📁 Upload Files")
    uploaded_file = st.file_uploader(
        "Upload Excel File",
        type=["xlsx", "xls", "xlsm"],
        key="uploader"
    )
    
    if uploaded_file is not None:
        if not st.session_state.file_uploaded:
            with st.spinner("🔄 Loading..."):
                temp_path = Path("uploads") / f"temp_{uploaded_file.name}"
                temp_path.parent.mkdir(exist_ok=True)
                
                with open(temp_path, "wb") as f:
                    f.write(uploaded_file.getvalue())
                
                agent = create_agent()
                result = agent.load_excel(str(temp_path))
                
                if result.get("success"):
                    st.session_state.file_uploaded = True
                    st.session_state.loaded_data = agent.df
                    st.session_state.current_file_name = uploaded_file.name
                    st.success(f"✅ Loaded: {result['rows']} rows × {len(result['columns'])} cols")
    
    if st.session_state.file_uploaded:
        st.divider()
        st.info(f"📎 {st.session_state.current_file_name}")
        
        if st.button("🗑️ Reset", use_container_width=True):
            st.session_state.file_uploaded = False
            st.session_state.loaded_data = None
            st.session_state.chat_history = []
            st.rerun()
    
    st.divider()
    
    # Quick Stats
    if st.session_state.file_uploaded and st.session_state.loaded_data is not None:
        df = st.session_state.loaded_data
        st.markdown("### 📈 Quick Stats")
        st.metric("📊 Rows", f"{len(df):,}")
        st.metric("📋 Columns", len(df.columns))
        st.metric("💾 Memory", f"{df.memory_usage(deep=True).sum()/1024**2:.2f} MB")

# =============================================================================
# Main Header
# =============================================================================

st.markdown("""
<div class="main-header">
    <h1>📊 AI Excel Agent</h1>
    <p>Transform Your Data Into Insights with AI</p>
    <p style="margin-top: 1rem; font-size: 1rem; opacity: 0.9;">Created by <strong>Syed Rafay</strong></p>
</div>
""", unsafe_allow_html=True)

# =============================================================================
# Welcome Screen
# =============================================================================

if not st.session_state.file_uploaded or st.session_state.loaded_data is None:
    st.markdown("""
    <div style="background: white; padding: 4rem; border-radius: 2rem; text-align: center; box-shadow: 0 10px 40px rgba(0,0,0,0.1); margin: 2rem auto; max-width: 900px;">
        <h2 style="color: #6366f1; font-size: 3rem; margin-bottom: 1rem;">👋 Welcome!</h2>
        <p style="color: #64748b; font-size: 1.2rem;">Upload an Excel file to unlock powerful AI-driven insights</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">📤</div>
            <h3 style="color: #6366f1; font-weight: 800;">Upload</h3>
            <p style="color: #64748b;">Upload Excel files easily</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">💬</div>
            <h3 style="color: #8b5cf6; font-weight: 800;">Ask</h3>
            <p style="color: #64748b;">Ask questions naturally</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">✨</div>
            <h3 style="color: #d946ef; font-weight: 800;">Get Insights</h3>
            <p style="color: #64748b;">Get instant AI analysis</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.stop()

# =============================================================================
# Data Analysis Interface
# =============================================================================

df = st.session_state.loaded_data

# Metrics
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{len(df):,}</div>
        <div class="metric-label">📊 Total Rows</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{len(df.columns)}</div>
        <div class="metric-label">📋 Columns</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{df.memory_usage(deep=True).sum()/1024**2:.2f}</div>
        <div class="metric-label">💾 Memory (MB)</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    dup_count = df.duplicated().sum()
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{dup_count}</div>
        <div class="metric-label">⚠️ Duplicates</div>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# Tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "💬 Chat",
    "📋 Data",
    "📊 Charts",
    "🧹 Clean",
    "💾 Export"
])

# =============================================================================
# Tab 1: Chat
# =============================================================================

with tab1:
    st.markdown("### 💬 Ask Questions")
    
    # Chat history
    for msg in st.session_state.chat_history:
        if msg["is_user"]:
            st.markdown(f'<div class="chat-user"><strong>👤 You:</strong><br>{msg["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="chat-ai"><strong>🤖 AI:</strong><br>{msg["content"]}</div>', unsafe_allow_html=True)
    
    user_input = st.chat_input("Ask about your data...")
    
    if user_input:
        st.session_state.chat_history.append({"content": user_input, "is_user": True})
        
        agent = create_agent()
        if st.session_state.loaded_data is not None:
            agent.df = st.session_state.loaded_data.copy()
            agent._data_loaded = True
        
        with st.spinner("🤔 Thinking..."):
            result = agent.process_query(user_input)
            response = result.get("response", "No response")
        
        if agent.df is not None and any(word in user_input.lower() for word in ["remove", "clean", "fill", "fix"]):
            st.session_state.loaded_data = agent.df
        
        st.session_state.chat_history.append({"content": response, "is_user": False})
        st.rerun()

# =============================================================================
# Tab 2: Data Preview
# =============================================================================

with tab2:
    st.markdown("### 📋 Data Preview")
    st.dataframe(df, use_container_width=True)
    
    # Download
    csv_data = df.to_csv(index=False)
    st.download_button(
        label="📥 Download CSV",
        data=csv_data,
        file_name=f"data_{st.session_state.current_file_name.replace('.xlsx', '')}.csv",
        mime="text/csv",
        use_container_width=True
    )

# =============================================================================
# Tab 3: Charts
# =============================================================================

with tab3:
    st.markdown("### 📊 Create Charts")
    
    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
    all_cols = df.columns.tolist()
    
    col1, col2 = st.columns(2)
    
    with col1:
        chart_type = st.selectbox(
            "Chart Type",
            ["bar", "line", "pie", "scatter", "histogram", "box", "area"],
            key="chart_type"
        )
        
        x_col = st.selectbox("X Axis", all_cols, key="x_col")
        
        if numeric_cols:
            y_col = st.selectbox("Y Axis", numeric_cols, key="y_col")
        else:
            y_col = st.selectbox("Y Axis", all_cols, key="y_col")
        
        chart_title = st.text_input("Chart Title", f"{chart_type.title()} Chart", key="chart_title")
    
    with col2:
        if st.button("🎨 Generate Chart", use_container_width=True, type="primary"):
            try:
                if chart_type == "bar":
                    fig = px.bar(df, x=x_col, y=y_col, title=chart_title)
                elif chart_type == "line":
                    fig = px.line(df, x=x_col, y=y_col, title=chart_title)
                elif chart_type == "pie":
                    fig = px.pie(df, names=x_col, values=y_col, title=chart_title)
                elif chart_type == "scatter":
                    fig = px.scatter(df, x=x_col, y=y_col, title=chart_title)
                elif chart_type == "histogram":
                    fig = px.histogram(df, x=y_col, title=chart_title)
                elif chart_type == "box":
                    fig = px.box(df, x=x_col, y=y_col, title=chart_title)
                elif chart_type == "area":
                    fig = px.area(df, x=x_col, y=y_col, title=chart_title)
                
                fig.update_layout(height=500, showlegend=True)
                st.plotly_chart(fig, use_container_width=True)
                
            except Exception as e:
                st.error(f"Error creating chart: {str(e)}")

# =============================================================================
# Tab 4: Clean Data
# =============================================================================

with tab4:
    st.markdown("### 🧹 Data Cleaning")
    
    # Data Quality Report
    st.markdown("#### ⚠️ Current Data Quality")
    
    col1, col2 = st.columns(2)
    
    with col1:
        missing = df.isnull().sum().sum()
        st.metric("Missing Values", missing)
    
    with col2:
        duplicates = df.duplicated().sum()
        st.metric("Duplicate Rows", duplicates)
    
    st.divider()
    
    # Cleaning Actions
    st.markdown("#### 🛠️ Cleaning Actions")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🗑️ Remove Duplicates", use_container_width=True):
            agent = create_agent()
            agent.df = df.copy()
            agent._data_loaded = True
            result = agent._remove_duplicates_action()
            st.session_state.loaded_data = agent.df
            st.success(result)
            st.rerun()
    
    with col2:
        if st.button("🔧 Fill Missing Values", use_container_width=True):
            agent = create_agent()
            agent.df = df.copy()
            agent._data_loaded = True
            result = agent._fill_nulls_action()
            st.session_state.loaded_data = agent.df
            st.success(result)
            st.rerun()
    
    with col3:
        if st.button("✨ Clean Everything", use_container_width=True):
            agent = create_agent()
            agent.df = df.copy()
            agent._data_loaded = True
            result = agent._clean_all_action()
            st.session_state.loaded_data = agent.df
            st.success(result)
            st.rerun()
    
    st.divider()
    
    if st.button("🔧 Fix Data Types", use_container_width=True):
        agent = create_agent()
        agent.df = df.copy()
        agent._data_loaded = True
        result = agent._fix_data_types()
        st.session_state.loaded_data = agent.df
        st.success(result)
        st.rerun()

# =============================================================================
# Tab 5: Export
# =============================================================================

with tab5:
    st.markdown("### 💾 Export Data")
    
    st.markdown("**Download your cleaned data in different formats:**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Excel Export
        excel_buffer = BytesIO()
        with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Data')
        
        st.download_button(
            label="📥 Download as Excel (.xlsx)",
            data=excel_buffer.getvalue(),
            file_name=f"clean_data_{st.session_state.current_file_name}",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )
    
    with col2:
        # CSV Export
        csv_data = df.to_csv(index=False)
        st.download_button(
            label="📥 Download as CSV",
            data=csv_data,
            file_name=f"clean_data_{st.session_state.current_file_name.replace('.xlsx', '')}.csv",
            mime="text/csv",
            use_container_width=True
        )
    
    st.divider()
    
    # PDF Report (Simple text-based)
    st.markdown("#### 📄 Generate Report")
    
    if st.button("📊 Generate Summary Report"):
        report = f"""
# AI Excel Agent - Data Report
Generated by: Syed Rafay
Date: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}

## Dataset Summary
- File: {st.session_state.current_file_name}
- Total Rows: {len(df):,}
- Total Columns: {len(df.columns)}
- Memory: {df.memory_usage(deep=True).sum()/1024**2:.2f} MB

## Columns
{', '.join(df.columns)}

## Statistics
{df.describe().to_string()}

## Data Quality
- Missing Values: {df.isnull().sum().sum()}
- Duplicate Rows: {df.duplicated().sum()}

---
Built with ❤️ by Syed Rafay
        """
        
        st.download_button(
            label="📥 Download Report (.txt)",
            data=report,
            file_name=f"data_report_{st.session_state.current_file_name.replace('.xlsx', '')}.txt",
            mime="text/plain",
            use_container_width=True
        )
        
        st.success("✅ Report generated! Click download above.")

# =============================================================================
# Footer
# =============================================================================

st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #64748b; padding: 2rem;">
    <p style="font-size: 0.9rem;">
        Built with ❤️ by <strong>Syed Rafay</strong> | AI Excel Agent © 2024 | 
        <span style="background: linear-gradient(135deg, #6366f1, #8b5cf6); color: white; padding: 0.5rem 1rem; border-radius: 2rem; font-size: 0.8rem;">v3.0 Ultimate</span>
    </p>
</div>
""", unsafe_allow_html=True)
