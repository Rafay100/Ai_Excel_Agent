"""
AI Excel Agent - Hugging Face Spaces Entry Point
"""
import sys
import os

# Add current directory to path FIRST
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from pathlib import Path

# Get the directory where app.py is located
BASE_DIR = Path(__file__).parent

# Add backend to Python path
sys.path.insert(0, str(BASE_DIR / 'backend'))

# Set environment variables for Hugging Face
os.environ['OPENAI_API_KEY'] = os.environ.get('OPENAI_API_KEY', '')
os.environ['UPLOAD_DIR'] = str(BASE_DIR / 'uploads')
os.environ['OUTPUT_DIR'] = str(BASE_DIR / 'outputs')

# Create necessary directories
os.makedirs(BASE_DIR / 'uploads', exist_ok=True)
os.makedirs(BASE_DIR / 'outputs', exist_ok=True)

# Import frontend UI
from frontend import ui
