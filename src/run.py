from indicators import MovingAverage, RSI
from main import Stock


ma_20 = MovingAverage(20)
ma_50 = MovingAverage(50)
rsi_14 = RSI(14)

apple_stock = Stock('AAPL', 600)

apple_stock.add_indicators([ma_20, ma_50, rsi_14])


data = apple_stock.get_history()

data.to_csv('output.csv', index=True)
