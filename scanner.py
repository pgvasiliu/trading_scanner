#!/usr/bin/env python

import argparse
import json
import math
import os
from   os.path import expanduser

import sys
sys.path.insert(0, './util')

import time
import warnings
warnings.filterwarnings("ignore")


from datetime import datetime, timedelta

from tradingview_ta import TA_Handler, Interval, Exchange


##############################
#####  local filesystem  #####
##############################
from util.upgrade      import get_analysts_upgrades_downgrades_marketwatch
from util.tradingview  import taJson
from util.support      import isSupport, isResistance, sr

from util.indicators   import SMA, WILLR, WMA, TEMA, RSI, RMA, EMA, ROC, wwma, ATR, ATR_bands

from util.yahoo        import download_yahoo
from util.fibonacci    import fib_retracement, fib


class txcolors:
    NEUTRAL = '\033[95m'
    #OKBLUE = '\033[94m'
    #OKCYAN = '\033[96m'
    BUY = '\033[92m'
    #WARNING = '\033[93m'
    SELL = '\033[91m'
    ENDC = '\033[0m'
    #BOLD = '\033[1m'
    #UNDERLINE = '\033[4m'
    YELLOW = '\033[92m'

def colorme ( string ):
    out = ''
    if 'BUY' in string:
        out = '\033[92m' + string + '\033[0m'
        return out
    if ',Upgrades,' in string:
        out = '\033[92m' + string + '\033[0m'
        return out


    if 'SELL' in string:
        out = '\033[91m' + string + '\033[0m'
        return out
    return string
    if ',Downgrades,' in string:
        out = '\033[91m' + string + '\033[0m'
        return out


#def calculate_rsi(p):
#    if (p < 20 ):
#        r = "RSI_ExtremelyOversold"
#    elif (p >= 20 and p <= 30):
#        r = "RSI_Oversold"
#    elif (p > 30 and p <= 45):
#        r = "RSI_ApproachingOversold"
#    elif (p > 45 and p <= 55):
#        r = "RSI_Neutral"
#    elif (p > 55 and p <= 70):
#        r = "RSI_ApproachingOverbought"
#    elif (p > 70 and p <= 80):
#        r = "RSI_Overbought"
#    elif (p > 80):
#        r = "RSI_ExtremelyOverbought"
#    else :
#        r= "UNKNOWN"
#    return r

def main(x, upgrades):
    #keys = ['BUY','SELL','NEUTRAL']

    #Intervals = { Interval.INTERVAL_1_DAY,
    #              Interval.INTERVAL_4_HOURS,
    #              Interval.INTERVAL_1_HOUR,
    #              Interval.INTERVAL_15_MINUTES
    #            }

    #interval = Interval.INTERVAL_1_DAY

    buy_list, rsi_list, ema_list = ( [], [], [] )
    early_list = []


    #today    = datetime.today()
    today     = time.strftime("%Y-%m-%d")

    import datetime as dt
    yesterday = (dt.datetime.now()-dt.timedelta(days=1)).strftime('%Y-%m-%d')

    # if today is Monday, we should access Fri's data not Sunday's
    if (dt.datetime.today().strftime('%A').lower()) == "monday":
        yesterday = (dt.datetime.now()-dt.timedelta(days=3)).strftime('%Y-%m-%d')

    homedir = os.path.expanduser("~")
    lockfile = homedir + '/.s.lock'

#    if not os.path.exists(lockfile):
#        with open(lockfile, 'w'): pass
#    else:
#        print('[*] ERROR: lockfile %s exists, exiting' % ( lockfile ) )
#        sys.exit(1)

