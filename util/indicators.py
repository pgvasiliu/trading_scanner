#################
#####  SMA  #####
#################

#def SMA ( close, t ):
#    import talib
#    return talib.SMA( close, t)

# https://github.com/Priyanshu154/Backtest/blob/511e2e8525b23a14ecdf5a48c28399c7fd41eb14/Backtest/Backtest/Indicator.py
#SMA starts here
def SMA(close, t):
    mas = []
    for i in range(t - 1):
        mas.append(-1)
    for i in range(len(close) - t + 1):
        summ = 0
        for j in range(i, t + i):
            summ = summ + close[j]
        meann = summ / t
        mas.append(meann)
    return mas
#SMA Ends here


#########################
#####  WILLIAMS %R  #####
#########################
#def WILLR ( high, low, close, t=14):
#    import talib
#    return  talib.WILLR ( h, l, c, t)

#def WILLR( data, t=14):
#  return talib.WILLR ( data['High'], data['Low'], data['Close'], timeperiod=t)


def WILLR (high, low, close, t):
    import pandas
    import numpy
    import math
    highh = high.rolling(t).max()
    lowl = low.rolling(t).min()
    wr = -100 * ((highh - close) / (highh - lowl))
    return wr


#William %R Starts Ahi Thi
#def WILLR(source,t,high,low):
#    W_R=[]
#    for i in range(0,t-1):
#        W_R.append(-1)
#
#    # hh is highest high
#    #ll is lowest low
#    hh=Rsi_high(high,t)
#    ll=Rsi_low(low,t)
#
#    for i in range(t-1,len(source)):
#        x=source[i]-hh[i]
#        y=hh[i]-ll[i]
#        z=x/y
#        z=z*(100)
#        W_R.append(z)
#
#    return W_R
#William %R Ends Here

#################
#####  WMA  #####
#################
#def wma(src, length):
#    return talib.WMA(src, length)

# https://github.com/Priyanshu154/Backtest/blob/511e2e8525b23a14ecdf5a48c28399c7fd41eb14/Backtest/Backtest/Indicator.py
# Weighted Moving Average(WMA) Starts Here
# Reference for code is taken from tradingview
def WMA(close, t):
    wma = []
    for i in range(t - 1):
        wma.append(-1)
    for i in range(t-1, len(close)):
        norm = 0.0
        summ = 0.0
        for j in range(0, t):
            weight = (t-j)*t
            norm = norm + weight
            summ = summ + (close[i-j]*weight)
        wma.append(summ/norm)
    return wma
# WMA Ends Here


##################
#####  TEMA  #####
##################
#def TEMA ( close, t):
#    import talib
#    return talib.TEMA(close, timeperiod=t)
#def double_ema(close, t):
#    import numpy as np
#    ema_val = ema(close, t)
#    return 2 * ema_val - ema(ema_val, t)

#def TEMA ( close, t ):
#    import numpy as np
#    ema_val = EMA (close, t)
#    return 3 * (ema_val - EMA ( ema_val, t)) + EMA( EMA( ema_val, t), t)

def TEMA ( df, t=30 ):
    ema1 = df['Close'].ewm(span = t ,adjust = False).mean()
    ema2 = ema1.ewm(span = t ,adjust = False).mean()
    ema3 = ema2.ewm(span = t ,adjust = False).mean()

    #stock[f'TEMA{span}'] = (3*ema1)-(3*ema2) + ema3
    return (3*ema1)-(3*ema2) + ema3


#################
#####  CCI  #####
#################
#def CCI ( data, t=20):
#  return talib.CCI ( data['High'], data['Low'], data['Close'], timeperiod=t)

## fisher inverse CCI
#def cci(high, low, close):
#    real = talib.CCI(numpy.asarray(high),numpy.asarray(low),numpy.asarray(close),timeperiod=20)
#    v1 = 0.1*(real/4)
#    v2 = talib.WMA(v1,timeperiod=9)
#    INV = []
#    for x in v2:
#        INV.append((math.exp(2*x)-1)/(math.exp(2*x)+1))
#    cciBuy = INV[-2] < -0.75 and INV[-1] >= -0.75
#    cciSell =INV[-1] <= 0.50
#    return cciBuy,cciSell,INV[-1]


