import streamlit as st
import QuantLib as ql
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import datetime

class DCDPricer:
    """
    Dual Currency Deposit (DCD) Pricer
    A DCD is a structured product that combines:
    1. A deposit in the base currency
    2. A short call option on the currency pair
    """
    
    def __init__(self, spot, domestic_rate, foreign_rate, volatility, maturity_days, 
                 currency_pair="EUR/USD", day_count_basis=360, settlement_days=2):
        self.spot = spot
        self.domestic_rate = domestic_rate
        self.foreign_rate = foreign_rate
        self.volatility = volatility
        self.maturity_days = maturity_days
        self.currency_pair = currency_pair
        self.day_count_basis = day_count_basis
        self.settlement_days = settlement_days
        
        # Parse currency pair
        self.base_currency, self.quote_currency = currency_pair.split("/")
        
        # Setup QuantLib environment
        self.setup_quantlib()
    
    def setup_quantlib(self):
        """Setup QuantLib calendar and day counter with proper conventions"""
        self.calendar = ql.TARGET()
        
        # Set day counter based on currency and basis
        if self.day_count_basis == 360:
            self.day_counter = ql.Thirty360(ql.Thirty360.BondBasis)
        else:
            self.day_counter = ql.Actual365Fixed()
        
        # Set evaluation date
        today = ql.Date.todaysDate()
        ql.Settings.instance().evaluationDate = today
        self.evaluation_date = today
        
        # Calculate option maturity date (T)
        self.option_maturity_date = self.calendar.advance(
            today, self.maturity_days, ql.Days, ql.ModifiedFollowing
        )
        
        # Calculate deposit settlement date (T + settlement_days)
        self.deposit_settlement_date = self.calendar.advance(
            self.option_maturity_date, self.settlement_days, ql.Days, ql.ModifiedFollowing
        )
        
        # Time calculations
        self.time_to_option_maturity = self.day_counter.yearFraction(today, self.option_maturity_date)
        self.time_to_deposit_settlement = self.day_counter.yearFraction(today, self.deposit_settlement_date)
        
        # For deposit rate calculation, use the deposit settlement period
        if self.day_count_basis == 360:
            self.deposit_year_fraction = self.maturity_days / 360.0
        else:
            self.deposit_year_fraction = self.maturity_days / 365.0
    
    def price_vanilla_option(self, strike, option_type='Call'):
        """Price a vanilla European option using Black-Scholes"""
        
        # Create option with option maturity (not deposit settlement)
        payoff = ql.PlainVanillaPayoff(
            ql.Option.Call if option_type == 'Call' else ql.Option.Put, 
            strike
        )
        exercise = ql.EuropeanExercise(self.option_maturity_date)
        option = ql.VanillaOption(payoff, exercise)
        
        # Market data
        spot_handle = ql.QuoteHandle(ql.SimpleQuote(self.spot))
        
        # Risk-free rate curves
        domestic_curve = ql.FlatForward(
            self.evaluation_date, 
            self.domestic_rate, 
            self.day_counter
        )
        foreign_curve = ql.FlatForward(
            self.evaluation_date, 
            self.foreign_rate, 
            self.day_counter
        )
        
        domestic_handle = ql.YieldTermStructureHandle(domestic_curve)
        foreign_handle = ql.YieldTermStructureHandle(foreign_curve)
        
        # Volatility
        vol_handle = ql.BlackVolTermStructureHandle(
            ql.BlackConstantVol(
                self.evaluation_date, 
                self.calendar, 
                self.volatility, 
                self.day_counter
            )
        )
        
        # Black-Scholes process
        bs_process = ql.GarmanKohlagenProcess(
            spot_handle, 
            foreign_handle, 
            domestic_handle, 
            vol_handle
        )
        
        # Pricing engine
        engine = ql.AnalyticEuropeanEngine(bs_process)
        option.setPricingEngine(engine)
        
        return {
            'price': option.NPV(),
            'delta': option.delta(),
            'gamma': option.gamma(),
            'theta': option.theta(),
            'vega': option.vega(),
            'rho': option.rho()
        }
    
    def calculate_maturity_adjusted_rate(self, base_rate, rate_curve_slope=0.0001, rate_structure=None):
        """
        Calculate maturity-adjusted deposit rate using tiered structure
        Can use either linear progression or tiered rate structure
        """
        if rate_structure is not None:
            # Use tiered rate structure
            for max_days, rate in sorted(rate_structure.items()):
                if self.maturity_days <= max_days:
                    return rate
            # If maturity exceeds all tiers, use the highest rate
            return max(rate_structure.values())
        else:
            # Fallback to linear progression
            maturity_years = self.maturity_days / 365.0
            adjusted_rate = base_rate + (rate_curve_slope * maturity_years * 365)
            return adjusted_rate
    
    def calculate_dcd_rate(self, strike, notional=1000000, base_rate=0.02, 
                          use_maturity_adjustment=True, rate_curve_slope=0.0001, rate_structure=None):
        """
        Calculate the enhanced rate for a DCD product
        DCD Rate = Adjusted Base Rate + Option Premium / (Notional * Time to Maturity)
        """
        # Calculate maturity-adjusted base rate
        if use_maturity_adjustment:
            adjusted_base_rate = self.calculate_maturity_adjusted_rate(base_rate, rate_curve_slope, rate_structure)
        else:
            adjusted_base_rate = base_rate
        
        # Price the embedded option
        option_result = self.price_vanilla_option(strike, 'Call')
        option_premium = option_result['price'] * notional
        
        # Enhanced rate calculation using deposit year fraction
        rate_enhancement = option_premium / (notional * self.deposit_year_fraction)
        enhanced_rate = adjusted_base_rate + rate_enhancement
        
        # Probability of conversion (option being in the money at option maturity)
        d2 = (np.log(self.spot / strike) + 
              (self.domestic_rate - self.foreign_rate - 0.5 * self.volatility**2) * self.time_to_option_maturity) / (self.volatility * np.sqrt(self.time_to_option_maturity))
        prob_conversion = 1 - ql.CumulativeNormalDistribution()(d2)
        
        return {
            'enhanced_rate': enhanced_rate,
            'base_rate': adjusted_base_rate,
            'rate_enhancement': rate_enhancement,
            'option_premium': option_premium,
            'probability_conversion': prob_conversion,
            'greeks': option_result,
            'notional_base_currency': notional,
            'notional_quote_currency': notional / strike  # Conversion amount if exercised
        }
    
    def create_rate_matrix(self, strike_range, maturity_range, notional=1000000, 
                          base_rate=0.02, use_maturity_adjustment=True, rate_curve_slope=0.0001, rate_structure=None):
        """Create a matrix of enhanced rates for different strikes and maturities"""
        results = []
        
        # Store original values
        original_maturity = self.maturity_days
        original_time_to_option_maturity = self.time_to_option_maturity
        original_time_to_deposit_settlement = self.time_to_deposit_settlement
        original_option_maturity_date = self.option_maturity_date
        original_deposit_settlement_date = self.deposit_settlement_date
        original_deposit_year_fraction = self.deposit_year_fraction
        
        for maturity in maturity_range:
            # Update maturity for this calculation
            self.maturity_days = int(maturity)  # Ensure it's an integer
            
            # Recalculate dates and time fractions
            self.option_maturity_date = self.calendar.advance(
                self.evaluation_date, 
                self.maturity_days, 
                ql.Days, 
                ql.ModifiedFollowing
            )
            self.deposit_settlement_date = self.calendar.advance(
                self.option_maturity_date, 
                self.settlement_days, 
                ql.Days, 
                ql.ModifiedFollowing
            )
            
            self.time_to_option_maturity = self.day_counter.yearFraction(
                self.evaluation_date, 
                self.option_maturity_date
            )
            self.time_to_deposit_settlement = self.day_counter.yearFraction(
                self.evaluation_date, 
                self.deposit_settlement_date
            )
            
            # Update deposit year fraction
            if self.day_count_basis == 360:
                self.deposit_year_fraction = self.maturity_days / 360.0
            else:
                self.deposit_year_fraction = self.maturity_days / 365.0
            
            row_data = []
            for strike in strike_range:
                try:
                    dcd_result = self.calculate_dcd_rate(
                        strike, notional, base_rate, 
                        use_maturity_adjustment, rate_curve_slope, rate_structure
                    )
                    row_data.append(dcd_result['enhanced_rate'] * 100)  # Convert to percentage
                except Exception as e:
                    # Handle any pricing errors gracefully
                    row_data.append(np.nan)
            
            results.append(row_data)
        
        # Restore original values
        self.maturity_days = original_maturity
        self.time_to_option_maturity = original_time_to_option_maturity
        self.time_to_deposit_settlement = original_time_to_deposit_settlement
        self.option_maturity_date = original_option_maturity_date
        self.deposit_settlement_date = original_deposit_settlement_date
        self.deposit_year_fraction = original_deposit_year_fraction
        
        return np.array(results)