#    # Time diff between now() and lockfile mtime. If more than 15 min, delete the lockfile
#    stat = os.stat(lockfile)
#    lockfile_mtime = (stat.st_mtime)
#    timediff = time.time() - stat.st_mtime
#    #print (stat.st_mtime)
#    #print(time.time())
#    if timediff > 1500:
#        if os.path.exists(lockfile):
#            os.unlink (lockfile)


    #with open("config_settings.json") as f:
    #    config = json.load(f)
    #    for key, value in config.items():
    #        os.environ[key] = str(value)
    with open('config_settings.json') as json_file:
        config_settings = json.load(json_file)

    folder = config_settings['data_folder']

    tickers_exchange_json = {}



    # load the tickers json config file
    with open(x) as f:
        data = json.load(f)
        ticker_exchange = dict(sorted(data.items()))

        # loop through tickers
        for symbol, exchange in ticker_exchange.items():

            advice = []

            upgrade_downgrade = '['
            for i in upgrades:
                if i['ticker'] == symbol:
                    upgrade_downgrade += "%s,%s,%s " % ( i['date'], i['rating'], i['analyst'])

            upgrade_downgrade += ']'

            # create folders and subfolders
            ticker_folder = folder + '/' + symbol + '_' + exchange
            try:
                os.makedirs(ticker_folder + '/' + today, exist_ok=True)
                os.makedirs(ticker_folder + '/' + yesterday, exist_ok=True)
            except OSError as e:
                if errno.EEXIST != e.errno:
                    raise

            oscCheck = 0
            maCheck  = 0
            #trend    = 'UP'

            json_analysis      = taJson(symbol, exchange, Interval.INTERVAL_1_DAY)
            #json_analysis_15m  = taJson(symbol, exchange, Interval.INTERVAL_15_MINUTES)
            #json_analysis_1h   = taJson(symbol, exchange, Interval.INTERVAL_1_HOUR)


            # overall rating, oscillator and moving averages recommendation
            recommendation      = json_analysis.summary['RECOMMENDATION']
            osc_recommendation  = json_analysis.oscillators['RECOMMENDATION']
            mave_recommendation = json_analysis.moving_averages['RECOMMENDATION']


            # indicator names + values
            ind     = json_analysis.indicators
            #ind_15m = json_analysis_15m.indicators
            #ind_1h  = json_analysis_1h.indicators

            # oscilators names + values
            osc = json_analysis.oscillators


            # current price
            #currentPrice = round ( ind["close"], 2 )
            price        = ind['close']
            price_string = str ( price )

            _low    = ind['low']
            _high   = ind['high']
            _open   = ind['open']
            _close  = ind['close']
            _vol    = ind['volume']
            _change = ind['change']

            _change_2dec = f'{_change:.2f}'

            ticker_data =  { 'open': _open, 'low': _low, 'high': _high, 'close': _close, 'volume': _vol, 'change': _change }


            OSC_INDICATORS = [ 'W%R', 'CCI', 'MACD', 'RSI', 'Stoch.RSI' ]
            osc_line = 'OSC: '
            for indicator in OSC_INDICATORS:
                oscResult = osc['COMPUTE'][indicator]
                if 'NEUTRAL' not in oscResult:
                    #print(f'{symbol} - Indicator for {indicator} is {oscResult}')
                    osc_line += ' ' + indicator + ' ' + oscResult + ','
                    #if osc['COMPUTE'][indicator] != 'SELL': oscCheck +=1



            #####  indicators  #####
            _rsi  = ind["RSI"]
            _rsi1 = ind['RSI[1]']


            #print ( calculate_rsi ( rsi ))

            _stock_k  = ind['Stoch.K']
            _stock_d  = ind['Stoch.D']

            _stock_k1 = ind['Stoch.K[1]']
            _stock_d1 = ind['Stoch.D[1]']

            _macd_orange   = float(ind["MACD.macd"])    # MACD blue   line
            _macd_blue     = float(ind["MACD.signal"])  # MACD orange line

            _ema10  = ind['EMA10']
            _ema20  = ind['EMA20']
            _ema30  = ind['EMA30']
            _ema50  = ind['EMA50']
            _ema100 = ind['EMA100']
            _ema200 = ind['EMA200']

            _cci20  = ind['CCI20']
            _cci201 = ind['CCI20[1]']

            _psar   = ind['P.SAR']

            _wr     = ind['W.R']

            _mom    = ind['Mom']
            _mom1   = ind['Mom[1]']


            stock_diff = round(_stock_k - _stock_d,2)
            rsi_diff   = round( _rsi - _rsi1,2)


            ticker_data['_rsi'], ticker_data['_rsi1'] = ( _rsi, _rsi1 )
            ticker_data['_stock_k'], ticker_data['_stock_d'], ticker_data['_stock_k1'], ticker_data['_stock_d1'] = ( _stock_k, _stock_d, _stock_k1, _stock_d1 )

            ticker_data['_macd_blue'],ticker_data['_macd_orange']   = ( _macd_blue, _macd_orange )
            ticker_data['_cci20'], ticker_data['_cci201'] = ( _cci20, _cci201 )
            ticker_data['_ema10'], ticker_data['_ema20'], ticker_data['_ema30'], ticker_data['_ema50'], ticker_data['_ema100'], ticker_data['_ema200'] = ( _ema10, _ema20, _ema30, _ema50, _ema100, _ema200  )

            ticker_data['_psar'] = _psar
            ticker_data['_wr']   = _wr

            ticker_data['_mom'], ticker_data['_mom1'] = ( _mom, _mom1 )
            ticker_data['_mom'], ticker_data['_mom1'] = ( _mom, _mom1 )

            ticker_data['stock_diff'] = stock_diff
            ticker_data['rsi_diff']   = rsi_diff


            _ao, _ao1, _ao2                                              = ( ind['AO'], ind['AO[1]'], ind['AO[2]'] )
            ticker_data['_ao'], ticker_data['_ao1'], ticker_data['_ao2'] = ( _ao, _ao1, _ao2 )



            #####  save data for today  #####
            file_dest = ticker_folder + '/' + today + '/' + 'data.json'
            with open(file_dest, 'w') as filehandle:
                filehandle.write( json.dumps ( ticker_data, indent=4) + '\n')

            #PANDAS_PATH = ticker_folder + '/' + today + '/' + 'pandas.json'
            #if os.path.exists(PANDAS_PATH):
            #    with open(PANDAS_PATH) as f:
            #        hist = pd.read_json(PANDAS_PATH)
            #        #print (hist.tail(5))
            #        data = hist[["Close"]]
            #        data = data.rename(columns = {'Close':'Actual_Close'})
            #        data["Target"] = hist.rolling(2).apply(lambda x: x.iloc[1] > x.iloc[0])["Close"]
            #        # Shift stock prices forward one day, so we're predicting tomorrow's stock prices from today's prices.
            #        prev = hist.copy()
            #        prev = prev.shift(1)
            #        predictors = ["Close", "Volume", "Open", "High", "Low"]
            #        data = data.join(prev[predictors]).iloc[1:]
            #        print ( data.tail() )
            #
            #else:
            #    ti = yf.Ticker(symbol)
            #    hist = ti.history(period="3mo")
            #    hist.to_json(PANDAS_PATH)

            # Load yesterday's json data. TradingView API does not return yesterday's data for volume and W%R
            volume1       = 500
            _wr1          = 500
            _macd_blue1   = 500
            _macd_orange1 = 500

            _ema101       = 500
            _ema201       = 500


            ##########################
            #####  PANDAS  data  #####
            ##########################
            df            = download_yahoo ( symbol )

            #####################
            #####  TEMA 30  #####
            #####################
            df['TEMA_30'] = TEMA ( df, 30 )
            tema_30       = df['TEMA_30'][-1]
            tema_301      = df['TEMA_30'][-2]


            ##################
            #####  EMA 9 #####
            ##################
            df['EMA_9']   = EMA ( df, 9 )
            ema_9         = df['EMA_9'][-1]
            ema_91        = df['EMA_9'][-2]


            ####################
            #####  ATR 14  #####
            ####################
            df['ATR_14']  = ATR ( df, 14 )
            atr_14        = df['ATR_14'][-1]
            atr_141       = df['ATR_14'][-2]


            #################
            #####  W%R  #####
            #################
            df['WILLR_14'] = WILLR ( df['High'], df['Low'], df['Close'], 14 )
            #df['WILLR_14'] = WILLR ( df, 14 )
            willr_14       = df['WILLR_14'][-1]
            willr_141      = df['WILLR_14'][-2]


            #print ( df.tail() )

            ####################################
            #####  FIBONACCI  retracement  #####
            ####################################
            fibonacci     = fib ( symbol )


            ###################################
            #####  ATR bands ( Keltner )  #####
            ###################################
            atr_band_lower, atr_band_higher = ATR_bands ( df, 14 )




            #####  // TEMA 30 strategy // #####
            if ( price > tema_30 ) and ( price > ema_9 ) and ( ema_9 > tema_30):
                print ( "TEMA , EMA 9 BUY" )

            # Buy If price currently lower than MA substracts by ATR (with some multiplier)
            # To reduce the false signal, check the William %R value and should be on the oversold area and previously reach < -95
            if ( ema_9 - ( 2 * atr_14) > _open ) and ( wpr < -80) and ( willr_141 < -95 ) and ( _close > _open ):
                print ( "TV BUY" )

            # Sell If price currently higher than MA add by ATR (with some multiplier)
            # To reduce the false signal, check the William %R value and should be on the overbought area and previously reach > -5
            if ( ema_9 + ( 2 * atr_14) < _close ) and ( wpr > -20 ) and ( willr_141 > -5 ):
                print ( "TV SELL" )




            yesterdays_data = ticker_folder + '/' + yesterday + '/' + 'data.json'

            if (os.path.exists(yesterdays_data)) and (os.stat(yesterdays_data).st_size > 0):
                lastModified    = datetime.fromtimestamp(os.stat(yesterdays_data).st_mtime).strftime('%Y-%m-%d')
                #if (lastModified != yesterday):
                with open(yesterdays_data) as yesterdays_json:
                    old_data = json.load(yesterdays_json)


                    # grab yesterday's numbers
                    if 'volume' in old_data:
                        volume1        = old_data['volume']

                    if '_wr' in old_data:
                        _wr1           = old_data['_wr']

                    if '_macd_blue' in old_data:
                        _macd_blue1    = old_data['_macd_blue']

                    if '_macd_orange' in old_data:
                        _macd_orange1  = old_data['_macd_orange']

                    if '_ema10' in old_data:
                        _ema101        = old_data['_ema10']

                    if '_ema50' in old_data:
                        _ema51         = old_data['_ema50']

                    if '_ema20' in old_data:
                        _ema201        = old_data['_ema200']

                    if 'price' in old_data:
                        price1         = old_data['price']


            #######################
            #####  GOOD  BUY  #####
            #######################

            if ( _close > _open):
                if ( _cci20 > _cci201 ) and ( _cci20 > 100 ) and ( _cci201 <= 100 ):
                    #print ("BUY: [%s] GOOD ---> CCI20 cross to upper level " % symbol )
                    msg = "BUY: GOOD [CCI20 cross to upper level]"
                    advice.append ( msg )

            if ( _close > _open):
                if ( _wr1 != 500 ):
                    if ( _wr > _wr1 ) and ( _wr > -20 ) and ( _wr1 < -20 ):
                        #print ("BUY: [%s] GOOD ---> WR 14 cross to overbought " % symbol )
                        msg = "BUY: GOOD [WR 14 cross to overbought]"
                        advice.append ( msg )

            # MOM indicator: crossing above 0 from below
            if ( _mom1 < 0 ) and ( _mom > 0 ):
                advice.append ( "SELL: GOOD [Mom cross above 0]")

            # price > yesterday's price
            if ( _change > 0 ):

                # EMA
                #if ( price > _ema10 > _ema20 > _ema50 > _ema100 > _ema200):
                if ( price > _ema10 ):

                    # MACD (12,26,9)
                    #if ( _macd_orange > _macd_blue ):

                        # CCI (20) > 100
                        if ( _cci20 >= 100 ):

                            # WR,14 > -20
                            #if ( _wr1 < -20 )and ( _wr > -20 ):
                            if ( _wr >= -20 ):

                                # RSI between 35 and 67
                                if ( _rsi >= 35 ) and ( _rsi <= 67 ):
                                    #print ( "BUY: [%s] w/o stockastic" % symbol )
                                    msg = "BUY: [w/o stockastic]"
                                    advice.append ( msg )

                                    if ( _stock_k - _stock_d >= 4.5 ):
                                        #print ("BUY: [%s] w stockastic" % symbol )
                                        msg = "BUY: [w stockastic]"
                                        advice.append ( msg )

            ########################
            #####  EARLY  BUY  #####
            ########################
            # if yesterday < -80, and today crossing over > -80
            if ( _wr1 != 500 ):
                if ( _wr1 < -80 ) and ( _wr > -80 ) and ( _wr > _wr1 ):
                    #print ("BUY: [%s] EARLY ---> WR cross -80 from below" % symbol )
                    msg = "BUY: EARLY [WR cross -80 from below]"
                    advice.append ( msg )

            if ( _cci20 > _cci201 ) and ( _cci20 > -100 ) and ( _cci201 < -100 ):
                #print ("BUY: [%s] EARLY ---> CCI cross -100 from below" % symbol )
                msg = "BUY: EARLY [CCI cross -100 from below]"
                advice.append ( msg )

            if ( _rsi < 42 ) and ( _rsi > _rsi1 ):
                #print ("BUY: [%s] EARLY ---> RSI" % ( symbol ) )
                msg = "BUY: EARLY [RSI going up]"
                advice.append ( msg )

            if ( _stock_k > _stock_d ) and ( _stock_k1 < _stock_d1 ) and ( _stock_k < 27):
                #print ("BUY: [%s] EARLY ---> STOCKASTIC CROSS" %  symbol )
                msg = "BUY: EARLY [STOCKASTIC CROSS]"
                advice.append ( msg )

            # if yesterday's macd exists, look for a cross on the upside
            if ( _macd_blue1 != 500):
                if ( _macd_blue1 > _macd_orange1 ) and ( _macd_blue < _macd_orange ):
                    #print ("BUY: [%s] EARLY ---> MACD CROSS" % symbol )
                    msg = "BUY: EARLY [MACD CROSS]"
                    advice.append ( msg )

            # AO oscillator: if previous AO < 0 and current AO > 0   ==> BUY signal
            if ( _ao1 < 0 ) and ( _ao > 0):
                advice.append ( "BUY: EARLY [AO croosing to positive value]" )


            ##########################
            #####  AMAZING  BUY  #####
            ##########################

            # EMA 10 crossing EMA 20 from above. Very bulish!!
            if ( _ema101 != 500):
                if ( price > _ema10 ) and ( _ema10 > _ema20 ) and ( _ema201 > _ema101):
                    #print ("BUY: [%s] AMAZING: EMA10/EMA20 CROSS FROM BELOW" % symbol )
                    msg = "BUY: AMAZING [EMA10/EMA20 CROSS FROM BELOW]"
                    advice.append ( msg )

            ######################
            #####  DIP  BUY  #####
            ######################
            if ( _macd_orange < _macd_blue ) and ( _macd_orange < 0 ) and ( _macd_blue < 0 ):
                if ( _cci20 >= -80 ):
                    if ( _wr <= -65 ):
                        if ( _rsi <= 45 ):
                            #print ("BUY: [%s] DIP 1" % symbol)
                            msg = "BUY: DIP [1]"
                            advice.append ( msg )

            if ( _macd_orange < _macd_blue ) and ( _macd_orange < 0 ) and ( _macd_blue < 0 ):
                if ( _cci201 < -81 ) and ( _cci20 > -80 ):
                    if ( _wr1 < -80 ) and ( _wr > -80 ):
                        if ( _rsi > _rsi1 ):
                            #print ("BUY: [%s] DIP 2" % symbol )
                            msg = "BUY: [%s] DIP 2" % symbol
                            advice.append ( msg )


            ###########################
            #####  GOLDEN  CROSS  #####
            ###########################
            if ( _ema101 != 500):
                # if yesterday ( EMA 50 < EMA 200 ) and today ( EMA 50 > 200 )
                if ( _ema51 < _ema201 ) and ( _ema50 > _ema201 ):
                    #print ("BUY: [%s] GOLDEN CROSS EMA 50 crossing EMA 200 from below" % symbol )
                    msg = "BUY: GOLDEN CROSS [EMA 50 crossing EMA 200 from below]"
                    advice.append ( msg )

            if (math.isclose( _ema50, _ema200, abs_tol = 0.08) == True) and ( _ema50 > _ema200 ):
                #print ("BUY: [%s] GOLDEN CROSS soon 50, 200 EMA" % symbol )
                msg = "BUY: GOLDEN CROSS [soon 50, 200 EMA]"
                advice.append ( msg )



            ##################
            #####  SELL  #####
            ##################
            # stock going down after being overbought:   ( W%R < -20 = cross -20 from above ),  ( CCI20 < 100 = cross 100 from above ),  ( RSI < 70 = cross 70 from above )
            if ( _cci20 <= 100 ) and ( _cci201 > 100 ) and ( _cci20 < _cci201 ):
                # IF PREV.W%R > [ - 80 ] AND CURRENT.W%R < [ - 80 ] ==> SELL SIGNAL
                if ( _wr1 > -20 ) and ( _wr1 > _wr ) and (_wr < -20 ):
                    if ( _rsi1 > _rsi ) and ( _rsi1 > 70 ) and ( _rsi < 70 ):
                        #print ("SELL STRONG: [%s]" % symbol )
                        msg = "SELL STRONG [CCI, WR, RSI]"
                        advice.append ( msg )

            # Williams % R indicator:
            if ( _wr1 != 500 ):
                if ( _wr < _wr1 ) and ( _wr < -20 ) and ( _wr1 > -20 ):
                    #print ("SELL: [%s] CCI crossing -20 from above" % symbol )
                    msg = "SELL: [CCI crossing -20 from above]"
                    advice.append ( msg )

            # Williams % R indicator:
            if ( _wr <= -80 ):
                msg = "SELL: [WR is < or = to -80 lower level]"
                advice.append ( msg )
                if ( _wr1 != 500 ):
                    if ( _wr1 > _wr ) and ( _wr1 > -80 ):
                        msg = "SELL FAST: [WR crossing -80 from above]"
                        advice.append ( msg )

            # CCI indicator:
            if ( _cci20 <= -100 ):
                msg = "SELL: [CCI20 %s is below -100. Could be a good DIP buy]" % _cci20
                advice.append ( msg )

            # EMA:
            if ( _ema101 != 500):
                if ( price < _ema10 ) and ( _ema10 < _ema20 ) and ( _ema201 > _ema101):
                    #print ("SELL FAST: [%s] EMA10/EMA20 CROSS FROM ABOVE" % ( symbol ) )
                    msg = "SELL FAST: EMA10/EMA20 CROSS FROM ABOVE"
                    advice.append ( msg )

            # AO oscilator: if previous AO > 0 and current AO < 0   ==> BUY signal
            if ( _ao1 > 0 ) and ( _ao < 0):
                advice.append ( "SELL: EARLY [AO croosing below 0 from above]" )

            # MOM indicator:
            if ( _mom1 > 0 ) and ( _mom < 0 ):
                advice.append ( "SELL: [Mom cross below 0]")

            ##########################
            #####  DEATH  CROSS  #####
            ##########################
            if ( _ema101 != 500):
                # if yesterday's ( EMA 50 > EMA 200 ) and today ( EMA 50 < EMA 200 )
                if ( _ema51 > _ema201 ) and ( _ema50 < _ema200 ):
                    #print ("SELL: [%s] DEATH CROSS EMA 50 crossing EMA 200 from above" % ( symbol ) )
                    msg = "SELL: DEATH CROSS [EMA 50 crossing EMA 200 from above]"
                    advice.append ( msg )


            if (math.isclose( _ema50, _ema200, abs_tol = 0.08) == True) and ( _ema50 < _ema200 ):
                #print ("SELL: [%s] BEAR CROSS soon 200, 50 EMA" % symbol)
                msg = "SELL: BEAR CROSS [soon 200, 50 EMA]"
                advice.append ( msg )


            #BUY_SIGS = round(json_analysis.summary['BUY'],0)
            #BUY_SIGS2 = round(json_analysis_15m.summary['BUY'],0)

            #if RSI<=30:
            #    if _MACD_15m > _MACD_15m_signal*0.95 and ( _MACD_1h > _MACD_1h_signal ):
            #        print ("%s MACD buy" % (symbol) )
            #    else:
            #        print ("%s MACD sell" % ( symbol ) )


            #if blue_line < orange_line and blue_line <= 0 and orange_line <= 0 and math.isclose(blue_line, orange_line, abs_tol = 0.04) == True and price < _EMA200 and RSI < 50:
            #    print("GOOD TIME TO DCA EOS")
            #if blue_line < orange_line and blue_line <= 0 and orange_line <= 0 and math.isclose(blue_line, orange_line, abs_tol = 0.04) == True and price > _EMA200:
            #    print("GOOD TIME TO ENTER TRADE")
            #if blue_line < orange_line and blue_line <= 0.200 and orange_line > 0 and math.isclose(blue_line, orange_line, abs_tol = 0.04) == True and price > _EMA200:
            #    print("GOOD TIME TO ENTER TRADE")
            #if blue_line > orange_line and blue_line > 0.240 and orange_line > 0 and math.isclose(blue_line, orange_line, abs_tol = 0.04) == True and price > _EMA200:
            #    print("GOOD TIME TO TAKE PROFIT")

            #####  BUY/SELL algo !!  #####
            #RSI_MIN   = 12  # Min RSI Level for Buy Signal - Under 25 considered oversold (12)
            #RSI_MAX   = 55  # Max RSI Level for Buy Signal - Over 80 considered overbought (55)

            #RSI_BUY   = 0.3 # Difference in RSI levels over last 2 timescales for a Buy Signal (-0.3)
            #STOCH_BUY = 10  # Difference between the Stoch K&D levels for a Buy Signal (10)

            #RSI_SELL = -5 # Difference in RSI levels over last 2 timescales for a Sell Signal (-5)
            #STOCH_SELL = -10 # Difference between the Stoch D&K levels for a Sell Signal (-10)
            #SIGNALS_SELL = 7 # Max number of buy signals on both INTERVALs to add coin to sell list (7)

            #if (RSI < 80) and (BUY_SIGS >= 10) and (STOCH_DIFF >= 0.01) and (RSI_DIFF >= 0.01):
            #    print(f'{symbol} Signals OSC:  RSI:{RSI}/{RSI1} DIFF: {RSI_DIFF} | STOCH_K/D:{STOCH_K}/{STOCH_D} DIFF: {STOCH_DIFF} | BUYS: {BUY_SIGS}_{BUY_SIGS2}/26 | {oscCheck}-{maCheck}')

            #if (RSI >= RSI_MIN and RSI <= RSI_MAX) and (RSI_DIFF >= RSI_BUY):
            #  if (STOCH_DIFF >= STOCH_BUY) and (STOCH_K >= STOCH_MIN and STOCH_K <= STOCH_MAX) and (STOCH_D >= STOCH_MIN and STOCH_D <= STOCH_MAX):
            #    if (BUY_SIGS >= MA_SUMMARY) and (BUY_SIGS2 >= MA_SUMMARY2) and (STOCH_K > STOCH_K1):
            #      if (oscCheck >= OSC_THRESHOLD and maCheck >= MA_THRESHOLD):

            #        print(f'\033[92m{symbol} Signals RSI: - Buy Signal Detected | {BUY_SIGS}_{BUY_SIGS2}/26')

            #        timestamp = datetime.now().strftime("%d/%m %H:%M:%S")
            #        print(f'  {symbol} Signals OSC: = RSI:{RSI}/{RSI1} DIFF: {RSI_DIFF} | STOCH_K/D:{STOCH_K}/{STOCH_D} DIFF: {STOCH_DIFF} | BUYS: {BUY_SIGS}_{BUY_SIGS2}/26 | {oscCheck}-{maCheck}\n')
            #      else:
            #        print(f'{SIGNAL_NAME} Signals RSI: - Stoch/RSI ok, not enough buy signals | {BUY_SIGS}_{BUY_SIGS2}/26 | {STOCH_DIFF}/{RSI_DIFF} | {STOCH_K}')


            #if ( _EMA10 > _EMA20 ) and ( currentPrice > _EMA200 ) and ( currentPrice > OPENING_PRICE) and (OPENING_PRICE > P_SAR ) and ( P_SAR > _EMA200 ):
            #    #and ( blue_line < orange_line ) and ( blue_line <= 0 and orange_line <= 0 ) and ( math.isclose(blue_line, orange_line, abs_tol = 0.04) == True ):
            #    position_ema = 'BUY'
            #    buy_list.append ( symbol )
            #else:
            #    position_ema = 'SELL'
            #print ("::::::: %s" % position_ema )

            #if daily_change <= -17.0000:
            #    # BUY DIP ?
            #if daily_change >= 17.0000:
            #    # SELL

            #if (BUY_SIGS < SIGNALS_SELL) and (BUY_SIGS2 < SIGNALS_SELL) and (STOCH_DIFF < STOCH_SELL) and (RSI_DIFF < RSI_SELL) and (STOCH_K < STOCH_K1):
            #    print(f'\033[33mSignals RSI: {symbol} - Sell Signal Detected | {BUY_SIGS}_{BUY_SIGS2}/26')

            #print(txcolors.NEUTRAL,'  {:8s}  {:10f}  ALL:{:25s} OSC:{:20s} {:35s}  {:10s}  '.format ( symbol, price, recommendation, osc_recommendation, osc_line, calculate_rsi(RSI) ),'',txcolors.ENDC)
            #print(txcolors.NEUTRAL,'  {:8s}  {:10s}  {:25s}   {:20s}   {:40s})  {:30s}  {:15s}  \033[33m[{:15s}] '.format ( symbol, price_string , colorme ( recommendation ), 'OSC:' + colorme ( osc_recommendation ), 'mAVE:' + colorme ( mave_recommendation ),
            print(txcolors.NEUTRAL,'  {:8s}  {:10s}   {:8s}%  {:25s}   {:20s}|   {:40s}  {:30s}   \033[33m{:15s} '.format ( symbol, price_string , _change_2dec ,
                colorme ( recommendation ), 'OSC:' + colorme ( osc_recommendation ), 'mAVE:' + colorme ( mave_recommendation ),
                osc_line,  colorme ( upgrade_downgrade ) ),'',txcolors.ENDC)

            message = 9 * ' '
            if ( len ( advice ) > 0):
                message += symbol + ' # ' + ", ".join( advice )
                print ( message )

            print ( "             SupRes   [%s] ---> %s" % ( symbol, sr ( symbol ) ) )
            print ( "             Fibona   [%s] ---> %s" % ( symbol, fibonacci ) )
            print ( "             ATR_band [%s] ---> (%.2f) %s  (%.2f)" % ( symbol, atr_band_lower, price_string, atr_band_higher ) )
            print('--------------------------------------------------------------------')

            time.sleep(2)
            #sys.exit(0)


    #####  BUY  list  #####
    #print ( buy_list )


    # Delete lock file before exit
    if os.path.exists(lockfile):
        os.unlink (lockfile)



if __name__ == "__main__":
    try:

        upgrades = get_analysts_upgrades_downgrades_marketwatch()

        parser = argparse.ArgumentParser()
        parser.add_argument('files', nargs='+')

        args=parser.parse_args()

        ticker_files = sorted ( set (args.files) )
        for myfile in ticker_files:
            print ("\n\n")
            print('--------------------------------------------------------------------')
            main(myfile, upgrades)

        sys.exit(0)

    except KeyboardInterrupt:
        homedir = os.path.expanduser("~")
        lockfile = homedir + '/.s.lock'
        if os.path.exists(lockfile):
            os.unlink (lockfile)
            print ('Interrupted')
            sys.exit(0)

    except Exception as e:
        print(e)

