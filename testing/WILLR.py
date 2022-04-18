#!/usr/bin/env python

import talib as ta
import yfinance as yf

import numpy as np
import math

import warnings
warnings.filterwarnings("ignore")

#import bisect

import pandas

import datetime


def WILLR (high, low, close, lookback):
    highh = high.rolling(lookback).max()
    lowl = low.rolling(lookback).min()
    wr = -100 * ((highh - close) / (highh - lowl))
    return wr


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


###################
#####  WILLR  #####
###################
print ("\nWILLR")

#data["WILLR_14"]  = talib.EMA( _close, 9 )
data['WILLR_14']  =ta.WILLR(np.array(data['High']),np.array(data['Low']), np.array(data['Close']), timeperiod=14)
data['WILLR_141'] = WILLR ( data['High'], data['Low'], data['Close'], 14 )

print (data.tail() )

#print ( data["TEMA_30"][-1])
#print ( TEMA ( data['TEMA_30', 30) )





