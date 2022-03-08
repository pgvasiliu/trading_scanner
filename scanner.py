#!/usr/bin/env python

import math
import os
import sys
import json
import pprint
import calendar
import time
from datetime import datetime, timedelta

from os.path import expanduser
from datetime import datetime, timedelta

#from tradingview_ta import TA_Handler#, Interval, Exchange
from tradingview_ta import TA_Handler, Interval

import colorama


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

#def convert_to_str(value):
#    new_str = str(value)
#    return new_string

#def scan_combined(rsi_list, ema_list):
#    for x in rsi_list:
#        for i in ema_list:
#            if (i.symbol == x.symbol):
#                combined_list.append(i)


def taJson(product, exch, myinterval):
    p = product.replace('-', '')
    ta = TA_Handler(
        symbol=p,
        screener="america",
        exchange=exch,
        interval=myinterval
    )
    try:
        analysis = ta.get_analysis()
        return analysis
    except Exception as e:
        print(f'{SIGNAL_NAME}Exception:')
        print(e)
        sys.exit(1)


def calculate_rsi(p):
    if (p < 20 ):
        r = "RSI_ExtremelyOversold"
    elif (p >= 20 and p <= 30):
        r = "RSI_Oversold"
    elif (p > 30 and p <= 45):
        r = "RSI_ApproachingOversold"
    elif (p > 45 and p <= 55):
        r = "RSI_Neutral"
    elif (p > 55 and p <= 70):
        r = "RSI_ApproachingOverbought"
    elif (p > 70 and p <= 80):
        r = "RSI_Overbought"
    elif (p > 80):
        r = "RSI_ExtremelyOverbought"
    else :
        r= "UNKNOWN"
    return r

