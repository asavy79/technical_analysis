import pandas as pd
import numpy as np
from abc import ABC, abstractmethod


class Indicator(ABC):
    def __init__(self):
        super().__init__()

    @abstractmethod
    def compute(self, stock_data):
        pass

    @abstractmethod
    def __str__(self):
        pass


class MovingAverage(Indicator):
    def __init__(self, period):
        super().__init__()
        self.period = period

    def compute(self, stock_data):

        try:
            history = stock_data['Close']
        except Exception as e:
            print(f"Error getting history for Close: {e}")
            return pd.Series()

        try:
            moving_averages = history.rolling(
                self.period).mean()
        except Exception as e:
            print(f"Error getting moving averages: {e}")
            return pd.Series()

        return moving_averages

    def __str__(self):
        return f'MA_{self.period}'


class RSI(Indicator):
    def __init__(self, period):
        super().__init__()
        self.period = period

    def compute(self, stock_data):

        try:
            history = stock_data['Close']
        except Exception as e:
            print(f"Error getting closing prices for stock: {e}")
            return pd.Series()

        try:
            differences = history.diff()
        except Exception as e:
            print(f"Error getting differences for stock: {e}")
            return pd.Series()

        rsi_values = self.get_rsi_values(differences)

        if rsi_values.empty:
            print(f"RSI values are empty")
            return pd.Series()
        return rsi_values

    def get_period(self):
        return self.period

    def get_rsi_values(self, differences):
        period = self.get_period()

        differences = differences.dropna()

        gains = differences.clip(lower=0)
        losses = -differences.clip(upper=0)

        avg_gain = gains.ewm(alpha=1/period, adjust=False).mean()
        avg_loss = losses.ewm(alpha=1/period, adjust=False).mean()

        try:
            rs = avg_gain / avg_loss
        except Exception as e:
            print(f"Error getting RS for stock: {e}")
            return pd.Series()

        # handle edge case where the stock has only gone up in the time period
        rs = rs.replace([np.inf, -np.inf], np.nan).fillna(0)

        rsi = 100 - (100 / (1+rs))
        return rsi

    def __str__(self):
        return f'RSI_{self.period}d'
