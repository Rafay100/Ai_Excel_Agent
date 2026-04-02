"""
AI Excel Agent - Hugging Face Spaces Entry Point

This file imports the ui.py module and runs it as a Streamlit app.
"""
import sys
import os
from pathlib import Path

# Get the directory where app.py is located
BASE_DIR = Path(__file__).parent

# Add backend to Python path (frontend already in path via ui import)
sys.path.insert(0, str(BASE_DIR / 'backend'))

# Set environment variables for Hugging Face
os.environ['OPENAI_API_KEY'] = os.environ.get('OPENAI_API_KEY', '')
os.environ['UPLOAD_DIR'] = str(BASE_DIR / 'uploads')
os.environ['OUTPUT_DIR'] = str(BASE_DIR / 'outputs')

# Create necessary directories
os.makedirs(BASE_DIR / 'uploads', exist_ok=True)
os.makedirs(BASE_DIR / 'outputs', exist_ok=True)

# Now import and run the UI
# ui.py has st.set_page_config() at module level, so we just import it
from frontend.ui import *
