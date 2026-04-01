"""
FastAPI Backend for AI Excel Agent

This module provides the REST API endpoints for the AI Excel Agent,
handling file uploads, queries, and data operations.
"""

import os
import uuid
import shutil
from typing import Optional, Dict, Any, List
from pathlib import Path

from fastapi import FastAPI, UploadFile, File, HTTPException, Depends, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from pydantic import BaseModel

from agent import AIExcelAgent, create_agent


# =============================================================================
# Configuration
# =============================================================================

UPLOAD_DIR = Path(__file__).parent.parent / "uploads"
OUTPUT_DIR = Path(__file__).parent.parent / "outputs"

# Ensure directories exist
UPLOAD_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)

# =============================================================================
# FastAPI App
# =============================================================================

app = FastAPI(
    title="AI Excel Agent API",
    description="REST API for AI-powered Excel data analysis and manipulation",
    version="1.0.0"
)

# Enable CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =============================================================================
# Global State
# =============================================================================

# Store agent instances per session
agents: Dict[str, AIExcelAgent] = {}

# =============================================================================
# Pydantic Models
# =============================================================================

class QueryRequest(BaseModel):
    """Request model for natural language queries."""
    query: str
    session_id: Optional[str] = None


class ToolRequest(BaseModel):
    """Request model for direct tool calls."""
    tool_name: str
    parameters: Dict[str, Any]
    session_id: Optional[str] = None


class APIKeyRequest(BaseModel):
    """Request model for setting API key."""
    api_key: str
    session_id: Optional[str] = None


class ChartRequest(BaseModel):
    """Request model for chart generation."""
    chart_type: str
    x_column: Optional[str] = None
    y_column: Optional[str] = None
    title: str = "Chart"
    group_by: Optional[str] = None
    agg_column: Optional[str] = None
    agg_func: str = "sum"
    session_id: Optional[str] = None


class CleanDataRequest(BaseModel):
    """Request model for data cleaning."""
    remove_nulls: bool = False
    fill_nulls: bool = False
    fill_value: Optional[Any] = None
    remove_duplicates: bool = False
    fix_types: bool = False
    columns: Optional[List[str]] = None
    session_id: Optional[str] = None


class ExportRequest(BaseModel):
    """Request model for data export."""
    format: str = "excel"
    columns: Optional[List[str]] = None
    session_id: Optional[str] = None


# =============================================================================
# Helper Functions
# =============================================================================

def get_or_create_agent(session_id: Optional[str] = None) -> AIExcelAgent:
    """
    Get existing agent or create a new one for the session.
    
    Args:
        session_id: Unique session identifier
        
    Returns:
        AIExcelAgent instance
    """
    if session_id and session_id in agents:
        return agents[session_id]
    
    # Create new session
    session_id = session_id or str(uuid.uuid4())
    agent = create_agent()
    agents[session_id] = agent
    return agent


def save_uploaded_file(file: UploadFile, session_id: str) -> str:
    """
    Save uploaded file to the uploads directory.
    
    Args:
        file: Uploaded file
        session_id: Session identifier
        
    Returns:
        Path to saved file
    """
    file_extension = Path(file.filename).suffix if file.filename else ".xlsx"
    file_path = UPLOAD_DIR / f"{session_id}{file_extension}"
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    return str(file_path)


# =============================================================================
# API Endpoints
# =============================================================================

