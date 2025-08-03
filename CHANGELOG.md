# DCD Pricer - Changelog

## Version 2.1.0 - Layout & Export Improvements

### 🎨 **UI/UX Enhancements**
- **Cleaner Main Interface**: Moved detailed scenarios and explanations to collapsible section at bottom
- **Better Font Sizing**: Improved readability of key metrics with custom HTML styling
- **Professional Layout**: Streamlined main dashboard for better focus on essential information

### 📊 **Export Capabilities**
- **SVG Downloads**: All Plotly charts now support SVG export format
  - Payoff diagrams: High-quality vector graphics
  - Rate matrix heatmaps: Scalable charts for presentations
  - Professional filename conventions with currency pair and maturity
- **Maintained PNG Support**: Original PNG export still available

### 📋 **Content Organization**
- **Collapsible Details Section**: "Detailed DCD Structure & Scenarios Analysis"
  - Currency scenarios with concrete examples
  - Risk-return analysis breakdown
  - Product mechanics timeline
  - Market sensitivity analysis
- **Streamlined Main View**: Focus on essential pricing results and visualization

### 🔧 **Technical Improvements**
- **Enhanced Plotly Configuration**: Custom download options and professional styling
- **Better Error Handling**: Improved user experience with validation
- **Optimized Performance**: Faster rendering with cleaner code structure

### 📈 **Chart Enhancements**
- **Professional Styling**: Better colors, annotations, and legends
- **Export-Ready**: Charts optimized for professional presentations
- **Interactive Features**: Enhanced tooltips and zoom functionality

## Previous Versions

### Version 2.0.0 - Market Conventions & Currency Features
- Professional day count conventions (360/365)
- Multi-currency support with proper labeling
- T+2 settlement modeling
- Maturity-dependent rate curves
- Corrected DCD payoff structure

### Version 1.0.0 - Initial Release
- Basic DCD pricing with QuantLib
- Streamlit web interface
- Rate matrix generation
- Greeks calculation