#################
#####  RSI  #####
#################
#def RSI ( close, t ):
#    import talib
#    return talib.RSI ( close, timeperiod=t)

# https://github.com/Priyanshu154/Backtest/blob/511e2e8525b23a14ecdf5a48c28399c7fd41eb14/Backtest/Backtest/Indicator.py
# RSI starts
def RSI(close, t):
    n = len(close)
    rsi = []
    Ups = 0.0
    Downs = 0.0
    for j in range(t-1):
        rsi.append(-1)
    #Ye sabse pehla avgU/avgD find karne ke liye simple average vala step
    for i in range(1,t):
        diff = close[i] - close[i-1]
        if(diff > 0):
            Ups += diff
        else:
            Downs += (-diff)

    preU = Ups/t
    preD = Downs/t
    #simple average mil gaya to hamara pehla rsi bi mil gaya
    rs = preU/preD
    rsi.append( (100 - (100/(1+rs))) )
    #yaha se prev_avgUp vala loop
    Ups = 0.0
    Downs = 0.0
    for i in range(t,n):
        diff = close[i] - close[i-1]
        if(diff > 0):
            Ups = diff
            Downs = 0.0
        else:
            Downs = (-diff)
            Ups = 0.0
        u = (1/t)*Ups + ((t-1)/t)*preU
        d = (1/t)*Downs + ((t-1)/t)*preD
        preU = u    #Update previous-Up and previous-Down
        preD = d
        rs = u/d
        rsi.append( (100 - (100/(1+rs))) )   #RSI for a particular date
    return rsi
#RSI Ends Here

##print ( RSI ( _close, 14 )[-1] )
#def RSI (data, time_window):
#    # Function to compute the RSI or Relative Strength Index for a stock. 
#    # Attempts to give a person an indication if a particular stock is over- or under-sold
#
#    diff = data.diff(1).dropna()
#    # diff in one field(one day)
#    #this preservers dimensions off diff values
#    up_chg = 0 * diff
#    down_chg = 0 * diff
#
#    # up change is equal to the positive difference, otherwise equal to zero
#    up_chg[diff > 0] = diff[ diff>0 ]
#
#    # down change is equal to negative deifference, otherwise equal to zero
#    down_chg[diff < 0] = diff[ diff < 0 ]
#
#    # check pandas documentation for ewm
#    # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.ewm.html
#    # values are related to exponential decay
#    # we set com=time_window-1 so we get decay alpha=1/time_window
#    up_chg_avg   = up_chg.ewm(com=time_window-1 , min_periods=time_window).mean()
#    down_chg_avg = down_chg.ewm(com=time_window-1 , min_periods=time_window).mean()
#
#    rsi = 100 - 100 / (1 + abs(up_chg_avg/down_chg_avg))
#
#    return rsi



#################
#####  RMA  #####
#################
# Rolling Moving Average(RMA) Starts here
def RMA(close, t):
    rma = []
    sma = SMA(close, t)
    for i in range(t):
        rma.append(sma[i])
    for i in range(t, len(close)):
        rma.append( (rma[i-1]*(t-1) + close[i])/t )
    return rma
# RMA Ends here


#################
#####  EMA  #####
#################
#def EMA(close, t):
#    import numpy as np
#    return talib.EMA ( np.array(close), t)

def EMA ( df, t=9 ):
    ema = df['Close'].ewm(span = t ,adjust = False).mean()
    return ( ema )


##EMA Starts Here
#def EMA(close, t):
#    sma= 0.0
#    n = len(close)
#    for i in range(t):
#        sma += close[i]
#    sma = sma/(t)
#    ema = []
#    for j in range(t-1):
#        ema.append(-1)
#    ema.append(sma)
#    m = 2/(t+1)
#    for i in range(t,n):
#        e = close[i]*m + ema[i-1]*(1-m)
#        ema.append(e)
#    return ema
##EMA ends here

# Rate Of Change(ROC) Starts here
#def ROC ( data, t=10):
#  return talib.ROC ( data['Close'], timeperiod=t)

def ROC(close, t):
    roc = []
    for i in range(t-1):
        roc.append(-1)
    for i in range(t-1, len(close)):
        sum = 100*(close[i]-close[i-t])/close[i-t]
        roc.append(sum)
    return roc
# ROC Ends here


##################
#####  MACD  #####
##################

