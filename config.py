"""Configuration settings for the backtesting project."""

import os
from dotenv import load_dotenv

load_dotenv()

# API Configuration
ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY", "demo")
FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY", "")

# Data Configuration
DATA_SOURCE = "yfinance"  # Options: yfinance, alpha_vantage, finnhub
CACHE_DIR = "data/cache"
OUTPUT_DIR = "results"

# Backtesting Configuration
INITIAL_CAPITAL = 100000  # Starting capital in USD
COMMISSION_RATE = 0.001  # 0.1% commission per trade
SLIPPAGE = 0.0001  # 0.01% slippage

# Strategy Configuration
SYMBOLS = ["AAPL", "MSFT", "GOOGL", "AMZN"]
START_DATE = "2022-01-01"
END_DATE = "2024-12-31"

# Technical Indicators
RSI_PERIOD = 14
MA_SHORT_PERIOD = 20
MA_LONG_PERIOD = 50
