"""
Simple Gradio Frontend for AI Excel Agent

Alternative to Streamlit - lighter and faster to install.
"""

import os
import sys
from pathlib import Path
import gradio as gr
import pandas as pd

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

from agent import AIExcelAgent, create_agent
from tools import ExcelTools


# Global agent storage
agents = {}


def get_agent(session_id: str = "default") -> AIExcelAgent:
    """Get or create agent for session."""
    if session_id not in agents:
        agents[session_id] = create_agent()
    return agents[session_id]


def upload_file(file, api_key: str, session_id: str = "default"):
    """Handle file upload."""
    if file is None:
        return "Please upload a file first.", None
    
    try:
        agent = get_agent(session_id)
        
        # Set API key if provided
        if api_key:
            agent.set_api_key(api_key)
        
        # Load the file
        result = agent.direct_tool_call("read_excel", file_path=file.name)
        
        if result.get("success"):
            df = agent.get_dataframe()
            summary = agent.direct_tool_call("summarize_data")
            
            summary_text = f"✅ Loaded: {os.path.basename(file.name)}\n"
            summary_text += f"Rows: {result.get('rows')}\n"
            summary_text += f"Columns: {', '.join(result.get('columns', []))}"
            
            return summary_text, df.head(10)
        else:
            return f"Error: {result.get('message')}", None
            
    except Exception as e:
        return f"Error: {str(e)}", None


def process_query(query, api_key: str, session_id: str = "default"):
    """Process natural language query."""
    if not query:
        return "Please enter a query.", None
    
    agent = get_agent(session_id)
    
    if api_key:
        agent.set_api_key(api_key)
    
    try:
        # Check if data is loaded
        df = agent.get_dataframe()
        if df is None:
            return "Please upload a file first.", None
        
        if api_key:
            result = agent.process_query(query)
            response = result.get("response", "No response")
        else:
            # Simple query handling without AI
            response = f"Query received: '{query}'\n\nPlease add your OpenAI API key for AI-powered responses."
        
        # Return updated data if available
        df = agent.get_dataframe()
        return response, df.head(10) if df is not None else None
        
    except Exception as e:
        return f"Error: {str(e)}", None


def summarize_data(api_key: str, session_id: str = "default"):
    """Generate data summary."""
    agent = get_agent(session_id)
    df = agent.get_dataframe()
    
    if df is None:
        return "No data loaded.", None
    
    try:
        summary = agent.direct_tool_call("summarize_data")
        
        if summary.get("success"):
            text = f"📊 Data Summary\n\n"
            text += f"Total Rows: {summary.get('total_rows')}\n"
            text += f"Total Columns: {summary.get('total_columns')}\n"
            text += f"Memory (MB): {summary.get('memory_usage_mb')}\n"
            text += f"Numeric Columns: {', '.join(summary.get('numeric_columns', []))}\n"
            text += f"Categorical Columns: {', '.join(summary.get('categorical_columns', []))}"
            
            return text, df.head(10)
        else:
            return summary.get("message"), None
            
    except Exception as e:
        return f"Error: {str(e)}", None


def clean_data(api_key: str, remove_nulls: bool, remove_dups: bool, session_id: str = "default"):
    """Clean the data."""
    agent = get_agent(session_id)
    df = agent.get_dataframe()
    
    if df is None:
        return "No data loaded.", None
    
    try:
        result = agent.direct_tool_call(
            "clean_data",
            remove_nulls=remove_nulls,
            remove_duplicates=remove_dups,
            fix_types=True
        )
        
        if result.get("success"):
            df = agent.get_dataframe()
            return f"✅ Data cleaned!\n{result.get('message')}", df.head(10)
        else:
            return result.get("message"), None
            
    except Exception as e:
        return f"Error: {str(e)}", None


