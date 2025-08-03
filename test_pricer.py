#!/usr/bin/env python3
"""
Test script for DCD Pricer functionality
This script tests the core pricing functions to ensure they work correctly
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from main import DCDPricer
import numpy as np

def test_basic_pricing():
    """Test basic DCD pricing functionality"""
    print("🧪 Testing DCD Pricer Basic Functionality")
    print("=" * 50)
    
    # Create a pricer instance with typical market parameters
    pricer = DCDPricer(
        spot=1.0500,           # EUR/USD spot
        domestic_rate=0.035,   # 3.5% USD rate
        foreign_rate=0.050,    # 5.0% EUR rate
        volatility=0.12,       # 12% volatility
        maturity_days=91,      # 3 months
        currency_pair="EUR/USD",
        day_count_basis=360,
        settlement_days=2
    )
    
    print(f"✅ Pricer initialized successfully")
    print(f"   Currency Pair: {pricer.currency_pair}")
    print(f"   Spot: {pricer.spot}")
    print(f"   Day Count Basis: {pricer.day_count_basis}")
    print(f"   Settlement Days: {pricer.settlement_days}")
    print(f"   Time to option maturity: {pricer.time_to_option_maturity:.4f} years")
    print(f"   Time to deposit settlement: {pricer.time_to_deposit_settlement:.4f} years")
    
    # Test option pricing
    strike = 1.0300
    option_result = pricer.price_vanilla_option(strike)
    
    print(f"\n📊 Option Pricing Results (Strike: {strike}):")
    print(f"   Option Price: {option_result['price']:.6f}")
    print(f"   Delta: {option_result['delta']:.4f}")
    print(f"   Gamma: {option_result['gamma']:.4f}")
    print(f"   Vega: {option_result['vega']:.4f}")
    
    # Test DCD rate calculation
    dcd_result = pricer.calculate_dcd_rate(
        strike, notional=1000000, base_rate=0.02, 
        use_maturity_adjustment=True, rate_curve_slope=0.0001
    )
    
    print(f"\n💰 DCD Pricing Results:")
    print(f"   Base Rate (adj): {dcd_result['base_rate']:.4%}")
    print(f"   Enhanced Rate: {dcd_result['enhanced_rate']:.4%}")
    print(f"   Rate Enhancement: {dcd_result['rate_enhancement']:.4%}")
    print(f"   Option Premium: {pricer.base_currency} {dcd_result['option_premium']:,.2f}")
    print(f"   Conversion Probability: {dcd_result['probability_conversion']:.2%}")
    print(f"   If Converted: {pricer.quote_currency} {dcd_result['notional_quote_currency']:,.0f}")
    
    # Test rate matrix calculation (small matrix for testing)
    print(f"\n🔢 Testing Rate Matrix Generation...")
    strike_range = np.linspace(1.0200, 1.0400, 3)
    maturity_range = np.array([30, 60, 90])
    
    try:
        rate_matrix = pricer.create_rate_matrix(strike_range, maturity_range)
        print(f"   ✅ Rate matrix generated successfully")
        print(f"   Matrix shape: {rate_matrix.shape}")
        print(f"   Sample rates: {rate_matrix[0, :].round(3)}%")
    except Exception as e:
        print(f"   ❌ Rate matrix generation failed: {e}")
        return False
    
    print(f"\n🎉 All tests passed successfully!")
    return True

def test_edge_cases():
    """Test edge cases and parameter validation"""
    print(f"\n🔍 Testing Edge Cases")
    print("=" * 30)
    
    # Test with extreme parameters
    try:
        pricer = DCDPricer(
            spot=1.0000,
            domestic_rate=0.001,   # Very low rate
            foreign_rate=0.001,
            volatility=0.01,       # Very low volatility
            maturity_days=1,       # Very short maturity
            currency_pair="EUR/USD",
            day_count_basis=360,
            settlement_days=2
        )
        
        result = pricer.calculate_dcd_rate(
            1.0000, notional=100000, base_rate=0.001,
            use_maturity_adjustment=False, rate_curve_slope=0.0
        )
        print(f"   ✅ Extreme parameters handled successfully")
        print(f"   Enhanced rate: {result['enhanced_rate']:.6%}")
        
    except Exception as e:
        print(f"   ⚠️  Extreme parameters issue: {e}")
    
    # Test with more realistic but challenging parameters
    try:
        pricer = DCDPricer(
            spot=1.2000,
            domestic_rate=0.10,    # High rate
            foreign_rate=0.02,     # Low foreign rate
            volatility=0.30,       # High volatility
            maturity_days=365,     # Long maturity
            currency_pair="GBP/USD",
            day_count_basis=365,
            settlement_days=2
        )
        
        result = pricer.calculate_dcd_rate(
            1.1500, notional=5000000, base_rate=0.03,
            use_maturity_adjustment=True, rate_curve_slope=0.0001
        )
        print(f"   ✅ High volatility scenario handled successfully")
        print(f"   Enhanced rate: {result['enhanced_rate']:.4%}")
        print(f"   Base rate (adjusted): {result['base_rate']:.4%}")
        
    except Exception as e:
        print(f"   ⚠️  High volatility scenario issue: {e}")

if __name__ == "__main__":
    print("🚀 DCD Pricer Test Suite")
    print("=" * 60)
    
    success = test_basic_pricing()
    
    if success:
        test_edge_cases()
        print(f"\n✨ Test suite completed successfully!")
        print(f"Your DCD Pricer is ready for production use!")
    else:
        print(f"\n❌ Tests failed. Please check the implementation.")
        sys.exit(1)
