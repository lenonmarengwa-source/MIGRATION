@echo off
REM Quick Start Testing Script for Windows
REM Zimbabwe Migration System - Streamlit

echo.
echo 🌍 Zimbabwe Migration System - Streamlit Testing
echo ==================================================
echo.

REM Check Python version
echo ✓ Checking Python version...
python --version
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo ✓ Creating virtual environment...
    python -m venv venv
    echo.
)

REM Activate virtual environment
echo ✓ Activating virtual environment...
call venv\Scripts\activate.bat
echo.

REM Install requirements
echo ✓ Installing dependencies (this may take a few minutes)...
pip install -q -r requirements.txt
echo ✓ Dependencies installed!
echo.

REM Create .env if it doesn't exist
if not exist ".env" (
    echo ✓ Creating .env file from template...
    copy .env.example .env
    echo ✓ Edit .env with your settings if needed
    echo.
)

REM Run Streamlit
echo ==================================================
echo 🚀 STARTING STREAMLIT APP
echo ==================================================
echo.
echo Access your app at: http://localhost:8501
echo.
echo Login Credentials:
echo   Username: admin
echo   Password: migration2026
echo.
echo Press Ctrl+C to stop the server
echo.
echo To stop and deactivate:
echo   deactivate
echo.
echo ==================================================
echo.

streamlit run web_system.py

pause
