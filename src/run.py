from indicators import SMA, RSI, EMA, MACDLine
from main import MarketData
from strategies import MovingAverageCross
from back_testing import BackTest
import pandas as pd


apple = MarketData("QQQ", "5y")

strategy = MovingAverageCross(20, 50, "SMA")


apple_raw_data = apple.get_raw_data()

backtester = BackTest(initial_capital=50000)

backtest = backtester.run_backtest(apple, strategy)

trades = pd.DataFrame(backtest['trades'])
print(trades)

# Big W trade make so much money
print(backtest['metrics']['final_capital'])
