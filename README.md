# DCD Pricer - Dual Currency Deposit Analysis Tool

A professional-grade financial application for pricing and analyzing Dual Currency Deposits (DCDs) using QuantLib and Streamlit.

## 🚀 Quick Start (For End Users)

### Option 1: Automatic Setup (Recommended)
1. **Download** all files to a folder on your computer
2. **Run the setup script**:
   - **Windows**: Double-click `setup.py` or run `python setup.py` in Command Prompt
   - **Mac/Linux**: Run `python3 setup.py` in Terminal
3. **Launch the application**:
   - **Windows**: Double-click `launch_dcd_pricer.bat`
   - **Mac/Linux**: Double-click `launch_dcd_pricer.sh` or run `./launch_dcd_pricer.sh`

### Option 2: Manual Setup
If the automatic setup doesn't work, follow these steps:

#### Requirements
- Python 3.8 or higher
- Internet connection for package installation

#### Installation Steps
1. **Install Python** (if not already installed):
   - Download from https://python.org/downloads/
   - During installation, check "Add Python to PATH"

2. **Open Terminal/Command Prompt** and navigate to the DCD Pricer folder

3. **Install required packages**:
   ```bash
   pip install streamlit QuantLib-Python numpy pandas plotly
   ```

4. **Run the application**:
   ```bash
   streamlit run main.py
   ```

5. **Open your browser** and go to: http://localhost:8501

## 📊 Features

### Core Functionality
- **Professional DCD Pricing**: Uses Garman-Kohlhagen FX option model via QuantLib
- **Tiered Rate Structure**: Configure realistic deposit rates for different maturity ranges
- **Interactive Analysis**: Real-time parameter adjustment with instant recalculation
- **Risk Assessment**: Conversion probability and Greek sensitivities
- **Rate Matrix Analysis**: Compare rates across different strikes and maturities

### Market Conventions
- **Multiple Currency Pairs**: EUR/USD, GBP/USD, USD/JPY, AUD/USD, USD/CHF, USD/CAD, NZD/USD
- **Day Count Conventions**: 360/365 day count basis with currency-specific defaults
- **Settlement Modeling**: T+2 business day settlement between option and deposit
- **Professional Styling**: Clean, emoji-free interface suitable for business use

### Visualization & Export
- **Payoff Diagrams**: Interactive charts showing DCD risk/return profile
- **Rate Heat Maps**: Visual matrix of enhanced rates vs strike/maturity
- **SVG Export**: High-quality chart exports for presentations
- **Detailed Analysis**: Expandable sections with comprehensive scenarios

## 🏦 Understanding DCDs

### What is a DCD?
A Dual Currency Deposit combines:
- **Enhanced deposit rate** (higher than regular deposits)
- **Currency conversion risk** (if exchange rate exceeds strike)

### Key Concepts
- **Strike Rate**: Exchange rate threshold for conversion
- **Enhanced Rate**: Higher interest rate you receive
- **Conversion Probability**: Likelihood of receiving foreign currency
- **Option Premium**: Value embedded in the enhanced rate

### Risk Profile
- **Below Strike**: Keep enhanced deposit in original currency ✅
- **Above Strike**: Principal converted at strike rate (miss upside) ⚠️

## 🔧 Configuration Options

### Rate Structure Types
1. **Tiered Rates** (Recommended): Define specific rates for maturity ranges
   - Example: 2.00% (1-21d), 2.10% (22-60d), 2.30% (61-90d)
2. **Linear Progression**: Rates increase smoothly with maturity

### Market Parameters
- **Spot Rate**: Current exchange rate
- **Interest Rates**: Domestic and foreign risk-free rates
- **Volatility**: Expected exchange rate volatility
- **Strike**: DCD conversion level

## 📁 File Structure
```
DCD Pricer/
├── main.py                    # Main application
├── setup.py                   # Automatic setup script
├── requirements.txt           # Package dependencies
├── launch_dcd_pricer.bat     # Windows launcher (auto-created)
├── launch_dcd_pricer.sh      # Mac/Linux launcher (auto-created)
├── README.md                 # This file
└── CHANGELOG.md              # Version history
```

## 🐛 Troubleshooting

### Common Issues

**"streamlit: command not found"**
- Ensure Python and pip are properly installed
- Try: `python -m streamlit run main.py`

**"No module named 'QuantLib'"**
- Install QuantLib: `pip install QuantLib-Python`
- On some systems: `pip3 install QuantLib-Python`

**Port already in use**
- Use different port: `streamlit run main.py --server.port 8502`

**Permission denied (Mac/Linux)**
- Make script executable: `chmod +x launch_dcd_pricer.sh`

### System-Specific Notes

**Windows:**
- Use Command Prompt or PowerShell
- Ensure Python is in system PATH
- Some antivirus software may flag Python scripts

**Mac:**
- May need to install Xcode command line tools: `xcode-select --install`
- Use Terminal application
- Allow Python through Gatekeeper if prompted

**Linux:**
- Install Python development headers: `sudo apt-get install python3-dev`
- Some distributions require separate pip installation

## 💡 Usage Tips

1. **Start Simple**: Use default parameters first to understand the interface
2. **Tiered Rates**: Switch to "Tiered Rates" for realistic market modeling
3. **Strike Selection**: Choose strikes close to current spot for balanced risk/reward
4. **Matrix Analysis**: Use rate matrix to compare multiple scenarios
5. **Export Charts**: Use SVG format for high-quality presentations

## � Updates

The application includes automatic chart refresh and real-time parameter updates. No manual refresh needed when changing inputs.

## 📞 Support

For technical issues:
1. Check the troubleshooting section above
2. Ensure all requirements are properly installed
3. Verify Python version compatibility (3.8+)

## ⚖️ Disclaimer

This tool is for educational and analysis purposes. Always consult with qualified financial professionals before making investment decisions. Past performance and theoretical models do not guarantee future results.