#def MACD(df, fastperiod=12, slowperiod=26, signalperiod=9):
#  return talib.MACD(df.close, fastperiod=fastperiod, slowperiod=slowperiod, signalperiod=signalperiod)[0]

#MACD Starts From Here
#def EMA_d(close, t):
#    sma = 0.0
#    n = len(close)
#    for i in range(t):
#        sma += close[i]
#    sma = sma / (t)
#    ema = []
#    ema.append(sma)
#    m = 2 / (t + 1)
#    for i in range(t, n):
#        e = close[i] * m + ema[i - t] * (1 - m)
#        ema.append(e)
#    return ema
#
#
#def EMA_MACD(t, macd):
#    sma = 0.0
#    n = len(macd)
#    for i in range(t):
#        sma += macd[i]
#    sma = sma / (t)
#    ema = []
#    ema.append(sma)
#    m = 2 / (t + 1)
#    for i in range(t, n):
#        e = macd[i] * m + ema[i - t] * (1 - m)
#        ema.append(e)
#    return ema
#
#
#def MACD(close,x, y, z):
#    val_pr = EMA_d(close, x)
#    val2_pr = EMA_d(close, y)
#    val = []
#    val2 = []
#    for i in range(x - 1):
#        val.append(0)
#    for i in range(y - 1):
#        val2.append(0)
#
#    for i in range(len(val_pr)):
#        val.append(val_pr[i])
#    for i in range(len(val2_pr)):
#        val2.append(val2_pr[i])
#
#    macd_line = []
#    macd_histogram = []
#    signal_line = []
#
#    for i in range(len(val)):
#        macd_line.append(val[i] - val2[i])
#
#    for i in range(z - 1):
#        signal_line.append(0)
#
#    signal_line_pr = EMA_MACD(z, macd_line)
#
#    for i in range(len(signal_line_pr)):
#        signal_line.append(signal_line_pr[i])
#
#    for i in range(len(val)):
#        macd_histogram.append(macd_line[i] - signal_line[i])
#
#    return macd_line, signal_line, macd_histogram
#
# macd_line, signal_line, macd_histogram = MACD(close, 12, 26, 9)
#MACD Ends Here
#
####################
#####  BBANDS  #####
####################
#def BBANDS(df, t=5, nbdevup=2, nbdevdn=2, matype=0):
#  return talib.BBANDS(df.close, timeperiod=t, nbdevup=nbdevup, nbdevdn=nbdevdn, matype=matype)
#
##Bollinger Band Starts Here
#def bollinger_band(close,n,r):
#    up = []
#    lo = []
#    ma = []
#    for i in range(n-1):
#        up.append(0)
#        lo.append(0)
#        ma.append(0)
#    for i in range(len(close)-n+1):
#        sum = 0
#        sqr = 0
#        for j in range(i, n+i):
#            sum = sum + close[j]
#        meann = sum/n
#        ma.append(sum / n)
#        for z in range(i, n+i):
#            sq = close[z]-meann
#            sqr = sqr + (sq*sq)
#        varr = sqr/n
#        std = math.sqrt(varr)
#        up.append(meann + (r*std))
#        lo.append(meann - (r*std))
#    return up,lo,ma
#
##Bollinger Band Ends here
#
#
#
#
#
##Money Flow Index starts here
#def MFI(high,low,close,volume,t):
#    mfi = []        #money flow index
#    typ = []        #typical price
#    raw_money = []  #raw money flow
#    mfr = []        #money flow ratio
#    for i in range(t):
#        mfi.append(-1)
#        mfr.append(-1)
#    ind = 1
#    typ.append( (high[0] + low[0] + close[0]) / 3)
#    raw_money.append(typ[0]*volume[0])  #first time assume it is positive
#
#    for i in range(1,len(close)):
#        typ.append( (high[i] + low[i] + close[i])/3 )
#        if(typ[ind] > typ[ind-1]):
#            raw_money.append( typ[i]*volume[i]  )
#        else:
#            raw_money.append( -typ[i]*volume[i]  )
#        ind = ind + 1
#    for i in range(t, len(close)):
#        positive_flows = 0.0
#        negative_flows = 0.0
#        for j in range(t):
#            if(raw_money[i-j] > 0):
#                positive_flows += raw_money[i-j]
#            else:
#                negative_flows += -raw_money[i-j]
#        if(negative_flows != 0):        ratio = positive_flows/negative_flows
#        else:                           ratio = positive_flows
#        mfr.append( ratio )
#        mfi.append( (100- (100/(1+ratio)) ) )
#    return mfi
##Money Flow Index ends here
#
#
#
## Stochastic Rsi Starts ahi thi
#def Rsi_high(high, t):
#
#   rsi_H = []
#   for i in range(0,t-1):
#        rsi_H.append(-1)
#
#
#   i = 0
#   for j in range(t, len(high)+1):
#        HIGH = high[i:t]
#        rsi_H.append(max(HIGH))
#        t += 1
#        i += 1
#
#   return rsi_H
#
#
#
#def Rsi_low(low, t):
#
#   rsi_L = []
#   for i in range(0,t-1):
#        rsi_L.append(-1)
#
#   i = 0
#
#   for j in range(t, len(low) + 1):
#        if low!=-1:
#            LOW = low[i:t]
#            rsi_L.append(min(LOW))
#            t += 1
#            i += 1
#
#   return rsi_L


