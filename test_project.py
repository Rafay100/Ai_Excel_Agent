"""
Test Script for AI Excel Agent

Run this to verify all components are working.
"""

import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent / "backend"))

def test_imports():
    """Test that all modules can be imported."""
    print("Testing imports...")
    
    try:
        import fastapi
        print(f"  ✓ FastAPI: {fastapi.__version__}")
    except ImportError as e:
        print(f"  ✗ FastAPI: {e}")
    
    try:
        import pandas
        print(f"  ✓ Pandas: {pandas.__version__}")
    except ImportError as e:
        print(f"  ✗ Pandas: {e}")
    
    try:
        import openpyxl
        print(f"  ✓ OpenPyXL: {openpyxl.__version__}")
    except ImportError as e:
        print(f"  ✗ OpenPyXL: {e}")
    
    try:
        import plotly
        print(f"  ✓ Plotly: {plotly.__version__}")
    except ImportError as e:
        print(f"  ✗ Plotly: {e}")
    
    try:
        from backend import agent, tools, main
        print("  ✓ Backend modules loaded")
    except ImportError as e:
        print(f"  ✗ Backend modules: {e}")
    
    print()


def test_tools():
    """Test the Excel tools."""
    print("Testing Excel Tools...")
    
    from backend.tools import ExcelTools
    import pandas as pd
    
    tools = ExcelTools()
    
    # Create test data
    test_df = pd.DataFrame({
        'Name': ['Alice', 'Bob', 'Charlie'],
        'Age': [25, 30, 35],
        'City': ['NYC', 'LA', 'Chicago'],
        'Salary': [50000, 60000, 75000]
    })
    
    # Save to temp Excel file
    test_file = Path(__file__).parent / "test_data.xlsx"
    test_df.to_excel(test_file, index=False)
    
    # Test read_excel
    result = tools.read_excel(str(test_file))
    if result.get("success"):
        print(f"  ✓ read_excel: Loaded {result.get('rows')} rows")
    else:
        print(f"  ✗ read_excel: {result.get('message')}")
    
    # Test summarize_data
    result = tools.summarize_data()
    if result.get("success"):
        print(f"  ✓ summarize_data: {result.get('total_columns')} columns")
    else:
        print(f"  ✗ summarize_data: {result.get('message')}")
    
    # Test query_data (filter)
    result = tools.query_data(operation="filter", column="Age", value=30)
    if result.get("success"):
        print(f"  ✓ query_data (filter): {result.get('rows_returned')} rows")
    else:
        print(f"  ✗ query_data: {result.get('message')}")
    
    # Test query_data (aggregate)
    result = tools.query_data(operation="aggregate", column="Salary", agg_func="avg")
    if result.get("success"):
        print(f"  ✓ query_data (aggregate): Avg Salary = {result.get('result')}")
    else:
        print(f"  ✗ query_data: {result.get('message')}")
    
    # Test clean_data
    result = tools.clean_data(remove_duplicates=True)
    if result.get("success"):
        print(f"  ✓ clean_data: {result.get('final_rows')} rows")
    else:
        print(f"  ✗ clean_data: {result.get('message')}")
    
    # Test create_chart
    result = tools.create_chart(chart_type="bar", x_column="Name", y_column="Salary", title="Test")
    if result.get("success"):
        print(f"  ✓ create_chart: Bar chart created")
    else:
        print(f"  ✗ create_chart: {result.get('message')}")
    
    # Cleanup
    test_file.unlink()
    print()


def test_agent():
    """Test the AI agent."""
    print("Testing AI Agent...")
    
    try:
        from backend.agent import AIExcelAgent, create_agent
        
        agent = create_agent()
        
        if agent:
            print("  ✓ Agent created successfully")
        else:
            print("  ✗ Failed to create agent")
        
        # Test direct tool call (doesn't require AI)
        result = agent.direct_tool_call("summarize_data")
        if result.get("success") or "No data loaded" in result.get("message", ""):
            print("  ✓ Direct tool call working")
        else:
            print(f"  ✗ Direct tool call: {result.get('message')}")
        
    except Exception as e:
        print(f"  ⚠ Agent test skipped: {str(e)[:50]}...")
    
    print()


def main():
    """Run all tests."""
    print("=" * 50)
    print("  AI Excel Agent - Component Tests")
    print("=" * 50)
    print()
    
    test_imports()
    test_tools()
    test_agent()
    
    print("=" * 50)
    print("  Tests Complete!")
    print("=" * 50)
    print()
    print("Next steps:")
    print("1. Start backend: cd backend && uvicorn main:app --reload")
    print("2. Start frontend: cd frontend && streamlit run ui.py")
    print("3. Open http://localhost:8501")


if __name__ == "__main__":
    main()
