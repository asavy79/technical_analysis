from indicators import SMA, RSI, EMA, MACDLine
from main import MarketData
from strategies import MovingAverageCross, RSICross
from back_testing import BackTest
import pandas as pd


apple = MarketData("aapl", "5y")

strategy = RSICross(14, 30, 70)


apple_raw_data = apple.get_raw_data()

initial_capital = 50000
backtester = BackTest(initial_capital)

backtest = backtester.run_backtest(apple, strategy)

trades = pd.DataFrame(backtest['trades'])
print(trades)

# Big W trade make so much money

final_capital = backtest['metrics']['final_capital']
print((final_capital-initial_capital) / initial_capital)

start_price = apple_raw_data['Close'].iloc[0]
end_price = apple_raw_data['Close'].iloc[-1]

print((end_price-start_price) / start_price)
