# DCD (Dual Currency Deposit) Pricer

A sophisticated pricing application for Dual Currency Deposits using QuantLib and Streamlit with professional-grade financial market conventions.

## What is a DCD?

A Dual Currency Deposit (DCD) is a structured financial product that combines:
1. **A deposit** in the base currency earning an enhanced interest rate
2. **A short call option** on the currency pair that may result in currency conversion

The investor receives a higher interest rate than a regular deposit, but risks receiving the principal in a different currency if the option is exercised.

## 🚀 Key Features

### 📊 **Professional Pricing Engine**
- **QuantLib Integration**: Black-Scholes-Merton with Garman-Kohlhagen for FX
- **Market Conventions**: Currency-specific day count bases (360/365)
- **Settlement Timing**: Proper T+2 settlement lag modeling
- **Term Structure**: Maturity-dependent deposit rate curves

### 💱 **Multi-Currency Support**
- **Currency Pairs**: EUR/USD, GBP/USD, USD/JPY, AUD/USD, USD/CHF, USD/CAD, NZD/USD
- **Day Count Conventions**: 
  - 360-day basis: EUR/USD, USD/JPY, USD/CHF (European/FX standard)
  - 365-day basis: GBP/USD, AUD/USD, USD/CAD, NZD/USD (UK/Commonwealth standard)
- **Dual Currency Display**: Shows amounts in both base and quote currencies
- **Currency Conversion**: Automatic calculation of conversion amounts

### 🏦 **Advanced Rate Modeling**
- **Base Rate Adjustment**: Maturity-dependent rate curves
- **Term Structure**: Configurable rate slope (bps per day)
- **Enhancement Calculation**: Precise option premium amortization
- **Settlement Lag**: Separate option maturity and deposit settlement dates

### 📈 **Comprehensive Analytics**
- **Real-time Pricing**: Interactive parameter adjustment
- **Payoff Visualization**: Currency-labeled payoff diagrams
- **Risk Metrics**: Complete Greeks calculation
- **Rate Matrices**: Multi-dimensional strike/maturity analysis
- **Probability Analysis**: Conversion risk assessment

## Installation & Setup

1. **Virtual Environment**: A virtual environment has been created in `.venv/`

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Application**:
   ```bash
   streamlit run main.py
   # or use the launcher
   ./launch.sh
   ```

## Usage Guide

### Market Parameters

**Currency Pair Selection:**
- Choose from major FX pairs with appropriate market conventions
- Day count basis automatically defaults to market standard
- Settlement days configurable (standard: T+2)

**Market Data:**
- **Spot Rate**: Current exchange rate
- **Domestic Rate**: Interest rate of the base currency (deposit currency)
- **Foreign Rate**: Interest rate of the quote currency
- **Volatility**: Implied volatility of the currency pair

### Product Configuration

**Maturity & Notional:**
- **Maturity**: Time to option expiration (days)
- **Notional**: Investment amount in base currency
- **Settlement**: Additional days between option maturity and deposit settlement

**Rate Structure:**
- **Base Deposit Rate**: Starting rate for the maturity
- **Term Structure**: Optional maturity adjustment
- **Rate Curve Slope**: Rate increase per day of maturity (basis points)

### Key Outputs

#### 📊 **Pricing Results**
- **Enhanced Rate**: The improved annual rate offered
- **Option Premium**: Value of the embedded call option (in base currency)
- **Conversion Probability**: Statistical likelihood of currency conversion

#### 💱 **Currency Scenarios**
- **No Conversion**: Receive enhanced deposit in base currency
- **Conversion**: Receive fixed amount in quote currency
- **Break-even Analysis**: Principal protection visualization

#### 📈 **Risk Analytics**
- **Greeks**: Delta, Gamma, Theta, Vega, Rho
- **Sensitivity Analysis**: Rate matrix across strikes and maturities
- **Market Risk**: Color-coded risk indicators

## Mathematical Framework

