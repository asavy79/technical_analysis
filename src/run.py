from indicators import SMA, RSI, EMA, MACDLine
from main import MarketData
from strategies import MovingAverageCross, RSICross, CustomStrategy, RSIExtremes
from back_testing import BackTest
import pandas as pd


apple = MarketData("spy", "5y")

rsi_cross_strategy = RSIExtremes(14, 30, 70)

ma_cross_strategy = MovingAverageCross(50, 200, "SMA")

custom_strategy = CustomStrategy(mode='any')

custom_strategy.add_strategy(ma_cross_strategy)
custom_strategy.add_strategy(rsi_cross_strategy)

sigs = custom_strategy.calculate_signals(apple)

print(sum(sigs['buy'] == True))
print(sum(sigs['sell'] == True))

df = custom_strategy.calculate_signals(apple)

backtester = BackTest(initial_capital=10000)

res = backtester.run_backtest(apple, custom_strategy)


# W trade
print(res)