@app.get("/")
async def root():
    """Root endpoint - API health check."""
    return {
        "status": "online",
        "service": "AI Excel Agent API",
        "version": "1.0.0"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


@app.post("/api/set-api-key")
async def set_api_key(request: APIKeyRequest):
    """
    Set OpenAI API key for a session.
    
    This enables the AI agent to process natural language queries.
    """
    try:
        agent = get_or_create_agent(request.session_id)
        agent.set_api_key(request.api_key)
        
        session_id = request.session_id or str(uuid.uuid4())
        agents[session_id] = agent
        
        return {
            "success": True,
            "message": "API key set successfully",
            "session_id": session_id
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/upload")
async def upload_file(
    file: UploadFile = File(...),
    session_id: Optional[str] = Form(None)
):
    """
    Upload an Excel file for analysis.
    
    Returns file information and preview of the data.
    """
    # Validate file type
    allowed_extensions = [".xlsx", ".xls", ".xlsm"]
    file_extension = Path(file.filename).suffix.lower() if file.filename else ""
    
    if file_extension not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type. Allowed: {', '.join(allowed_extensions)}"
        )
    
    try:
        # Generate or use existing session ID
        session_id = session_id or str(uuid.uuid4())
        
        # Save the file
        file_path = save_uploaded_file(file, session_id)
        
        # Get or create agent and load the file
        agent = get_or_create_agent(session_id)
        agents[session_id] = agent
        
        # Read the Excel file
        result = agent.direct_tool_call("read_excel", file_path=file_path)
        
        if not result.get("success"):
            raise HTTPException(status_code=400, detail=result.get("message"))
        
        return {
            "success": True,
            "session_id": session_id,
            "file_name": file.filename,
            "file_path": file_path,
            "data": result
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/query")
async def process_query(request: QueryRequest):
    """
    Process a natural language query about the data.
    
    The AI agent will analyze the query and perform appropriate operations.
    """
    try:
        agent = get_or_create_agent(request.session_id)
        
        if not agent:
            raise HTTPException(status_code=400, detail="No data loaded. Please upload a file first.")
        
        result = agent.process_query(request.query)
        
        return {
            "success": result.get("success", False),
            "response": result.get("response"),
            "session_id": request.session_id
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/tool")
async def call_tool(request: ToolRequest):
    """
    Directly call a specific tool with parameters.
    
    Available tools: read_excel, summarize_data, query_data, 
    create_chart, clean_data, export_data
    """
    try:
        agent = get_or_create_agent(request.session_id)
        result = agent.direct_tool_call(request.tool_name, **request.parameters)
        
        return {
            "success": result.get("success", False),
            "data": result,
            "session_id": request.session_id
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/summarize")
async def summarize_data(session_id: Optional[str] = None):
    """
    Get summary statistics of the loaded dataset.
    """
    try:
        agent = get_or_create_agent(session_id)
        result = agent.direct_tool_call("summarize_data")
        
        return {
            "success": result.get("success", False),
            "data": result,
            "session_id": session_id
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/chart")
async def generate_chart(request: ChartRequest):
    """
    Generate a chart from the loaded data.
    
    Returns chart image (base64) and plotly JSON for interactive display.
    """
    try:
        agent = get_or_create_agent(request.session_id)
        
        params = {
            "chart_type": request.chart_type,
            "x_column": request.x_column,
            "y_column": request.y_column,
            "title": request.title,
            "group_by": request.group_by,
            "agg_column": request.agg_column,
            "agg_func": request.agg_func
        }
        
        result = agent.direct_tool_call("create_chart", **params)
        
        return {
            "success": result.get("success", False),
            "data": result,
            "session_id": request.session_id
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/clean")
async def clean_data(request: CleanDataRequest):
    """
    Clean the loaded dataset.
    
    Options include removing nulls, filling nulls, removing duplicates,
    and fixing data types.
    """
    try:
        agent = get_or_create_agent(request.session_id)
        
        params = {
            "remove_nulls": request.remove_nulls,
            "fill_nulls": request.fill_nulls,
            "fill_value": request.fill_value,
            "remove_duplicates": request.remove_duplicates,
            "fix_types": request.fix_types,
            "columns": request.columns
        }
        
        result = agent.direct_tool_call("clean_data", **params)
        
        return {
            "success": result.get("success", False),
            "data": result,
            "session_id": request.session_id
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/export")
async def export_data(request: ExportRequest):
    """
    Export the processed data to a file.
    
    Returns a download link for the exported file.
    """
    try:
        agent = get_or_create_agent(request.session_id)
        
        if not request.session_id:
            raise HTTPException(status_code=400, detail="Session ID required for export")
        
        output_filename = f"{request.session_id}_export"
        output_path = OUTPUT_DIR / output_filename
        
        params = {
            "output_path": str(output_path),
            "format": request.format,
            "columns": request.columns
        }
        
        result = agent.direct_tool_call("export_data", **params)
        
        if result.get("success"):
            return {
                "success": True,
                "data": result,
                "download_url": f"/api/download/{output_filename}.{request.format}",
                "session_id": request.session_id
            }
        else:
            return {
                "success": False,
                "message": result.get("message"),
                "session_id": request.session_id
            }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/download/{filename}")
async def download_file(filename: str):
    """
    Download an exported file.
    """
    file_path = OUTPUT_DIR / filename
    
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")
    
    return FileResponse(
        path=file_path,
        filename=filename,
        media_type="application/octet-stream"
    )


@app.get("/api/data")
async def get_data(
    session_id: Optional[str] = None,
    limit: int = 100
):
    """
    Get the current data preview.
    """
    try:
        agent = get_or_create_agent(session_id)
        df = agent.get_dataframe()
        
        if df is None:
            return {
                "success": False,
                "message": "No data loaded",
                "session_id": session_id
            }
        
        # Limit rows and convert to dict
        preview_df = df.head(limit)
        preview_data = preview_df.to_dict('records')
        
        # Handle non-serializable types
        for row in preview_data:
            for key, val in row.items():
                if hasattr(val, 'isoformat'):  # datetime
                    row[key] = val.isoformat()
                elif val != val:  # NaN check
                    row[key] = None
        
        return {
            "success": True,
            "data": preview_data,
            "columns": list(df.columns),
            "total_rows": len(df),
            "session_id": session_id
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/columns")
async def get_columns(session_id: Optional[str] = None):
    """
    Get information about the loaded columns.
    """
    try:
        agent = get_or_create_agent(session_id)
        column_info = agent.get_column_info()
        
        return {
            "success": True,
            "columns": column_info,
            "session_id": session_id
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/api/session/{session_id}")
async def delete_session(session_id: str):
    """
    Delete a session and clean up resources.
    """
    try:
        if session_id in agents:
            agents[session_id].reset()
            del agents[session_id]
        
        # Clean up uploaded file
        upload_file = UPLOAD_DIR / f"{session_id}*"
        for f in UPLOAD_DIR.glob(f"{session_id}*"):
            f.unlink()
        
        return {
            "success": True,
            "message": "Session deleted successfully"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/reset")
async def reset_session(session_id: Optional[str] = None):
    """
    Reset the current session (clear data but keep API key).
    """
    try:
        if session_id and session_id in agents:
            agents[session_id].reset()
        
        return {
            "success": True,
            "message": "Session reset successfully",
            "session_id": session_id
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# =============================================================================
# Main Entry Point
# =============================================================================

if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=True
    )
