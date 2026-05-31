"""Utility functions for the backtesting project."""


import pandas as pd
import numpy as np
from typing import Tuple, List


def calculate_metrics(returns: pd.Series) -> dict:
    """Calculate common performance metrics from returns."""
    total_return = (1 + returns).prod() - 1
    annual_return = (1 + total_return) ** (252 / len(returns)) - 1
    annual_volatility = returns.std() * np.sqrt(252)
    sharpe_ratio = annual_return / annual_volatility if annual_volatility > 0 else 0
    
    return {
        "total_return": total_return,
        "annual_return": annual_return,
        "volatility": annual_volatility,
        "sharpe_ratio": sharpe_ratio,
    }


def calculate_drawdown(cumulative_returns: pd.Series) -> Tuple[float, int]:
    """Calculate maximum drawdown and days to recovery."""
    running_max = cumulative_returns.expanding().max()
    drawdown = (cumulative_returns - running_max) / running_max
    max_drawdown = drawdown.min()
    
    # Find days to recovery from max drawdown
    max_drawdown_idx = drawdown.idxmin()
    after_max = cumulative_returns[cumulative_returns.index > max_drawdown_idx]
    recovery = after_max[after_max >= running_max[max_drawdown_idx]]
    
    days_to_recovery = len(recovery) if len(recovery) > 0 else None
    
    return max_drawdown, days_to_recovery


def calculate_win_rate(returns: pd.Series) -> float:
    """Calculate percentage of winning trading days."""
    winning_days = (returns > 0).sum()
    return winning_days / len(returns) if len(returns) > 0 else 0


def identify_trades(positions: pd.Series) -> List[dict]:
    """Identify individual trades from position series."""
    trades = []
    position_diff = positions.diff().fillna(0)
    
    entry_idx = position_diff[position_diff > 0].index.tolist()
    exit_idx = position_diff[position_diff < 0].index.tolist()
    
    for i, entry in enumerate(entry_idx):
        if i < len(exit_idx):
            exit = exit_idx[i]
            trades.append({
                "entry_date": entry,
                "exit_date": exit,
                "days_held": (exit - entry).days,
            })
    
    return trades


def calculate_trade_metrics(trades: List[dict]) -> dict:
    """Calculate metrics from trade history."""
    if not trades:
        return {"total_trades": 0, "avg_days_held": 0}
    
    total_trades = len(trades)
    avg_days_held = np.mean([t["days_held"] for t in trades])
    
    return {
        "total_trades": total_trades,
        "avg_days_held": avg_days_held,
    }


def format_metrics_report(metrics: dict, title: str = "Performance Report") -> str:
    """Format metrics as a readable string report."""
    report = f"\n{title}\n"
    report += "=" * 50 + "\n"
    
    for key, value in metrics.items():
        if isinstance(value, float):
            if "return" in key.lower() or "volatility" in key.lower():
                report += f"{key:.<35} {value:>12.2%}\n"
            else:
                report += f"{key:.<35} {value:>12.4f}\n"
        else:
            report += f"{key:.<35} {value:>12}\n"
    
    return report
