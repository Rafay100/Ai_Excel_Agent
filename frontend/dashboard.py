"""
Dashboard Page for AI Excel Agent

Advanced analytics dashboard with visualizations and insights.
"""

import sys
from pathlib import Path
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))
from agent import AIExcelAgent, create_agent


def render_dashboard():
    """Render the analytics dashboard."""
    
    st.set_page_config(
        page_title="Dashboard | AI Excel Agent",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
        
        .stApp {
            font-family: 'Inter', sans-serif;
        }
        
        .dashboard-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 2rem;
            border-radius: 1rem;
            margin-bottom: 2rem;
            color: white;
        }
        
        .dashboard-header h1 {
            margin: 0;
            font-size: 2.5rem;
        }
        
        .kpi-card {
            background: white;
            padding: 1.5rem;
            border-radius: 0.75rem;
            box-shadow: 0 4px 15px rgba(0,0,0,0.08);
            border-left: 4px solid #667eea;
            transition: transform 0.2s;
        }
        
        .kpi-card:hover {
            transform: translateY(-3px);
        }
        
        .kpi-value {
            font-size: 2rem;
            font-weight: 700;
            color: #667eea;
        }
        
        .kpi-label {
            color: #666;
            font-size: 0.9rem;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        .chart-container {
            background: white;
            padding: 1.5rem;
            border-radius: 0.75rem;
            box-shadow: 0 4px 15px rgba(0,0,0,0.08);
            margin-bottom: 1.5rem;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown("""
    <div class="dashboard-header">
        <h1>📊 Analytics Dashboard</h1>
        <p>Advanced data insights and visualizations</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Check if data is loaded
    agent = create_agent()
    df = agent.get_dataframe()
    
    if df is None:
        st.info("👈 Please upload a file from the main page to view the dashboard")
        st.stop()
    
    # KPI Row
    st.markdown("### Key Metrics")
    col1, col2, col3, col4, col5 = st.columns(5)
    
    numeric_df = df.select_dtypes(include=['number'])
    
    with col1:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-value">{len(df):,}</div>
            <div class="kpi-label">Total Rows</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-value">{len(df.columns)}</div>
            <div class="kpi-label">Columns</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-value">{df.duplicated().sum():,}</div>
            <div class="kpi-label">Duplicates</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        null_count = df.isnull().sum().sum()
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-value">{null_count:,}</div>
            <div class="kpi-label">Missing Values</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col5:
        mem_mb = round(df.memory_usage(deep=True).sum() / 1024**2, 2)
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-value">{mem_mb}</div>
            <div class="kpi-label">Memory (MB)</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.divider()
    
    # Charts Row 1
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("##### Distribution Overview")
        if len(numeric_df.columns) > 0:
            first_numeric = numeric_df.columns[0]
            fig = px.histogram(
                df, 
                x=first_numeric, 
                nbins=30,
                title=f"Distribution of {first_numeric}",
                color_discrete_sequence=['#667eea']
            )
            fig.update_layout(showlegend=False, height=400)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No numeric data for histogram")
    
    with col2:
        st.markdown("##### Correlation Heatmap")
        if len(numeric_df.columns) > 1:
            corr_matrix = numeric_df.corr()
            fig = px.imshow(
                corr_matrix,
                color_continuous_scale='RdBu_r',
                title='Feature Correlation',
                aspect='auto'
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Need at least 2 numeric columns")
    
    # Charts Row 2
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("##### Box Plot Analysis")
        if len(numeric_df.columns) > 0:
            first_numeric = numeric_df.columns[0]
            fig = px.box(
                df, 
                y=first_numeric,
                title=f"{first_numeric} - Box Plot",
                color_discrete_sequence=['#764ba2']
            )
            fig.update_layout(showlegend=False, height=400)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No numeric data for box plot")
    
    with col2:
        st.markdown("##### Data Quality")
        quality_data = pd.DataFrame({
            'Column': df.columns.tolist(),
            'Missing': df.isnull().sum().values,
            'Complete': (len(df) - df.isnull().sum()).values
        })
        
        fig = go.Figure(data=[
            go.Bar(
                name='Complete',
                x=quality_data['Column'],
                y=quality_data['Complete'],
                marker_color='#667eea'
            ),
            go.Bar(
                name='Missing',
                x=quality_data['Column'],
                y=quality_data['Missing'],
                marker_color='#ff6b6b'
            )
        ])
        
        fig.update_layout(
            barmode='stack',
            title='Data Completeness by Column',
            height=400,
            showlegend=True
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Data Summary
    st.divider()
    st.markdown("### 📋 Detailed Statistics")
    
    if len(numeric_df.columns) > 0:
        stats_df = numeric_df.describe()
        st.dataframe(stats_df, use_container_width=True)
    
    # Raw Data
    st.divider()
    st.markdown("### 📄 Raw Data Preview")
    st.dataframe(df.head(50), use_container_width=True, hide_index=True)


if __name__ == "__main__":
    render_dashboard()