###################
#####  STOCH  #####
###################

#def STOCH(df, fastk_period=5, slowk_period=3, slowd_period=3, slowk_matype=0, slowd_matype=0):
#  return talib.STOCH(df.high, df.low, df.close, fastk_period=fastk_period, slowk_period=slowk_period, slowk_matype=slowk_matype, slowd_period=slowd_period, slowd_matype=slowd_matype)

#def get_stochastic_oscillator(close_price, low_price, high_price, period=3):
#    """
#    Reference: https://www.investopedia.com/terms/s/stochasticoscillator.asp
#    """
#
#    _close = data['Close']
#    _low   = data['Low']
#    _high  = data['High']
#    sok = ((close - _low.rolling(14).min()) / ( _high.rolling(14).max() - _low.rolling(14).min())) * 100
#    sod = sok.rolling(period).mean()
#
#    return sok, sod


#def stoch(source, high, low, t,rt,close):
#    rsi_high = []
#    rsi_low = []
#
#    rsi_low = Rsi_low(high, t)
#    rsi_high = Rsi_high(low, t)
#
#    count=0
#    for x in rsi_low:
#        if(x==-1):
#            count+=1
#
#    Stochastic=[]
#    for i in range(0,count):
#        Stochastic.append(-1)
#
#    cnt=0
#    rsi=RSI(close,rt)
#    for i in range(count,(len(source))):
#        y=(rsi[i]-rsi_low[i])
#        z=(rsi_high[i]-rsi_low[i])
#        w=y/z
#        Stochastic.append(w*100)
#        cnt+=1
#
#
#    return Stochastic,count
#
#def sma(rsi,t,count):
#    x=[]
#    cnt=0
#    for i in range(0,count):
#        x.append(-1)
#        cnt+=1
#    for i in range(t-1):
#        x.append(-1)
#        cnt += 1
#
#    cnt+=1
#    cnt1=cnt
#
#    for i in range(cnt,len(rsi)+1):
#        temp=rsi[cnt1-t:cnt1]
#        sum=0.0000
#        for j in temp:
#            sum=sum+j
#
#        sum=sum/t
#        cnt1+=1
#        del temp
#        x.append(sum)
#
#
#    return x
#
#
#def S_RSI(close, t, K, D, rt):
#    # rt=rsi peroid
#    # t=Stochastic Rsi Period
#    # K=main line
#    # D= moving average of K
#
#    rsi =RSI(close, rt)
#    Stochstic,count=stoch(rsi, rsi, rsi,t,rt,close)
#    k = sma(Stochstic,K,count)
#    d = sma(k,D,count)
#
#    return k,d
#
#    #k= blue line on trading view
#    #d= orange line on trading view
#
## Stochastic Rsi Ends Here
#
##Ichimoku Cloud Starts ahi thi
#
#def IC_high(high,t):
#
#    ic_high = []
#    for i in range(0,t-1):
#        ic_high.append(-1)
#
#    i = 0
#    for j in range(t, len(high)+1):
#        HIGH = high[i:t]
#        ic_high.append(max(HIGH))
#        t += 1
#        i += 1
#
#    return ic_high
#
#def IC_low(low,t):
#
#    ic_low = []
#    for i in range(0,t-1):
#        ic_low.append(-1)
#
#    i = 0
#    for j in range(t, len(low)+1):
#        LOW= low[i:t]
#        ic_low.append(min(LOW))
#        t += 1
#        i += 1
#
#    return ic_low
#
#def average(ic_high,ic_low,high):
#    cnt=0
#    cnt1=0
#    cnt2=0
#    avg=[]
#    for i in ic_high:
#        if i == -1:
#            cnt1=cnt1+1
#
#    for i in ic_low:
#        if i == -1:
#            cnt2=cnt2+1
#
#    if cnt2>cnt1:
#        cnt=cnt2
#    else:
#        cnt=cnt1
#
#    for i in range(0,cnt):
#        avg.append(-1)
#
#    for i in range (cnt,len(high)):
#        avg.append((ic_high[i]+ic_low[i])/2)
#
#    return avg
#
#def lag(close,time):
#    lag1=[]
#
#    for i in close:
#        lag1.append(i)
#
#    return lag1
#
#def Icloud(high,low,close,c_period,b_period,span_b_period,lag_span_period):
#
#    #c_line is conversion line also known as Tenken-san
#    #b_line is base line also known as kijun-san
#    #other all are time peroids
#
#    c_high=IC_high(high,c_period)
#    c_low=IC_low(low,c_period)
#    conversion_line=average(c_high,c_low,high)
#
#    b_high=IC_high(high,b_period)
#    b_low=IC_low(low,b_period)
#    base_line=average(b_high,b_low,high)
#
#    span_a=average(conversion_line,base_line,high)
#
#    span_b_high = IC_high(high,span_b_period)
#    span_b_low = IC_low(low,span_b_period)
#    span_b= average(span_b_high,span_b_low,high)
#
#    lag_span=lag(close,lag_span_period)
#
#    return conversion_line,base_line,span_a,span_b,lag_span
#    #the last array of all values is matching with last value on trading view.
#
#Ichimoku Cloud Ends Here