def main():
    st.set_page_config(
        page_title="DCD Pricer - Dual Currency Deposit",
        page_icon="💱",
        layout="wide"
    )
    
    st.title("DCD (Dual Currency Deposit) Pricer")
    
    # Add informational section
    with st.expander("About Dual Currency Deposits", expanded=False):
        st.markdown("""
        **What is a DCD?**
        
        A Dual Currency Deposit (DCD) is a structured financial product that offers enhanced returns by combining:
        - **Enhanced Deposit Rate**: Higher interest rate than regular deposits
        - **Currency Option**: Short call option that may result in currency conversion
        
        **How it works:**
        1. You deposit money in the base currency (e.g., USD)
        2. You receive a higher interest rate than regular deposits
        3. If the exchange rate exceeds the strike at maturity, your principal is converted to the foreign currency
        4. If the exchange rate stays below the strike, you receive your enhanced deposit in the original currency
        
        **Key Considerations:**
        - **Higher Returns**: Enhanced interest rates
        - **Currency Risk**: Potential conversion to foreign currency
        - **Probability**: Conversion probability shown in real-time
        """)
    
    st.markdown("---")
    
    # Sidebar for parameters
    st.sidebar.header("Market Parameters")
    
    # Currency pair selection with day count conventions
    currency_pairs = {
        "EUR/USD": {"default_basis": 360, "convention": "European"},
        "GBP/USD": {"default_basis": 365, "convention": "UK/US"},
        "USD/JPY": {"default_basis": 360, "convention": "USD/Asian"},
        "AUD/USD": {"default_basis": 365, "convention": "Australian"},
        "USD/CHF": {"default_basis": 360, "convention": "USD/Swiss"},
        "USD/CAD": {"default_basis": 365, "convention": "North American"},
        "NZD/USD": {"default_basis": 365, "convention": "New Zealand"}
    }
    
    currency_pair = st.sidebar.selectbox(
        "Currency Pair",
        list(currency_pairs.keys()),
        index=0
    )
    
    # Day count basis
    default_basis = currency_pairs[currency_pair]["default_basis"]
    day_count_basis = st.sidebar.selectbox(
        f"Day Count Basis ({currency_pairs[currency_pair]['convention']} default: {default_basis})",
        [360, 365],
        index=0 if default_basis == 360 else 1
    )
    
    # Settlement days
    settlement_days = st.sidebar.number_input(
        "Settlement Days (Option → Deposit)", 
        value=2, step=1, min_value=0, max_value=5,
        help="Standard FX settlement is T+2"
    )
    
    # Market data inputs
    spot = st.sidebar.number_input("Spot Rate", value=1.0500, step=0.0001, format="%.4f")
    domestic_rate = st.sidebar.number_input("Domestic Rate (%)", value=3.5, step=0.1) / 100
    foreign_rate = st.sidebar.number_input("Foreign Rate (%)", value=5.0, step=0.1) / 100
    volatility = st.sidebar.number_input("Volatility (%)", value=12.0, step=0.5) / 100
    
    # Product parameters
    st.sidebar.header("Product Parameters")
    maturity_days = st.sidebar.number_input("Maturity (Days)", value=91, step=1)
    
    # Notional with currency specification
    base_currency, quote_currency = currency_pair.split("/")
    notional = st.sidebar.number_input(
        f"Notional Amount ({base_currency})", 
        value=1000000, step=100000,
        help=f"Deposit amount in {base_currency}"
    )
    
    # Enhanced deposit rate parameters
    st.sidebar.subheader("Deposit Rate Structure")
    
    rate_structure_type = st.sidebar.radio(
        "Rate Structure Type",
        ["Tiered Rates", "Linear Progression"],
        help="Choose how deposit rates vary with maturity"
    )
    
    rate_structure = None
    
    if rate_structure_type == "Tiered Rates":
        st.sidebar.markdown("**Define Rate Tiers:**")
        st.sidebar.caption("Enter rates for different maturity ranges (rates apply up to the specified days)")
        
        # Default tiered structure
        tier1_days = st.sidebar.number_input("Tier 1: Up to (days)", value=21, step=1, min_value=1)
        tier1_rate = st.sidebar.number_input("Tier 1: Rate (%)", value=2.00, step=0.01) / 100
        
        tier2_days = st.sidebar.number_input("Tier 2: Up to (days)", value=60, step=1, min_value=tier1_days+1)
        tier2_rate = st.sidebar.number_input("Tier 2: Rate (%)", value=2.10, step=0.01) / 100
        
        tier3_days = st.sidebar.number_input("Tier 3: Up to (days)", value=90, step=1, min_value=tier2_days+1)
        tier3_rate = st.sidebar.number_input("Tier 3: Rate (%)", value=2.30, step=0.01) / 100
        
        tier4_days = st.sidebar.number_input("Tier 4: Up to (days)", value=180, step=1, min_value=tier3_days+1)
        tier4_rate = st.sidebar.number_input("Tier 4: Rate (%)", value=2.50, step=0.01) / 100
        
        tier5_days = st.sidebar.number_input("Tier 5: Above (days)", value=365, step=1, min_value=tier4_days+1)
        tier5_rate = st.sidebar.number_input("Tier 5: Rate (%)", value=2.80, step=0.01) / 100
        
        rate_structure = {
            tier1_days: tier1_rate,
            tier2_days: tier2_rate,
            tier3_days: tier3_rate,
            tier4_days: tier4_rate,
            tier5_days: tier5_rate
        }
        
        # Display current tier for selected maturity
        current_rate = None
        for max_days, rate in sorted(rate_structure.items()):
            if maturity_days <= max_days:
                current_rate = rate
                break
        if current_rate is None:
            current_rate = max(rate_structure.values())
        
        st.sidebar.info(f"Current maturity ({maturity_days}d) rate: {current_rate:.3%}")
        
    else:
        # Linear progression (original method)
        base_rate = st.sidebar.number_input("Base Deposit Rate (%)", value=2.0, step=0.1) / 100
        
        use_maturity_adjustment = st.sidebar.checkbox(
            "Apply Maturity Term Structure", 
            value=True,
            help="Longer maturities typically command higher base rates"
        )
        
        if use_maturity_adjustment:
            rate_curve_slope = st.sidebar.number_input(
                "Rate Curve Slope (bps/day)", 
                value=0.1, step=0.01, 
                help="Rate increase per day of maturity"
            ) / 10000  # Convert bps to decimal
        else:
            rate_curve_slope = 0.0
            
        # Set base_rate for compatibility
        if rate_structure_type == "Linear Progression":
            # For linear progression, we'll still pass base_rate
            pass
    
    # For tiered rates, we need to set some base_rate for compatibility
    if rate_structure_type == "Tiered Rates":
        base_rate = tier1_rate  # Use first tier as base
        use_maturity_adjustment = True
        rate_curve_slope = 0.0
    
    # Strike parameter
    strike = st.sidebar.number_input("Strike Rate", value=1.0300, step=0.0001, format="%.4f")
    
    # Create pricer instance
    pricer = DCDPricer(
        spot, domestic_rate, foreign_rate, volatility, maturity_days,
        currency_pair, day_count_basis, settlement_days
    )
    
    # Main content area
    st.subheader(f"DCD Pricing Results ({currency_pair})")
    
    # Calculate DCD rate
    dcd_result = pricer.calculate_dcd_rate(
        strike, notional, base_rate, use_maturity_adjustment, rate_curve_slope, rate_structure
    )
    
    # Display key metrics in a single line
    metrics_col1, metrics_col2, metrics_col3 = st.columns(3)
    
    with metrics_col1:
        st.markdown(f"""
        <div style="text-align: center;">
            <h4 style="margin-bottom: 5px;">Enhanced Rate</h4>
            <h2 style="color: green; margin: 0; font-size: 1.8rem;">{dcd_result['enhanced_rate']:.3%}</h2>
            <p style="color: gray; font-size: 0.9rem; margin: 0;">+{(dcd_result['enhanced_rate'] - dcd_result['base_rate']):.3%}</p>
            <p style="font-size: 0.8rem; margin: 0;">Annual rate on {base_currency} deposit</p>
        </div>
        """, unsafe_allow_html=True)
    
    with metrics_col2:
        st.markdown(f"""
        <div style="text-align: center;">
            <h4 style="margin-bottom: 5px;">Option Premium</h4>
            <h3 style="color: blue; margin: 0; font-size: 1.5rem;">{base_currency} {dcd_result['option_premium']:,.0f}</h3>
            <p style="font-size: 0.8rem; margin: 0;">Value of embedded call option</p>
        </div>
        """, unsafe_allow_html=True)
    
    with metrics_col3:
        st.markdown(f"""
        <div style="text-align: center;">
            <h4 style="margin-bottom: 5px;">Conversion Probability</h4>
            <h2 style="color: orange; margin: 0; font-size: 1.8rem;">{dcd_result['probability_conversion']:.1%}</h2>
            <p style="font-size: 0.8rem; margin: 0;">Probability of receiving {quote_currency} instead</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Payoff Diagram Section
    # Payoff Diagram Section
    st.markdown("---")
    st.subheader(f"DCD Payoff Diagram ({currency_pair})")
    
    # Create CORRECT payoff diagram for DCD (short call structure)
    spot_range = np.linspace(spot * 0.8, spot * 1.2, 100)
    
    enhanced_deposit_amount = notional * (1 + dcd_result['enhanced_rate'] * pricer.deposit_year_fraction)
    
    # Calculate payoffs - CORRECTED
    final_payoff_eur = []  # Always show in EUR terms for clarity
    
    for s in spot_range:
        if s > strike:
            # Option exercised - we are FORCED to convert our EUR to USD at strike
            # We get: notional * strike USD
            # But we wanted to keep our EUR, so we lose the opportunity
            usd_received = notional * strike
            # This USD amount is worth: usd_received / s EUR at current market rate
            eur_equivalent = usd_received / s
            final_payoff_eur.append(eur_equivalent)
        else:
            # Option not exercised - we keep our enhanced EUR deposit
            final_payoff_eur.append(enhanced_deposit_amount)
    
    fig = go.Figure()
    
    # Add the DCD payoff line
    fig.add_trace(go.Scatter(
        x=spot_range, 
        y=final_payoff_eur,
        mode='lines',
        name='DCD Payoff (EUR equivalent)',
        line=dict(color='blue', width=3),
        hovertemplate=f'{currency_pair}: %{{x:.4f}}<br>EUR Equivalent: %{{y:,.0f}}<extra></extra>'
    ))
    
    # Add reference lines
    fig.add_hline(y=notional, line_dash="dot", line_color="gray", 
                 annotation_text=f"Original Principal: {notional:,.0f} {base_currency}")
    
    fig.add_hline(y=enhanced_deposit_amount, line_dash="dot", line_color="green", 
                 annotation_text=f"Enhanced Deposit: {enhanced_deposit_amount:,.0f} {base_currency}")
    
    fig.add_vline(x=strike, line_dash="dash", line_color="red", 
                 annotation_text=f"Strike: {strike:.4f}")
    fig.add_vline(x=spot, line_dash="dash", line_color="blue", 
                 annotation_text=f"Current Spot: {spot:.4f}")
    
    fig.update_layout(
        title=f"DCD Payoff at Maturity ({maturity_days} days + {settlement_days} settlement)",
        xaxis_title=f"{currency_pair} Rate at Option Maturity",
        yaxis_title=f"Final Value (in {base_currency} equivalent)",
        height=400,
        showlegend=True
    )
    
    # Configure Plotly to enable SVG download
    config = {
        'toImageButtonOptions': {
            'format': 'svg',  # Set default format to SVG
            'filename': f'DCD_Payoff_{currency_pair}_{maturity_days}d',
            'height': 400,
            'width': 800,
            'scale': 1
        },
        'modeBarButtonsToAdd': [
            'downloadsvg'  # Add SVG download button
        ],
        'displayModeBar': True,
        'displaylogo': False
    }
    
    st.plotly_chart(fig, use_container_width=True, config=config)
    
    # Rate Structure and Greeks in 2-column layout
    st.markdown("---")
    details_col1, details_col2 = st.columns(2)
    
    with details_col1:
        st.subheader("Rate Structure")
        if rate_structure_type == "Tiered Rates":
            # Show tiered rate structure
            tier_data = []
            for i, (max_days, rate) in enumerate(sorted(rate_structure.items()), 1):
                if i == 1:
                    tier_data.append({"Tier": f"Tier {i}", "Days": f"1-{max_days}", "Rate": f"{rate:.3%}"})
                else:
                    prev_days = sorted(rate_structure.keys())[i-2] + 1
                    tier_data.append({"Tier": f"Tier {i}", "Days": f"{prev_days}-{max_days}", "Rate": f"{rate:.3%}"})
            
            tier_df = pd.DataFrame(tier_data)
            st.dataframe(tier_df, use_container_width=True)
            
            # Highlight current tier
            current_tier = None
            for i, (max_days, rate) in enumerate(sorted(rate_structure.items()), 1):
                if maturity_days <= max_days:
                    current_tier = i
                    break
            if current_tier:
                st.info(f"Current maturity ({maturity_days}d) uses Tier {current_tier}: {dcd_result['base_rate']:.3%}")
        else:
            # Show linear progression structure
            rate_info = pd.DataFrame([
                {"Component": f"Base Rate ({maturity_days}d)", "Value": f"{dcd_result['base_rate']:.3%}"},
                {"Component": "Option Enhancement", "Value": f"{dcd_result['rate_enhancement']:.3%}"},
                {"Component": "**Total Enhanced Rate**", "Value": f"**{dcd_result['enhanced_rate']:.3%}**"},
                {"Component": f"Day Count Basis", "Value": f"{day_count_basis} days/year"},
                {"Component": "Settlement Lag", "Value": f"T+{settlement_days} days"}
            ])
            st.dataframe(rate_info, use_container_width=True)
    
    with details_col2:
        st.subheader("Option Greeks")
        greeks_df = pd.DataFrame([
            {"Greek": "Delta", "Value": f"{dcd_result['greeks']['delta']:.4f}", "Description": "Sensitivity to spot price"},
            {"Greek": "Gamma", "Value": f"{dcd_result['greeks']['gamma']:.4f}", "Description": "Delta sensitivity"},
            {"Greek": "Theta", "Value": f"{dcd_result['greeks']['theta']:.4f}", "Description": "Time decay (per day)"},
            {"Greek": "Vega", "Value": f"{dcd_result['greeks']['vega']:.4f}", "Description": "Volatility sensitivity"},
            {"Greek": "Rho", "Value": f"{dcd_result['greeks']['rho']:.4f}", "Description": "Interest rate sensitivity"}
        ])
        st.dataframe(greeks_df, use_container_width=True)
    
    # Rate Matrix Section
    st.markdown("---")
    st.subheader("Enhanced Rate Matrix Analysis")
    
    # Matrix parameters
    matrix_col1, matrix_col2 = st.columns(2)
    
    with matrix_col1:
        strike_min = st.number_input("Strike Range - Min", value=spot * 0.95, step=0.001, format="%.4f")
        strike_max = st.number_input("Strike Range - Max", value=spot * 1.05, step=0.001, format="%.4f")
        strike_steps = st.number_input("Strike Steps", value=10, step=1)
    
    with matrix_col2:
        maturity_min = st.number_input("Maturity Range - Min (Days)", value=30, step=1)
        maturity_max = st.number_input("Maturity Range - Max (Days)", value=180, step=1)
        maturity_steps = st.number_input("Maturity Steps", value=6, step=1)
    
    if st.button("Generate Rate Matrix", type="primary"):
        # Validate inputs
        if strike_min >= strike_max:
            st.error("Strike minimum must be less than strike maximum")
            return
        
        if maturity_min >= maturity_max:
            st.error("Maturity minimum must be less than maturity maximum")
            return
        
        if strike_steps < 2 or maturity_steps < 2:
            st.error("Number of steps must be at least 2")
            return
        
        with st.spinner("Calculating rate matrix..."):
            try:
                # Generate ranges
                strike_range = np.linspace(strike_min, strike_max, int(strike_steps))
                maturity_range = np.linspace(maturity_min, maturity_max, int(maturity_steps), dtype=int)
                
                # Calculate matrix
                rate_matrix = pricer.create_rate_matrix(
                    strike_range, maturity_range, notional, base_rate,
                    use_maturity_adjustment, rate_curve_slope, rate_structure
                )
                
                # Check for any NaN values
                if np.isnan(rate_matrix).any():
                    st.warning("Some calculations resulted in invalid values. This may be due to extreme parameter combinations.")
                
                # Create heatmap
                fig = go.Figure(data=go.Heatmap(
                    z=rate_matrix,
                    x=[f"{s:.4f}" for s in strike_range],
                    y=[f"{m}d" for m in maturity_range],
                    colorscale='RdYlGn',
                    text=np.round(rate_matrix, 3),
                    texttemplate="%{text}%",
                    textfont={"size": 10},
                    colorbar=dict(title="Enhanced Rate (%)")
                ))
                
                fig.update_layout(
                    title="Enhanced Rate Matrix (Strike vs Maturity)",
                    xaxis_title="Strike Levels",
                    yaxis_title="Maturity",
                    height=500
                )
                
                # Configure SVG download for heatmap
                heatmap_config = {
                    'toImageButtonOptions': {
                        'format': 'svg',
                        'filename': f'DCD_Rate_Matrix_{currency_pair}_{maturity_min}-{maturity_max}d',
                        'height': 500,
                        'width': 900,
                        'scale': 1
                    },
                    'modeBarButtonsToAdd': [
                        'downloadsvg'
                    ],
                    'displayModeBar': True,
                    'displaylogo': False
                }
                
                st.plotly_chart(fig, use_container_width=True, config=heatmap_config)
                
                # Display matrix as table
                st.subheader("Rate Matrix Table")
                matrix_df = pd.DataFrame(
                    rate_matrix, 
                    index=[f"{m} days" for m in maturity_range],
                    columns=[f"{s:.4f}" for s in strike_range]
                )
                st.dataframe(matrix_df.round(3), use_container_width=True)
                
            except Exception as e:
                st.error(f"Error generating rate matrix: {str(e)}")
                st.info("Please check your input parameters and try again.")
    
    # Key Insights Section
    st.markdown("---")
    st.subheader("Key Insights & Risk Analysis")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**Rate Enhancement**")
        enhancement_bps = (dcd_result['enhanced_rate'] - base_rate) * 10000
        st.metric("Rate Enhancement", f"{enhancement_bps:.0f} bps")
        
        if enhancement_bps > 500:
            st.success("High enhancement - attractive for yield seekers")
        elif enhancement_bps > 200:
            st.info("Moderate enhancement - balanced risk/reward")
        else:
            st.warning("Low enhancement - consider longer maturity or different strike")
    
    with col2:
        st.markdown("**Risk Assessment**")
        prob = dcd_result['probability_conversion']
        st.metric("Conversion Risk", f"{prob:.1%}")
        
        if prob < 0.20:
            st.success("Low conversion risk")
        elif prob < 0.50:
            st.info("Moderate conversion risk")
        else:
            st.warning("High conversion risk - monitor carefully")
    
    with col3:
        st.markdown("**Market Sensitivity**")
        vega_pct = dcd_result['greeks']['vega'] * 100  # Convert to percentage
        st.metric("Volatility Sensitivity", f"{vega_pct:.2f}%")
        
        if abs(vega_pct) > 20:
            st.warning("High volatility sensitivity")
        elif abs(vega_pct) > 10:
            st.info("Moderate volatility sensitivity")
        else:
            st.success("Low volatility sensitivity")
    
    # Footer with technical notes
    st.markdown("---")
    st.markdown("**Technical Notes:**")
    st.caption(f"""
    • Pricing Model: Garman-Kohlhagen (FX Black-Scholes) via QuantLib
    • Currency Pair: {currency_pair} | Day Count: {day_count_basis} days/year | Settlement: T+{settlement_days}
    • Current Spot: {spot:.4f} | Strike: {strike:.4f} | Moneyness: {(spot/strike-1)*100:+.2f}%
    • Option Maturity: {pricer.time_to_option_maturity:.4f} years ({maturity_days} days)
    • Deposit Settlement: {pricer.time_to_deposit_settlement:.4f} years ({maturity_days + settlement_days} days)
    • Interest Rate Differential: {(domestic_rate-foreign_rate)*100:+.2f}% ({base_currency}-{quote_currency})
    • Deposit Year Fraction: {pricer.deposit_year_fraction:.4f} ({maturity_days}/{day_count_basis})
    """)
    
    # Detailed Scenarios and Structure Explanation - Collapsible Section
    with st.expander("Detailed DCD Structure & Scenarios Analysis", expanded=False):
        st.markdown("### Currency Scenarios")
        
        scenario_col1, scenario_col2 = st.columns(2)
        
        with scenario_col1:
            st.success(f"**Scenario 1: Rate ≤ {strike:.4f} (Good Outcome)**\n\n"
                      f"• Call option expires worthless\n"
                      f"• You keep: **{base_currency} {notional * (1 + dcd_result['enhanced_rate'] * pricer.deposit_year_fraction):,.0f}**\n"
                      f"• Principal: {base_currency} {notional:,.0f}\n"
                      f"• Interest: {base_currency} {notional * dcd_result['enhanced_rate'] * pricer.deposit_year_fraction:,.0f}\n"
                      f"• **Enhanced Rate: {dcd_result['enhanced_rate']:.3%}**")
        
        with scenario_col2:
            usd_received = notional * strike
            st.error(f"**Scenario 2: Rate > {strike:.4f} (Conversion)**\n\n"
                    f"• Call option exercised against you\n"
                    f"• You receive: **{quote_currency} {usd_received:,.0f}** (fixed)\n"
                    f"• You miss gains above {strike:.4f} rate\n"
                    f"• **Loss increases as {currency_pair} rises**\n"
                    f"• No interest earned on deposit")
        
        st.markdown("---")
        st.markdown("### DCD Payoff Structure Explained")
        
        st.info(f"""
        **You are SHORT a call option on {currency_pair}:**
        
        **Below Strike (≤ {strike:.4f})**: 
        - Call option expires worthless
        - You keep: **{enhanced_deposit_amount:,.0f} {base_currency}** (enhanced deposit)
        - **This is the preferred outcome**
        
        **Above Strike (> {strike:.4f})**: 
        - Call option exercised against you
        - You must sell your {base_currency} at strike rate of {strike:.4f}
        - You receive: **{notional * strike:,.0f} {quote_currency}** (fixed amount)
        - **Loss**: You miss out on higher market rates above {strike:.4f}
        
        **Concrete Example:**
        If {currency_pair} = 1.20 at maturity and strike = {strike:.4f}:
        - Without DCD: {notional:,.0f} {base_currency} → {notional * 1.20:,.0f} {quote_currency}
        - With DCD: {notional:,.0f} {base_currency} → {notional * strike:,.0f} {quote_currency}
        - **Your loss: {notional * (1.20 - strike):,.0f} {quote_currency}!**
        """)
        
        st.markdown("---")
        st.markdown("### Risk-Return Analysis")
        
        analysis_col1, analysis_col2, analysis_col3 = st.columns(3)
        
        with analysis_col1:
            st.markdown("**Enhanced Yield**")
            st.write(f"• Base Rate: {dcd_result['base_rate']:.3%}")
            st.write(f"• Enhancement: +{dcd_result['rate_enhancement']:.3%}")
            st.write(f"• **Total: {dcd_result['enhanced_rate']:.3%}**")
            st.write(f"• Extra Income: {base_currency} {notional * dcd_result['rate_enhancement'] * pricer.deposit_year_fraction:,.0f}")
        
        with analysis_col2:
            st.markdown("**Conversion Risk**")
            st.write(f"• Probability: {dcd_result['probability_conversion']:.1%}")
            st.write(f"• Strike Level: {strike:.4f}")
            st.write(f"• Current Spot: {spot:.4f}")
            moneyness = (spot/strike - 1) * 100
            st.write(f"• Moneyness: {moneyness:+.2f}%")
        
        with analysis_col3:
            st.markdown("**Market Sensitivity**")
            st.write(f"• Delta: {dcd_result['greeks']['delta']:.4f}")
            st.write(f"• Vega: {dcd_result['greeks']['vega']:.4f}")
            st.write(f"• Theta: {dcd_result['greeks']['theta']:.4f}")
            st.write(f"• Volatility: {volatility:.1%}")
        
        st.markdown("---")
        st.markdown("### Product Mechanics")
        
        st.write(f"""
        **Timeline:**
        1. **Today**: Deposit {notional:,.0f} {base_currency}
        2. **Day {maturity_days}**: Option maturity - check if {currency_pair} > {strike:.4f}
        3. **Day {maturity_days + settlement_days}**: Settlement and payout
        
        **Option Premium**: {base_currency} {dcd_result['option_premium']:,.0f}
        **Enhancement Period**: {pricer.deposit_year_fraction:.4f} years ({maturity_days}/{day_count_basis} days)
        **Settlement Convention**: T+{settlement_days} business days
        **Day Count**: {day_count_basis} days/year ({currency_pairs[currency_pair]['convention']} convention)
        """)

if __name__ == "__main__":
    main()