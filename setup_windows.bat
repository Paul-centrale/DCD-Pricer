@echo off
chcp 65001 >nul
title DCD Pricer - Easy Setup
color 0A

echo.
echo ============================================
echo          DCD PRICER - EASY SETUP
echo ============================================
echo.
echo This will automatically install everything needed
echo for the DCD Pricer to work on your computer.
echo.
echo Requirements: Internet connection
echo Estimated time: 2-5 minutes
echo.
pause

echo.
echo [1/4] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found!
    echo.
    echo Please install Python first:
    echo 1. Go to https://python.org/downloads/
    echo 2. Download and install Python 3.8 or higher
    echo 3. IMPORTANT: Check "Add Python to PATH" during installation
    echo 4. Restart this setup after Python installation
    echo.
    pause
    exit /b 1
) else (
    echo ✅ Python found
)

echo.
echo [2/4] Installing required packages...
echo This may take a few minutes...
pip install streamlit numpy pandas plotly
if errorlevel 1 (
    echo ❌ Package installation failed
    echo Trying alternative method...
    python -m pip install streamlit numpy pandas plotly
    if errorlevel 1 (
        echo ❌ Alternative installation failed
        echo Please check your internet connection and try again
        pause
        exit /b 1
    )
)

echo.
echo Installing QuantLib (advanced financial library)...
pip install QuantLib-Python
if errorlevel 1 (
    echo ⚠️ QuantLib installation failed - this is common
    echo The app will work but with reduced functionality
)

echo.
echo [3/4] Creating launch shortcut...
echo streamlit run main.py > run_dcd_pricer.bat
echo.
echo [4/4] Testing installation...
python -c "import streamlit, numpy, pandas, plotly; print('✅ All packages working')"
if errorlevel 1 (
    echo ❌ Package test failed
    echo Some packages may not be working correctly
    pause
    exit /b 1
)

echo.
echo ============================================
echo          SETUP COMPLETED SUCCESSFULLY!
echo ============================================
echo.
echo To start the DCD Pricer:
echo 1. Double-click "run_dcd_pricer.bat" 
echo 2. Or run: streamlit run main.py
echo.
echo The app will open in your web browser at:
echo http://localhost:8501
echo.
echo You can now close this window.
echo.
pause