### Enhanced Rate Calculation
```
Enhanced Rate = Adjusted Base Rate + (Option Premium / (Notional × Deposit Year Fraction))

Where:
- Adjusted Base Rate = Base Rate + (Rate Curve Slope × Maturity Days)
- Deposit Year Fraction = Maturity Days / Day Count Basis (360 or 365)
- Option Premium = Black-Scholes Call Option Value × Notional
```

### Settlement Timing
```
Option Maturity Date = Trade Date + Maturity Days
Deposit Settlement Date = Option Maturity Date + Settlement Days (typically T+2)
```

### Day Count Conventions
- **360-day basis**: Used for EUR/USD, USD/JPY, USD/CHF
- **365-day basis**: Used for GBP/USD, AUD/USD, USD/CAD, NZD/USD

## Example Scenarios

### Scenario 1: EUR/USD DCD
- **Investment**: $1,000,000 USD for 91 days
- **Currency Pair**: EUR/USD at 1.0500
- **Strike**: 1.0300 (2.9% out-of-the-money)
- **Base Rate**: 2.0% → Enhanced Rate: ~12.5%
- **If EUR/USD ≤ 1.0300**: Receive $1,031,250 USD
- **If EUR/USD > 1.0300**: Receive €970,874 EUR

### Scenario 2: GBP/USD DCD  
- **Investment**: $2,000,000 USD for 180 days
- **Currency Pair**: GBP/USD at 1.2500
- **Strike**: 1.2000 (4.0% out-of-the-money)
- **Day Count**: 365-day basis
- **Enhanced Rate**: Varies based on volatility and term structure

## Technical Implementation

### Core Technologies
- **QuantLib**: Professional quantitative finance library
- **Streamlit**: Interactive web application framework
- **Plotly**: Advanced financial visualizations
- **NumPy/Pandas**: Numerical computing and data analysis

### Financial Models
- **Garman-Kohlhagen**: FX option pricing model
- **Black-Scholes-Merton**: Underlying option theory
- **Risk-Neutral Valuation**: Market-consistent pricing

### Market Conventions
- **Business Day Calendars**: TARGET calendar for date calculations
- **Day Count Methods**: 30/360 and Actual/365 conventions
- **Settlement Conventions**: T+2 FX settlement standard

## File Structure

```
DCD Pricer/
├── main.py              # Main Streamlit application
├── test_pricer.py       # Comprehensive test suite
├── config.py            # Configuration parameters
├── launch.sh            # Easy startup script
├── requirements.txt     # Python dependencies
├── README.md           # This documentation
└── .venv/              # Virtual environment
```

## Risk Considerations

### 🔴 **Currency Risk**
- Principal may be converted to foreign currency
- Exchange rate risk on converted amounts
- Hedging considerations for risk management

### 📊 **Interest Rate Risk**
- Sensitivity to domestic and foreign rate changes
- Term structure risk for longer maturities
- Basis risk between deposit and option rates

### 📈 **Volatility Risk**
- Higher volatility increases option value and enhanced rates
- Volatility smile and term structure effects
- Model risk from constant volatility assumption

### ⏱️ **Time Decay**
- Option value decreases as maturity approaches
- Theta risk for dynamic hedging
- Settlement timing considerations

## Advanced Features

### 🔢 **Rate Matrix Analysis**
Generate comprehensive rate matrices showing enhanced rates across:
- **Strike Range**: From deep out-of-the-money to at-the-money
- **Maturity Range**: Short-term (30 days) to long-term (365+ days)
- **Heat Maps**: Color-coded visualization for quick analysis
- **Data Export**: Tabular format for further analysis

### 📊 **Risk Management Tools**
- **Greeks Dashboard**: Real-time sensitivity analysis
- **Scenario Analysis**: Stress testing across market conditions
- **Break-even Analysis**: Principal protection levels
- **Probability Distributions**: Monte Carlo capabilities

### 🏦 **Client Presentation Features**
- **Professional Layouts**: Clean, institutional-grade interface
- **Export Capabilities**: Charts and tables for client materials
- **Multi-currency Display**: Clear currency labeling
- **Risk Disclaimers**: Built-in compliance considerations

This enhanced DCD pricer provides institutional-quality pricing and risk management capabilities for structured deposit products.
