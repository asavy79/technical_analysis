from abc import ABC, abstractmethod
from typing import List, Dict
import pandas as pd
import numpy as np
from src.indicators import SMA, EMA, RSI, MACDLine, MACDSignal, MACDHistogram
from src.main import MarketData


class Strategy(ABC):
    @abstractmethod
    def get_required_indicators(self) -> List:
        """Return list of indicators this strategy needs"""
        pass

    @classmethod
    def generate_from_params(cls, params: dict):
        """Instantation strategy object from api route parameters"""
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

    @classmethod
    def generate_from_params(cls, params: dict):
        if 'lower_period' not in params or 'upper_period' not in params or 'ma_type' not in params:
            raise ValueError(
                "Moving average parameters must include 'lower_period', 'upper_period', and 'ma_type'")

        lower_period, upper_period, ma_type = int(params['lower_period']), int(
            params['upper_period']), params['ma_type']
        return cls(lower_period, upper_period, ma_type)

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

    @classmethod
    def generate_from_params(cls, params: dict):
        if 'rsi_period' not in params or 'lower_bound' not in params or 'upper_bound' not in params:
            raise ValueError(
                "RSI cross parameters must include 'rsi_period', 'lower_bound', and 'upper_bound'")

        rsi_period, lower_bound, upper_bound = int(params[
            'rsi_period']), int(params['lower_bound']), int(params['upper_bound'])
        return cls(rsi_period, lower_bound, upper_bound)

    def get_required_indicators(self) -> List:
        return [self.rsi_indicator]

    def calculate_signals(self, market_data) -> Dict[str, pd.Series]:

        try:
            rsi_values = market_data.get_indicator_data(self.rsi_indicator)
        except Exception as e:
            raise ValueError(f"Error computing RSI: {e}")

        # RSI crosses above lower bound - buy!
        buy_signals = (rsi_values > self.lower_bound) & (
            rsi_values.shift(1) <= self.lower_bound)

        # RSI crosses below upper bound - sell!
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

    @classmethod
    def generate_from_params(cls, params: dict):
        if 'rsi_period' not in params or 'oversold_threshold' not in params or 'overbought_threshold' not in params:
            raise ValueError(
                "RSI extreme parameters must include 'rsi_period', 'oversold_threshold', and 'overbought_threshold'")

        rsi_period, oversold_threshold, overbought_threshold = int(params[
            'rsi_period']), int(params['oversold_threshold']), int(params['overbought_threshold'])
        return cls(rsi_period, oversold_threshold, overbought_threshold)

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

    @classmethod
    def generate_from_params(cls, params: dict):
        if 'short_period' not in params or 'long_period' not in params or 'signal_period' not in params:
            raise ValueError(
                "RSI cross parameters must include 'short_period', 'long_period', and 'signal_period'")

        short_period, long_period, signal_period = int(params[
            'short_period']), int(params['long_period']), int(params['signal_period'])
        return cls(short_period, long_period, signal_period)

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

    @classmethod
    def generate_from_params(cls, params: dict):
        if 'short_period' not in params or 'long_period' not in params or 'signal_period' not in params:
            raise ValueError(
                "RSI cross parameters must include 'short_period', 'long_period', and 'signal_period'")

        short_period, long_period, signal_period = int(params[
            'short_period']), int(params['long_period']), int(params['signal_period'])
        return cls(short_period, long_period, signal_period)

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


class CustomStrategy(Strategy):

    def __init__(self, mode='all'):
        self.strategies: List[Strategy] = []
        if mode not in ['all', 'any', 'majority']:
            print(mode)
            raise ValueError(
                "Custom strategy mode must be either 'all', 'any', or 'majority'")
        self.mode = mode

    @classmethod
    def generate_from_params(cls, params: dict):
        if 'mode' not in params:
            raise ValueError(
                "Parameters for initializing a custom strategy must include 'mode'")

        return cls(params['mode'])

    def add_strategy(self, strategy: Strategy):
        self.strategies.append(strategy)

    def validate_data(self, market_data):

        for s in self.strategies:
            s.validate_data(market_data)

    def get_required_indicators(self):
        res = []

        for s in self.strategies:
            indicators = s.get_required_indicators()
            res += indicators
        return res

    def calculate_signals(self, market_data: MarketData):

        if not self.strategies:
            raise ValueError("No strategies added yet!")

        buy_df = pd.DataFrame()
        sell_df = pd.DataFrame()
        for num, s in enumerate(self.strategies):
            new_col = s.calculate_signals(market_data)
            new_label = f"Strategy_{num}"
            buy_df[new_label] = new_col['buy']
            sell_df[new_label] = new_col['sell']

        if self.mode == 'all':
            combined_buy = buy_df.all(axis=1)
            combined_sell = sell_df.all(axis=1)
        else:
            combined_buy = buy_df.any(axis=1)
            combined_sell = sell_df.any(axis=1)

        return {
            'buy': combined_buy,
            'sell': combined_sell
        }

        # Loop through strategies and use bitwise and to generate buy and sell markers
