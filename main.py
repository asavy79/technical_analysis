import yfinance as yf


class Stock:
    def __init__(self, ticker: str, period: int):
        self.ticker = ticker
        self.period = period
        self.history = self.__get_history()

    def __get_history(self):
        history = yf.Ticker(self.ticker).history(period=f"{self.period}d")
        return history

    def get_col(self, col_name):
        return self.history[col_name]

    def get_cols(self, col_names):
        return self.history[col_names]

    def get_dates(self):
        return self.history.index

    def get_period(self):
        return self.period

    def get_ticker(self):
        return self.ticker


apple_stock = Stock("AAPL", 10)
