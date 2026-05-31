"""Fetch historical data from financial APIs."""

import yfinance as yf
import pandas as pd
import os
from config import CACHE_DIR, DATA_SOURCE


class DataFetcher:
    """Fetch and cache historical stock data."""

    def __init__(self, source: str = "yfinance"):
        """Initialize the data fetcher."""
        self.source = source
        os.makedirs(CACHE_DIR, exist_ok=True)

    def fetch_data(self, symbol: str, start_date: str, end_date: str) -> pd.DataFrame:
        """Fetch historical data for a symbol."""
        cache_path = os.path.join(CACHE_DIR, f"{symbol}_{start_date}_{end_date}.csv")

        # Return cached data if available
        if os.path.exists(cache_path):
            print(f"Loading cached data for {symbol}")
            return pd.read_csv(cache_path, index_col=0, parse_dates=True)

        print(f"Fetching data for {symbol} from {start_date} to {end_date}")

        if self.source == "yfinance":
            data = self._fetch_yfinance(symbol, start_date, end_date)
        else:
            raise ValueError(f"Unknown data source: {self.source}")

        # Cache the data
        data.to_csv(cache_path)
        return data

    @staticmethod
    def _fetch_yfinance(symbol: str, start_date: str, end_date: str) -> pd.DataFrame:
        """Fetch data from Yahoo Finance."""
        ticker = yf.Ticker(symbol)
        data = ticker.history(start=start_date, end=end_date)
        return data

    def fetch_multiple(
        self, symbols: list, start_date: str, end_date: str
    ) -> dict:
        """Fetch data for multiple symbols."""
        data = {}
        for symbol in symbols:
            data[symbol] = self.fetch_data(symbol, start_date, end_date)
        return data
