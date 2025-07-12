from indicators import MovingAverage, RSI
from main import Stock
from strategies import SMACross, RSICross


ma_20 = MovingAverage(20)
ma_50 = MovingAverage(50)
rsi_14 = RSI(14)

apple_stock = Stock('AAPL', 600)

apple_stock.add_indicators([ma_20, ma_50, rsi_14])


data = apple_stock.get_history()


strategy = SMACross(str(ma_20), str(ma_50))

rsi_strategy = RSICross(str(rsi_14), 30, 70)

signals = rsi_strategy.calculate_signals(data)

signals.to_csv('signals.csv', index=True)
