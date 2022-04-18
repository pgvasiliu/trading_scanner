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


def EMA ( df, t=9 ):
    ema = df['Close'].ewm(span = t ,adjust = False).mean()
    return ( ema )



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
#####  EMA  #####
#################
print ("\nEMA")

data["EMA_9"]  = talib.EMA( _close, 9 )
data['EMA_91'] = EMA ( data, 9 )

print (data.tail() )

#print ( data["TEMA_30"][-1])
#print ( TEMA ( data['TEMA_30', 30) )





