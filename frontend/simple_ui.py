"""
Simple Streamlit Frontend - AI Excel Agent
Works WITHOUT API key - Rule-based AI
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

# Page config
st.set_page_config(page_title="AI Excel Agent", page_icon="📊", layout="wide")

# Initialize session state
if "file_uploaded" not in st.session_state:
    st.session_state.file_uploaded = False
if "loaded_data" not in st.session_state:
    st.session_state.loaded_data = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Header
st.title("📊 AI Excel Agent")
st.markdown("**Upload an Excel file and ask questions!**")

# Sidebar - File Upload
with st.sidebar:
    st.header("⚙️ Settings")
    
    uploaded_file = st.file_uploader(
        "Upload Excel File",
        type=["xlsx", "xls", "xlsm"],
        key="uploader"
    )
    
    if uploaded_file is not None:
        if not st.session_state.file_uploaded:
            with st.spinner("Loading..."):
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
                    st.success(f"✅ Loaded: {result['rows']} rows, {result['columns']}")
                else:
                    st.error(f"❌ Error: {result.get('message')}")
    
    if st.session_state.file_uploaded:
        st.success("✅ File loaded!")
        if st.button("🗑️ Reset"):
            st.session_state.file_uploaded = False
            st.session_state.loaded_data = None
            st.session_state.chat_history = []
            st.rerun()

# Main content
if not st.session_state.file_uploaded:
    st.info("👈 Upload a file using the sidebar to get started!")
    
    st.markdown("### 🎯 Example Questions:")
    st.markdown("""
    - What is in the file?
    - Show me summary
    - What are the column statistics?
    - Check for missing values
    - Show the data
    """)
else:
    df = st.session_state.loaded_data
    
    # Show data preview
    st.subheader("📄 Data Preview")
    st.dataframe(df.head(10), use_container_width=True)
    
    # Show stats
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Rows", len(df))
    with col2:
        st.metric("Columns", len(df.columns))
    with col3:
        st.metric("Memory", f"{df.memory_usage(deep=True).sum()/1024**2:.2f} MB")
    
    st.divider()
    
    # Chat interface
    st.subheader("💬 Ask Questions")
    
    # Show chat history
    for msg in st.session_state.chat_history:
        if msg["is_user"]:
            st.markdown(f"**👤 You:** {msg['content']}")
        else:
            st.markdown(f"**🤖 AI:** {msg['content']}")
    
    # Input
    user_input = st.chat_input("Ask about your data...")
    
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
        with st.spinner("Thinking..."):
            result = agent.process_query(user_input)
            response = result.get("response", "No response")
        
        # Add AI response
        st.session_state.chat_history.append({"content": response, "is_user": False})
        st.rerun()
