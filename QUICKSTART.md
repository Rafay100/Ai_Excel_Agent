# 🚀 Quick Start Guide - AI Excel Agent

Get up and running in 5 minutes!

---

## ⚡ Fastest Way to Start

### Option 1: One-Click Launch (Windows)

```bash
# Double-click or run:
D:\Ai_Excel_Agent\run.bat
```

This will:
1. Install missing dependencies
2. Start the backend server
3. Start the frontend UI
4. Open your browser automatically

---

### Option 2: Manual Start (All Platforms)

#### Step 1: Install Dependencies (5 minutes)

```bash
cd D:\Ai_Excel_Agent

# Install all packages
pip install -r requirements.txt

# Additional for charts
pip install kaleido
```

#### Step 2: Start Backend (Terminal 1)

```bash
cd D:\Ai_Excel_Agent\backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

✅ You should see: `Uvicorn running on http://127.0.0.1:8000`

#### Step 3: Start Frontend (Terminal 2)

```bash
cd D:\Ai_Excel_Agent\frontend
streamlit run ui.py --server.port 8501
```

✅ You should see: `You can now view your Streamlit app in your browser.`

#### Step 4: Open Browser

Navigate to: **http://localhost:8501**

---

## 🎯 First Time Usage

### 1. Load Sample Data (No Upload Needed!)

- Click **"📋 Load Sample Data"** in the sidebar
- Sample product sales data will load automatically
- You'll see metrics appear instantly

### 2. Try Quick Queries

Click these buttons in order:
1. **📊 Summary** - See data overview
2. **🔢 Statistics** - View column statistics
3. **📈 Top Values** - See top rows

### 3. Chat with Your Data

Type in the chat box:
```
"Show me total sales"
"Filter products with price > 100"
"Create a bar chart of sales by region"
```

### 4. Create a Chart

1. Go to **Charts** tab
2. Click **📈 Chart** in sidebar
3. Select:
   - Chart Type: `bar`
   - X Axis: `Region`
   - Y Axis: `Sales`
4. Click **🎨 Generate Chart**

### 5. Export Results

1. Click **💾 Export** in sidebar
2. Download link appears
3. Save your processed data

---

## 🔑 Optional: Enable AI Features

To use natural language queries:

1. Get OpenAI API key from: https://platform.openai.com/api-keys
2. Enter key in sidebar's **🔑 OpenAI API Key** field
3. Press Enter
4. ✅ "API key saved!" appears

Now you can ask questions like:
- "What's the average price by category?"
- "Show me the best selling product"
- "Create a pie chart of sales distribution"

---

## 📁 Upload Your Own Excel File

1. Click **"Choose an Excel file"** in sidebar
2. Select your `.xlsx`, `.xls`, or `.xlsm` file
3. Wait for "Loading file..." to complete
4. ✅ File name appears when ready

### Supported Formats
- ✅ `.xlsx` (Excel 2007+)
- ✅ `.xls` (Excel 97-2003)
- ✅ `.xlsm` (Excel with macros)

---

## 🛠️ Troubleshooting

### "streamlit: command not found"

```bash
# Install streamlit
pip install streamlit

# Or run directly with Python
python -m streamlit run frontend/ui.py
```

### "No module named 'pandas'"

```bash
pip install pandas openpyxl plotly
```

### Port Already in Use

**Backend (8000):**
```bash
# Use different port
uvicorn main:app --reload --port 8001
```

**Frontend (8501):**
```bash
# Use different port
streamlit run ui.py --server.port 8502
```

### Slow Installation

The first install takes time due to large packages. Be patient!

**Faster minimal install:**
```bash
pip install fastapi uvicorn pandas openpyxl streamlit plotly
```

---

## ✅ Verify Installation

Run the test script:

```bash
cd D:\Ai_Excel_Agent
python test_project.py
```

Expected output:
```
✓ FastAPI: 0.128.0
✓ Pandas: 3.0.2
✓ OpenPyXL: 3.1.5
✓ Plotly: 6.6.0
✓ Backend modules loaded
✓ read_excel: Loaded 3 rows
✓ summarize_data: 4 columns
✓ query_data (filter): 1 rows
✓ query_data (aggregate): Avg Salary = 61666.67
✓ clean_data: 3 rows
✓ Agent created successfully
✓ Direct tool call working
```

---

## 📊 What You'll See

### Main Interface
```
┌─────────────────────────────────────────────────────┐
│                                                     │
│         📊 AI Excel Agent                           │
│   Intelligent Data Analysis Powered by AI           │
│                                                     │
├─────────────────────────────────────────────────────┤
│                                                     │
│  [Total Rows]  [Columns]  [Memory]  [Duplicates]   │
│     1,234         15        2.5 MB       0         │
│                                                     │
├─────────────────────────────────────────────────────┤
│  💬 Chat  |  📊 Data  |  📈 Charts                 │
│  ────────────────────────────────────────           │
│  👤 You: Show me total sales                       │
│  🤖 AI: The total sales are $123,456...            │
│                                                     │
│  [Ask about your data...]                  [Send]  │
└─────────────────────────────────────────────────────┘
```

### Sidebar
```
┌──────────────────┐
│  ⚙️ Settings     │
│  ─────────────   │
│  🔑 API Key      │
│  [•••••••••••]   │
│                  │
│  📁 Upload       │
│  [Drop file]     │
│                  │
│  ⚡ Quick        │
│  [Summary][Clean]│
│  [Chart][Export] │
│                  │
│  📋 Sample Data  │
│  [Load Sample]   │
└──────────────────┘
```

---

## 🎓 Next Steps

After getting started:

1. **Read UI Guide**: `UI_GUIDE.md` - Detailed UI features
2. **Read API Docs**: `README.md` - Full API reference
3. **Try Dashboard**: `streamlit run frontend/dashboard.py`
4. **Explore API**: http://localhost:8000/docs

---

## 📞 Need Help?

### Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| App won't start | Check Python version (3.9+) |
| Charts not showing | Install kaleido: `pip install kaleido` |
| File upload fails | Check file format (.xlsx) |
| AI not responding | Add OpenAI API key |

### Still Stuck?

1. Check `README.md` for detailed docs
2. Review `SETUP.md` for installation help
3. Run `python test_project.py` to diagnose

---

## 🎉 You're Ready!

Open **http://localhost:8501** and start analyzing!

**Happy Data Analyzing! 📊✨**
