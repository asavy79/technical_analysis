from backend.create_strategy import create_strategy
from src.back_testing import BackTest
from src.main import MarketData
from backend.models import BacktestRequest
from backend.create_strategy import create_strategy


def run_backtest(request: BacktestRequest):
    stock_object = MarketData(request.ticker, request.period)

    custom_strategy = create_strategy(request.strategies)

    backtest_object = BackTest(initial_capital=int(request.initial_capital))

    results = backtest_object.run_backtest(stock_object, custom_strategy)
    return results['metrics']
