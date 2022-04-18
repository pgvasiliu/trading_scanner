#!/usr/bin/env python

import talib
import yfinance as yf

import numpy
import math

import warnings
warnings.filterwarnings("ignore")

#import bisect

import pandas

import datetime


def TEMA ( df, t=30 ):
    ema1 = df['Close'].ewm(span = t ,adjust = False).mean()
    ema2 = ema1.ewm(span = t ,adjust = False).mean()
    ema3 = ema2.ewm(span = t ,adjust = False).mean()

    #stock[f'TEMA{span}'] = (3*ema1)-(3*ema2) + ema3
    return (3*ema1)-(3*ema2) + ema3



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


##################
#####  TEMA  #####
##################
print ("\nTEMA")

data["TEMA_30"]  = talib.TEMA( _close, 30 )
data['TEMA_301'] = TEMA ( data, 30 )

print (data.tail() )

#print ( data["TEMA_30"][-1])
#print ( TEMA ( data['TEMA_30', 30) )





