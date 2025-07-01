# Technical Analysis Learning Project

A Python-based technical analysis tool I built to learn about algorithmic trading and market analysis. This project explores various technical indicators and trading strategies, with a particular focus on moving average crossovers.

## 🎯 Project Goals

This project was created to:
- Learn about technical analysis and algorithmic trading concepts
- Implement and test various trading strategies from scratch
- Understand market dynamics through data analysis
- Build a foundation for more advanced trading algorithms

## 🔍 Key Findings

Through extensive backtesting and analysis, I discovered that the **50-200 day moving average crossover strategy** shows remarkable effectiveness:

- **Consistent Performance**: The 50-200 day MA crossover provides reliable signals for major trend changes
- **Risk Management**: This longer-term strategy helps avoid false signals common in shorter-term indicators
- **Market Timing**: Particularly effective for identifying major bull/bear market transitions
- **Reduced Noise**: Longer moving averages filter out market noise and focus on significant trends

## 🚀 Features Implemented

- **Stock Data Retrieval**: Real-time data fetching using Yahoo Finance API
- **Technical Indicators**: Moving averages with customizable periods
- **Trading Strategies**: Moving Average Crossover with configurable parameters
- **Backtesting Framework**: Comprehensive strategy evaluation with performance metrics
- **Data Analysis**: Historical performance analysis and signal generation

## 📁 Project Structure

```
src/
├── main.py          # Core Stock class for data handling
├── indicators.py    # Technical indicators (Moving Averages)
├── strategies.py    # Trading strategies implementation
├── back_testing.py  # Backtesting framework
└── test_func.py     # Testing utilities
```

## 🛠️ Installation & Setup

1. **Clone the repository:**
```bash
git clone [your-repository-url]
cd technical_analysis
```

2. **Install dependencies:**
```bash
pip install yfinance pandas numpy
```

## 💡 Usage Examples

### Basic Stock Analysis
```python
from main import Stock

# Analyze Apple stock with 200 days of data
apple_stock = Stock("AAPL", 200)

# Get closing prices and dates
close_prices = apple_stock.get_col("Close")
dates = apple_stock.get_dates()
```

### Moving Average Analysis
```python
from indicators import MovingAverage
from main import Stock

# Create stock instance
stock = Stock("AAPL", 200)

# Calculate 50 and 200-day moving averages
ma_50 = MovingAverage(50)
ma_200 = MovingAverage(200)

ma_50_values = ma_50.compute(stock)
ma_200_values = ma_200.compute(stock)
```

### Strategy Implementation
```python
from strategies import MovingAverageCross
from main import Stock

# Initialize the 50-200 day crossover strategy
strategy = MovingAverageCross(lower_ma=50, higher_ma=200)

# Get trading signals
bullish_signals = strategy.calculate_bullish_cross(stock)
bearish_signals = strategy.calculate_bearish_cross(stock)
```

## 📈 Learning Outcomes

This project has been instrumental in my understanding of:
- **Market Analysis**: How technical indicators work in real market conditions
- **Algorithm Design**: Building robust trading algorithms from scratch
- **Data Processing**: Handling large datasets and time series analysis
- **Backtesting**: The critical role of historical testing in strategy validation

## 🔄 Ongoing Development


## 🤝 Contributing

This is primarily a learning project, but I'm always open to feedback and suggestions for improvement!

## 📚 Resources Used

- Financial data APIs and documentation
- Python libraries for data analysis and visualization
- Market research on effective trading strategies

---

*This project represents my journey into algorithmic trading and technical analysis. The 50-200 day moving average crossover strategy has proven to be a reliable foundation for understanding market trends and developing more sophisticated trading approaches.*
