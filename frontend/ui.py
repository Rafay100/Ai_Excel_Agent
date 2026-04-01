"""
Beautiful Streamlit Frontend - AI Excel Agent
Modern, Professional UI with Rule-based AI (No API Key Needed!)
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
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))
from agent_gemini import create_agent

# =============================================================================
# Page Configuration & Custom CSS
# =============================================================================

st.set_page_config(
    page_title="AI Excel Agent",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Modern Professional CSS
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
    
    /* Global Styles */
    .stApp {
        font-family: 'Poppins', sans-serif;
        background: linear-gradient(135deg, #f5f7fa 0%, #e4e8ec 100%);
    }
    
    /* Main Header */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 3rem;
        border-radius: 1.5rem;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 10px 40px rgba(102, 126, 234, 0.4);
        animation: gradientShift 5s ease infinite;
    }
    
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .main-header h1 {
        color: white;
        font-size: 3rem;
        font-weight: 700;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        letter-spacing: -1px;
    }
    
    .main-header p {
        color: rgba(255,255,255,0.95);
        font-size: 1.2rem;
        margin-top: 0.5rem;
        font-weight: 300;
    }
    
    /* Metric Cards */
    .metric-card {
        background: white;
        padding: 2rem;
        border-radius: 1rem;
        text-align: center;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        transition: all 0.3s ease;
        border: 2px solid transparent;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 30px rgba(102, 126, 234, 0.3);
        border-color: #667eea;
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.5rem;
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: #666;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-weight: 600;
    }
    
    /* Chat Messages */
    .chat-user {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.2rem 1.5rem;
        border-radius: 1.5rem 1.5rem 0.5rem 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
        animation: slideIn 0.3s ease;
    }
    
    .chat-ai {
        background: white;
        color: #333;
        padding: 1.2rem 1.5rem;
        border-radius: 1.5rem 1.5rem 1.5rem 0.5rem;
        margin: 1rem 0;
        border-left: 5px solid #667eea;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        animation: slideIn 0.3s ease;
    }
    
    @keyframes slideIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.8rem 1.5rem;
        border-radius: 0.75rem;
        font-weight: 600;
        font-size: 0.95rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 25px rgba(102, 126, 234, 0.4);
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    
    [data-testid="stSidebar"] * {
        color: white !important;
    }
    
    .sidebar-header {
        text-align: center;
        padding: 2rem 0;
        border-bottom: 2px solid rgba(255,255,255,0.3);
        margin-bottom: 2rem;
    }
    
    .sidebar-header h2 {
        color: white;
        font-size: 1.8rem;
        margin: 0;
    }
    
    /* File Uploader */
    .stFileUploader {
        border: 2px dashed rgba(255,255,255,0.5);
        border-radius: 1rem;
        padding: 1.5rem;
        background: rgba(255,255,255,0.1);
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        justify-content: center;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 55px;
        padding: 0 2rem;
        border-radius: 1rem;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    
    /* Welcome Box */
    .welcome-box {
        background: white;
        padding: 3rem;
        border-radius: 1.5rem;
        text-align: center;
        box-shadow: 0 10px 40px rgba(0,0,0,0.1);
        margin: 2rem auto;
        max-width: 800px;
    }
    
    .welcome-box h2 {
        color: #667eea;
        font-size: 2.5rem;
        margin-bottom: 1rem;
    }
    
    .welcome-box p {
        color: #666;
        font-size: 1.1rem;
        line-height: 1.8;
    }
    
    /* Feature Cards */
    .feature-card {
        background: white;
        padding: 2rem;
        border-radius: 1rem;
        text-align: center;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        transition: all 0.3s ease;
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 30px rgba(102, 126, 234, 0.2);
    }
    
    .feature-icon {
        font-size: 3rem;
        margin-bottom: 1rem;
    }
    
    /* Success/Error Boxes */
    .success-box {
        background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
        border: 2px solid #28a745;
        color: #155724;
        padding: 1.5rem;
        border-radius: 1rem;
        margin: 1rem 0;
        font-weight: 500;
    }
    
    /* Dataframe Styling */
    .dataframe {
        border-radius: 1rem;
        overflow: hidden;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
    }
    
    /* Quick Query Buttons */
    .query-btn {
        background: white;
        border: 2px solid #667eea;
        color: #667eea;
        padding: 1rem;
        border-radius: 0.75rem;
        font-weight: 600;
        transition: all 0.3s ease;
        cursor: pointer;
    }
    
    .query-btn:hover {
        background: #667eea;
        color: white;
        transform: translateY(-2px);
    }
    
    /* Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #764ba2;
    }
</style>
""", unsafe_allow_html=True)

