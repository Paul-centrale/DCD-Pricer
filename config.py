# DCD Pricer Configuration
# Default market parameters and settings

DEFAULT_PARAMS = {
    "market": {
        "spot": 1.0500,
        "domestic_rate": 0.035,  # 3.5%
        "foreign_rate": 0.050,   # 5.0%
        "volatility": 0.12       # 12%
    },
    "product": {
        "maturity_days": 91,
        "notional": 1000000,
        "base_rate": 0.02,       # 2.0%
        "strike": 1.0300
    },
    "matrix": {
        "strike_range_pct": 0.05,  # ±5% around spot
        "strike_steps": 10,
        "maturity_min": 30,
        "maturity_max": 180,
        "maturity_steps": 6
    }
}

CURRENCY_PAIRS = [
    "EUR/USD", "GBP/USD", "USD/JPY", 
    "AUD/USD", "USD/CHF", "USD/CAD",
    "NZD/USD", "EUR/GBP", "EUR/JPY"
]

# Typical market data ranges for validation
VALIDATION_RANGES = {
    "spot": (0.5, 2.0),
    "rates": (0.0, 0.10),      # 0% to 10%
    "volatility": (0.05, 0.50), # 5% to 50%
    "maturity": (1, 365),       # 1 day to 1 year
    "notional": (10000, 100000000)  # $10K to $100M
}
