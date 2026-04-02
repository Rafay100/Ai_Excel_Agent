# AI Excel Agent

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109.0-green.svg)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.29.0-red.svg)](https://streamlit.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A production-ready AI-powered Excel data analysis agent that enables natural language interaction with Excel files. Built with FastAPI backend, Streamlit frontend, and LangChain-based AI agent system.

![AI Excel Agent Demo](https://img.shields.io/badge/Status-Production_Ready-brightgreen)

## 🌟 Features

### Core Capabilities
- **📤 File Upload**: Upload Excel files (.xlsx, .xls, .xlsm) through an intuitive web interface
- **🤖 AI-Powered Analysis**: Ask questions in natural language and get intelligent responses
- **📊 Data Visualization**: Generate bar charts, line charts, pie charts, scatter plots, and histograms
- **🔍 Data Operations**: Filter, sort, aggregate, and group data with simple commands
- **🧹 Data Cleaning**: Remove nulls, fix data types, eliminate duplicates automatically
- **💾 Export Results**: Download processed data in Excel or CSV format

### Modern UI Features
- **💬 Chat Interface**: Conversational AI interaction with message history
- **📈 Interactive Dashboard**: Analytics dashboard with KPI cards and visualizations
- **🎨 Chart Builder**: Visual chart creation with preview
- **📊 Data Preview**: Multi-tab view with data, columns, and data quality
- **⚡ Quick Actions**: One-click operations for common tasks
- **📱 Responsive Design**: Modern gradient theme with smooth animations

### 🎨 New Professional UI (2026)
- **Beautiful Gradient Theme**: Purple gradient (#667eea → #764ba2)
- **KPI Metric Cards**: Animated cards showing key data metrics
- **Color-Coded Chat**: Purple bubbles for user, white for AI
- **Tabbed Navigation**: Chat, Data, and Charts tabs
- **Quick Query Buttons**: 6 one-click analysis buttons
- **Chart Builder**: Visual chart creation interface
- **Data Quality Panel**: Missing values and duplicates detection
- **Welcome Screen**: Guided onboarding for new users

📖 **See [UI_GUIDE.md](UI_GUIDE.md) for complete UI documentation**
🚀 **See [QUICKSTART.md](QUICKSTART.md) for 5-minute setup**

### Technical Features
- **Tool-Calling Agent**: LangChain-based agent with 6 specialized tools
- **RESTful API**: Full-featured FastAPI backend with comprehensive endpoints
- **Interactive UI**: Modern Streamlit interface with chat-based interaction
- **Session Management**: Multi-session support with isolated data contexts
- **Error Handling**: Robust error handling with informative messages

## 🏗️ Architecture

```
Ai_Excel_Agent/
├── backend/
│   ├── agent.py          # Core AI agent with tool-calling pattern
│   ├── tools.py          # Excel operation tools (6 tools)
│   ├── main.py           # FastAPI REST API server
│   └── __init__.py
├── frontend/
│   ├── ui.py             # Modern Streamlit web interface (NEW!)
│   ├── dashboard.py      # Analytics dashboard page (NEW!)
│   ├── ui_gradio.py      # Alternative Gradio UI
│   └── __init__.py
├── uploads/              # Temporary upload storage
├── outputs/              # Exported files storage
├── requirements.txt      # Python dependencies
├── README.md             # Main documentation
├── UI_GUIDE.md           # UI features guide (NEW!)
├── QUICKSTART.md         # 5-minute setup guide (NEW!)
├── SETUP.md              # Installation guide
├── UI_IMPROVEMENTS.md    # UI comparison doc (NEW!)
├── run.bat               # Windows quick-start script
└── test_project.py       # Test script
```

### Component Overview

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   Streamlit UI  │────▶│   FastAPI API   │────▶│   AI Agent      │
│   (frontend/)   │◀────│   (backend/)    │◀────│   (agent.py)    │
└─────────────────┘     └─────────────────┘     └────────┬────────┘
                                                         │
                          ┌──────────────────────────────┼──────────────────────────────┐
                          │                              │                              │
                          ▼                              ▼                              ▼
                   ┌─────────────┐              ┌─────────────┐              ┌─────────────┐
                   │  read_excel │              │ query_data  │              │ create_chart│
                   │  summarize  │              │ clean_data  │              │ export_data │
                   └─────────────┘              └─────────────┘              └─────────────┘
```

## 🚀 Quick Start

### Prerequisites

- Python 3.9 or higher
- OpenAI API Key (for AI-powered queries)
- pip or conda package manager

### Installation

1. **Clone or download the project:**
   ```bash
   cd Ai_Excel_Agent
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install kaleido for chart export (required for static images):**
   ```bash
   pip install kaleido
   ```

### Running the Application

#### Option 1: Run Backend and Frontend Separately

**Terminal 1 - Start FastAPI Backend:**
```bash
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2 - Start Streamlit Frontend:**
```bash
cd frontend
streamlit run ui.py --server.port 8501
```

#### Option 2: Run Frontend Only (Direct Import Mode)

The frontend can run independently by directly importing backend modules:

```bash
streamlit run frontend/ui.py --server.port 8501
```

### Access the Application

- **Streamlit UI**: http://localhost:8501
- **FastAPI Docs**: http://localhost:8000/docs
- **API Health**: http://localhost:8000/health

## 📖 Usage Guide

### 1. Upload an Excel File

1. Open the Streamlit interface
2. Enter your OpenAI API key in the sidebar (for AI queries)
3. Upload your Excel file using the file uploader
4. Wait for the data to load and summary to generate

### 2. Ask Natural Language Questions

With AI enabled (API key provided):
```
- "Show me a summary of the data"
- "What is the average sales by region?"
- "Filter rows where age is greater than 30"
- "Create a bar chart of monthly revenue"
- "Remove all duplicate rows"
```

### 3. Use Quick Actions

- **View Summary**: Display dataset statistics
- **Clean Data**: Apply data cleaning operations
- **Create Chart**: Build visualizations interactively
- **Export Data**: Download processed data

### 4. API Usage Examples

#### Upload File
```bash
curl -X POST "http://localhost:8000/api/upload" \
  -F "file=@your_file.xlsx" \
  -F "session_id=unique-session-123"
```

#### Query Data
```bash
curl -X POST "http://localhost:8000/api/query" \
  -H "Content-Type: application/json" \
  -d '{"query": "Show me the average sales", "session_id": "unique-session-123"}'
```

#### Generate Chart
```bash
curl -X POST "http://localhost:8000/api/chart" \
  -H "Content-Type: application/json" \
  -d '{
    "chart_type": "bar",
    "x_column": "Region",
    "y_column": "Sales",
    "title": "Sales by Region",
    "session_id": "unique-session-123"
  }'
```

## 🛠️ API Reference

### Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API health check |
| GET | `/health` | Health status |
| POST | `/api/set-api-key` | Set OpenAI API key |
| POST | `/api/upload` | Upload Excel file |
| POST | `/api/query` | Natural language query |
| POST | `/api/tool` | Direct tool call |
| POST | `/api/summarize` | Get data summary |
| POST | `/api/chart` | Generate chart |
| POST | `/api/clean` | Clean data |
| POST | `/api/export` | Export data |
| GET | `/api/download/{filename}` | Download file |
| GET | `/api/data` | Get data preview |
| GET | `/api/columns` | Get column info |
| DELETE | `/api/session/{id}` | Delete session |
| POST | `/api/reset` | Reset session |

### Tool Definitions

#### read_excel
Load an Excel file into memory.
```json
{
  "file_path": "path/to/file.xlsx"
}
```

#### summarize_data
Get comprehensive statistics about the dataset.
```json
{}  // No parameters needed
```

#### query_data
Perform data operations (filter, aggregate, sort, group, select).
```json
{
  "operation": "filter",
  "column": "Age",
  "condition": "Age > 30",
  "limit": 100
}
```

#### create_chart
Generate visualizations.
```json
{
  "chart_type": "bar",
  "x_column": "Category",
  "y_column": "Value",
  "title": "My Chart"
}
```

#### clean_data
Clean the dataset.
```json
{
  "remove_nulls": true,
  "remove_duplicates": true,
  "fix_types": true
}
```

#### export_data
Export processed data.
```json
{
  "output_path": "outputs/my_file",
  "format": "excel",
  "columns": ["Col1", "Col2"]
}
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENAI_API_KEY` | OpenAI API key | None |
| `UPLOAD_DIR` | Upload directory | `./uploads` |
| `OUTPUT_DIR` | Output directory | `./outputs` |

### Model Configuration

The agent uses `gpt-4o-mini` by default. You can change this in `backend/agent.py`:

```python
agent = create_agent(api_key="your-key", model="gpt-4")
```

## 📁 Example Data

Create a sample Excel file for testing:

```python
import pandas as pd

# Create sample data
df = pd.DataFrame({
    'Name': ['Alice', 'Bob', 'Charlie', 'David', 'Eve'],
    'Age': [25, 30, 35, 28, 32],
    'City': ['NYC', 'LA', 'Chicago', 'NYC', 'LA'],
    'Salary': [50000, 60000, 75000, 55000, 65000],
    'Department': ['IT', 'HR', 'IT', 'HR', 'IT']
})

# Save to Excel
df.to_excel('sample_data.xlsx', index=False)
```

## 🧪 Testing

### Manual Testing Checklist

- [ ] Upload Excel file successfully
- [ ] View data summary
- [ ] Ask natural language questions (with API key)
- [ ] Generate bar chart
- [ ] Generate line chart
- [ ] Generate pie chart
- [ ] Clean data (remove nulls)
- [ ] Export processed data
- [ ] Download exported file

### API Testing with cURL

```bash
# Health check
curl http://localhost:8000/health

# Get API docs
curl http://localhost:8000/docs
```

## 🚨 Troubleshooting

### Common Issues

**Issue: "No module named 'tools'"**
```bash
# Ensure you're running from the correct directory
cd backend
python main.py
```

**Issue: "OpenAI API key not provided"**
- Add your API key in the Streamlit sidebar
- Or set environment variable: `export OPENAI_API_KEY=your-key`

**Issue: "Chart generation failed"**
```bash
# Install kaleido for static image export
pip install kaleido
```

**Issue: "File upload fails"**
- Check file format (.xlsx, .xls, .xlsm)
- Ensure uploads/ directory exists and is writable

## 📊 Performance Considerations

- **Large Files**: Files with >100,000 rows may experience slower processing
- **Memory**: Data is loaded into memory; ensure sufficient RAM
- **API Rate Limits**: OpenAI API has rate limits; consider caching for production
- **Session Cleanup**: Sessions are stored in memory; implement cleanup for long-running deployments

## 🔒 Security Notes

- **API Keys**: Never commit API keys to version control
- **File Uploads**: Implement file size limits in production
- **CORS**: Configure allowed origins appropriately for production
- **Session Management**: Current implementation is in-memory; use Redis for production

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📧 Contact

For questions or support, please open an issue in the repository.

## 🙏 Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) - Modern web framework
- [Streamlit](https://streamlit.io/) - Data app framework
- [LangChain](https://langchain.com/) - AI agent framework
- [Plotly](https://plotly.com/) - Visualization library
- [Pandas](https://pandas.pydata.org/) - Data manipulation

---

**Built with ❤️ for data professionals**
"# Ai_Excel_Agent" 
"# Ai_Excel_Agent" 
