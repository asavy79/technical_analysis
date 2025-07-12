from indicators import SMA, RSI, EMA
from main import Stock
from strategies import MovingAverageCross, RSICross


ma_20 = SMA(20)
ma_50 = SMA(50)
rsi_14 = RSI(14)
ema_50 = EMA(50)
ema_200 = EMA(200)

apple_stock = Stock('AAPL', 600)

apple_stock.add_indicators([ma_20, ma_50, rsi_14, ema_50, ema_200])


data = apple_stock.get_history()

data.to_csv('output.csv', index=True)


strategy = MovingAverageCross(str(ma_20), str(ma_50))

rsi_strategy = RSICross(str(rsi_14), 30, 70)

ema_strategy = MovingAverageCross(str(ema_50), str(ema_200))

signals = ema_strategy.calculate_signals(data)

signals.to_csv('signals.csv', index=True)
