import yfinance as yf
import pandas as pd
import numpy as np


stock = yf.Ticker("AAPL")

history = stock.history(period="15d")["Close"]

print(history)

print(history.diff())
