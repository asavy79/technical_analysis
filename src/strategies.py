import numpy as np
from abc import ABC, abstractmethod
import pandas as pd


class Strategy(ABC):
    def __init__(self):
        super().__init__()

    @abstractmethod
    def calculate_signals(self, stock_data: pd.DataFrame):
        pass


class MovingAverageCross(Strategy):
    def __init__(self, lower_column: str, upper_column):
        super().__init__()
        self.lower_column = lower_column
        self.upper_column = upper_column

    def calculate_signals(self, stock_data):

        if self.lower_column not in stock_data.columns:
            raise ValueError(
                f"Column '{self.lower_column}' not found in stock_data")

        if self.upper_column not in stock_data.columns:
            raise ValueError(
                f"Column '{self.lower_column}' not found in stock_data")

        df = stock_data[[self.lower_column, self.upper_column]].dropna().copy()

        signals = pd.Series(0, index=df.index)

        prev_short = df[self.lower_column].shift(1)
        prev_long = df[self.upper_column].shift(1)

        golden_cross = (prev_short < prev_long) & (
            df[self.lower_column] > df[self.upper_column])
        death_cross = (prev_short > prev_long) & (
            df[self.lower_column] < df[self.upper_column])

        signals[golden_cross] = 1  # Buy
        signals[death_cross] = -1  # Sell

        return signals


class RSICross(Strategy):
    def __init__(self, rsi_column: str, lower_bound: int, upper_bound: int):
        super().__init__()
        self.rsi_column = rsi_column
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound

    def calculate_signals(self, stock_data):

        if self.rsi_column not in stock_data.columns:
            raise ValueError(
                f"Column '{self.rsi_column}' not found in stock_data.")

        df = stock_data.copy()
        df = df.dropna(subset=[self.rsi_column])

        signals = pd.Series(0, index=df.index)
        rsi_data = df[self.rsi_column]
        rsi_prev = rsi_data.shift(1)

        golden_cross = (rsi_prev > self.lower_bound) & (
            rsi_data < self.lower_bound)

        death_cross = (rsi_prev < self.upper_bound) & (
            rsi_data > self.upper_bound)

        signals[golden_cross] = 1  # Buy
        signals[death_cross] = -1  # Sell

        return signals
