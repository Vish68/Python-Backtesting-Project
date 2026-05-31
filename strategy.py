"""Trading strategies for backtesting."""

import pandas as pd
import numpy as np
from ta.momentum import RSIIndicator
from ta.trend import SMAIndicator


class TradingStrategy:
    """Base class for trading strategies."""

    def __init__(self, data: pd.DataFrame):
        """Initialize the strategy with price data."""
        self.data = data.copy()
        self.signals = pd.DataFrame(index=data.index)
        self.signals["Close"] = data["Close"]
        self.signals["Position"] = 0.0

    def generate_signals(self):
        """Generate trading signals. Override in subclasses."""
        raise NotImplementedError


class RSIMomentumStrategy(TradingStrategy):
    """RSI-based momentum trading strategy."""

    def __init__(self, data: pd.DataFrame, rsi_period: int = 14):
        """Initialize RSI strategy."""
        super().__init__(data)
        self.rsi_period = rsi_period

    def generate_signals(self):
        """Generate signals based on RSI indicator."""
        rsi = RSIIndicator(
            close=self.data["Close"], window=self.rsi_period, fillna=False
        )
        self.signals["RSI"] = rsi.rsi()

        # Buy signal: RSI < 30 (oversold)
        # Sell signal: RSI > 70 (overbought)
        self.signals["Position"] = 0.0
        self.signals.loc[self.signals["RSI"] < 30, "Position"] = 1.0  # Buy
        self.signals.loc[self.signals["RSI"] > 70, "Position"] = 0.0  # Sell

        return self.signals


class MovingAverageCrossoverStrategy(TradingStrategy):
    """Moving average crossover strategy."""

    def __init__(
        self, data: pd.DataFrame, short_window: int = 20, long_window: int = 50
    ):
        """Initialize MA crossover strategy."""
        super().__init__(data)
        self.short_window = short_window
        self.long_window = long_window

    def generate_signals(self):
        """Generate signals based on MA crossover."""
        sma_short = SMAIndicator(
            close=self.data["Close"], window=self.short_window, fillna=False
        )
        sma_long = SMAIndicator(
            close=self.data["Close"], window=self.long_window, fillma=False
        )

        self.signals["SMA_Short"] = sma_short.sma_indicator()
        self.signals["SMA_Long"] = sma_long.sma_indicator()

        # Buy signal: Short MA crosses above Long MA
        # Sell signal: Short MA crosses below Long MA
        self.signals["Position"] = 0.0
        self.signals.loc[
            self.signals["SMA_Short"] > self.signals["SMA_Long"], "Position"
        ] = 1.0

        return self.signals


class CombinedStrategy(TradingStrategy):
    """Combined RSI + Moving Average strategy."""

    def __init__(
        self,
        data: pd.DataFrame,
        rsi_period: int = 14,
        short_window: int = 20,
        long_window: int = 50,
    ):
        """Initialize combined strategy."""
        super().__init__(data)
        self.rsi_period = rsi_period
        self.short_window = short_window
        self.long_window = long_window

    def generate_signals(self):
        """Generate signals combining RSI and MA crossover."""
        # RSI signals
        rsi = RSIIndicator(
            close=self.data["Close"], window=self.rsi_period, fillna=False
        )
        self.signals["RSI"] = rsi.rsi()

        # MA signals
        sma_short = SMAIndicator(
            close=self.data["Close"], window=self.short_window, fillna=False
        )
        sma_long = SMAIndicator(
            close=self.data["Close"], window=self.long_window, fillna=False
        )
        self.signals["SMA_Short"] = sma_short.sma_indicator()
        self.signals["SMA_Long"] = sma_long.sma_indicator()

        # Combined logic: Buy when RSI is < 50 AND short MA > long MA
        self.signals["Position"] = 0.0
        buy_condition = (self.signals["RSI"] < 50) & (
            self.signals["SMA_Short"] > self.signals["SMA_Long"]
        )
        self.signals.loc[buy_condition, "Position"] = 1.0

        return self.signals
