"""
Excel Operations Tools Module

This module provides all the tools/functions that the AI agent can use
to interact with Excel files and perform data operations.
"""

import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend for server environments
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.io as pio
from typing import Optional, Dict, Any, List
from pathlib import Path
import json
import base64
from io import BytesIO


class ExcelTools:
    """
    Collection of tools for Excel file operations.
    Each tool is designed to be called by the AI agent.
    """
    
    def __init__(self):
        self.df: Optional[pd.DataFrame] = None
        self.file_path: Optional[str] = None
        self.column_info: Dict[str, str] = {}
    
    def read_excel(self, file_path: str) -> Dict[str, Any]:
        """
        Read an Excel file and load it into memory.
        
        Args:
            file_path: Path to the Excel file
            
        Returns:
            Dictionary with file info, columns, and preview
        """
        try:
            self.file_path = file_path
            self.df = pd.read_excel(file_path, engine='openpyxl')
            
            # Store column types for later reference
            self.column_info = {
                col: str(dtype) for col, dtype in self.df.dtypes.items()
            }
            
            return {
                "success": True,
                "message": f"Successfully loaded Excel file",
                "rows": len(self.df),
                "columns": list(self.df.columns),
                "column_types": self.column_info,
                "preview": self.df.head(5).to_dict('records'),
                "shape": self.df.shape
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Error reading Excel file: {str(e)}"
            }
    
    def summarize_data(self) -> Dict[str, Any]:
        """
        Generate comprehensive summary statistics of the dataset.
        
        Returns:
            Dictionary with statistical summary and insights
        """
        if self.df is None:
            return {"success": False, "message": "No data loaded. Please upload a file first."}
        
        try:
            # Separate numeric and categorical columns
            numeric_cols = self.df.select_dtypes(include=['number']).columns.tolist()
            categorical_cols = self.df.select_dtypes(include=['object', 'category']).columns.tolist()
            
            summary = {
                "success": True,
                "total_rows": len(self.df),
                "total_columns": len(self.df.columns),
                "column_names": list(self.df.columns),
                "numeric_columns": numeric_cols,
                "categorical_columns": categorical_cols,
                "memory_usage_mb": round(self.df.memory_usage(deep=True).sum() / 1024**2, 2),
                "null_counts": self.df.isnull().sum().to_dict(),
                "duplicate_rows": int(self.df.duplicated().sum())
            }
            
            # Add numeric statistics
            if numeric_cols:
                summary["numeric_stats"] = self.df[numeric_cols].describe().to_dict()
            
            # Add categorical value counts (top 5 for each)
            if categorical_cols:
                summary["categorical_stats"] = {}
                for col in categorical_cols:
                    value_counts = self.df[col].value_counts().head(5)
                    summary["categorical_stats"][col] = value_counts.to_dict()
            
            return summary
        except Exception as e:
            return {"success": False, "message": f"Error summarizing data: {str(e)}"}
    
    def query_data(
        self,
        operation: str,
        column: Optional[str] = None,
        value: Optional[Any] = None,
        columns: Optional[List[str]] = None,
        group_by: Optional[List[str]] = None,
        agg_func: Optional[str] = None,
        sort_by: Optional[str] = None,
        sort_ascending: bool = True,
        limit: Optional[int] = None,
        condition: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Perform various data operations: filtering, aggregation, sorting, grouping.
        
        Args:
            operation: Type of operation (filter, aggregate, sort, group, select)
            column: Column to operate on
            value: Value for comparison/filtering
            columns: List of columns to select
            group_by: Columns to group by
            agg_func: Aggregation function (sum, mean, count, min, max)
            sort_by: Column to sort by
            sort_ascending: Sort order
            limit: Number of rows to return
            condition: Custom filter condition (e.g., "age > 30")
            
        Returns:
            Dictionary with operation results
        """
        if self.df is None:
            return {"success": False, "message": "No data loaded."}
        
        try:
            result_df = self.df.copy()
            
            # Filtering operations
            if operation == "filter":
                if condition:
                    # Support custom conditions like "age > 30"
                    result_df = result_df.query(condition)
                elif column and value is not None:
                    result_df = result_df[result_df[column] == value]
            
            # Aggregation operations
            elif operation == "aggregate":
                if agg_func and column:
                    agg_functions = {
                        "sum": "sum",
                        "mean": "mean",
                        "avg": "mean",
                        "count": "count",
                        "min": "min",
                        "max": "max",
                        "std": "std",
                        "median": "median"
                    }
                    func = agg_functions.get(agg_func.lower(), agg_func)
                    result = getattr(result_df[column], func)()
                    
                    # Handle case where result is a Series (grouped aggregation)
                    if isinstance(result, pd.Series):
                        result_df = result.reset_index()
                        result_df.columns = ['index', column]
                    else:
                        return {
                            "success": True,
                            "operation": operation,
                            "result": float(result) if isinstance(result, (int, float)) else str(result),
                            "message": f"{agg_func} of {column}: {result}"
                        }
            
            # Grouping operations
            elif operation == "group":
                if group_by and agg_func and column:
                    agg_functions = {
                        "sum": "sum",
                        "mean": "mean",
                        "avg": "mean",
                        "count": "count",
                        "min": "min",
                        "max": "max"
                    }
                    func = agg_functions.get(agg_func.lower(), agg_func)
                    result_df = result_df.groupby(group_by)[column].agg(func).reset_index()
            
            # Sorting operations
            elif operation == "sort":
                if sort_by:
                    result_df = result_df.sort_values(
                        by=sort_by, 
                        ascending=sort_ascending
                    )
            
            # Column selection
            elif operation == "select":
                if columns:
                    result_df = result_df[columns]
            
            # Apply limit
            if limit:
                result_df = result_df.head(limit)
            
            # Convert to serializable format
            result_data = result_df.to_dict('records')
            
            # Handle non-serializable types
            for row in result_data:
                for key, val in row.items():
                    if pd.isna(val):
                        row[key] = None
                    elif isinstance(val, (pd.Timestamp, pd.DatetimeTZDtype)):
                        row[key] = str(val)
            
            return {
                "success": True,
                "operation": operation,
                "rows_returned": len(result_df),
                "columns": list(result_df.columns),
                "data": result_data[:50],  # Limit preview to 50 rows
                "total_rows": len(result_df)
            }
            
        except Exception as e:
            return {"success": False, "message": f"Error in query operation: {str(e)}"}
    
    def create_chart(
        self,
        chart_type: str,
        x_column: Optional[str] = None,
        y_column: Optional[str] = None,
        title: str = "Chart",
        group_by: Optional[str] = None,
        agg_column: Optional[str] = None,
        agg_func: str = "sum"
    ) -> Dict[str, Any]:
        """
        Create various types of charts from the data.
        
        Args:
            chart_type: Type of chart (bar, line, pie, scatter, histogram)
            x_column: Column for x-axis
            y_column: Column for y-axis
            title: Chart title
            group_by: Column to group by (for pie/bar charts)
            agg_column: Column to aggregate
            agg_func: Aggregation function
            
        Returns:
            Dictionary with chart image (base64) and plotly JSON
        """
        if self.df is None:
            return {"success": False, "message": "No data loaded."}
        
        try:
            # Prepare data for charting
            plot_df = self.df.copy()
            
            # Handle grouped data
            if group_by and agg_column:
                agg_functions = {
                    "sum": "sum",
                    "mean": "mean",
                    "avg": "mean",
                    "count": "count"
                }
                func = agg_functions.get(agg_func.lower(), agg_func)
                plot_df = plot_df.groupby(group_by)[agg_column].agg(func).reset_index()
                x_column = group_by
                y_column = agg_column
            
            # Validate columns exist
            if x_column and x_column not in plot_df.columns:
                return {"success": False, "message": f"Column '{x_column}' not found."}
            if y_column and y_column not in plot_df.columns:
                return {"success": False, "message": f"Column '{y_column}' not found."}
            
            # Create figure based on chart type
            fig = None
            
            if chart_type == "bar":
                if x_column and y_column:
                    fig = px.bar(plot_df, x=x_column, y=y_column, title=title)
                elif group_by:
                    # Auto-detect numeric column for y-axis
                    numeric_cols = plot_df.select_dtypes(include=['number']).columns
                    if len(numeric_cols) > 0:
                        y_column = numeric_cols[0]
                        fig = px.bar(plot_df, x=group_by, y=y_column, title=title)
            
            elif chart_type == "line":
                if x_column and y_column:
                    fig = px.line(plot_df, x=x_column, y=y_column, title=title)
            
            elif chart_type == "pie":
                if x_column and y_column:
                    fig = px.pie(plot_df, names=x_column, values=y_column, title=title)
                elif group_by and agg_column:
                    fig = px.pie(plot_df, names=group_by, values=agg_column, title=title)
            
            elif chart_type == "scatter":
                if x_column and y_column:
                    fig = px.scatter(plot_df, x=x_column, y=y_column, title=title)
            
            elif chart_type == "histogram":
                if x_column:
                    fig = px.histogram(plot_df, x=x_column, title=title)
                elif y_column:
                    fig = px.histogram(plot_df, x=y_column, title=title)
            
            if fig is None:
                return {
                    "success": False, 
                    "message": "Could not create chart. Please specify valid columns."
                }
            
            # Generate plotly JSON for interactive display
            plotly_json = pio.to_json(fig)
            
            # Generate static image (base64)
            img_buffer = BytesIO()
            fig.write_image(img_buffer, format='png', width=800, height=500, scale=2)
            img_buffer.seek(0)
            img_base64 = base64.b64encode(img_buffer.read()).decode('utf-8')
            
            return {
                "success": True,
                "chart_type": chart_type,
                "title": title,
                "plotly_json": plotly_json,
                "image_base64": f"data:image/png;base64,{img_base64}",
                "columns_used": {"x": x_column, "y": y_column}
            }
            
        except Exception as e:
            return {"success": False, "message": f"Error creating chart: {str(e)}"}
    
    def clean_data(
        self,
        remove_nulls: bool = False,
        fill_nulls: bool = False,
        fill_value: Any = None,
        remove_duplicates: bool = False,
        fix_types: bool = False,
        columns: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Clean the dataset by handling nulls, duplicates, and type issues.
        
        Args:
            remove_nulls: Remove rows with null values
            fill_nulls: Fill null values with specified value
            fill_value: Value to fill nulls with (default: 0 for numeric, 'Unknown' for text)
            remove_duplicates: Remove duplicate rows
            fix_types: Attempt to fix column types
            columns: Specific columns to clean (optional)
            
        Returns:
            Dictionary with cleaning results
        """
        if self.df is None:
            return {"success": False, "message": "No data loaded."}
        
        try:
            original_rows = len(self.df)
            actions_performed = []
            
            # Remove nulls
            if remove_nulls:
                if columns:
                    self.df = self.df.dropna(subset=columns)
                else:
                    self.df = self.df.dropna()
                rows_after = len(self.df)
                if rows_after < original_rows:
                    actions_performed.append(f"Removed {original_rows - rows_after} rows with nulls")
                original_rows = rows_after
            
            # Fill nulls
            if fill_nulls:
                if columns:
                    for col in columns:
                        if fill_value is not None:
                            self.df[col] = self.df[col].fillna(fill_value)
                        else:
                            # Auto-detect fill value
                            if self.df[col].dtype in ['int64', 'float64']:
                                self.df[col] = self.df[col].fillna(0)
                            else:
                                self.df[col] = self.df[col].fillna('Unknown')
                else:
                    for col in self.df.columns:
                        if fill_value is not None:
                            self.df[col] = self.df[col].fillna(fill_value)
                        else:
                            if self.df[col].dtype in ['int64', 'float64']:
                                self.df[col] = self.df[col].fillna(0)
                            else:
                                self.df[col] = self.df[col].fillna('Unknown')
                actions_performed.append("Filled null values")
            
            # Remove duplicates
            if remove_duplicates:
                original_rows = len(self.df)
                self.df = self.df.drop_duplicates()
                if len(self.df) < original_rows:
                    actions_performed.append(f"Removed {original_rows - len(self.df)} duplicate rows")
            
            # Fix types
            if fix_types:
                for col in self.df.columns:
                    # Try to convert to numeric
                    if self.df[col].dtype == 'object':
                        try:
                            self.df[col] = pd.to_numeric(self.df[col])
                            actions_performed.append(f"Converted '{col}' to numeric")
                        except (ValueError, TypeError):
                            pass  # Keep as object type
                    
                    # Convert to datetime if looks like dates
                    if self.df[col].dtype == 'object':
                        try:
                            self.df[col] = pd.to_datetime(self.df[col])
                            actions_performed.append(f"Converted '{col}' to datetime")
                        except (ValueError, TypeError):
                            pass
            
            # Update column info
            self.column_info = {
                col: str(dtype) for col, dtype in self.df.dtypes.items()
            }
            
            return {
                "success": True,
                "message": "Data cleaning completed",
                "actions_performed": actions_performed,
                "final_rows": len(self.df),
                "final_columns": len(self.df.columns),
                "column_types": self.column_info,
                "null_counts": self.df.isnull().sum().to_dict()
            }
            
        except Exception as e:
            return {"success": False, "message": f"Error cleaning data: {str(e)}"}
    
    def export_data(
        self,
        output_path: str,
        format: str = "excel",
        columns: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Export the processed data to a file.
        
        Args:
            output_path: Path for the output file
            format: Output format (excel, csv)
            columns: Specific columns to export
            
        Returns:
            Dictionary with export results
        """
        if self.df is None:
            return {"success": False, "message": "No data loaded."}
        
        try:
            export_df = self.df.copy()
            
            # Select specific columns if provided
            if columns:
                export_df = export_df[columns]
            
            # Export based on format
            if format.lower() == "excel":
                if not output_path.endswith('.xlsx'):
                    output_path += '.xlsx'
                export_df.to_excel(output_path, index=False, engine='openpyxl')
            elif format.lower() == "csv":
                if not output_path.endswith('.csv'):
                    output_path += '.csv'
                export_df.to_csv(output_path, index=False)
            else:
                return {"success": False, "message": f"Unsupported format: {format}"}
            
            return {
                "success": True,
                "message": f"Data exported successfully",
                "output_path": output_path,
                "rows_exported": len(export_df),
                "columns_exported": list(export_df.columns),
                "format": format
            }
            
        except Exception as e:
            return {"success": False, "message": f"Error exporting data: {str(e)}"}
    
    def get_dataframe(self) -> Optional[pd.DataFrame]:
        """Return the current dataframe."""
        return self.df
    
    def reset_data(self) -> Dict[str, Any]:
        """Reset the current data."""
        self.df = None
        self.file_path = None
        self.column_info = {}
        return {"success": True, "message": "Data reset successfully"}


# Create a global instance for easy access
excel_tools = ExcelTools()
