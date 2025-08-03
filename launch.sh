#!/bin/bash

# DCD Pricer Launcher Script
# This script launches the Streamlit DCD pricer application

echo "🚀 Starting DCD Pricer Application..."
echo "=================================="

# Navigate to the project directory
cd "$(dirname "$0")"

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "Please run the setup first."
    exit 1
fi

# Activate virtual environment and start Streamlit
echo "📦 Activating virtual environment..."
source .venv/bin/activate

echo "🌐 Starting Streamlit server..."
echo "The application will open in your browser at: http://localhost:8501"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Start Streamlit
python -m streamlit run main.py

echo ""
echo "👋 DCD Pricer stopped. Goodbye!"
