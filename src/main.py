import yfinance as yf
import pandas as pd
from typing import List
from indicators import Indicator


class Stock:
    def __init__(self, ticker: str, period: int):
        self.ticker = ticker
        self.period = period
        self.history = self.__load_history()

    def get_history(self):
        return self.history

    def __load_history(self):
        try:
            history = yf.Ticker(self.ticker).history(period=f"{self.period}d")
            return history
        except Exception as e:
            print(f"Error getting history for {self.ticker}: {e}")
            return pd.DataFrame()

    def add_indicators(self, strategies: List[Indicator]):
        history = self.get_history()
        try:
            for strategy in strategies:
                label, vals = str(strategy), strategy.compute(history)
                self.history[label] = vals

        except Exception as e:
            print("Failed to add strategies")

    def get_col(self, col_name: str):
        if col_name not in self.history.columns:
            raise ValueError(f"Column {col_name} not found in history")
        if self.history.empty:
            raise ValueError("History is empty")
        return self.history[col_name]

    def get_cols(self, col_names: list[str]):
        for col_name in col_names:
            if col_name not in self.history.columns:
                raise ValueError(f"Column {col_name} not found in history")
        if self.history.empty:
            raise ValueError("History is empty")
        return self.history[col_names]

    def get_dates(self):
        return self.history.index

    def get_period(self):
        return self.period

    def get_ticker(self):
        return self.ticker