def main():
    keys = ['BUY','SELL','NEUTRAL']

    Intervals = { Interval.INTERVAL_1_DAY,
                  Interval.INTERVAL_4_HOURS,
                  Interval.INTERVAL_1_HOUR,
                  Interval.INTERVAL_15_MINUTES
                }

    interval = Interval.INTERVAL_1_DAY

    buy_list, rsi_list, ema_list = ( [], [], [] )

    today = datetime.today()
    thirty_days_ago = today - timedelta(days=30)
    tt = thirty_days_ago.strftime("%Y-%m-%d")

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


    with open("config_settings.json") as f:
        config = json.load(f)
        for key, value in config.items():
            os.environ[key] = str(value)

    tickers_exchange_json = {}
    with open('config_tickers.json') as f:
        data = json.load(f)
        ticker_exchange = dict(sorted(data.items()))

        for symbol, exchange in ticker_exchange.items():

            oscCheck=0
            maCheck=0

            json_analysis      = taJson(symbol, exchange, Interval.INTERVAL_1_DAY)
            json_analysis_15m  = taJson(symbol, exchange, Interval.INTERVAL_15_MINUTES)
            json_analysis_1h   = taJson(symbol, exchange, Interval.INTERVAL_1_HOUR)

            recommendation = json_analysis.summary['RECOMMENDATION']

            # indicator names + values
            ind     = json_analysis.indicators
            ind_15m = json_analysis_15m.indicators
            ind_1h  = json_analysis_1h.indicators

            # oscilators names + values
            osc = json_analysis.oscillators


            currentPrice = round ( ind["close"], 2 )
            OPENING_PRICE= round ( ind['open'],  2 )
            daily_change = ind['change']

            P_SAR = round ( ind['P.SAR'], 2 )

            # RSI
            RSI = round (ind["RSI"], 2)
            #print ( calculate_rsi ( rsi ))

            RSI1 = round(ind['RSI[1]'],2)

            STOCH_K = round(ind['Stoch.K'],2)
            STOCH_D = round(ind['Stoch.D'],2)

            STOCH_K1 = round(ind['Stoch.K[1]'],2)
            STOCH_D1 = round(ind['Stoch.D[1]'],2)


            #####  MACD  #####
            blue_line   = ind["MACD.macd"]   #BLUE LINE
            orange_line = ind["MACD.signal"] #ORANGE LINE

            _MACD_15m        = ind_15m['MACD.macd']
            _MACD_15m_signal = ind_15m['MACD.signal']
            _MACD_1h         = ind_1h['MACD.macd']
            _MACD_1h_signal  = ind_1h['MACD.signal']

            #####  EMA  #####
            _EMA10  = ind['EMA10']
            _EMA20  = ind['EMA20']
            _EMA30  = ind['EMA30']
            _EMA50  = ind['EMA50']
            _EMA200 = ind['EMA200']

            STOCH_DIFF = round(STOCH_K - STOCH_D,2)
            RSI_DIFF = round(RSI - RSI1,2)

            BUY_SIGS = round(json_analysis.summary['BUY'],0)
            BUY_SIGS2 = round(json_analysis_15m.summary['BUY'],0)

            if RSI<=30:
                if _MACD_15m > _MACD_15m_signal*0.95 and ( _MACD_1h > _MACD_1h_signal ):
                    print ('%s MACD buy')
                else:
                    print ('%s MACD sell')


            #if blue_line < orange_line and blue_line <= 0 and orange_line <= 0 and math.isclose(blue_line, orange_line, abs_tol = 0.04) == True and price < _EMA200 and RSI < 50:
            #    print("GOOD TIME TO DCA EOS")
            #if blue_line < orange_line and blue_line <= 0 and orange_line <= 0 and math.isclose(blue_line, orange_line, abs_tol = 0.04) == True and price > _EMA200:
            #    print("GOOD TIME TO ENTER TRADE")
            #if blue_line < orange_line and blue_line <= 0.200 and orange_line > 0 and math.isclose(blue_line, orange_line, abs_tol = 0.04) == True and price > _EMA200:
            #    print("GOOD TIME TO ENTER TRADE")
            #if blue_line > orange_line and blue_line > 0.240 and orange_line > 0 and math.isclose(blue_line, orange_line, abs_tol = 0.04) == True and price > _EMA200:
            #    print("GOOD TIME TO TAKE PROFIT")

            #####  BUY/SELL algo !!  #####
            RSI_MIN   = 12  # Min RSI Level for Buy Signal - Under 25 considered oversold (12)
            RSI_MAX   = 55  # Max RSI Level for Buy Signal - Over 80 considered overbought (55)

            RSI_BUY   = 0.3 # Difference in RSI levels over last 2 timescales for a Buy Signal (-0.3)
            STOCH_BUY = 10  # Difference between the Stoch K&D levels for a Buy Signal (10)

            RSI_SELL = -5 # Difference in RSI levels over last 2 timescales for a Sell Signal (-5)
            STOCH_SELL = -10 # Difference between the Stoch D&K levels for a Sell Signal (-10)
            SIGNALS_SELL = 7 # Max number of buy signals on both INTERVALs to add coin to sell list (7)


            if (math.isclose(_EMA20, _EMA50, abs_tol = 0.08) == True) and ( _EMA_20 > _EMA50 ):
                print ("GOLDEN CROSS soon 20, 50 EMA")
            if (math.isclose(_EMA20, _EMA50, abs_tol = 0.08) == True) and ( _EMA_20 < _EMA50 ):
                print ("BEAR CROSS soon 20, 50 EMA")

            if (RSI < 80) and (BUY_SIGS >= 10) and (STOCH_DIFF >= 0.01) and (RSI_DIFF >= 0.01):
                print(f'{symbol} Signals OSC:  RSI:{RSI}/{RSI1} DIFF: {RSI_DIFF} | STOCH_K/D:{STOCH_K}/{STOCH_D} DIFF: {STOCH_DIFF} | BUYS: {BUY_SIGS}_{BUY_SIGS2}/26 | {oscCheck}-{maCheck}')

            if (RSI >= RSI_MIN and RSI <= RSI_MAX) and (RSI_DIFF >= RSI_BUY):
              if (STOCH_DIFF >= STOCH_BUY) and (STOCH_K >= STOCH_MIN and STOCH_K <= STOCH_MAX) and (STOCH_D >= STOCH_MIN and STOCH_D <= STOCH_MAX):
                if (BUY_SIGS >= MA_SUMMARY) and (BUY_SIGS2 >= MA_SUMMARY2) and (STOCH_K > STOCH_K1):
                  if (oscCheck >= OSC_THRESHOLD and maCheck >= MA_THRESHOLD):

                    print(f'\033[92m{symbol} Signals RSI: - Buy Signal Detected | {BUY_SIGS}_{BUY_SIGS2}/26')

                    timestamp = datetime.now().strftime("%d/%m %H:%M:%S")
                    print(f'  {symbol} Signals OSC: = RSI:{RSI}/{RSI1} DIFF: {RSI_DIFF} | STOCH_K/D:{STOCH_K}/{STOCH_D} DIFF: {STOCH_DIFF} | BUYS: {BUY_SIGS}_{BUY_SIGS2}/26 | {oscCheck}-{maCheck}\n')
                  else:
                    print(f'{SIGNAL_NAME} Signals RSI: - Stoch/RSI ok, not enough buy signals | {BUY_SIGS}_{BUY_SIGS2}/26 | {STOCH_DIFF}/{RSI_DIFF} | {STOCH_K}')

            
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

            if (BUY_SIGS < SIGNALS_SELL) and (BUY_SIGS2 < SIGNALS_SELL) and (STOCH_DIFF < STOCH_SELL) and (RSI_DIFF < RSI_SELL) and (STOCH_K < STOCH_K1):
                print(f'\033[33mSignals RSI: {symbol} - Sell Signal Detected | {BUY_SIGS}_{BUY_SIGS2}/26')

            print(txcolors.NEUTRAL,'  {:8s}  {:10f}  {:15s}  {:12f}  {:12f}  {:12s}  '.format ( symbol, currentPrice, recommendation, RSI1, RSI, calculate_rsi(RSI) ),'x',txcolors.ENDC)
            print('--------------------------------------------------------------------------')

            time.sleep(1)
            #sys.exit(0)


    #####  BUY  list  #####
    print ( buy_list )


    # Delete lock file before exit
    if os.path.exists(lockfile):
        os.unlink (lockfile)

    sys.exit(0)


if __name__ == "__main__":
    try:
        main()

    except KeyboardInterrupt:
        homedir = os.path.expanduser("~")
        lockfile = homedir + '/.s.lock'
        if os.path.exists(lockfile):
            os.unlink (lockfile)
            print ('Interrupted')
            sys.exit(0)

    except Exception as e:
        print(e)

