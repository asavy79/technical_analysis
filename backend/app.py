from fastapi import FastAPI, HTTPException
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
import logging
from backend.models import BacktestRequest
from backend.run import run_backtest
from backend.strategy_config import available_strategies


app = FastAPI()


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/backtest")
async def root(body: BacktestRequest):
    logger.info(
        f"Running backtest for {body.ticker} with {body.strategies} strategies")

    try:
        results = run_backtest(body)
        return results
    except Exception as e:
        logger.error(f"Error running backtest: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/strategies")
async def get_strategies():
    return available_strategies


if __name__ == "__main__":
    uvicorn.run("backend.app:app", host="0.0.0.0", port=8000, reload=True)
