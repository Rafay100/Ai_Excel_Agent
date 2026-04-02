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
        query_lower = query.lower().strip()
        
        if self.df is None:
            return "❌ No data loaded. Please upload an Excel file first."
        
        # Greeting
        if query_lower in ["hi", "hello", "hey", "start"]:
            return f"👋 Hello! I'm your AI Excel Agent. Your file has **{len(self.df):,} rows** and **{len(self.df.columns)} columns**. Ask me anything about your data!"
        
        # Summary questions - be more specific
        if any(phrase in query_lower for phrase in ["summary", "summarize", "overview"]):
            return self._get_data_summary()
        
        if any(phrase in query_lower for phrase in ["what is in", "whats in", "what's in", "about this file", "tell me about this"]):
            return self._get_data_summary()
        
        # Column names/list - be specific
        if any(phrase in query_lower for phrase in ["column names", "list columns", "what columns", "name of columns"]):
            return f"📋 **Column Names:**\n\nThis dataset has **{len(self.df.columns)} columns**:\n\n" + "\n".join([f"• {col}" for col in self.df.columns])
        
        # Column statistics - be specific
        if any(phrase in query_lower for phrase in ["column statistic", "column stats", "describe columns"]):
            return self._get_column_stats()
        
        # Statistics - general
        if query_lower in ["statistics", "stats", "show statistics", "show stats"]:
            return self._get_column_stats()
        
        # Row count questions - be specific
        if any(phrase in query_lower for phrase in ["how many rows", "row count", "number of rows", "total rows"]):
            return f"📊 **Row Count:**\n\nThe dataset has **{len(self.df):,} rows**."
        
        # Show data/display - be specific
        if "show" in query_lower and "row" in query_lower:
            try:
                nums = [int(s) for s in query_lower.split() if s.isdigit()]
                num = nums[0] if nums else 5
                return f"📋 **First {num} Rows:**\n\n{self.df.head(num).to_string()}"
            except:
                return f"📋 **First 5 Rows:**\n\n{self.df.head(5).to_string()}"
        
        if "display" in query_lower and "row" in query_lower:
            return f"📋 **First 5 Rows:**\n\n{self.df.head(5).to_string()}"
        
        # Missing values - be specific
        if any(phrase in query_lower for phrase in ["missing values", "missing data", "null values", "check for missing", "any missing"]):
            return self._get_missing_values()
        
        # Duplicates - be specific
        if any(phrase in query_lower for phrase in ["duplicate", "duplicates", "any duplicates", "check duplicate"]):
            return self._get_duplicates()
        
        # Data types - be specific
        if any(phrase in query_lower for phrase in ["data types", "column types", "type of columns"]):
            return self._get_data_types()
        
        # Salary - specific
        if "salary" in query_lower:
            return self._get_salary_info(query_lower)
        
        # Sales - specific
        if "sales" in query_lower:
            return self._get_sales_info(query_lower)
        
        # Sum/total - be specific to column
        if "sum" in query_lower or "total" in query_lower:
            if "quantity" in query_lower:
                return self._get_column_sum("Quantity")
            if "sales" in query_lower:
                return self._get_column_sum("Sales")
            return self._get_totals()
        
        # Average - be specific
        if any(phrase in query_lower for phrase in ["average", "mean", "avg"]):
            return self._get_averages()
        
        # Min/Max - be specific
        if any(phrase in query_lower for phrase in ["minimum", "maximum", "min", "max", "highest", "lowest"]):
            return self._get_min_max()
        
        # Clean/remove - be specific
        if "remove" in query_lower:
            if "duplicate" in query_lower:
                return self._remove_duplicates_action()
            if "null" in query_lower or "missing" in query_lower:
                return self._remove_nulls_action()
        
        # Fill nulls
        if any(phrase in query_lower for phrase in ["fill null", "fill missing", "fill values"]):
            return self._fill_nulls_action()
        
        # Fix data types
        if any(phrase in query_lower for phrase in ["fix type", "fix data type", "correct type"]):
            return self._fix_data_types()
        
        # Clean all - complete cleaning
        if any(phrase in query_lower for phrase in ["clean all", "clean everything", "fix everything", "make clean", "clean data", "clean file", "poori tarah clean"]):
            return self._clean_all_action()
        
        # Clean - ask for clarification or do basic clean
        if "clean" in query_lower:
            return self._clean_all_action()
        
        # Default - provide general info
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
            return "✅ **No Missing Values!**\n\nYour data is complete - there are no missing or null values in any column."
        
        info = f"⚠️ **Missing Values Report**\n\n**Total missing values: {total_missing}**\n\n"
        
        for col, count in missing.items():
            if count > 0:
                pct = (count / len(self.df)) * 100
                info += f"• **{col}:** {count} missing ({pct:.1f}%)\n"
        
        return info

    def _get_duplicates(self) -> str:
        """Get duplicate rows information."""
        dup_count = self.df.duplicated().sum()
        
        if dup_count == 0:
            return "✅ **No Duplicates!**\n\nYour dataset has no duplicate rows - all records are unique."
        
        return f"⚠️ **Duplicate Rows Found**\n\nFound **{dup_count:,} duplicate rows** in the dataset.\n\nYou can remove them by asking: 'Remove duplicate rows'"

    def _get_data_types(self) -> str:
        """Get data types for all columns."""
        types = "📋 **Column Data Types**\n\n"
        for col, dtype in self.column_info.items():
            types += f"• **{col}:** `{dtype}`\n"
        return types

    def _get_averages(self) -> str:
        """Get average/mean for numeric columns."""
        numeric_cols = self.df.select_dtypes(include=['number']).columns
        
        if len(numeric_cols) == 0:
            return "No numeric columns found for average calculation."
        
        info = "📊 **Average Values**\n\n"
        for col in numeric_cols:
            avg = self.df[col].mean()
            info += f"• **{col}:** {avg:,.2f}\n"
        
        return info

    def _get_min_max(self) -> str:
        """Get min/max for numeric columns."""
        numeric_cols = self.df.select_dtypes(include=['number']).columns
        
        if len(numeric_cols) == 0:
            return "No numeric columns found."
        
        info = "📊 **Min/Max Values**\n\n"
        for col in numeric_cols:
            min_val = self.df[col].min()
            max_val = self.df[col].max()
            info += f"• **{col}:** Min={min_val:,.2f} | Max={max_val:,.2f}\n"
        
        return info

    def _get_totals(self) -> str:
        """Get sum/total for numeric columns."""
        numeric_cols = self.df.select_dtypes(include=['number']).columns
        
        if len(numeric_cols) == 0:
            return "No numeric columns found."
        
        info = "📊 **Total Values**\n\n"
        for col in numeric_cols:
            total = self.df[col].sum()
            info += f"• **{col}:** {total:,.2f}\n"
        
        return info

    def _get_column_sum(self, column_name: str) -> str:
        """Get sum for a specific column."""
        # Try to find matching column
        actual_col = None
        for col in self.df.columns:
            if column_name.lower() in col.lower():
                actual_col = col
                break
        
        if actual_col is None or actual_col not in self.df.columns:
            return f"Column '{column_name}' not found."
        
        if not pd.api.types.is_numeric_dtype(self.df[actual_col]):
            return f"Column '{actual_col}' is not numeric."
        
        total = self.df[actual_col].sum()
        return f"📊 **Sum of {actual_col}**\n\n**Total: {total:,.2f}**"

    def _filter_data(self, query: str) -> str:
        """Filter data based on simple conditions."""
        try:
            # Try to extract column name and value
            numeric_cols = self.df.select_dtypes(include=['number']).columns
            
            if len(numeric_cols) > 0:
                col = numeric_cols[0]
                # Show top 5 by first numeric column
                sorted_df = self.df.nlargest(5, col)
                return f"📊 **Top 5 by {col}:**\n\n{sorted_df.to_string()}"
            
            return "Please specify which column to filter by."
        except Exception as e:
            return f"Could not filter: {str(e)}"

    def _remove_duplicates_action(self) -> str:
        """Action to remove duplicates."""
        dup_count = self.df.duplicated().sum()
        if dup_count == 0:
            return "✅ No duplicates to remove! Your data is already clean."
        
        # Actually remove duplicates
        original_rows = len(self.df)
        self.df = self.df.drop_duplicates()
        new_rows = len(self.df)
        removed = original_rows - new_rows
        
        # Update session state via return
        return f"✅ **Duplicates Removed!**\n\n• Original rows: {original_rows}\n• New rows: {new_rows}\n• **Removed: {removed} duplicate rows**\n\nYour data is now clean!"

    def _remove_nulls_action(self) -> str:
        """Action to remove nulls."""
        missing = self.df.isnull().sum().sum()
        if missing == 0:
            return "✅ No missing values to remove! Your data is already clean."
        
        # Actually remove rows with nulls
        original_rows = len(self.df)
        self.df = self.df.dropna()
        new_rows = len(self.df)
        removed = original_rows - new_rows
        
        return f"✅ **Null Values Removed!**\n\n• Original rows: {original_rows}\n• New rows: {new_rows}\n• **Removed: {removed} rows with missing values**\n\nYour data is now clean!"

    def _fill_nulls_action(self) -> str:
        """Action to fill null values with mean/median."""
        missing = self.df.isnull().sum().sum()
        if missing == 0:
            return "✅ No missing values to fill! Your data is already complete."
        
        # Fill numeric columns with mean, text with 'Unknown'
        filled_count = 0
        for col in self.df.columns:
            if self.df[col].isnull().sum() > 0:
                if pd.api.types.is_numeric_dtype(self.df[col]):
                    self.df[col] = self.df[col].fillna(self.df[col].mean())
                else:
                    self.df[col] = self.df[col].fillna('Unknown')
                filled_count += self.df[col].notna().sum()
        
        return f"✅ **Missing Values Filled!**\n\n• Filled numeric columns with **mean**\n• Filled text columns with **'Unknown'**\n• **Total filled: {missing} values**\n\nYour data is now complete!"

    def _fix_data_types(self) -> str:
        """Fix incorrect data types."""
        changes = []
        
        for col in self.df.columns:
            # Try to convert to numeric
            if self.df[col].dtype == 'object':
                try:
                    self.df[col] = pd.to_numeric(self.df[col])
                    changes.append(f"• **{col}**: Text → Number")
                except:
                    pass
            
            # Try to convert to datetime
            if self.df[col].dtype == 'object' and 'date' in col.lower():
                try:
                    self.df[col] = pd.to_datetime(self.df[col])
                    changes.append(f"• **{col}**: Text → Date")
                except:
                    pass
        
        if not changes:
            return "✅ Data types look good! No fixes needed."
        
        return f"✅ **Data Types Fixed!**\n\n" + "\n".join(changes) + "\n\nYour data types are now correct!"

    def _clean_all_action(self) -> str:
        """Complete data cleaning - remove duplicates, nulls, fix types."""
        actions = []
        
        # Remove duplicates
        dup_count = self.df.duplicated().sum()
        if dup_count > 0:
            original = len(self.df)
            self.df = self.df.drop_duplicates()
            actions.append(f"✅ Removed {original - len(self.df)} duplicates")
        
        # Remove nulls
        missing = self.df.isnull().sum().sum()
        if missing > 0:
            original = len(self.df)
            self.df = self.df.dropna()
            actions.append(f"✅ Removed {original - len(self.df)} rows with missing values")
        
        # Fix types
        for col in self.df.columns:
            if self.df[col].dtype == 'object':
                try:
                    self.df[col] = pd.to_numeric(self.df[col])
                    actions.append(f"✅ Converted {col} to numeric")
                except:
                    pass
        
        if not actions:
            return "✅ Your data is already clean! No issues found."
        
        return f"🎉 **Complete Data Cleaning Done!**\n\n" + "\n".join(actions) + "\n\n**Your Excel file is now clean and accurate!** ✨"

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
