from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
import logging
from models import BacktestRequest


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


@app.get("/strategy")
async def root(body: BacktestRequest):
    logger.info("Hello from the main api route!")
    return {
        "message": f"Welcome to the backtesting engine!",
    }


if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
