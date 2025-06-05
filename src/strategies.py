from src.main import Stock
from src.indicators import MovingAverage
import numpy as np
from abc import ABC, abstractmethod


class Strategy(ABC):
    def __init__(self):
        super().__init__()

    @abstractmethod
    def calculate_bullish_signal(self, stock_data: Stock):
        pass

    @abstractmethod
    def calculate_bearish_signal(self, stock_data: Stock):
        pass


class MovingAverageCross:
    def __init__(self, lower_ma: int, higher_ma: int):
        self.lower_ma = lower_ma
        self.higher_ma = higher_ma

    def calculate_bullish_signal(self, stock_data: Stock):
        ma_lower = MovingAverage(self.lower_ma)
        ma_upper = MovingAverage(self.higher_ma)

        ma_lower_values = np.array(ma_lower.compute(stock_data))
        ma_upper_values = np.array(ma_upper.compute(stock_data))

        indices = []
        arr_len = len(ma_lower_values)

        for i in range(1, arr_len):
            if ma_lower_values[i-1] < ma_upper_values[i-1] and ma_lower_values[i] > ma_upper_values[i]:
                indices.append(i)

        history = stock_data.history
        return history.iloc[indices][:]

    def calculate_bearish_signal(self, stock_data: Stock):
        ma_lower = MovingAverage(self.lower_ma)
        ma_upper = MovingAverage(self.higher_ma)

        ma_lower_values = np.array(ma_lower.compute(stock_data))
        ma_upper_values = np.array(ma_upper.compute(stock_data))

        indices = []
        arr_len = len(ma_lower_values)

        for i in range(1, arr_len):
            if ma_lower_values[i-1] > ma_upper_values[i-1] and ma_lower_values[i] < ma_upper_values[i]:
                indices.append(i)

        history = stock_data.history
        return history.iloc[indices][:]
