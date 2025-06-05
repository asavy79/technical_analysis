# Technical Analysis Tool

A Python-based technical analysis tool for stock market analysis that implements various technical indicators and trading strategies.

## Features

- Stock data retrieval using Yahoo Finance API
- Technical indicators implementation (Moving Averages)
- Trading strategies (Moving Average Crossover)
- Backtesting capabilities

## Project Structure

- `main.py`: Core Stock class for handling stock data and basic operations
- `indicators.py`: Implementation of technical indicators (Moving Averages)
- `strategies.py`: Trading strategies implementation (Moving Average Crossover)
- `back_testing.py`: Backtesting framework for strategy evaluation

## Installation

1. Clone the repository:

```bash
git clone [your-repository-url]
cd technical_analysis
```

2. Install the required dependencies:

```bash
pip install yfinance pandas numpy
```

## Usage

### Basic Stock Data Retrieval

```python
from main import Stock

# Create a Stock instance for Apple with 10 days of historical data
apple_stock = Stock("AAPL", 10)

# Get specific columns
close_prices = apple_stock.get_col("Close")
dates = apple_stock.get_dates()
```

### Using Technical Indicators

```python
from indicators import MovingAverage
from main import Stock

# Create a Stock instance
stock = Stock("AAPL", 20)

# Calculate 20-day moving average
ma = MovingAverage(20)
ma_values = ma.compute(stock)
```

### Implementing Trading Strategies

```python
from strategies import MovingAverageCross
from main import Stock

# Create a Stock instance
stock = Stock("AAPL", 50)

# Initialize Moving Average Crossover strategy
strategy = MovingAverageCross(lower_ma=20, higher_ma=50)

# Calculate bullish crossovers
bullish_signals = strategy.calculate_bullish_cross(stock)

# Calculate bearish crossovers
bearish_signals = strategy.calculate_bearish_cross(stock)
```

## Contributing

Feel free to contribute!
