################################
#####  SUPPORT/RESISTANCE  #####
################################

import pandas as pd
import numpy as np
import math

import matplotlib.dates as mpl_dates

import yfinance as yf


def isSupport(df,i):
    support = df['Low'][i] < df['Low'][i-1]  and df['Low'][i] < df['Low'][i+1] and df['Low'][i+1] < df['Low'][i+2] and df['Low'][i-1] < df['Low'][i-2]
    return support

def isResistance(df,i):
    resistance = df['High'][i] > df['High'][i-1]  and df['High'][i] > df['High'][i+1] and df['High'][i+1] > df['High'][i+2] and df['High'][i-1] > df['High'][i-2]
    return resistance

def sr ( name ):
    mylist = []

    def isFarFromLevel(l):
        return np.sum([abs(l-x) < s  for x in levels]) == 0


    import datetime as dt
    start = (dt.datetime.now()-dt.timedelta(days=365)).strftime('%Y-%m-%d')

    ticker = yf.Ticker(name)
    df = ticker.history(interval="1d", start=start)

    df['Date'] = pd.to_datetime(df.index)
    df['Date'] = df['Date'].apply(mpl_dates.date2num)
    df = df.loc[:,['Date', 'Open', 'High', 'Low', 'Close']]

    s =  np.mean(df['High'] - df['Low'])

    levels = []
    for i in range(2,df.shape[0]-2):
        if isSupport(df,i):
            l = df['Low'][i]

            if isFarFromLevel(l):
                levels.append((i,l))

        elif isResistance(df,i):
            l = df['High'][i]

            if isFarFromLevel(l):
                levels.append((i,l))

    for a, b in levels:
        b = "%.2f" % b 
        mylist.append ( b )
    sorted_float = sorted( mylist, key = lambda x:float(x))

    return sorted_float