#################
#####  ATR  #####
#################

#def ATR ( _high, _low, _close, t=14 ):
#    import talib
#
#    return talib.ATR(_high, _low, _close, timeperiod=t)

# https://stackoverflow.com/questions/40256338/calculating-average-true-range-atr-on-ohlc-data-with-python
def wwma(values, n):
    """
     J. Welles Wilder's EMA
    """
    return values.ewm(alpha=1/n, adjust=False).mean()

# https://stackoverflow.com/questions/40256338/calculating-average-true-range-atr-on-ohlc-data-with-python
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

##ATR Starts Ahi Thi
#def tr(high,low,close):
#    X=[]
#    Y=[-1]
#    Z=[-1]
#    TR=[-1]
#    for i in range(len(low)):
#        X.append(high[i]-low[i])
#
#    for i in range(1,len(high)):
#        Y.append(abs(high[i]-close[i-1]))
#
#    for i in range(1,len(low)):
#        Z.append(abs(low[i]-close[i-1]))
#
#    for i in range(1,len(low)):
#        TR.append(max(X[i],Y[i],Z[i]))
#
#    return TR

#def ATR( source, high, low, close, t):
##Source Might be EITHER EMA,RMA,SMA OR WMA.
##At the moment WMA & RMA isn't added so it will return None
##T Is Time Period
##take source as a string
#
#    TR=tr()
#
#    source=source.upper()
#
#    if source=="EMA":
#        ema=EMA(TR,t)
#    elif source == "RMA":
#        rma=RMA(TR,t)
#    elif source == "WMA":
#        wma=WMA(TR,t)
#    else:
#        sma=SMA(TR,t)
#
#    #for returning
#    if source=="EMA":
#        return ema
#    elif source == "RMA":
#        return rma
#    elif source == "WMA":
#        return wma
#    else:
#        return sma
#
##ATR Ends Here


########################
#####  ATR  BANDS  #####
########################
def ATR_bands ( data, t=14 ):

    import talib

    _open  = data['Open']
    _close = data['Close']
    _high  = data['High']
    _low   = data['Low']

    #atr = talib.ATR(_high, _low, _close, t)
    atr = ATR( data, t)

    atr_multiplicator = 2.0
    atr_basis = talib.EMA ( _close, 20)

    atr_band_upper = atr_basis + atr_multiplicator * atr
    atr_band_lower = atr_basis - atr_multiplicator * atr

    return atr_band_lower[-1], atr_band_upper[-1]


