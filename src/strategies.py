from abc import ABC, abstractmethod
from typing import List, Dict
import pandas as pd
import numpy as np
from indicators import SMA, EMA, RSI, MACDLine, MACDSignal, MACDHistogram
from main import MarketData


class Strategy(ABC):
    @abstractmethod
    def get_required_indicators(self) -> List:
        """Return list of indicators this strategy needs"""
        pass

    @abstractmethod
    def calculate_signals(self, market_data) -> Dict[str, pd.Series]:
        """Return dict with 'buy' and 'sell' signal Series"""
        pass

    def validate_data(self, market_data):
        """Ensure all required indicators can be computed"""
        for indicator in self.get_required_indicators():
            try:
                market_data.get_indicator_data(indicator)
            except Exception as e:
                raise ValueError(f"Cannot compute {indicator}: {e}")


class MovingAverageCross(Strategy):
    def __init__(self, lower_period: int, upper_period: int, ma_type: str = "SMA"):
        if lower_period <= 0 or upper_period <= 0:
            raise ValueError("Periods must be positive")
        if lower_period >= upper_period:
            raise ValueError("lower_period must be less than upper_period")

        self.lower_period = lower_period
        self.upper_period = upper_period

        if ma_type.upper() == "SMA":
            self.lower_ma = SMA(lower_period)
            self.upper_ma = SMA(upper_period)
        elif ma_type.upper() == "EMA":
            self.lower_ma = EMA(lower_period)
            self.upper_ma = EMA(upper_period)
        else:
            raise ValueError("ma_type must be 'SMA' or 'EMA'")

    def get_required_indicators(self) -> List:
        return [self.lower_ma, self.upper_ma]

    def calculate_signals(self, market_data: MarketData) -> Dict[str, pd.Series]:
        self.validate_data(market_data)

        try:
            lower_values = market_data.get_indicator_data(self.lower_ma)
            upper_values = market_data.get_indicator_data(self.upper_ma)
        except Exception as e:
            raise ValueError(f"Error computing indicators: {e}")

        # Remove NaN values from the series because those suck
        aligned_lower, aligned_upper = lower_values.align(
            upper_values, join='inner')

        bullish_cross = (aligned_lower > aligned_upper) & (
            aligned_lower.shift(1) <= aligned_upper.shift(1))

        bearish_cross = (aligned_lower < aligned_upper) & (
            aligned_lower.shift(1) >= aligned_upper.shift(1))

        return {
            'buy': bullish_cross.fillna(False),
            'sell': bearish_cross.fillna(False)
        }


class RSICross(Strategy):
    def __init__(self, rsi_period: int, lower_bound: float, upper_bound: float):
        if rsi_period <= 0:
            raise ValueError("RSI period must be positive")
        if not (0 < lower_bound < upper_bound < 100):
            raise ValueError(
                "Bounds must be: 0 < lower_bound < upper_bound < 100")

        self.rsi_period = rsi_period
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
        self.rsi_indicator = RSI(rsi_period)

    def get_required_indicators(self) -> List:
        return [self.rsi_indicator]

    def calculate_signals(self, market_data) -> Dict[str, pd.Series]:

        try:
            rsi_values = market_data.get_indicator_data(self.rsi_indicator)
        except Exception as e:
            raise ValueError(f"Error computing RSI: {e}")

        # RSI crosses above lower bound - totally a buy!
        buy_signals = (rsi_values > self.lower_bound) & (
            rsi_values.shift(1) <= self.lower_bound)

        # RSI crosses below upper bound - totally a sell!
        sell_signals = (rsi_values < self.upper_bound) & (
            rsi_values.shift(1) >= self.upper_bound)

        return {
            'buy': buy_signals.fillna(False),
            'sell': sell_signals.fillna(False)
        }


class RSIExtremes(Strategy):
    def __init__(self, rsi_period: int, oversold_threshold: float = 30, overbought_threshold: float = 70):
        if rsi_period <= 0:
            raise ValueError("RSI period must be positive")
        if not (0 < oversold_threshold < overbought_threshold < 100):
            raise ValueError(
                "Thresholds must be: 0 < oversold < overbought < 100")

        self.rsi_period = rsi_period
        self.oversold_threshold = oversold_threshold
        self.overbought_threshold = overbought_threshold
        self.rsi_indicator = RSI(rsi_period)

    def get_required_indicators(self) -> List:
        return [self.rsi_indicator]

    def calculate_signals(self, market_data) -> Dict[str, pd.Series]:
        """Generate signals based on RSI extreme levels"""
        rsi_values = market_data.get_indicator_data(self.rsi_indicator)

        # Buy when RSI is oversold (below threshold)
        buy_signals = rsi_values < self.oversold_threshold

        # Sell when RSI is overbought (above threshold)
        sell_signals = rsi_values > self.overbought_threshold

        return {
            'buy': buy_signals.fillna(False),
            'sell': sell_signals.fillna(False)
        }


class MACDCross(Strategy):
    def __init__(self, short_period: int = 12, long_period: int = 26, signal_period: int = 9):
        if short_period <= 0 or long_period <= 0 or signal_period <= 0:
            raise ValueError("All periods must be positive")
        if short_period >= long_period:
            raise ValueError("Short period must be less than long period")

        self.short_period = short_period
        self.long_period = long_period
        self.signal_period = signal_period

        self.macd_line = MACDLine(short_period, long_period)
        self.macd_signal = MACDSignal(short_period, long_period, signal_period)

    def get_required_indicators(self) -> List:
        return [self.macd_line, self.macd_signal]

    def calculate_signals(self, market_data) -> Dict[str, pd.Series]:

        try:
            macd_line = market_data.get_indicator_data(self.macd_line)
            signal_line = market_data.get_indicator_data(self.macd_signal)
        except Exception as e:
            raise ValueError(f"Error computing MACD: {e}")

        # Get rid of NaN and only keep values that are present in both series ;)
        aligned_macd, aligned_signal = macd_line.align(
            signal_line, join='inner')

        # Bullish: MACD line crosses above signal line - buy!
        buy_signals = (aligned_macd > aligned_signal) & (
            aligned_macd.shift(1) <= aligned_signal.shift(1))

        # Bearish: MACD line crosses below signal line - sell!
        sell_signals = (aligned_macd < aligned_signal) & (
            aligned_macd.shift(1) >= aligned_signal.shift(1))

        return {
            'buy': buy_signals.fillna(False),
            'sell': sell_signals.fillna(False)
        }


class MACDHistogramStrategy(Strategy):
    def __init__(self, short_period: int = 12, long_period: int = 26, signal_period: int = 9):
        if short_period <= 0 or long_period <= 0 or signal_period <= 0:
            raise ValueError("All periods must be positive")
        if short_period >= long_period:
            raise ValueError("Short period must be less than long period")

        self.short_period = short_period
        self.long_period = long_period
        self.signal_period = signal_period

        self.macd_histogram = MACDHistogram(
            short_period, long_period, signal_period)

    def get_required_indicators(self) -> List:
        return [self.macd_histogram]

    def calculate_signals(self, market_data) -> Dict[str, pd.Series]:
        """Generate signals based on MACD histogram zero crossings"""
        histogram = market_data.get_indicator_data(self.macd_histogram)

        # Buy when histogram crosses above zero (momentum turning positive!)
        buy_signals = (histogram > 0) & (histogram.shift(1) <= 0)

        # Sell when histogram crosses below zero (momentum turning negative!)
        sell_signals = (histogram < 0) & (histogram.shift(1) >= 0)

        return {
            'buy': buy_signals.fillna(False),
            'sell': sell_signals.fillna(False)
        }
