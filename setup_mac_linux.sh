#!/bin/bash

# DCD Pricer - Easy Setup for Mac/Linux
# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}"
echo "============================================"
echo "          DCD PRICER - EASY SETUP"
echo "============================================"
echo -e "${NC}"
echo "This will automatically install everything needed"
echo "for the DCD Pricer to work on your computer."
echo ""
echo "Requirements: Internet connection"
echo "Estimated time: 2-5 minutes"
echo ""
read -p "Press Enter to continue or Ctrl+C to cancel..."

echo ""
echo -e "${BLUE}[1/4] Checking Python installation...${NC}"

# Check for Python 3
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
    PIP_CMD="pip3"
    echo -e "${GREEN}✅ Python 3 found${NC}"
elif command -v python &> /dev/null; then
    # Check if it's Python 3
    python_version=$(python --version 2>&1)
    if [[ $python_version == *"Python 3"* ]]; then
        PYTHON_CMD="python"
        PIP_CMD="pip"
        echo -e "${GREEN}✅ Python 3 found${NC}"
    else
        echo -e "${RED}❌ Python 3 not found!${NC}"
        echo ""
        echo "Please install Python 3 first:"
        echo "• macOS: brew install python3 or download from https://python.org"
        echo "• Ubuntu/Debian: sudo apt-get install python3 python3-pip"
        echo "• CentOS/RHEL: sudo yum install python3 python3-pip"
        echo ""
        exit 1
    fi
else
    echo -e "${RED}❌ Python not found!${NC}"
    echo ""
    echo "Please install Python 3 first:"
    echo "• macOS: brew install python3 or download from https://python.org"
    echo "• Ubuntu/Debian: sudo apt-get install python3 python3-pip"
    echo "• CentOS/RHEL: sudo yum install python3 python3-pip"
    echo ""
    exit 1
fi

echo ""
echo -e "${BLUE}[2/4] Installing required packages...${NC}"
echo "This may take a few minutes..."

# Install packages
$PIP_CMD install streamlit numpy pandas plotly
if [ $? -ne 0 ]; then
    echo -e "${YELLOW}Trying alternative installation method...${NC}"
    $PYTHON_CMD -m pip install streamlit numpy pandas plotly
    if [ $? -ne 0 ]; then
        echo -e "${RED}❌ Package installation failed${NC}"
        echo "Please check your internet connection and try again"
        echo "You may also need to run: sudo $PIP_CMD install streamlit numpy pandas plotly"
        exit 1
    fi
fi

echo ""
echo "Installing QuantLib (advanced financial library)..."
$PIP_CMD install QuantLib-Python
if [ $? -ne 0 ]; then
    echo -e "${YELLOW}⚠️ QuantLib installation failed - this is common${NC}"
    echo "The app will work but with reduced functionality"
fi

echo ""
echo -e "${BLUE}[3/4] Creating launch script...${NC}"
cat > run_dcd_pricer.sh << 'EOF'
#!/bin/bash
echo "Starting DCD Pricer..."
echo "Browser will open at: http://localhost:8501"
echo "Press Ctrl+C to stop the application"
echo ""
streamlit run main.py
EOF
chmod +x run_dcd_pricer.sh

echo ""
echo -e "${BLUE}[4/4] Testing installation...${NC}"
$PYTHON_CMD -c "import streamlit, numpy, pandas, plotly; print('✅ All packages working')"
if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Package test failed${NC}"
    echo "Some packages may not be working correctly"
    exit 1
fi

echo ""
echo -e "${GREEN}"
echo "============================================"
echo "          SETUP COMPLETED SUCCESSFULLY!"
echo "============================================"
echo -e "${NC}"
echo "To start the DCD Pricer:"
echo "1. Run: ./run_dcd_pricer.sh"
echo "2. Or run: streamlit run main.py"
echo ""
echo "The app will open in your web browser at:"
echo "http://localhost:8501"
echo ""
echo "You can now close this terminal."
echo ""
