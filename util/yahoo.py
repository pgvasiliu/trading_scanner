import yfinance as yf
import pandas as pd

def download_yahoo ( symbol ):

    # Yahoo fix for '.' 

    symbol = symbol.replace ( '.', '-' )

    ticker = yf.Ticker( symbol )

    hist = ticker.history(period='1y', interval='1d')

    return pd.DataFrame(hist)

    #import yfinance as yf
    #import datetime

    #ticker = yf.Ticker( symbol )
    #start = (datetime.datetime.now()-datetime.timedelta(days=365)).strftime('%Y-%m-%d')
    #df = ticker.history(start=start)
    #df = df.rename(columns={'Date':'date','Open':'open','High':'high','Low':'low','Close':'close','Volume':'volume','Dividends':'dividends' , 'Stock Splits':'splits'})
    #df['turnover'] = 0
    #return df

#print ( download_yahoo ( 'BRK.B' ) )
