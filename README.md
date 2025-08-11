# Technical Analysis & Strategy Backtesting Platform

A comprehensive technical analysis platform featuring both Python-based strategy development and a modern web interface for strategy testing and visualization. This project demonstrates object-oriented design principles applied to financial data analysis and algorithmic trading research.

## Overview

This platform provides a complete toolkit for developing, testing, and analyzing trading strategies with both programmatic and web-based interfaces.

## Architecture

### Backend Components

**Core Engine (`src/`)**

- `main.py` - MarketData class with intelligent indicator caching
- `indicators.py` - Technical indicator implementations (SMA, EMA, RSI, MACD)
- `strategies.py` - Trading strategy framework with multiple implementations
- `back_testing.py` - Comprehensive backtesting engine with performance metrics

**Web API (`backend/`)**

- `app.py` - FastAPI server with CORS support
- `models.py` - Pydantic data models for API requests
- `run.py` - Backtesting execution interface
- `strategy_config.py` - Available strategy configurations

### Frontend (`frontend/`)

Modern React application built with TypeScript and Tailwind CSS featuring:

- Interactive custom strategy configuration interface
- Real-time backtesting execution
- Results visualization with metrics cards
- Trade-by-trade analysis tables

## Features

### Technical Indicators

- **Simple Moving Average (SMA)** - Configurable period lengths
- **Exponential Moving Average (EMA)** - Smoothed price averaging
- **Relative Strength Index (RSI)** - Momentum oscillator with customizable periods
- **MACD Components** - Line, Signal Line, and Histogram with separate implementations

### Trading Strategies

- **Moving Average Crossover** - Both SMA and EMA with configurable periods
- **RSI Crossover** - Signal generation based on RSI threshold crossings
- **RSI Extremes** - Buy/sell signals from overbought/oversold levels
- **MACD Crossover** - Classic MACD line vs signal line strategy
- **MACD Histogram** - Momentum signals from histogram zero crossings
- **Custom Strategy** - Combine multiple strategies with AND/OR logic

### Performance Analysis

- **Comprehensive Metrics** - Total return, win rate, Sharpe ratio, maximum drawdown
- **Trade Analysis** - Entry/exit prices, duration, individual trade returns
- **Risk Assessment** - Drawdown analysis and risk-adjusted returns

## Installation & Setup

### Prerequisites

- Python 3.8+
- Node.js 16+
- npm or yarn

### Backend Setup

1. **Install Python dependencies:**

```bash
pip install -r requirements.txt
```

2. **Start the FastAPI server:**

```bash
python -m backend.app
```

The API will be available at `http://localhost:8000`

### Frontend Setup

1. **Install dependencies:**

```bash
cd frontend
npm install
```

2. **Start the development server:**

```bash
npm run dev
```

The web interface will be available at `http://localhost:5173`

## Usage

### Python API

```python
from src.main import MarketData
from src.strategies import MovingAverageCross, RSICross
from src.back_testing import BackTest

# Create market data instance
data = MarketData("AAPL", "2y")

# Configure strategy
strategy = MovingAverageCross(lower_period=50, upper_period=200, ma_type="SMA")

# Run backtest
backtest = BackTest(initial_capital=10000)
results = backtest.run_backtest(data, strategy)
backtest.print_results(results)
```

### Web Interface

1. Open the web application
2. Add one or more trading strategies using the interface
3. Enter a stock ticker symbol (e.g., "AAPL", "TSLA")
4. Set initial capital and time period
5. Click "Test Strategy" to run the backtest
6. Review comprehensive results including performance metrics and trade history

### Strategy Configuration Examples

**Moving Average Crossover:**

- Lower Period: 50
- Upper Period: 200
- MA Type: SMA

**RSI Extremes:**

- RSI Period: 14
- Oversold Threshold: 30
- Overbought Threshold: 70

**MACD Crossover:**

- Short Period: 12
- Long Period: 26
- Signal Period: 9

## Technical Implementation

### Object-Oriented Design

- **Abstract Base Classes** - Strategy and Indicator interfaces ensure consistency
- **Intelligent Caching** - Indicators are cached to prevent recomputation
- **Parameterized Strategies** - Easy experimentation with different configurations
- **Data Validation** - Comprehensive input validation and error handling

### API Design

- **RESTful Interface** - Clean API endpoints for strategy execution
- **Type Safety** - Pydantic models for request/response validation
- **CORS Support** - Enables frontend-backend communication
- **Error Handling** - Graceful error responses with detailed messages

### Frontend Architecture

- **TypeScript** - Type-safe React components
- **Tailwind CSS** - Utility-first styling framework
- **Component Architecture** - Reusable UI components for consistency
- **State Management** - Efficient state handling for strategy configuration

## Testing

The project includes comprehensive testing:

```bash
# Run Python tests
python -m pytest tests/

# Run frontend linting
cd frontend
npm run lint
```

## API Endpoints

- `POST /backtest` - Execute strategy backtest
- `GET /strategies` - Retrieve available strategy configurations

## Project Structure

```
tech-analysis/
├── src/                    # Core Python engine
│   ├── main.py            # Market data management
│   ├── indicators.py      # Technical indicators
│   ├── strategies.py      # Trading strategies
│   └── back_testing.py    # Backtesting framework
├── backend/               # FastAPI web server
│   ├── app.py            # Main API application
│   ├── models.py         # Data models
│   └── run.py            # Execution interface
├── frontend/              # React web application
│   ├── src/
│   │   ├── components/   # UI components
│   │   ├── pages/        # Application pages
│   │   ├── services/     # API communication
│   │   └── utils/        # Helper functions
│   └── package.json
├── tests/                 # Test suite
└── requirements.txt       # Python dependencies
```

## Contributing

This project demonstrates modern software engineering practices applied to financial markets. Contributions and suggestions for improvements are welcome.

## Disclaimer

This software is for educational and research purposes only. Past performance does not guarantee future results. Trading strategies should be thoroughly tested and validated before any real-world application.
