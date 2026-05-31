"""Backtesting engine for evaluating trading strategies."""

import pandas as pd
import numpy as np
from config import COMMISSION_RATE, SLIPPAGE


class Backtester:
    """Execute and evaluate a trading strategy on historical data."""

    def __init__(
        self, initial_capital: float, commission_rate: float, slippage: float
    ):
        """Initialize the backtester."""
        self.initial_capital = initial_capital
        self.commission_rate = commission_rate
        self.slippage = slippage
        self.results = None

    def run(self, signals: pd.DataFrame) -> pd.DataFrame:
        """Run the backtest on signals."""
        data = signals.copy()
        data["Position_Shift"] = data["Position"].shift(1)  # Previous position
        data["Daily_Return"] = data["Close"].pct_change()
        
        # Calculate strategy returns
        data["Strategy_Return"] = data["Position_Shift"] * data["Daily_Return"]
        
        # Apply slippage on position changes
        position_change = (data["Position"] - data["Position_Shift"]).abs()
        data["Slippage_Cost"] = position_change * self.slippage
        
        # Apply commission on trades
        data["Commission_Cost"] = position_change * self.commission_rate
        
        # Net return after costs
        data["Net_Return"] = (
            data["Strategy_Return"] - data["Slippage_Cost"] - data["Commission_Cost"]
        )
        
        # Calculate cumulative returns
        data["Cumulative_Return"] = (1 + data["Net_Return"]).cumprod()
        data["Portfolio_Value"] = self.initial_capital * data["Cumulative_Return"]
        
        # Buy and hold benchmark
        data["Benchmark_Return"] = data["Daily_Return"]
        data["Benchmark_Cumulative"] = (1 + data["Benchmark_Return"]).cumprod()
        data["Benchmark_Value"] = self.initial_capital * data["Benchmark_Cumulative"]
        
        self.results = data
        return data

    def get_performance_metrics(self) -> dict:
        """Calculate performance metrics."""
        if self.results is None:
            raise ValueError("Run backtest first using .run()")

        results = self.results.dropna()
        
        # Returns
        total_return = (results["Portfolio_Value"].iloc[-1] / self.initial_capital) - 1
        annual_return = (1 + total_return) ** (252 / len(results)) - 1
        
        # Volatility
        daily_returns = results["Net_Return"]
        annual_volatility = daily_returns.std() * np.sqrt(252)
        
        # Sharpe Ratio (assuming 0% risk-free rate)
        sharpe_ratio = (annual_return / annual_volatility) if annual_volatility > 0 else 0
        
        # Maximum Drawdown
        cumulative = (1 + results["Net_Return"]).cumprod()
        running_max = cumulative.expanding().max()
        drawdown = (cumulative - running_max) / running_max
        max_drawdown = drawdown.min()
        
        # Win Rate
        winning_days = (results["Net_Return"] > 0).sum()
        total_days = len(results)
        win_rate = winning_days / total_days if total_days > 0 else 0
        
        # Compare to benchmark
        benchmark_return = (results["Benchmark_Value"].iloc[-1] / self.initial_capital) - 1
        benchmark_annual_return = (1 + benchmark_return) ** (252 / len(results)) - 1
        
        return {
            "Total Return": f"{total_return:.2%}",
            "Annual Return": f"{annual_return:.2%}",
            "Annual Volatility": f"{annual_volatility:.2%}",
            "Sharpe Ratio": f"{sharpe_ratio:.2f}",
            "Maximum Drawdown": f"{max_drawdown:.2%}",
            "Win Rate": f"{win_rate:.2%}",
            "Final Portfolio Value": f"${results['Portfolio_Value'].iloc[-1]:,.2f}",
            "Benchmark Return": f"{benchmark_return:.2%}",
            "Benchmark Annual Return": f"{benchmark_annual_return:.2%}",
            "Outperformance": f"{total_return - benchmark_return:.2%}",
        }
