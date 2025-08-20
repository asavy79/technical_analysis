from pydantic import BaseModel
from typing import List, Literal


class StrategyConfig(BaseModel):
    type: Literal["moving_average_cross",
                  "rsi_extremes", "rsi_cross", "macd_cross"]
    params: dict


class BacktestRequest(BaseModel):
    ticker: str
    period: str
    initial_capital: str
    strategies: List[StrategyConfig]
    mode: str
