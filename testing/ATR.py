#!/usr/bin/env python

import talib
import yfinance as yf

import numpy as np
import math

import warnings
warnings.filterwarnings("ignore")

#import bisect

import pandas as pd

import datetime

import talib

# https://stackoverflow.com/questions/40256338/calculating-average-true-range-atr-on-ohlc-data-with-python
def wwma(values, n):
    """
     J. Welles Wilder's EMA
    """
    return values.ewm(alpha=1/n, adjust=False).mean()

def ATR (df, n=14):
    data = df.copy()
    high = data['High']
    low = data['Low']
    close = data['Close']
    data['tr0'] = abs(high - low)
    data['tr1'] = abs(high - close.shift())
    data['tr2'] = abs(low - close.shift())
    tr = data[['tr0', 'tr1', 'tr2']].max(axis=1)
    atr = wwma(tr, n)
    return atr

ticker = 'SLB'

#data = yf.download(ticker, period='1y', interval='1d')
#data = data.dropna()

ticker = yf.Ticker( ticker )
start = (datetime.datetime.now()-datetime.timedelta(days=365)).strftime('%Y-%m-%d')
data = ticker.history(start=start)



_open  = data['Open']
_close = data['Close']
_high  = data['High']
_low   = data['Low']


#################
#####  ATR  #####
#################
print ("\nATR")
data["ATR_14"] = talib.ATR(data['High'], data['Low'], data['Close'], 14)
#print ( data["ATR_14"][-1])
#print ( calculate_ATR ( data ) )

data['ATR_144'] = ATR ( data, 14 )

print (data.tail() )






