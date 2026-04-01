"""
AI Agent Module

This module implements the core AI agent that uses a tool-calling pattern
to interact with Excel data. The agent can understand natural language
queries and translate them into appropriate tool calls.

Note: Uses direct OpenAI API for Python 3.14+ compatibility.
LangChain imports are lazy to avoid Python 3.14 compatibility issues.
"""

import json
import re
import os
from typing import Dict, Any, List, Optional, Callable

# Handle imports for both direct execution and module import
try:
    from tools import ExcelTools
except ImportError:
    from backend.tools import ExcelTools

# Lazy import flag
_LANGCHAIN_IMPORT_ATTEMPTED = False
_LANGCHAIN_AVAILABLE = False
_OPENAI_AVAILABLE = False


# Define the system prompt for the agent
SYSTEM_PROMPT = """
You are an AI Excel Agent designed to help users analyze and manipulate Excel data.

You have access to the following tools:
1. read_excel - Load an Excel file into memory
2. summarize_data - Get comprehensive statistics about the dataset
3. query_data - Perform operations like filtering, aggregation, sorting, and grouping
4. create_chart - Generate visualizations (bar, line, pie, scatter, histogram)
5. clean_data - Clean the dataset by handling nulls, duplicates, and type issues
6. export_data - Export processed data to Excel or CSV

When a user asks a question:
1. First understand what they want to accomplish
2. Choose the appropriate tool(s) to use
3. Call the tool with the correct parameters
4. Present the results in a clear, human-readable format

For data operations:
- Use "filter" operation to filter rows based on conditions
- Use "aggregate" operation for sum, avg, count, min, max calculations
- Use "group" operation for groupby aggregations
- Use "sort" operation to sort data
- Use "select" operation to choose specific columns

For charts:
- bar: Compare values across categories
- line: Show trends over time
- pie: Show proportions/percentages
- scatter: Show relationships between two variables
- histogram: Show distribution of a single variable

Always explain what you're doing and present results clearly.
If you encounter an error, explain it and suggest alternatives.
"""


