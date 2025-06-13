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
        l = 1

        differences = np.array(differences)

        pos_changes, neg_changes = 0.0, 0.0

        period = self.get_period()

        arr = []

        for r in range(1, len(differences)):
            print(differences[r])
            if differences[r] > 0:
                pos_changes += abs(differences[r])
            else:
                neg_changes += abs(differences[r])
            if (r - l)+1 == period:
                avg_loss, avg_gain = float(
                    neg_changes) / period, float(pos_changes) / period
                if avg_loss == 0:
                    rsi = 100.00
                else:
                    rs = avg_gain / avg_loss
                    rsi = 100 - (100 / (1 + rs))
                arr.append(rsi)
                if differences[l] < 0:
                    neg_changes -= abs(differences[l])
                else:
                    pos_changes -= abs(differences[l])
                l += 1
        return np.array(arr)


rsi_14 = RSI(14)

stock = Stock("AAPL", 100)

rsi_vals = rsi_14.compute(stock)
