import yfinance as yf
import pandas as pd
from typing import Dict, Any


class MarketData:
    def __init__(self, ticker: str, period: str):
        if not ticker or not isinstance(ticker, str):
            raise ValueError("Ticker must be a non-empty string")
        if not period or not isinstance(period, str):
            raise ValueError("Period must be a non-empty string")

        self.ticker = ticker.upper()
        self.period = period
        self.raw_data = self._fetch_data()
        self._indicator_cache: Dict[str, pd.Series] = {}

    def _fetch_data(self) -> pd.DataFrame:
        try:
            data = yf.Ticker(self.ticker).history(period=self.period)
            if data.empty:
                raise ValueError(f"No data found for ticker {self.ticker}")
            return data
        except Exception as e:
            raise ValueError(f"Error fetching data for {self.ticker}: {e}")

    def get_indicator_data(self, indicator) -> pd.Series:
        indicator_key = str(indicator)

        if indicator_key not in self._indicator_cache:
            try:
                self._indicator_cache[indicator_key] = indicator.compute(
                    self.raw_data)
            except Exception as e:
                raise ValueError(f"Error computing {indicator_key}: {e}")

        return self._indicator_cache[indicator_key]

    def get_raw_data(self) -> pd.DataFrame:
        return self.raw_data

    def get_ticker(self) -> str:
        return self.ticker

    def get_period(self) -> str:
        return self.period

    def clear_cache(self):
        self._indicator_cache.clear()
