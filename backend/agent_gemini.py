"""
AI Agent Module - Works WITHOUT API Key
Uses smart rule-based responses for common Excel questions
"""

import json
import re
from typing import Dict, Any, Optional


class AIExcelAgent:
    """AI Agent with rule-based responses (no API needed)."""

    def __init__(self, api_key: Optional[str] = None, model: str = "rule-based"):
        self.api_key = api_key
        self.model = model
        self.init_error = None
        self.df = None
        self.column_info = {}
        self._data_loaded = False

    def set_api_key(self, api_key: str):
        """Set API key (not used in rule-based mode)."""
        self.api_key = api_key

    def load_excel(self, file_path: str) -> Dict[str, Any]:
        """Load Excel file."""
        try:
            import pandas as pd
            import os
            
            print(f"[DEBUG] Loading Excel from: {file_path}")
            print(f"[DEBUG] File exists: {os.path.exists(file_path)}")
            
            df_temp = pd.read_excel(file_path, engine='openpyxl')
            self.df = df_temp.copy()
            self._data_loaded = True
            
            print(f"[DEBUG] Loaded {len(self.df)} rows, {len(self.df.columns)} columns")

            cols = list(self.df.columns)
            self.column_info = {}
            for col in cols:
                try:
                    self.column_info[col] = str(self.df[col].dtype)
                except:
                    self.column_info[col] = "unknown"

            return {
                "success": True,
                "rows": len(self.df),
                "columns": cols
            }
        except Exception as e:
            print(f"[DEBUG] Error loading Excel: {str(e)}")
            return {"success": False, "message": str(e)}

    def get_summary(self) -> Dict[str, Any]:
        """Get data summary."""
        if not self._data_loaded or self.df is None:
            return {"success": False, "message": "No data loaded"}
        try:
            return {
                "success": True,
                "total_rows": len(self.df),
                "total_columns": len(self.df.columns),
                "column_names": list(self.df.columns)
            }
        except Exception as e:
            return {"success": False, "message": str(e)}

    def _smart_response(self, query: str) -> str:
        """Generate smart rule-based responses."""
        query_lower = query.lower()
        
        if self.df is None:
            return "No data loaded. Please upload an Excel file first."
        
        # Summary questions
        if any(word in query_lower for word in ["summary", "summarize", "overview", "about", "what in", "what's in", "what is in"]):
            return self._get_data_summary()
        
        # Column questions
        if any(word in query_lower for word in ["column", "field", "attribute"]):
            if "statistic" in query_lower or "stats" in query_lower:
                return self._get_column_stats()
            if "name" in query_lower or "list" in query_lower:
                return f"The dataset has {len(self.df.columns)} columns: {', '.join(self.df.columns)}"
        
        # Row questions
        if "row" in query_lower:
            if "how many" in query_lower or "count" in query_lower:
                return f"The dataset has {len(self.df):,} rows."
            if "show" in query_lower or "display" in query_lower:
                return f"Here are the first 5 rows:\n\n{self.df.head().to_string()}"
        
        # Statistics questions
        if any(word in query_lower for word in ["statistic", "stats", "average", "mean", "median", "min", "max", "total", "sum"]):
            return self._get_statistics(query_lower)
        
        # Salary questions (common use case)
        if "salary" in query_lower:
            return self._get_salary_info(query_lower)
        
        # Sales questions
        if "sales" in query_lower:
            return self._get_sales_info(query_lower)
        
        # Data types
        if "type" in query_lower or "dtype" in query_lower:
            return self._get_data_types()
        
        # Missing values
        if any(word in query_lower for word in ["missing", "null", "empty", "nan"]):
            return self._get_missing_values()
        
        # Default response with data info
        return self._get_data_summary()

    def _get_data_summary(self) -> str:
        """Get data summary."""
        summary = f"📊 **Dataset Summary**\n\n"
        summary += f"• **Total Rows:** {len(self.df):,}\n"
        summary += f"• **Total Columns:** {len(self.df.columns)}\n"
        summary += f"• **Columns:** {', '.join(self.df.columns)}\n"
        
        # Memory
        mem_mb = self.df.memory_usage(deep=True).sum() / 1024**2
        summary += f"• **Memory Usage:** {mem_mb:.2f} MB\n"
        
        # Duplicates
        dup_count = self.df.duplicated().sum()
        summary += f"• **Duplicate Rows:** {dup_count}\n"
        
        return summary

    def _get_column_stats(self) -> str:
        """Get column statistics."""
        stats = "📊 **Column Statistics**\n\n"
        
        numeric_cols = self.df.select_dtypes(include=['number']).columns
        if len(numeric_cols) > 0:
            stats += "**Numeric Columns:**\n"
            for col in numeric_cols:
                stats += f"\n• **{col}:**\n"
                stats += f"  - Mean: {self.df[col].mean():.2f}\n"
                stats += f"  - Median: {self.df[col].median():.2f}\n"
                stats += f"  - Min: {self.df[col].min():.2f}\n"
                stats += f"  - Max: {self.df[col].max():.2f}\n"
                stats += f"  - Std Dev: {self.df[col].std():.2f}\n"
        
        return stats

    def _get_statistics(self, query: str) -> str:
        """Get specific statistics."""
        numeric_cols = self.df.select_dtypes(include=['number']).columns
        
        if len(numeric_cols) == 0:
            return "No numeric columns found for statistical analysis."
        
        stats = "📊 **Statistics**\n\n"
        for col in numeric_cols[:5]:  # Limit to first 5 numeric columns
            stats += f"**{col}:**\n"
            if "average" in query or "mean" in query:
                stats += f"  • Average: {self.df[col].mean():.2f}\n"
            if "median" in query:
                stats += f"  • Median: {self.df[col].median():.2f}\n"
            if "min" in query:
                stats += f"  • Minimum: {self.df[col].min():.2f}\n"
            if "max" in query:
                stats += f"  • Maximum: {self.df[col].max():.2f}\n"
            if "sum" in query or "total" in query:
                stats += f"  • Total: {self.df[col].sum():.2f}\n"
            if "std" in query or "deviation" in query:
                stats += f"  • Std Dev: {self.df[col].std():.2f}\n"
            stats += "\n"
        
        return stats

    def _get_salary_info(self, query: str) -> str:
        """Get salary information."""
        # Look for salary column
        salary_col = None
        for col in self.df.columns:
            if 'salary' in col.lower() or 'pay' in col.lower() or 'income' in col.lower():
                salary_col = col
                break
        
        if salary_col is None:
            # Try first numeric column
            numeric_cols = self.df.select_dtypes(include=['number']).columns
            if len(numeric_cols) > 0:
                salary_col = numeric_cols[0]
            else:
                return "No salary or numeric column found."
        
        info = f"💰 **Salary Information** (from column: {salary_col})\n\n"
        info += f"• **Average Salary:** {self.df[salary_col].mean():,.2f}\n"
        info += f"• **Median Salary:** {self.df[salary_col].median():,.2f}\n"
        info += f"• **Min Salary:** {self.df[salary_col].min():,.2f}\n"
        info += f"• **Max Salary:** {self.df[salary_col].max():,.2f}\n"
        info += f"• **Total Payroll:** {self.df[salary_col].sum():,.2f}\n"
        
        return info

    def _get_sales_info(self, query: str) -> str:
        """Get sales information."""
        # Look for sales column
        sales_col = None
        for col in self.df.columns:
            if 'sales' in col.lower() or 'revenue' in col.lower() or 'amount' in col.lower():
                sales_col = col
                break
        
        if sales_col is None:
            numeric_cols = self.df.select_dtypes(include=['number']).columns
            if len(numeric_cols) > 0:
                sales_col = numeric_cols[0]
            else:
                return "No sales or numeric column found."
        
        info = f"📈 **Sales Information** (from column: {sales_col})\n\n"
        info += f"• **Total Sales:** {self.df[sales_col].sum():,.2f}\n"
        info += f"• **Average Sale:** {self.df[sales_col].mean():,.2f}\n"
        info += f"• **Min Sale:** {self.df[sales_col].min():,.2f}\n"
        info += f"• **Max Sale:** {self.df[sales_col].max():,.2f}\n"
        
        return info

    def _get_data_types(self) -> str:
        """Get data types for all columns."""
        types = "📋 **Column Data Types**\n\n"
        for col, dtype in self.column_info.items():
            types += f"• **{col}:** {dtype}\n"
        return types

    def _get_missing_values(self) -> str:
        """Get missing values information."""
        missing = self.df.isnull().sum()
        total_missing = missing.sum()
        
        if total_missing == 0:
            return "✅ No missing values found! Your data is complete."
        
        info = f"⚠️ **Missing Values Report**\n\n"
        info += f"Total missing values: {total_missing}\n\n"
        
        for col, count in missing.items():
            if count > 0:
                pct = (count / len(self.df)) * 100
                info += f"• **{col}:** {count} ({pct:.1f}%)\n"
        
        return info

    def process_query(self, query: str) -> Dict[str, Any]:
        """Process query using rule-based AI."""
        try:
            response = self._smart_response(query)
            return {
                "success": True,
                "response": response,
                "has_data": self._data_loaded
            }
        except Exception as e:
            return {
                "success": False,
                "response": f"Error: {str(e)}"
            }

    def direct_tool_call(self, tool_name: str, **kwargs) -> Dict[str, Any]:
        """Direct tool call."""
        if tool_name == "read_excel":
            return self.load_excel(kwargs.get("file_path", ""))
        elif tool_name == "summarize_data":
            return self.get_summary()
        else:
            return {"success": False, "message": f"Unknown tool: {tool_name}"}

    def get_dataframe(self):
        """Get current dataframe."""
        return self.df if self._data_loaded else None

    def reset(self):
        """Reset agent state."""
        self.df = None
        self.column_info = {}
        self._data_loaded = False


def create_agent(api_key: Optional[str] = None, model: str = "rule-based") -> AIExcelAgent:
    """Create agent instance."""
    return AIExcelAgent(api_key=api_key, model=model)
