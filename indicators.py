import yfinance as yf
import pandas as pd
import numpy as np
from abc import ABC, abstractmethod
from main import Stock


class Indicator(ABC):
    def __init__(self):
        super().__init__()

    @abstractmethod
    def compute(self, stock_data: Stock):
        pass


class MovingAverage(Indicator):
    def __init__(self, period):
        super().__init__()
        self.period = period

    def compute(self, stock_data: Stock):

        history_days = stock_data.get_period()
        total_sub = history_days + self.period
        ticker = stock_data.get_ticker()

        history = yf.Ticker(ticker).history(period=f"{total_sub}d")
        moving_averages = history["Close"].rolling(
            self.period).mean()
        return moving_averages[self.period:][:]
