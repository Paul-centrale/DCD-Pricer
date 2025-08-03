#!/bin/bash
echo "Starting DCD Pricer..."
echo ""
echo "Opening browser at: http://localhost:8501"
echo "Press Ctrl+C to stop the application"
echo ""

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    if ! command -v python &> /dev/null; then
        echo "Python is not installed or not in PATH"
        echo "Please install Python from https://python.org/downloads/"
        read -p "Press Enter to continue..."
        exit 1
    else
        PYTHON_CMD="python"
    fi
else
    PYTHON_CMD="python3"
fi

# Check if streamlit is available
$PYTHON_CMD -c "import streamlit" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "Streamlit is not installed. Installing dependencies..."
    $PYTHON_CMD -m pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "Failed to install dependencies"
        read -p "Press Enter to continue..."
        exit 1
    fi
fi

# Start the application
$PYTHON_CMD -m streamlit run main.py
