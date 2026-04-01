# AI Excel Agent - Setup Guide

## Quick Start (Windows)

### Step 1: Install Dependencies

```bash
# Navigate to project directory
cd D:\Ai_Excel_Agent

# Install core packages (this may take a few minutes)
pip install -r requirements.txt
```

### Step 2: Start the Backend

Open Terminal 1:
```bash
cd D:\Ai_Excel_Agent\backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

You should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
```

### Step 3: Start the Frontend

Open Terminal 2:

**Option A - Streamlit (Recommended):**
```bash
cd D:\Ai_Excel_Agent\frontend
streamlit run ui.py --server.port 8501
```

**Option B - Gradio (Lighter/Faster):**
```bash
pip install gradio
cd D:\Ai_Excel_Agent\frontend
python ui_gradio.py
```

### Step 4: Access the Application

- **Frontend UI**: http://localhost:8501
- **API Documentation**: http://localhost:8000/docs

---

## Troubleshooting

### "streamlit is not recognized"
Streamlit is still installing. Wait for the installation to complete, then try again.

### "No module named 'tools'"
Run from the correct directory:
```bash
cd D:\Ai_Excel_Agent\frontend
streamlit run ui.py
```

### Python 3.14 Compatibility
Some packages may not be fully compatible with Python 3.14 yet. If you encounter issues:
1. Use Python 3.11 or 3.12 (recommended)
2. Or use the Gradio frontend which has fewer dependencies

### Slow Installation
The installation may take time due to package sizes. Be patient - it's downloading pandas, numpy, etc.

---

## Minimal Installation (Fastest)

If you want to get started quickly with minimal dependencies:

```bash
# Install only essentials
pip install fastapi uvicorn python-multipart pandas openpyxl plotly

# For frontend, use Gradio (lighter than Streamlit)
pip install gradio

# Run backend
cd backend
uvicorn main:app --reload

# Run frontend (in another terminal)
cd ../frontend
python ui_gradio.py
```

---

## Verify Installation

```bash
# Check Python version
python --version  # Should be 3.9+

# Check key packages
python -c "import fastapi; print('FastAPI:', fastapi.__version__)"
python -c "import pandas; print('Pandas:', pandas.__version__)"
python -c "import streamlit; print('Streamlit:', streamlit.__version__)"
```

---

## Usage

1. Open http://localhost:8501
2. Enter your OpenAI API key (optional, for AI queries)
3. Upload an Excel file
4. Ask questions or use quick actions

Enjoy! 🚀
