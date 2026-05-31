# Python Backtesting Project

A comprehensive backtesting framework for evaluating trading strategies using historical market data from APIs.

## Features

- **Multiple Data Sources**: Yahoo Finance (primary), with support for Alpha Vantage and Finnhub
- **Three Trading Strategies**:
  - RSI Momentum Strategy: Trades based on oversold/overbought conditions
  - Moving Average Crossover: Trades on SMA 20/50 crossovers
  - Combined Strategy: Hybrid approach using RSI + MA signals
- **Realistic Backtesting**: Includes commission, slippage, and transaction costs
- **Comprehensive Metrics**: Sharpe ratio, max drawdown, win rate, and more
- **Performance Visualization**: Charts for portfolio value, drawdowns, signals, and returns
- **Strategy Comparison**: Compare multiple strategies on the same asset

## Project Structure

```
├── config.py              # Configuration and settings
├── data_fetcher.py        # API data fetching and caching
├── strategy.py            # Trading strategy implementations
├── backtester.py          # Backtesting engine
├── analysis.py            # Results analysis and visualization
├── functions.py           # Utility functions
├── main.py               # Main entry point
├── requirements.txt      # Python dependencies
├── .env.example         # Environment variables template
└── README.md            # This file
```

## Installation

1. **Clone the repository**:
   ```bash
   cd /workspaces/Python-Backtesting-Project
   ```

2. **Create virtual environment** (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure API keys** (optional):
   ```bash
   cp .env.example .env
   # Edit .env and add your API keys if using Alpha Vantage or Finnhub
   ```

## Usage

### Run a Single Strategy Backtest

Test RSI strategy on Apple stock:
```bash
python main.py AAPL rsi
```

Test MA Crossover strategy on Microsoft:
```bash
python main.py MSFT ma
```

Test Combined strategy on Google:
```bash
python main.py GOOGL combined
```

### Compare All Strategies

Compare all three strategies on a stock:
```bash
python main.py TSLA
```

### Default Backtest

```bash
python main.py
# Defaults to AAPL with RSI strategy
```

## Configuration

Edit `config.py` to customize:

- **INITIAL_CAPITAL**: Starting portfolio value (default: $100,000)
- **COMMISSION_RATE**: Trading commission as percentage (default: 0.1%)
- **SLIPPAGE**: Price slippage for trades (default: 0.01%)
- **START_DATE** / **END_DATE**: Backtest period
- **RSI_PERIOD**: RSI indicator period (default: 14)
- **MA_SHORT_PERIOD**: Short MA period (default: 20)
- **MA_LONG_PERIOD**: Long MA period (default: 50)

## Strategies Explained

### RSI Momentum Strategy
- **Buy Signal**: RSI < 30 (oversold condition)
- **Sell Signal**: RSI > 70 (overbought condition)
- **Best For**: Mean-reversion trading

### Moving Average Crossover Strategy
- **Buy Signal**: 20-day MA > 50-day MA (uptrend)
- **Sell Signal**: 20-day MA < 50-day MA (downtrend)
- **Best For**: Trend-following strategies

### Combined Strategy
- **Buy Signal**: RSI < 50 AND 20-day MA > 50-day MA
- **Sell Signal**: Either condition fails
- **Best For**: Balanced approach combining trend and momentum

## Performance Metrics

The backtester calculates:

- **Total Return**: Overall profit/loss percentage
- **Annual Return**: Annualized return rate
- **Annual Volatility**: Annualized standard deviation of returns
- **Sharpe Ratio**: Risk-adjusted return (higher is better)
- **Maximum Drawdown**: Largest peak-to-trough decline
- **Win Rate**: Percentage of profitable trading days
- **Outperformance**: Strategy return vs. buy-and-hold benchmark

## Output Files

Results are saved to the `results/` directory:

- `{SYMBOL}_portfolio_performance.png`: Strategy vs. benchmark comparison
- `{SYMBOL}_drawdown.png`: Maximum drawdown visualization
- `{SYMBOL}_signals.png`: Buy/sell signals on price chart
- `{SYMBOL}_returns_dist.png`: Return distribution analysis

## API Information

### Yahoo Finance (Primary)
- **No API key required**
- **Free tier**: Unlimited requests
- **Data source**: `yfinance` library

### Alpha Vantage (Optional)
- **Website**: https://www.alphavantage.co/
- **Free tier**: 5 requests/minute, 500/day
- **Key needed**: Yes

### Finnhub (Optional)
- **Website**: https://finnhub.io/
- **Free tier**: 60 API calls/minute
- **Key needed**: Yes

## Extending the Project

### Add a New Strategy

1. Create a class in `strategy.py` inheriting from `TradingStrategy`
2. Implement the `generate_signals()` method
3. Add import and option to `main.py`

```python
class MyStrategy(TradingStrategy):
    def generate_signals(self):
        # Your logic here
        self.signals["Position"] = ...
        return self.signals
```

### Add New Metrics

Edit `backtester.py`'s `get_performance_metrics()` method to calculate additional metrics.

### Add New Data Sources

1. Add method to `DataFetcher` class
2. Update `DATA_SOURCE` in `config.py`

## Important Notes

- **Past performance ≠ Future results**: Backtesting on historical data doesn't guarantee future profits
- **Market conditions change**: Strategies that worked in the past may fail in different market conditions
- **Risk management**: Always use stop-losses and position sizing in live trading
- **Costs matter**: Commission and slippage can significantly impact returns

## Example Output

```
============================================================
Backtesting AAPL with RSI Strategy
============================================================
✓ Data fetched: 504 trading days
✓ Signals generated
✓ Backtest completed

                  Performance Metrics
------------------------------------------------------------
Total Return.................................. 45.23%
Annual Return................................ 15.62%
Annual Volatility............................ 18.45%
Sharpe Ratio.................................  0.85
Maximum Drawdown............................ -22.34%
Win Rate..................................... 52.30%
Final Portfolio Value................. $145,230.00
Benchmark Return............................ 28.90%
Benchmark Annual Return....................... 10.05%
Outperformance............................. 16.33%
```

## Troubleshooting

**Issue**: "ModuleNotFoundError: No module named 'yfinance'"
- **Solution**: Run `pip install -r requirements.txt`

**Issue**: "Connection error downloading data"
- **Solution**: Check internet connection, Yahoo Finance might be rate-limiting
- Wait a few minutes and try again

**Issue**: Indicator values are NaN
- **Solution**: Increase START_DATE or RSI_PERIOD; indicators need historical data to calculate

## License

This project is open source and available for educational purposes.

## Disclaimer

This project is for educational purposes only. It is not financial advice. Always consult with a financial advisor before making investment decisions. Trading and investing carry substantial risk of loss.