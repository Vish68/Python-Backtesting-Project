"""Analysis and visualization of backtesting results."""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import os
from config import OUTPUT_DIR


class BacktestAnalyzer:
    """Analyze and visualize backtesting results."""

    def __init__(self, results: pd.DataFrame, symbol: str):
        """Initialize the analyzer."""
        self.results = results
        self.symbol = symbol
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        sns.set_style("darkgrid")

    def plot_portfolio_performance(self, save: bool = True):
        """Plot portfolio value over time."""
        fig, ax = plt.subplots(figsize=(14, 7))

        ax.plot(
            self.results.index,
            self.results["Portfolio_Value"],
            label="Strategy",
            linewidth=2,
            color="blue",
        )
        ax.plot(
            self.results.index,
            self.results["Benchmark_Value"],
            label="Buy & Hold Benchmark",
            linewidth=2,
            color="orange",
            linestyle="--",
        )

        ax.set_xlabel("Date", fontsize=12)
        ax.set_ylabel("Portfolio Value ($)", fontsize=12)
        ax.set_title(f"Portfolio Performance - {self.symbol}", fontsize=14, fontweight="bold")
        ax.legend(fontsize=11)
        ax.grid(True, alpha=0.3)

        if save:
            plt.savefig(
                os.path.join(OUTPUT_DIR, f"{self.symbol}_portfolio_performance.png"),
                dpi=300,
                bbox_inches="tight",
            )
        plt.show()

    def plot_drawdown(self, save: bool = True):
        """Plot drawdown over time."""
        cumulative = (1 + self.results["Net_Return"]).cumprod()
        running_max = cumulative.expanding().max()
        drawdown = (cumulative - running_max) / running_max * 100

        fig, ax = plt.subplots(figsize=(14, 6))
        ax.fill_between(drawdown.index, drawdown, 0, alpha=0.3, color="red")
        ax.plot(drawdown.index, drawdown, linewidth=1.5, color="red")

        ax.set_xlabel("Date", fontsize=12)
        ax.set_ylabel("Drawdown (%)", fontsize=12)
        ax.set_title(f"Maximum Drawdown - {self.symbol}", fontsize=14, fontweight="bold")
        ax.grid(True, alpha=0.3)

        if save:
            plt.savefig(
                os.path.join(OUTPUT_DIR, f"{self.symbol}_drawdown.png"),
                dpi=300,
                bbox_inches="tight",
            )
        plt.show()

    def plot_signals(self, save: bool = True):
        """Plot price with buy/sell signals."""
        fig, ax = plt.subplots(figsize=(14, 7))

        ax.plot(
            self.results.index, self.results["Close"], label="Close Price", linewidth=2
        )

        # Buy signals (position changes from 0 to 1)
        buy_signals = self.results[
            (self.results["Position"] == 1) & (self.results["Position_Shift"] != 1)
        ]
        ax.scatter(
            buy_signals.index,
            buy_signals["Close"],
            color="green",
            marker="^",
            s=100,
            label="Buy Signal",
            alpha=0.7,
        )

        # Sell signals (position changes from 1 to 0)
        sell_signals = self.results[
            (self.results["Position"] == 0) & (self.results["Position_Shift"] == 1)
        ]
        ax.scatter(
            sell_signals.index,
            sell_signals["Close"],
            color="red",
            marker="v",
            s=100,
            label="Sell Signal",
            alpha=0.7,
        )

        ax.set_xlabel("Date", fontsize=12)
        ax.set_ylabel("Price ($)", fontsize=12)
        ax.set_title(f"Price and Trading Signals - {self.symbol}", fontsize=14, fontweight="bold")
        ax.legend(fontsize=11)
        ax.grid(True, alpha=0.3)

        if save:
            plt.savefig(
                os.path.join(OUTPUT_DIR, f"{self.symbol}_signals.png"),
                dpi=300,
                bbox_inches="tight",
            )
        plt.show()

    def plot_daily_returns(self, save: bool = True):
        """Plot distribution of daily returns."""
        fig, axes = plt.subplots(1, 2, figsize=(14, 5))

        # Histogram
        axes[0].hist(
            self.results["Net_Return"] * 100, bins=50, alpha=0.7, color="blue"
        )
        axes[0].axvline(
            self.results["Net_Return"].mean() * 100, color="red", linestyle="--"
        )
        axes[0].set_xlabel("Daily Return (%)", fontsize=11)
        axes[0].set_ylabel("Frequency", fontsize=11)
        axes[0].set_title("Distribution of Daily Returns", fontsize=12, fontweight="bold")
        axes[0].grid(True, alpha=0.3)

        # Cumulative distribution
        sorted_returns = self.results["Net_Return"].sort_values()
        axes[1].plot(
            sorted_returns.values * 100,
            range(len(sorted_returns)),
            linewidth=2,
            color="blue",
        )
        axes[1].set_xlabel("Daily Return (%)", fontsize=11)
        axes[1].set_ylabel("Cumulative Count", fontsize=11)
        axes[1].set_title("Cumulative Distribution of Returns", fontsize=12, fontweight="bold")
        axes[1].grid(True, alpha=0.3)

        plt.tight_layout()
        if save:
            plt.savefig(
                os.path.join(OUTPUT_DIR, f"{self.symbol}_returns_dist.png"),
                dpi=300,
                bbox_inches="tight",
            )
        plt.show()
