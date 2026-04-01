@echo off
REM AI Excel Agent - Quick Start Script

echo ========================================
echo   AI Excel Agent - Setup and Run
echo ========================================
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found. Please install Python 3.9+
    pause
    exit /b 1
)

echo [1/3] Checking dependencies...
python -c "import fastapi" >nul 2>&1
if errorlevel 1 (
    echo Installing dependencies...
    pip install -r requirements.txt
) else (
    echo Dependencies OK
)

echo.
echo [2/3] Starting Backend...
echo Backend will run at: http://localhost:8000
echo API Docs at: http://localhost:8000/docs
start "" cmd /k "cd backend && uvicorn main:app --reload --host 0.0.0.0 --port 8000"

timeout /t 3 /nobreak >nul

echo.
echo [3/3] Starting Frontend...
echo Frontend will run at: http://localhost:8501
start "" cmd /k "cd frontend && streamlit run ui.py --server.port 8501"

echo.
echo ========================================
echo   Application Starting...
echo   - Backend: http://localhost:8000
echo   - Frontend: http://localhost:8501
echo ========================================
echo.
echo Press any key to exit this window
pause >nul
