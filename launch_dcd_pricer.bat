@echo off
echo Starting DCD Pricer...
echo.
echo Opening browser at: http://localhost:8501
echo Press Ctrl+C to stop the application
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo Python is not installed or not in PATH
    echo Please install Python from https://python.org/downloads/
    pause
    exit /b 1
)

REM Check if streamlit is available
python -c "import streamlit" >nul 2>&1
if errorlevel 1 (
    echo Streamlit is not installed. Installing dependencies...
    python -m pip install -r requirements.txt
    if errorlevel 1 (
        echo Failed to install dependencies
        pause
        exit /b 1
    )
)

REM Start the application
python -m streamlit run main.py
pause
