#!/usr/bin/env python

import talib
import yfinance as yf

import numpy as np
import math

import warnings
warnings.filterwarnings("ignore")

import bisect

import pandas as pd

import datetime


def RSI (data, time_window):
    # Function to compute the RSI or Relative Strength Index for a stock. 
    # Attempts to give a person an indication if a particular stock is over- or under-sold

    diff = data.diff(1).dropna()
    # diff in one field(one day)
    #this preservers dimensions off diff values
    up_chg = 0 * diff
    down_chg = 0 * diff

    # up change is equal to the positive difference, otherwise equal to zero
    up_chg[diff > 0] = diff[ diff>0 ]

    # down change is equal to negative deifference, otherwise equal to zero
    down_chg[diff < 0] = diff[ diff < 0 ]

    # check pandas documentation for ewm
    # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.ewm.html
    # values are related to exponential decay
    # we set com=time_window-1 so we get decay alpha=1/time_window
    up_chg_avg   = up_chg.ewm(com=time_window-1 , min_periods=time_window).mean()
    down_chg_avg = down_chg.ewm(com=time_window-1 , min_periods=time_window).mean()

    rsi = 100 - 100 / (1 + abs(up_chg_avg/down_chg_avg))

    return rsi



ticker = 'SLB'

ticker = yf.Ticker( ticker )
start = (datetime.datetime.now()-datetime.timedelta(days=365)).strftime('%Y-%m-%d')
data = ticker.history(start=start)


#_open  = data['Open']
_close = data['Close']
#_high  = data['High']
#_low   = data['Low']


#################
#####  RSI  #####
#################
print ( "RSI" )
data["RSI_14"] = talib.RSI(_close, timeperiod=14)
data["RSI_144"] = RSI ( _close, 14 )
#print ( data["RSI_14"][-1])
#print ( computeRSI ( _close, 14 )[-1] )


print (data.tail() )