def create_chart(chart_type: str, x_col: str, y_col: str, api_key: str, session_id: str = "default"):
    """Create a chart."""
    agent = get_agent(session_id)
    df = agent.get_dataframe()
    
    if df is None:
        return "No data loaded.", None
    
    try:
        result = agent.direct_tool_call(
            "create_chart",
            chart_type=chart_type,
            x_column=x_col,
            y_column=y_col,
            title=f"{chart_type.title()} Chart"
        )
        
        if result.get("success"):
            return f"✅ Chart created: {chart_type}", None
        else:
            return result.get("message"), None
            
    except Exception as e:
        return f"Error: {str(e)}", None


def export_data(api_key: str, session_id: str = "default"):
    """Export data to CSV."""
    agent = get_agent(session_id)
    df = agent.get_dataframe()
    
    if df is None:
        return "No data loaded.", None
    
    try:
        output_path = f"outputs/export_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}"
        result = agent.direct_tool_call(
            "export_data",
            output_path=output_path,
            format="csv"
        )
        
        if result.get("success"):
            return f"✅ Exported to: {result.get('output_path')}", None
        else:
            return result.get("message"), None
            
    except Exception as e:
        return f"Error: {str(e)}", None


# Build Gradio Interface
with gr.Blocks(title="AI Excel Agent", theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 📊 AI Excel Agent")
    gr.Markdown("Upload Excel files and analyze them with AI")
    
    session_id = gr.State("default")
    
    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("### Settings")
            api_key_input = gr.Textbox(
                label="OpenAI API Key",
                type="password",
                placeholder="sk-..."
            )
            
            gr.Markdown("### Upload File")
            file_upload = gr.File(
                label="Excel File",
                file_types=[".xlsx", ".xls", ".xlsm"]
            )
            upload_btn = gr.Button("Load File", variant="primary")
            
            gr.Markdown("### Quick Actions")
            summary_btn = gr.Button("📊 Summary", variant="secondary")
            
            with gr.Accordion("Clean Data"):
                clean_nulls = gr.Checkbox(label="Remove Nulls")
                clean_dups = gr.Checkbox(label="Remove Duplicates")
                clean_btn = gr.Button("Apply Cleaning")
            
            with gr.Accordion("Create Chart"):
                chart_type = gr.Dropdown(
                    ["bar", "line", "scatter", "pie", "histogram"],
                    label="Chart Type"
                )
                x_col = gr.Dropdown([], label="X Column")
                y_col = gr.Dropdown([], label="Y Column")
                chart_btn = gr.Button("Generate Chart")
            
            export_btn = gr.Button("💾 Export CSV")
        
        with gr.Column(scale=2):
            gr.Markdown("### Chat")
            chat_input = gr.Textbox(
                label="Ask about your data",
                placeholder="e.g., 'Show me the average sales'",
                lines=2
            )
            chat_btn = gr.Button("Send", variant="primary")
            
            output_text = gr.Textbox(label="Response", lines=6)
            data_preview = gr.Dataframe(label="Data Preview")
    
    # Event handlers
    upload_btn.click(
        upload_file,
        inputs=[file_upload, api_key_input, session_id],
        outputs=[output_text, data_preview]
    )
    
    chat_btn.click(
        process_query,
        inputs=[chat_input, api_key_input, session_id],
        outputs=[output_text, data_preview]
    )
    
    summary_btn.click(
        summarize_data,
        inputs=[api_key_input, session_id],
        outputs=[output_text, data_preview]
    )
    
    clean_btn.click(
        clean_data,
        inputs=[api_key_input, clean_nulls, clean_dups, session_id],
        outputs=[output_text, data_preview]
    )
    
    chart_btn.click(
        create_chart,
        inputs=[chart_type, x_col, y_col, api_key_input, session_id],
        outputs=[output_text, data_preview]
    )
    
    export_btn.click(
        export_data,
        inputs=[api_key_input, session_id],
        outputs=[output_text, data_preview]
    )


if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=8501)
