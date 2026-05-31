@echo off
REM Quick start script for Windows

echo.
echo ==========================================
echo Python Backtesting Framework
echo ==========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed. Please install Python 3.8+
    pause
    exit /b 1
)

echo Python found: 
python --version

REM Check and install dependencies
echo.
echo Checking dependencies...
python -c "import yfinance, pandas, numpy, matplotlib" 2>nul
if errorlevel 1 (
    echo Installing required packages...
    pip install -q -r requirements.txt
    echo Dependencies installed
) else (
    echo All dependencies already installed
)

echo.
echo ==========================================
echo Running Backtest
echo ==========================================
echo.

if "%1"=="" (
    echo Usage: run.bat [SYMBOL] [STRATEGY]
    echo.
    echo Examples:
    echo   run.bat AAPL rsi          - Test RSI on Apple
    echo   run.bat MSFT ma           - Test MA on Microsoft
    echo   run.bat GOOGL combined    - Test Combined on Google
    echo   run.bat TSLA              - Compare all strategies on Tesla
    echo.
    echo Running default: AAPL with RSI strategy...
    echo.
    python main.py AAPL rsi
) else (
    python main.py %*
)

echo.
echo ==========================================
echo Backtest Complete!
echo ==========================================
echo Results saved in: results/
pause
