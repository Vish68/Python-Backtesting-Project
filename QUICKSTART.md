# Getting Started Guide

## Quick Start (2 minutes)

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run a Backtest
```bash
python main.py AAPL rsi
```

### 3. View Results
- Charts saved in `results/` directory
- Performance metrics printed to console

---

## Running Different Strategies

### RSI Momentum Strategy
```bash
python main.py AAPL rsi
```
Best for: Mean-reversion traders

### Moving Average Crossover
```bash
python main.py MSFT ma
```
Best for: Trend followers

### Combined Strategy
```bash
python main.py GOOGL combined
```
Best for: Balanced approach

---

## Compare All Strategies on One Stock
```bash
python main.py TSLA
```

---

## Using the Run Scripts

### On Linux/Mac
```bash
chmod +x run.sh
./run.sh AAPL rsi
```

### On Windows
```cmd
run.bat AAPL rsi
```

---

## Project Files Explained

| File | Purpose |
|------|---------|
| `config.py` | Configuration (capital, periods, dates) |
| `data_fetcher.py` | Download data from Yahoo Finance |
| `strategy.py` | Three trading strategies |
| `backtester.py` | Core backtesting engine |
| `analysis.py` | Charts and visualizations |
| `functions.py` | Utility functions |
| `main.py` | Entry point - run this |
| `results/` | Output folder (charts, CSV) |

---

## Configuration

Edit `config.py` to customize:

```python
INITIAL_CAPITAL = 100000      # Starting money
COMMISSION_RATE = 0.001        # 0.1% per trade
SLIPPAGE = 0.0001              # 0.01% price slippage
START_DATE = "2022-01-01"      # Backtest start
END_DATE = "2024-12-31"        # Backtest end
RSI_PERIOD = 14                # RSI calculation period
MA_SHORT_PERIOD = 20           # Short MA
MA_LONG_PERIOD = 50            # Long MA
```

---

## Understanding Results

### Key Metrics

- **Total Return**: Overall profit percentage
- **Sharpe Ratio**: Risk-adjusted return (higher is better)
- **Max Drawdown**: Largest peak-to-trough loss
- **Win Rate**: % of profitable days
- **Outperformance**: vs buy-and-hold benchmark

### Example Results
```
Total Return........................45.23%
Annual Return......................15.62%
Sharpe Ratio......................... 0.85
Maximum Drawdown....................-22.34%
Win Rate............................52.30%
Outperformance.....................+16.33%
```

---

## Troubleshooting

**"ModuleNotFoundError"**
- Run: `pip install -r requirements.txt`

**"Data fetch failed"**
- Check internet connection
- Yahoo Finance might be rate-limiting
- Wait a few minutes and try again

**"NaN values in indicators"**
- Need more historical data
- Increase START_DATE to earlier date
- Indicators need several periods to calculate

---

## Next Steps

1. ✅ Run the default backtest
2. ✅ Try different strategies on different stocks
3. ✅ Modify parameters in `config.py`
4. ✅ Compare results across periods
5. ✅ Add your own custom strategy

---

## Tips for Better Results

- **Test multiple stocks**: Not all strategies work on all assets
- **Try different periods**: Market conditions vary over time
- **Optimize parameters**: Find the best RSI period, MA lengths, etc.
- **Consider costs**: Commission and slippage matter
- **Risk management**: Always use position sizing and stops in live trading

---

## Need Help?

See the main [README.md](README.md) for:
- Complete project documentation
- Detailed strategy explanations
- API information
- How to extend the framework

---

**Ready? Run `python main.py AAPL rsi` to get started!**
