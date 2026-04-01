@echo off
REM AI Excel Agent - Run with UTF-8 support
chcp 65001 >nul
set PYTHONUTF8=1
set PYTHONIOENCODING=utf-8
cd /d "%~dp0frontend"
streamlit run ui.py --server.port 8501