##Super Trend Starts Ahi Thi
##tx3 uses rma in atr & super trend uses atr so if you want to check use rma in atr in tx3
#def ST(s_atr,t_atr,mul,high,low,close):
#    #s_atr Is Source for ATR & t_atr is Time Period For ATR
#    #mul is multiplier
#    up=[]
#    down=[]
#    f_down=[]
#    f_up=[]
#    st=[]
#    cnt=0
#    atr=ATR(s_atr,t_atr)
#    for i in range(0,t_atr-1):
#        up.append(-1)
#        f_up.append(-1)
#        down.append(-1)
#        f_down.append(-1)
#        st.append(-1)
#        cnt+=1
#    for i in range(cnt,len(high)):
#       x=high[i]
#       y=low[i]
#       z=(x+y)/2
#       w=atr[i]*mul
#       up.append(z+w)
#       down.append(z-w)
#    for i in range(cnt,len(close)):
#
#        if (i!=len(close)):
#            if ( (up[i] < f_up[i-1]) or (close[i-1] > f_up[i-1])):
#                f_up.append(up[i])
#            else:
#                f_up.append(f_up[i-1])
#
#            if ( (down[i]>f_down[i-1]) or (close[i-1]<f_down[i-1])):
#                f_down.append(down[i])
#            else:
#                f_down.append(f_down[i-1])
#
#    for i in range(cnt,len(high)):
#
#        if ((st[i-1]==f_up[i-1]) and (close[i]<f_up[i])):
#            st.append(f_up[i])
#        elif((st[i-1]==f_up[i-1]) and (close[i]>f_up[i])):
#            st.append(f_down[i])
#        elif((st[i-1]==f_down[i-1]) and (close[i]>f_down[i])):
#            st.append(f_down[i])
#        elif((st[i-1]==f_down[i-1]) and (close[i]<f_down[i])):
#            st.append(f_up[i])
#
#    return st
##Super Trend Ends Here():


##ADX Starts Ahi Thi
#def changeh(high):
#    h=[-1]
#    for i in range(1,len(high)):
#        h.append(high[i]-high[i-1])
#
#    return h
#
#def changel(low):
#    l=[-1]
#    for i in range(1,len(low)):
#        l.append(low[i-1]-low[i])
#
#    return l
#
#def ADX(adx_t,di_t,high,low,close):
#
#    plus_di=[-1]
#    minus_di=[-1]
#    s_plus=[]
#    s_minus=[]
#    plus=[]
#    minus=[]
#    sum=[]
#    dx=[]
#    adx=[]
#
#    h=changeh(high)
#    l=changel(low)
#    atr=ATR("rma",di_t)
#
#    for i in range(1,len(close)):
#        if( (h[i]>l[i]) and (h[i]>0) ):
#            plus_di.append(h[i])
#        else:
#            plus_di.append(0)
#
#    for i in range(1,len(close)):
#        if( (l[i]>h[i]) and (l[i]>0) ):
#            minus_di.append(l[i])
#        else:
#            minus_di.append(0)
#
#
#    s_plus=RMA(plus_di,di_t)
#    s_minus=RMA(minus_di,di_t)
#
#    for i in range(0,di_t):
#        plus.append(-1)
#        minus.append(-1)
#
#    for i in range(di_t,len(s_plus)):
#        x=100*s_plus[i]
#        x=x/atr[i]
#        plus.append(x)
#
#    for i in range(di_t,len(s_minus)):
#        x=100*s_minus[i]
#        x=x/atr[i]
#        minus.append(x)
#
#    for i in range(0,di_t):
#        sum.append(-1)
#        dx.append(-1)
#
#    for i in range(di_t,len(plus)):
#        sum.append(plus[i]+minus[i])
#
#    for i in range(di_t,len(sum)):
#        y=abs(plus[i]-minus[i])
#        y=y/sum[i]
#        y=y*100
#        dx.append(y)
#
#    adx=RMA(dx,adx_t)
#
#    return adx
##ADX Ends Here


#################
#####  MOM  #####
#################
#def MOM ( data, n):
#    return data['Close'] / data['Close'].shift(n) - 1


