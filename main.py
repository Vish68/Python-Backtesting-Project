"""Main script to run the backtesting project."""

import sys
from data_fetcher import DataFetcher
from strategy import (
    RSIMomentumStrategy,
    MovingAverageCrossoverStrategy,
    CombinedStrategy,
)
from backtester import Backtester
from analysis import BacktestAnalyzer
from config import (
    INITIAL_CAPITAL,
    COMMISSION_RATE,
    SLIPPAGE,
    START_DATE,
    END_DATE,
    RSI_PERIOD,
    MA_SHORT_PERIOD,
    MA_LONG_PERIOD,
)


def run_backtest(symbol: str, strategy_type: str = "rsi"):
    """Run a complete backtest for a symbol."""
    print(f"\n{'='*60}")
    print(f"Backtesting {symbol} with {strategy_type.upper()} Strategy")
    print(f"{'='*60}")

    # Fetch data
    fetcher = DataFetcher()
    data = fetcher.fetch_data(symbol, START_DATE, END_DATE)
    print(f"✓ Data fetched: {len(data)} trading days")

    # Generate signals based on strategy
    if strategy_type == "rsi":
        strategy = RSIMomentumStrategy(data, rsi_period=RSI_PERIOD)
    elif strategy_type == "ma":
        strategy = MovingAverageCrossoverStrategy(
            data, short_window=MA_SHORT_PERIOD, long_window=MA_LONG_PERIOD
        )
    elif strategy_type == "combined":
        strategy = CombinedStrategy(
            data,
            rsi_period=RSI_PERIOD,
            short_window=MA_SHORT_PERIOD,
            long_window=MA_LONG_PERIOD,
        )
    else:
        raise ValueError(f"Unknown strategy: {strategy_type}")

    signals = strategy.generate_signals()
    print(f"✓ Signals generated")

    # Run backtest
    backtester = Backtester(INITIAL_CAPITAL, COMMISSION_RATE, SLIPPAGE)
    results = backtester.run(signals)
    print(f"✓ Backtest completed")

    # Display metrics
    metrics = backtester.get_performance_metrics()
    print(f"\n{'Performance Metrics':^60}")
    print(f"{'-'*60}")
    for key, value in metrics.items():
        print(f"{key:.<40} {value:>18}")

    # Analysis and plots
    analyzer = BacktestAnalyzer(results, symbol)
    
    print(f"\n{'Generating visualizations...':^60}")
    analyzer.plot_portfolio_performance()
    analyzer.plot_drawdown()
    analyzer.plot_signals()
    analyzer.plot_daily_returns()

    return results, metrics


def compare_strategies(symbol: str):
    """Compare all strategies for a symbol."""
    print(f"\n{'='*60}")
    print(f"Strategy Comparison for {symbol}")
    print(f"{'='*60}\n")

    strategies = ["rsi", "ma", "combined"]
    all_results = {}
    all_metrics = {}

    for strategy in strategies:
        try:
            results, metrics = run_backtest(symbol, strategy)
            all_results[strategy] = results
            all_metrics[strategy] = metrics
        except Exception as e:
            print(f"Error running {strategy} strategy: {e}")

    # Summary comparison
    print(f"\n{'='*60}")
    print(f"Summary Comparison")
    print(f"{'='*60}")
    
    for strategy, metrics in all_metrics.items():
        print(f"\n{strategy.upper()} Strategy:")
        print(f"  Total Return: {metrics['Total Return']}")
        print(f"  Sharpe Ratio: {metrics['Sharpe Ratio']}")
        print(f"  Max Drawdown: {metrics['Maximum Drawdown']}")
        print(f"  Win Rate: {metrics['Win Rate']}")


if __name__ == "__main__":
    # Example usage
    symbol = "AAPL"

    if len(sys.argv) > 1:
        symbol = sys.argv[1].upper()
        if len(sys.argv) > 2:
            strategy_type = sys.argv[2].lower()
            run_backtest(symbol, strategy_type)
        else:
            compare_strategies(symbol)
    else:
        # Run default backtest
        run_backtest(symbol, "rsi")
        
        print("\n\nUsage examples:")
        print("  python main.py AAPL rsi          # Test RSI strategy on AAPL")
        print("  python main.py MSFT ma           # Test MA strategy on MSFT")
        print("  python main.py GOOGL combined    # Test combined strategy on GOOGL")
        print("  python main.py TSLA              # Compare all strategies on TSLA")
