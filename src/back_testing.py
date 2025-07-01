from strategies import MovingAverageCross
from main import Stock
import numpy as np


class BackTest:
    def __init__(self, strategy, initial_dollars):
        self.strategy = strategy
        self.initial_dollars = initial_dollars

    def calculate_return(self, stock_data: Stock):
        pass

    def simulate_trades(self, stock_data: Stock):
        buy, sell = self.generate_signals(stock_data)
        print(buy.index)
        print(sell.index)
        buy_prices, sell_prices = np.array(
            buy['Close']), np.array(sell['Close'])
        print(buy_prices)
        print(sell_prices)
        total_return = 1
        for i in range(len(buy_prices)):
            total_return *= (sell_prices[i] / buy_prices[i])
        return round(total_return * self.initial_dollars, 2)

    def generate_signals(self, stock_data: Stock):
        buy = self.strategy.calculate_bullish_signal(stock_data)
        sell = self.strategy.calculate_bearish_signal(stock_data)
        first_buy_date = buy.index[0]
        sell = sell[sell.index > first_buy_date]
        if len(sell) > len(buy):
            sell = sell[:len(buy)][:]
        elif len(sell) < len(buy):
            buy = buy[:len(sell)][:]
        return buy, sell

    def compute_metrics(self):
        pass


# stock_data = Stock("SPY", 1000)
# strategy = MovingAverageCross(20, 60)
# backTest = BackTest(strategy, 1000)

# print(backTest.simulate_trades(stock_data))