class AIExcelAgent:
    """
    AI Agent for Excel data analysis and manipulation.

    Uses LangChain's tool-calling agent pattern (or direct OpenAI API)
    to enable natural language interaction with Excel data.
    """

    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-4o-mini"):
        """
        Initialize the AI Excel Agent.

        Args:
            api_key: OpenAI API key (optional, can be set via environment)
            model: LLM model to use
        """
        self.tools_instance = ExcelTools()
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY")
        self.model = model
        self.llm = None
        self.agent_executor = None
        self.message_history = []
        self.openai_client = None
        self.use_langchain = False

        # Initialize LLM if API key is provided
        if self.api_key:
            self._initialize_llm()

    def _initialize_llm(self):
        """Initialize the language model and agent executor."""
        global _LANGCHAIN_IMPORT_ATTEMPTED, _LANGCHAIN_AVAILABLE, _OPENAI_AVAILABLE
        
        if not self.api_key:
            return

        # Try LangChain first (lazy import)
        if not _LANGCHAIN_IMPORT_ATTEMPTED:
            _LANGCHAIN_IMPORT_ATTEMPTED = True
            try:
                from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
                from langchain_core.tools import Tool
                from langchain_openai import ChatOpenAI
                from langchain.agents import AgentExecutor, create_openai_tools_agent
                from langchain_community.chat_message_histories import ChatMessageHistory
                _LANGCHAIN_AVAILABLE = True
            except Exception as e:
                print(f"LangChain import failed: {e}")
                _LANGCHAIN_AVAILABLE = False

        if _LANGCHAIN_AVAILABLE:
            try:
                from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
                from langchain_core.tools import Tool
                from langchain_openai import ChatOpenAI
                from langchain.agents import AgentExecutor, create_openai_tools_agent
                from langchain_community.chat_message_histories import ChatMessageHistory

                self.llm = ChatOpenAI(
                    model=self.model,
                    temperature=0.1,
                    api_key=self.api_key
                )

                tools = self._create_langchain_tools()
                prompt = ChatPromptTemplate.from_messages([
                    ("system", SYSTEM_PROMPT),
                    MessagesPlaceholder(variable_name="chat_history"),
                    ("human", "{input}"),
                    MessagesPlaceholder(variable_name="agent_scratchpad")
                ])

                agent = create_openai_tools_agent(self.llm, tools, prompt)
                self.agent_executor = AgentExecutor(
                    agent=agent,
                    tools=tools,
                    verbose=False,
                    handle_parsing_errors=True,
                    max_iterations=5
                )
                self.message_history = ChatMessageHistory()
                self.use_langchain = True
                return

            except Exception as e:
                print(f"LangChain init failed: {e}, trying direct OpenAI API...")
                _LANGCHAIN_AVAILABLE = False

        # Check OpenAI availability (lazy import)
        if not _OPENAI_AVAILABLE and not _LANGCHAIN_AVAILABLE:
            try:
                from openai import OpenAI
                _OPENAI_AVAILABLE = True
            except Exception:
                pass

        # Fall back to direct OpenAI API
        if _OPENAI_AVAILABLE:
            try:
                from openai import OpenAI
                self.openai_client = OpenAI(api_key=self.api_key)
                self.use_langchain = False
            except Exception as e:
                print(f"OpenAI API init failed: {e}")
    
    def _create_langchain_tools(self) -> List[Tool]:
        """
        Create LangChain tools from the ExcelTools methods.
        
        Returns:
            List of LangChain Tool objects
        """
        tools = []
        
        # Tool 1: Read Excel
        tools.append(Tool(
            name="read_excel",
            func=lambda path: json.dumps(self.tools_instance.read_excel(path)),
            description="Load an Excel file. Input: file path. Returns: file info, columns, and preview."
        ))
        
        # Tool 2: Summarize Data
        tools.append(Tool(
            name="summarize_data",
            func=lambda _: json.dumps(self.tools_instance.summarize_data()),
            description="Get summary statistics of the loaded data. No input needed."
        ))
        
        # Tool 3: Query Data
        def query_data_wrapper(params: str) -> str:
            """Wrapper for query_data that parses JSON parameters."""
            try:
                kwargs = json.loads(params)
                result = self.tools_instance.query_data(**kwargs)
                return json.dumps(result)
            except json.JSONDecodeError:
                return json.dumps({"success": False, "message": "Invalid parameters. Expected JSON."})
        
        tools.append(Tool(
            name="query_data",
            func=query_data_wrapper,
            description="""Perform data operations. Parameters (JSON):
            - operation: filter, aggregate, sort, group, select
            - column: column name to operate on
            - value: value for filtering
            - columns: list of columns to select
            - group_by: list of columns to group by
            - agg_func: sum, mean, avg, count, min, max
            - sort_by: column to sort by
            - sort_ascending: true/false
            - limit: number of rows to return
            - condition: filter condition like "age > 30"
            """
        ))
        
        # Tool 4: Create Chart
        def create_chart_wrapper(params: str) -> str:
            """Wrapper for create_chart that parses JSON parameters."""
            try:
                kwargs = json.loads(params)
                result = self.tools_instance.create_chart(**kwargs)
                # Remove base64 image from JSON response (too large)
                if "image_base64" in result:
                    result["has_image"] = True
                return json.dumps(result)
            except json.JSONDecodeError:
                return json.dumps({"success": False, "message": "Invalid parameters. Expected JSON."})
        
        tools.append(Tool(
            name="create_chart",
            func=create_chart_wrapper,
            description="""Create a chart. Parameters (JSON):
            - chart_type: bar, line, pie, scatter, histogram
            - x_column: column for x-axis
            - y_column: column for y-axis
            - title: chart title
            - group_by: column to group by
            - agg_column: column to aggregate
            - agg_func: sum, mean, count
            """
        ))
        
        # Tool 5: Clean Data
        def clean_data_wrapper(params: str) -> str:
            """Wrapper for clean_data that parses JSON parameters."""
            try:
                kwargs = json.loads(params)
                result = self.tools_instance.clean_data(**kwargs)
                return json.dumps(result)
            except json.JSONDecodeError:
                return json.dumps({"success": False, "message": "Invalid parameters. Expected JSON."})
        
        tools.append(Tool(
            name="clean_data",
            func=clean_data_wrapper,
            description="""Clean the dataset. Parameters (JSON):
            - remove_nulls: true/false
            - fill_nulls: true/false
            - fill_value: value to fill nulls
            - remove_duplicates: true/false
            - fix_types: true/false
            - columns: list of specific columns
            """
        ))
        
        # Tool 6: Export Data
        def export_data_wrapper(params: str) -> str:
            """Wrapper for export_data that parses JSON parameters."""
            try:
                kwargs = json.loads(params)
                result = self.tools_instance.export_data(**kwargs)
                return json.dumps(result)
            except json.JSONDecodeError:
                return json.dumps({"success": False, "message": "Invalid parameters. Expected JSON."})
        
        tools.append(Tool(
            name="export_data",
            func=export_data_wrapper,
            description="""Export data to file. Parameters (JSON):
            - output_path: path for output file
            - format: excel or csv
            - columns: list of columns to export
            """
        ))
        
        return tools
    
    def set_api_key(self, api_key: str):
        """
        Set the OpenAI API key and initialize the LLM.
        
        Args:
            api_key: OpenAI API key
        """
        self.api_key = api_key
        self._initialize_llm()
    
    def process_query(self, query: str) -> Dict[str, Any]:
        """
        Process a natural language query using the agent.

        Args:
            query: User's natural language query

        Returns:
            Dictionary with response and any generated data
        """
        global _LANGCHAIN_AVAILABLE, _OPENAI_AVAILABLE
        
        # If no AI is available, provide basic response
        if not self.api_key:
            return {
                "success": True,
                "message": "AI not configured. Using basic operations.",
                "response": f"Query received: '{query}'. Please add your OpenAI API key for AI-powered responses. You can still use direct operations via the API."
            }

        # Use LangChain if available and initialized
        if _LANGCHAIN_AVAILABLE and self.use_langchain and self.agent_executor:
            try:
                from langchain_core.messages import HumanMessage, AIMessage
                
                response = self.agent_executor.invoke({
                    "input": query,
                    "chat_history": self.message_history.messages
                })

                self.message_history.add_message(HumanMessage(content=query))
                self.message_history.add_message(AIMessage(content=response.get("output", "")))

                df = self.tools_instance.get_dataframe()

                return {
                    "success": True,
                    "response": response.get("output", ""),
                    "has_data": df is not None,
                    "data_preview": df.head(10).to_dict('records') if df is not None else None
                }

            except Exception as e:
                print(f"LangChain query failed: {e}")
                _LANGCHAIN_AVAILABLE = False
                # Fall through to OpenAI API

        # Use direct OpenAI API
        if _OPENAI_AVAILABLE and self.openai_client:
            try:
                # Build tool descriptions for the prompt
                tool_descriptions = """
Available tools:
1. summarize_data - Get data statistics (no parameters)
2. query_data - Filter/aggregate/sort data (operation, column, value, agg_func, group_by, etc.)
3. create_chart - Create bar/line/pie/scatter/histogram charts (chart_type, x_column, y_column, title)
4. clean_data - Remove nulls/duplicates, fix types (remove_nulls, remove_duplicates, fix_types)
5. export_data - Export to excel/csv (output_path, format)
"""

                df = self.tools_instance.get_dataframe()
                if df is not None:
                    tool_descriptions += f"\nCurrent data columns: {list(df.columns)}\n"
                    tool_descriptions += f"Column types: {self.tools_instance.column_info}\n"

                response = self.openai_client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": SYSTEM_PROMPT + "\n" + tool_descriptions},
                        {"role": "user", "content": query}
                    ],
                    temperature=0.1,
                    max_tokens=1000
                )

                ai_response = response.choices[0].message.content

                # Try to parse and execute any tool calls in the response
                result = self._parse_and_execute_response(ai_response)

                return {
                    "success": True,
                    "response": result.get("response", ai_response),
                    "has_data": df is not None,
                    "data_preview": df.head(10).to_dict('records') if df is not None else None
                }

            except Exception as e:
                print(f"OpenAI query failed: {e}")
                return {
                    "success": False,
                    "message": f"Error processing query: {str(e)}",
                    "response": f"I encountered an error: {str(e)}. Please try again."
                }

        # Fallback: no AI available
        return {
            "success": True,
            "message": "AI not available. Using basic operations.",
            "response": f"Query received: '{query}'. Please provide a valid OpenAI API key for AI-powered responses."
        }

    def _parse_and_execute_response(self, response: str) -> Dict[str, Any]:
        """Parse AI response and execute any tool calls."""
        # Look for JSON-like tool calls in the response
        import re
        json_pattern = r'\{[^{}]*"operation"[^{}]*\}'
        matches = re.findall(json_pattern, response, re.IGNORECASE)

        if matches:
            try:
                params = json.loads(matches[0])
                result = self.tools_instance.query_data(**params)
                return {
                    "response": f"Executed operation: {params.get('operation')}\nResult: {json.dumps(result, indent=2)}",
                    "tool_result": result
                }
            except:
                pass

        return {"response": response}
    
    def direct_tool_call(self, tool_name: str, **kwargs) -> Dict[str, Any]:
        """
        Directly call a tool without going through the LLM.
        Useful for programmatic operations.
        
        Args:
            tool_name: Name of the tool to call
            **kwargs: Arguments to pass to the tool
            
        Returns:
            Tool execution result
        """
        tool_methods = {
            "read_excel": self.tools_instance.read_excel,
            "summarize_data": self.tools_instance.summarize_data,
            "query_data": self.tools_instance.query_data,
            "create_chart": self.tools_instance.create_chart,
            "clean_data": self.tools_instance.clean_data,
            "export_data": self.tools_instance.export_data
        }
        
        if tool_name not in tool_methods:
            return {"success": False, "message": f"Unknown tool: {tool_name}"}
        
        try:
            result = tool_methods[tool_name](**kwargs)
            return result
        except Exception as e:
            return {"success": False, "message": f"Error calling {tool_name}: {str(e)}"}
    
    def get_dataframe(self) -> Optional[Any]:
        """Get the current dataframe."""
        return self.tools_instance.get_dataframe()
    
    def reset(self):
        """Reset the agent state."""
        self.tools_instance.reset_data()
        self.message_history.clear()
    
    def get_column_info(self) -> Dict[str, str]:
        """Get information about loaded columns."""
        return self.tools_instance.column_info


# Convenience function for creating agent
def create_agent(api_key: Optional[str] = None, model: str = "gpt-4o-mini") -> AIExcelAgent:
    """
    Create and return an AI Excel Agent instance.
    
    Args:
        api_key: OpenAI API key
        model: LLM model to use
        
    Returns:
        AIExcelAgent instance
    """
    return AIExcelAgent(api_key=api_key, model=model)