# =============================================================================
# Session State Initialization
# =============================================================================

if "file_uploaded" not in st.session_state:
    st.session_state.file_uploaded = False
if "loaded_data" not in st.session_state:
    st.session_state.loaded_data = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "current_file_name" not in st.session_state:
    st.session_state.current_file_name = None

# =============================================================================
# Sidebar
# =============================================================================

with st.sidebar:
    # Sidebar Header
    st.markdown("""
    <div class="sidebar-header">
        <h2>⚙️ Settings</h2>
    </div>
    """, unsafe_allow_html=True)
    
    # File Upload
    st.markdown("### 📁 Upload Excel File")
    uploaded_file = st.file_uploader(
        "Choose an Excel file",
        type=["xlsx", "xls", "xlsm"],
        help="Upload your Excel file (.xlsx, .xls, .xlsm)",
        key="uploader"
    )
    
    if uploaded_file is not None:
        if not st.session_state.file_uploaded:
            with st.spinner("🔄 Loading file..."):
                # Save file temporarily
                temp_path = Path("uploads") / f"temp_{uploaded_file.name}"
                temp_path.parent.mkdir(exist_ok=True)
                
                with open(temp_path, "wb") as f:
                    f.write(uploaded_file.getvalue())
                
                # Load with agent
                agent = create_agent()
                result = agent.load_excel(str(temp_path))
                
                if result.get("success"):
                    st.session_state.file_uploaded = True
                    st.session_state.loaded_data = agent.df
                    st.session_state.current_file_name = uploaded_file.name
                    st.markdown(f"""
                    <div class="success-box">
                        ✅ Loaded Successfully!<br>
                        📊 {result['rows']} rows × {len(result['columns'])} columns
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.error(f"❌ Error: {result.get('message')}")
    
    if st.session_state.file_uploaded:
        st.divider()
        st.markdown("### 📊 Current File")
        st.info(f"📄 {st.session_state.current_file_name}")
        
        if st.button("🗑️ Reset Session", use_container_width=True, type="secondary"):
            st.session_state.file_uploaded = False
            st.session_state.loaded_data = None
            st.session_state.chat_history = []
            st.session_state.current_file_name = None
            st.rerun()
    
    st.divider()
    
    # Quick Stats
    if st.session_state.file_uploaded and st.session_state.loaded_data is not None:
        df = st.session_state.loaded_data
        st.markdown("### 📈 Quick Stats")
        st.metric("Total Rows", f"{len(df):,}")
        st.metric("Total Columns", len(df.columns))
        st.metric("Memory Usage", f"{df.memory_usage(deep=True).sum()/1024**2:.2f} MB")

# =============================================================================
# Main Content
# =============================================================================

# Header
st.markdown("""
<div class="main-header">
    <h1>📊 AI Excel Agent</h1>
    <p>Intelligent Data Analysis Powered by AI</p>
</div>
""", unsafe_allow_html=True)

if not st.session_state.file_uploaded or st.session_state.loaded_data is None:
    # Welcome Screen
    st.markdown("""
    <div class="welcome-box">
        <h2>👋 Welcome!</h2>
        <p>Upload an Excel file to start analyzing your data with AI-powered insights.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Feature Cards
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">📤</div>
            <h3>Upload</h3>
            <p>Upload your Excel files (.xlsx, .xls, .xlsm) easily</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">💬</div>
            <h3>Ask</h3>
            <p>Ask questions in natural language about your data</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">📊</div>
            <h3>Analyze</h3>
            <p>Get instant AI-powered insights and analysis</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.divider()
    
    # Example Queries
    st.markdown("### 🎯 Example Questions You Can Ask:")
    
    examples = pd.DataFrame({
        "📊 Analysis": ["What is in the file?", "Show me a summary", "What are the column statistics?"],
        "🔍 Filtering": ["Show top 5 rows", "Filter by salary", "Show data types"],
        "⚠️ Data Quality": ["Check for missing values", "Remove duplicates", "Clean the data"]
    })
    
    st.dataframe(examples, use_container_width=True, hide_index=True)
    
else:
    # Data is loaded - Show analysis interface
    df = st.session_state.loaded_data
    
    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{len(df):,}</div>
            <div class="metric-label">Total Rows</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{len(df.columns)}</div>
            <div class="metric-label">Columns</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{df.memory_usage(deep=True).sum()/1024**2:.2f}</div>
            <div class="metric-label">Memory (MB)</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        dup_count = df.duplicated().sum()
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{dup_count}</div>
            <div class="metric-label">Duplicates</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.divider()
    
    # Tabs
    tab1, tab2, tab3, tab4 = st.tabs(["💬 Chat", "📋 Data", "📊 Statistics", "⚠️ Data Quality"])
    
    with tab1:
        # Chat Interface
        st.markdown("### 💬 Ask Questions About Your Data")
        
        # Chat history
        chat_container = st.container()
        with chat_container:
            if st.session_state.chat_history:
                for msg in st.session_state.chat_history:
                    if msg["is_user"]:
                        st.markdown(f'<div class="chat-user"><strong>👤 You:</strong><br>{msg["content"]}</div>', unsafe_allow_html=True)
                    else:
                        st.markdown(f'<div class="chat-ai"><strong>🤖 AI:</strong><br>{msg["content"]}</div>', unsafe_allow_html=True)
            else:
                st.info("👆 Ask your first question below!")
        
        # Input
        user_input = st.chat_input(
            "Ask about your data... (e.g., 'Show me summary', 'What are the statistics?')",
            key="chat_input"
        )
        
        if user_input:
            # Add user message
            st.session_state.chat_history.append({"content": user_input, "is_user": True})
            
            # Create agent and load data
            agent = create_agent()
            if st.session_state.loaded_data is not None:
                agent.df = st.session_state.loaded_data.copy()
                agent._data_loaded = True
                agent.column_info = {col: str(dtype) for col, dtype in df.dtypes.items()}
            
            # Get response
            with st.spinner("🤔 Thinking..."):
                result = agent.process_query(user_input)
                response = result.get("response", "No response")
            
            # Add AI response
            st.session_state.chat_history.append({"content": response, "is_user": False})
            st.rerun()
    
    with tab2:
        # Data Preview
        st.markdown("### 📋 Data Preview")
        st.dataframe(df, use_container_width=True)
        
        # Download button
        csv_data = df.to_csv(index=False)
        st.download_button(
            label="📥 Download as CSV",
            data=csv_data,
            file_name=f"data_{st.session_state.current_file_name.replace('.xlsx', '')}.csv",
            mime="text/csv",
            use_container_width=True
        )
    
    with tab3:
        # Statistics
        st.markdown("### 📊 Column Statistics")
        
        # Numeric columns
        numeric_cols = df.select_dtypes(include=['number']).columns
        if len(numeric_cols) > 0:
            st.markdown("**Numeric Columns:**")
            stats_df = df[numeric_cols].describe()
            st.dataframe(stats_df, use_container_width=True)
        else:
            st.info("No numeric columns found for statistical analysis.")
        
        st.divider()
        
        # Column info
        st.markdown("**Column Information:**")
        col_info = pd.DataFrame({
            "Column Name": df.columns.tolist(),
            "Data Type": [str(dtype) for dtype in df.dtypes],
            "Non-Null Count": df.count().values,
            "Null Count": df.isnull().sum().values
        })
        st.dataframe(col_info, use_container_width=True, hide_index=True)
    
    with tab4:
        # Data Quality
        st.markdown("### ⚠️ Data Quality Report")
        
        # Missing values
        st.markdown("**Missing Values:**")
        null_counts = df.isnull().sum()
        total_missing = null_counts.sum()
        
        if total_missing == 0:
            st.success("✅ No missing values found! Your data is complete.")
        else:
            st.warning(f"⚠️ Found {total_missing} missing values total")
            null_df = pd.DataFrame({
                "Column": null_counts[null_counts > 0].index.tolist(),
                "Missing Count": null_counts[null_counts > 0].values,
                "Percentage": [(c / len(df)) * 100 for c in null_counts[null_counts > 0].values]
            })
            st.dataframe(null_df, use_container_width=True, hide_index=True)
        
        st.divider()
        
        # Duplicates
        st.markdown("**Duplicate Rows:**")
        dup_count = df.duplicated().sum()
        if dup_count == 0:
            st.success("✅ No duplicate rows found!")
        else:
            st.warning(f"⚠️ Found {dup_count:,} duplicate rows")
        
        st.divider()
        
        # Data types
        st.markdown("**Data Types:**")
        for col, dtype in df.dtypes.items():
            st.info(f"**{col}**: {dtype}")

# =============================================================================
# Footer
# =============================================================================

st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 2rem;">
    <p>Built with ❤️ using Streamlit | AI Excel Agent © 2024</p>
</div>
""", unsafe_allow_html=True)
