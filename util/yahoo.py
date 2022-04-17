import yfinance as yf
import pandas as pd

def download_yahoo ( symbol ):
    ticker = yf.Ticker( symbol )

    hist = ticker.history(period='1y', interval='1d')

    return pd.DataFrame(hist)


