#!/bin/bash
# Quick start script for the backtesting project

echo "=========================================="
echo "Python Backtesting Framework"
echo "=========================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8+"
    exit 1
fi

echo "✓ Python 3 found: $(python3 --version)"
echo ""

# Check if requirements are installed
echo "Checking dependencies..."
python3 -c "import yfinance, pandas, numpy, matplotlib" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "⚠️  Installing required packages..."
    pip install -q -r requirements.txt
    echo "✓ Dependencies installed"
else
    echo "✓ All dependencies already installed"
fi

echo ""
echo "=========================================="
echo "Running Backtest"
echo "=========================================="
echo ""

# Run default backtest (AAPL with RSI strategy)
if [ -z "$1" ]; then
    echo "Usage: ./run.sh [SYMBOL] [STRATEGY]"
    echo ""
    echo "Examples:"
    echo "  ./run.sh AAPL rsi          # Test RSI on Apple"
    echo "  ./run.sh MSFT ma           # Test MA on Microsoft"
    echo "  ./run.sh GOOGL combined    # Test Combined on Google"
    echo "  ./run.sh TSLA              # Compare all strategies on Tesla"
    echo ""
    echo "Running default: AAPL with RSI strategy..."
    echo ""
    python3 main.py AAPL rsi
else
    python3 main.py "$@"
fi

echo ""
echo "=========================================="
echo "Backtest Complete!"
echo "=========================================="
echo "Results saved in: results/"
