
from main import MarketData
from strategies import MovingAverageCross, RSICross, RSIExtremes, MACDCross, MACDHistogramStrategy
from back_testing import BackTest
from indicators import SMA, EMA, RSI, MACDLine, MACDSignal, MACDHistogram


def demonstrate_50_200_strategy():
    """Demonstrate the effective 50-200 day moving average strategy"""
    print("=" * 60)
    print("DEMONSTRATING 50-200 DAY MOVING AVERAGE STRATEGY")
    print("=" * 60)

    # Create market data for SPY (S&P 500 ETF) over 2 years
    market_data = MarketData("SPY", "5y")

    # Create the 50-200 day SMA crossover strategy
    strategy = MovingAverageCross(
        lower_period=50, upper_period=200, ma_type="SMA")

    # Run backtest
    backtest = BackTest(initial_capital=10000)
    results = backtest.run_backtest(market_data, strategy)

    # Print results
    backtest.print_results(results)

    return results


def demonstrate_rsi_strategy():
    """Demonstrate RSI crossover strategy"""
    print("\n" + "=" * 60)
    print("DEMONSTRATING RSI CROSSOVER STRATEGY")
    print("=" * 60)

    market_data = MarketData("AAPL", "1y")

    strategy = RSICross(rsi_period=14, lower_bound=30, upper_bound=70)

    backtest = BackTest(initial_capital=10000)
    results = backtest.run_backtest(market_data, strategy)

    backtest.print_results(results)

    return results


def demonstrate_indicator_caching():
    """Demonstrate how indicator caching works"""
    print("\n" + "=" * 60)
    print("DEMONSTRATING INDICATOR CACHING")
    print("=" * 60)

    market_data = MarketData("TSLA", "6mo")

    sma_20 = SMA(20)

    print("First computation (will be cached):")
    values1 = market_data.get_indicator_data(sma_20)
    print(f"SMA_20 computed, length: {len(values1)}")

    print("\nSecond computation (will use cache):")
    values2 = market_data.get_indicator_data(sma_20)
    print(f"SMA_20 retrieved from cache, length: {len(values2)}")

    print(f"\nValues are identical: {values1.equals(values2)}")

    print(f"Cache keys: {list(market_data._indicator_cache.keys())}")


def demonstrate_macd_strategy():
    print("\n" + "=" * 60)
    print("DEMONSTRATING MACD CROSSOVER STRATEGY")
    print("=" * 60)

    market_data = MarketData("MSFT", "1y")

    strategy = MACDCross(short_period=12, long_period=26, signal_period=9)

    backtest = BackTest(initial_capital=10000)
    results = backtest.run_backtest(market_data, strategy)

    backtest.print_results(results)

    return results


def demonstrate_macd_components():
    print("\n" + "=" * 60)
    print("DEMONSTRATING MACD SEPARATE COMPONENTS")
    print("=" * 60)

    market_data = MarketData("NVDA", "6mo")

    macd_line = MACDLine(12, 26)
    macd_signal = MACDSignal(12, 26, 9)
    macd_histogram = MACDHistogram(12, 26, 9)

    print("Computing MACD components separately:")

    line_values = market_data.get_indicator_data(macd_line)
    signal_values = market_data.get_indicator_data(macd_signal)
    histogram_values = market_data.get_indicator_data(macd_histogram)

    print(f"MACD Line: {len(line_values)} values")
    print(f"Signal Line: {len(signal_values)} values")
    print(f"Histogram: {len(histogram_values)} values")

    print(f"\nLatest values:")
    print(f"MACD Line: {line_values.iloc[-1]:.4f}")
    print(f"Signal Line: {signal_values.iloc[-1]:.4f}")
    print(f"Histogram: {histogram_values.iloc[-1]:.4f}")

    print(f"\nCache now contains: {list(market_data._indicator_cache.keys())}")


def compare_strategies():
    """Compare different strategies on the same data"""
    print("\n" + "=" * 60)
    print("COMPARING DIFFERENT STRATEGIES ON SAME DATA")
    print("=" * 60)

    market_data = MarketData("QQQ", "1y")

    strategies = [
        ("20-50 SMA Cross", MovingAverageCross(20, 50, "SMA")),
        ("50-200 SMA Cross", MovingAverageCross(50, 200, "SMA")),
        ("12-26 EMA Cross", MovingAverageCross(12, 26, "EMA")),
        ("RSI Cross (14, 30-70)", RSICross(14, 30, 70)),
        ("MACD Cross (12-26-9)", MACDCross(12, 26, 9)),
        ("MACD Histogram", MACDHistogramStrategy(12, 26, 9)),
    ]

    backtest = BackTest(initial_capital=10000)
    results = {}

    for name, strategy in strategies:
        print(f"\n--- {name} ---")
        try:
            result = backtest.run_backtest(market_data, strategy)
            results[name] = result
            print(f"Total Return: {result['metrics']['total_return']:.2%}")
            print(f"Win Rate: {result['metrics']['win_rate']:.2%}")
            print(f"Total Trades: {result['metrics']['total_trades']}")
        except Exception as e:
            print(f"Error running {name}: {e}")

    # Find best performing strategy
    if results:
        best_strategy = max(
            results.items(), key=lambda x: x[1]['metrics']['total_return'])
        print(f"\n🏆 Best performing strategy: {best_strategy[0]}")
        print(
            f"   Total Return: {best_strategy[1]['metrics']['total_return']:.2%}")


def main():
    """Main demonstration function"""
    print("Technical Analysis Learning Project - Demonstration")
    print("This script demonstrates the new improved system design")

    try:
        demonstrate_50_200_strategy()

        demonstrate_rsi_strategy()

        demonstrate_macd_strategy()

        demonstrate_indicator_caching()
        demonstrate_macd_components()

        compare_strategies()

    except Exception as e:
        print(f"Error during demonstration: {e}")
        print("Make sure you have internet connection for data fetching.")


if __name__ == "__main__":
    main()
