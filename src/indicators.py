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


class RSI(Indicator):
    def __init__(self, period):
        super().__init__()
        self.period = period

    def compute(self, stock_data: Stock):

        history_days = stock_data.get_period()
        total_sub = history_days + self.period
        ticker = stock_data.get_ticker()

        history = yf.Ticker(ticker).history(period=f"{total_sub}d")["Close"]
        differences = history.diff()

        rsi_values = self.get_rsi_values(differences)

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

        rs = avg_gain / avg_loss

        # handle edge case where the stock has only gone up in the time period
        rs = rs.replace([np.inf, -np.inf], np.nan).fillna(0)

        rsi = 100 - (100 / (1+rs))
        return rsi


indicator = RSI(period=14)


stock = Stock("AAPL", 100)
mas = indicator.compute(stock)

print(mas)
