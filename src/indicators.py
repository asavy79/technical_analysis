import pandas as pd
import numpy as np
from abc import ABC, abstractmethod


class Indicator(ABC):
    @abstractmethod
    def compute(self, raw_data: pd.DataFrame) -> pd.Series:
        """Compute indicator values from raw OHLCV data"""
        pass

    @abstractmethod
    def __str__(self) -> str:
        # Allows you to cache indicators
        pass

    def __eq__(self, other):
        return str(self) == str(other)

    def __hash__(self):
        return hash(str(self))


class SMA(Indicator):
    def __init__(self, period: int):
        if period <= 0:
            raise ValueError("Period must be positive")
        self.period = period

    def compute(self, raw_data: pd.DataFrame) -> pd.Series:
        if 'Close' not in raw_data.columns:
            raise ValueError("Close column required for SMA")
        if len(raw_data) < self.period:
            raise ValueError(
                f"Not enough data points. Need at least {self.period}, got {len(raw_data)}")

        try:
            return raw_data['Close'].rolling(window=self.period).mean()
        except Exception as e:
            raise ValueError(f"Error computing SMA: {e}")

    def __str__(self):
        return f"SMA_{self.period}"


class EMA(Indicator):
    def __init__(self, period: int):
        if period <= 0:
            raise ValueError("Period must be positive")
        self.period = period

    def compute(self, raw_data: pd.DataFrame) -> pd.Series:
        if 'Close' not in raw_data.columns:
            raise ValueError("Close column required for EMA")
        if len(raw_data) < self.period:
            raise ValueError(
                f"Not enough data points. Need at least {self.period}, got {len(raw_data)}")

        try:
            return raw_data['Close'].ewm(span=self.period, adjust=False).mean()
        except Exception as e:
            raise ValueError(f"Error computing EMA: {e}")

    def __str__(self):
        return f"EMA_{self.period}"


class RSI(Indicator):
    def __init__(self, period: int):
        if period <= 0:
            raise ValueError("Period must be positive")
        self.period = period

    def compute(self, raw_data: pd.DataFrame) -> pd.Series:
        if 'Close' not in raw_data.columns:
            raise ValueError("Close column required for RSI")
        if len(raw_data) < self.period + 1:
            raise ValueError(
                f"Not enough data points. Need at least {self.period + 1}, got {len(raw_data)}")

        try:
            close_prices = raw_data['Close']
            differences = close_prices.diff()

            # Separate gains and losses
            gains = differences.clip(lower=0)
            losses = -differences.clip(upper=0)

            # Calculate exponential moving averages
            avg_gain = gains.ewm(alpha=1/self.period, adjust=False).mean()
            avg_loss = losses.ewm(alpha=1/self.period, adjust=False).mean()

            # Calculate RS and RSI
            rs = avg_gain / avg_loss

            # Handle edge cases (division by zero, infinite values)
            rs = rs.replace([np.inf, -np.inf], np.nan)
            rsi = 100 - (100 / (1 + rs))
            rsi[:self.period] = np.nan
            return rsi

        except Exception as e:
            raise ValueError(f"Error computing RSI: {e}")

    def __str__(self):
        return f"RSI_{self.period}"


class MACDLine(Indicator):
    def __init__(self, short_period: int = 12, long_period: int = 26):
        if short_period <= 0 or long_period <= 0:
            raise ValueError("All periods must be positive")
        if short_period >= long_period:
            raise ValueError("Short period must be less than long period")

        self.short_period = short_period
        self.long_period = long_period

    def compute(self, raw_data: pd.DataFrame) -> pd.Series:
        if 'Close' not in raw_data.columns:
            raise ValueError("Close column required for MACD")
        if len(raw_data) < self.long_period:
            raise ValueError(f"Not enough data points for MACD calculation")

        try:
            # Calculate EMAs
            ema_short = EMA(self.short_period).compute(raw_data)
            ema_long = EMA(self.long_period).compute(raw_data)

            # MACD line = short EMA - long EMA
            macd_line = ema_short - ema_long
            return macd_line

        except Exception as e:
            raise ValueError(f"Error computing MACD line: {e}")

    def __str__(self):
        return f"MACD_Line_{self.short_period}_{self.long_period}"


class MACDSignal(Indicator):
    def __init__(self, short_period: int = 12, long_period: int = 26, signal_period: int = 9):
        if short_period <= 0 or long_period <= 0 or signal_period <= 0:
            raise ValueError("All periods must be positive")
        if short_period >= long_period:
            raise ValueError("Short period must be less than long period")

        self.short_period = short_period
        self.long_period = long_period
        self.signal_period = signal_period
        self.macd_line = MACDLine(short_period, long_period)

    def compute(self, raw_data: pd.DataFrame) -> pd.Series:
        if 'Close' not in raw_data.columns:
            raise ValueError("Close column required for MACD Signal")
        if len(raw_data) < self.long_period + self.signal_period:
            raise ValueError(
                f"Not enough data points for MACD Signal calculation")

        try:
            # Get MACD line
            macd_line = self.macd_line.compute(raw_data)

            # Signal line = EMA of MACD line
            signal_line = macd_line.ewm(
                span=self.signal_period, adjust=False).mean()
            return signal_line

        except Exception as e:
            raise ValueError(f"Error computing MACD signal: {e}")

    def __str__(self):
        return f"MACD_Signal_{self.short_period}_{self.long_period}_{self.signal_period}"


class MACDHistogram(Indicator):
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

    def compute(self, raw_data: pd.DataFrame) -> pd.Series:
        if 'Close' not in raw_data.columns:
            raise ValueError("Close column required for MACD Histogram")
        if len(raw_data) < self.long_period + self.signal_period:
            raise ValueError(
                f"Not enough data points for MACD Histogram calculation")

        try:
            # Get MACD line and signal line
            macd_line = self.macd_line.compute(raw_data)
            signal_line = self.macd_signal.compute(raw_data)

            # Histogram = MACD line - signal line
            histogram = macd_line - signal_line
            return histogram

        except Exception as e:
            raise ValueError(f"Error computing MACD histogram: {e}")

    def __str__(self):
        return f"MACD_Histogram_{self.short_period}_{self.long_period}_{self.signal_period}"
