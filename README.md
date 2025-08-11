# Technical Analysis Research Project

A Python-based technical analysis tool I built to learn about algorithmic trading and market analysis. This project includes various technical indicators and trading strategies, with a particular focus on moving average crossovers and RSI crosses.

## 🎯 Project Goals

This project was created to:
- Learn about technical analysis and algorithmic trading concepts
- Implement and test various trading strategies from scratch
- Significantly speed up the process of strategy backtesting


## 🚀 Features Implemented

### **Core Architecture**
- **MarketData Class**: Centralized data management with automatic indicator caching
- **Indicator Framework**: Extensible system supporting SMA, EMA, RSI, and MACD components
- **Strategy System**: Parameterized strategies that automatically determine data requirements
- **Backtesting Engine**: Comprehensive performance analysis with professional metrics

### **Technical Indicators**
- **Simple Moving Average (SMA)**: Configurable period lengths
- **Exponential Moving Average (EMA)**: Configurable period lengths  
- **Relative Strength Index (RSI)**: Momentum oscillator with customizable periods
- **MACD Components**: Separate classes for MACD Line, Signal Line, and Histogram

### **Trading Strategies**
- **Moving Average Crossover**: Supports both SMA and EMA with any period combination
- **RSI Crossover**: Configurable overbought/oversold thresholds
- **RSI Extremes**: Buy/sell based on RSI levels
- **MACD Crossover**: Classic MACD line vs signal line strategy
- **MACD Histogram**: Momentum-based signals from histogram zero crossings

### **Performance Analysis**
- **Comprehensive Metrics**: Total return, win rate, Sharpe ratio, maximum drawdown
- **Trade Tracking**: Detailed entry/exit analysis with duration and returns
- **Strategy Comparison**: Side-by-side performance evaluation
- **Professional Reporting**: Formatted results with key statistics

## 📁 Project Structure

```
src/
├── main.py           # MarketData class for data management and caching
├── indicators.py     # Technical indicator implementations
├── strategies.py     # Trading strategy implementations
├── back_testing.py   # Backtesting framework with performance metrics
└── test_func.py      # Demonstration script and usage examples

tests/
└── test_sma.py       # Unit tests for SMA indicator
```

## 🛠️ Installation & Setup

1. **Clone the repository:**
```bash
git clone [your-repository-url]
cd technical_analysis
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

## 💡 Usage Examples

### **Basic Market Data and Indicators**
```python
from main import MarketData
from indicators import SMA, EMA, RSI, MACDLine

# Create market data with automatic caching
data = MarketData("AAPL", "2y")

# Create indicators
sma_50 = SMA(50)
sma_200 = SMA(200)
rsi_14 = RSI(14)

# Get indicator values (automatically cached)
sma_50_values = data.get_indicator_data(sma_50)
sma_200_values = data.get_indicator_data(sma_200)
rsi_values = data.get_indicator_data(rsi_14)
```

### **Strategy Implementation**
```python
from strategies import MovingAverageCross, RSICross, MACDCross
from back_testing import BackTest

# Create the effective 50-200 day strategy
strategy = MovingAverageCross(lower_period=50, upper_period=200, ma_type="SMA")

# Create RSI strategy
rsi_strategy = RSICross(rsi_period=14, lower_bound=30, upper_bound=70)

# Create MACD strategy
macd_strategy = MACDCross(short_period=12, long_period=26, signal_period=9)

# Run comprehensive backtests
backtest = BackTest(initial_capital=10000)
results = backtest.run_backtest(data, strategy)
backtest.print_results(results)
```

### **MACD Components Usage**
```python
from indicators import MACDLine, MACDSignal, MACDHistogram

# Use MACD components separately
macd_line = MACDLine(12, 26)
macd_signal = MACDSignal(12, 26, 9)
macd_histogram = MACDHistogram(12, 26, 9)

# Each component is cached independently
line_values = data.get_indicator_data(macd_line)
signal_values = data.get_indicator_data(macd_signal)
histogram_values = data.get_indicator_data(macd_histogram)
```

### **Strategy Comparison**
```python
# Compare multiple strategies on the same data
strategies = [
    ("50-200 SMA Cross", MovingAverageCross(50, 200, "SMA")),
    ("12-26 EMA Cross", MovingAverageCross(12, 26, "EMA")),
    ("RSI Cross", RSICross(14, 30, 70)),
    ("MACD Cross", MACDCross(12, 26, 9)),
]

for name, strategy in strategies:
    results = backtest.run_backtest(data, strategy)
    print(f"{name}: {results['metrics']['total_return']:.2%} return")
```

## 🔧 Technical Highlights

### **Intelligent Caching System**
- Indicators are automatically cached to prevent recomputation
- Cache keys based on indicator parameters ensure accuracy
- Significant performance improvements for complex strategies

### **Flexible Strategy Framework**
- Strategies automatically determine their data requirements
- Parameterized approach allows easy experimentation
- Built-in validation ensures data compatibility

### **Professional Backtesting**
- Realistic trade simulation with proper position management
- Comprehensive performance metrics including Sharpe ratio and drawdown
- Detailed trade-by-trade analysis

### **Robust Error Handling**
- Input validation for all parameters
- Graceful handling of API failures and data issues
- Clear error messages for debugging


## 🧪 Testing & Validation

- **Unit Tests**: Testing for the main features
- **Integration Tests**: End-to-end strategy validation
- **Performance Tests**: Backtesting across multiple market conditions

## 🤝 Contributing

This is primarily a learning project, but I'm always open to feedback and suggestions for improvement!

## 📚 Resources Used

- Technical analysis literature and trading books
- Financial data APIs (Yahoo Finance) and documentation
- Python libraries for data analysis and visualization
- Market research on effective trading strategies
- Software engineering best practices and design patterns


---

*Use at your own risk. No strategy generated here is guaranteed to generate positive returns. Have fun ;)*
