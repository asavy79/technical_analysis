from src.strategies import CustomStrategy, MovingAverageCross, RSICross, RSIExtremes
from typing import List, Literal
from models import StrategyConfig

strategy_mapping = {
    "moving_average_cross": MovingAverageCross,
    "rsi_extremes": RSIExtremes,
    "rsi_cross": RSICross
}


def create_strategy(strategies: List[StrategyConfig]):
    custom_strategy = CustomStrategy(mode="any")
    try:

        for strategy_config in strategies:
            if strategy_config.type not in strategy_mapping:
                raise ValueError("Strategy not yet implemented!")

            strategy_builder = strategy_mapping[strategy_config.type]

            new_strategy = strategy_builder()

            custom_strategy.add_strategy(new_strategy)

    except Exception as e:
        raise e
