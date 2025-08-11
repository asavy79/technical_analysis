from src.strategies import CustomStrategy, MovingAverageCross, RSICross, RSIExtremes, Strategy, MACDCross
from typing import List, Literal
from backend.models import StrategyConfig

strategy_mapping = {
    "moving_average_cross": MovingAverageCross,
    "rsi_extremes": RSIExtremes,
    "rsi_cross": RSICross,
    "macd_cross": MACDCross
}


def create_strategy(strategies: List[StrategyConfig]):
    custom_strategy = CustomStrategy(mode="any")
    try:

        for strategy_config in strategies:
            if strategy_config.type not in strategy_mapping:
                raise ValueError("Strategy not yet implemented!")

            strategy_builder: Strategy = strategy_mapping[strategy_config.type]

            strategy_object = strategy_builder.generate_from_params(
                strategy_config.params)

            custom_strategy.add_strategy(strategy_object)

        return custom_strategy
    except Exception as e:
        raise e
