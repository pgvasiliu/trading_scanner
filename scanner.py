#!/usr/bin/env python

import math
import os
import sys
import json
import pprint
import calendar

from os.path import expanduser

import time
from datetime import datetime, timedelta

#from tradingview_ta import TA_Handler#, Interval, Exchange
from tradingview_ta import TA_Handler, Interval

#import colorama
import argparse


from bs4 import BeautifulSoup
import requests


def get_analysts_upgrades_downgrades_marketwatch():
    def add_data_to_dict(n_check, n_val, key, val, storage_dict):

        if n_val == n_check:
            storage_dict[key] = val.string

    url = "https://www.marketwatch.com/tools/upgrades-downgrades"
    raw_page = requests.get(url)
    soup = BeautifulSoup(raw_page.content, 'lxml')

    table = soup.find('table')
    raw_data_rows = table.find_all('tr')

    row_text_data = list()

    for tr in raw_data_rows[1:]:

        data = dict()
        for n, td in enumerate(tr):
            add_data_to_dict(1, n, "date", td.string, data)
            add_data_to_dict(3, n, "ticker", td.string, data)
            add_data_to_dict(5, n, "company", td.string, data)
            add_data_to_dict(7, n, "rating", td.string, data)
            add_data_to_dict(9, n, "analyst", td.string, data)

        row_text_data.append(data)

    return row_text_data



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
    if 'SELL' in string:
        out = '\033[91m' + string + '\033[0m'
        return out
    return string

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
    if exch in [ "TSX", "TSE" ]:
        screener = "canada"
    else:
        screener = "america"

    ta = TA_Handler(
        symbol=p,
        screener=screener,
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

    interval = Interval.INTERVAL_1_DAY

    buy_list, rsi_list, ema_list = ( [], [], [] )
    early_list = []


    #today    = datetime.today()
    today     = time.strftime("%Y-%m-%d")
    tt = datetime.today() - timedelta(days=1)
    yesterday = tt.strftime("%Y-%m-%d")

    # if today is Monday, we should access Fri's data not Sunday's
    if (datetime.today().strftime('%A').lower()) == "monday":
        tt = datetime.today() - timedelta(days=3)
        yesterday = tt.strftime("%Y-%m-%d")

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

            ticker_data['stock_diff'] = stock_diff
            ticker_data['rsi_diff']   = rsi_diff



            #####  save data for today  #####
            file_dest = ticker_folder + '/' + today + '/' + 'data.json'
            with open(file_dest, 'w') as filehandle:
                filehandle.write( json.dumps ( ticker_data, indent=4) + '\n')


            #################
            #####  BUY  #####
            #################

            # Load yesterday's json data. TradingView API does not return yesterday's data for volume and W%R
            volume1 = 0
            _wr1    = 0

            yesterdays_data = ticker_folder + '/' + yesterday + '/' + 'data.json'
            if (os.path.exists(yesterdays_data)) and (os.stat(yesterdays_data).st_size > 0):
                with open(yesterdays_data) as yesterdays_json:
                    old_data = json.load(yesterdays_json)
                    if 'volume' in old_data:
                        volume1 = old_data['volume']
                    if '_wr' in old_data:
                        _wr1    = old_data['_wr']
                # [ ..... ]
            # [ ..... ]



            #######################
            #####  GOOD  BUY  #####
            #######################

            # price > yesterday's price
            if ( _change > 0 ):

                # EMA
                if ( price > _ema10 > _ema20 > _ema50 > _ema100 > _ema200):

                    # MACD (12,26,9)
                    if ( _macd_orange > _macd_blue ):

                        # CCI (20) > 100
                        if ( _cci20 > 100 ):

                            # WR,14 > -20
                            if ( _wr > -20 ):

                                # RSI < 70 and going UP
                                if ( _rsi < 70 ):
                                    print ("BUY")

            ##########################
            #####  AWESOME  BUY  #####
            ##########################


            ##########################
            #####  AMAZING  BUY  #####
            ##########################

            ######################
            #####  DIP  BUY  #####
            ######################
            if ( _macd_orange < _macd_blue ) and ( _macd_orange < 0 ) and ( _macd_blue < 0 ):
                if ( _cci20 > -80 ):
                    if ( _wr < -65 ):
                        if ( _rsi < 45 ):
                            print ("Buy DIP")


            ##################
            #####  SELL  #####
            ##################
            # stock going down after being overbought:   ( W%R < -20 = cross -20 from above ),  ( CCI20 < 100 = cross 100 from above ),  ( RSI < 70 = cross 70 from above )
            if ( _cci20 < 100 ) and ( _cci201 > 100 ) and ( _cci20 < _cci201 ):
                if ( _wr1 > -20 ) and ( _wr1 > _wr ) and (_wr < -20 ):
                    if ( _rsi1 > _rsi ) and ( _rsi1 > 70 ) and ( _rsi < 70 ):
                        print ("STRONG SELL !!!")


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


            #if (math.isclose(_EMA50, _EMA200, abs_tol = 0.08) == True) and ( _EMA_50 > _EMA200 ):
            #    print ("GOLDEN CROSS soon 20, 50 EMA")
            #if (math.isclose(_EMA50, _EMA200, abs_tol = 0.08) == True) and ( _EMA_50 < _EMA200 ):
            #    print ("BEAR CROSS soon 20, 50 EMA")

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
            print(txcolors.NEUTRAL,'  {:8s}  {:10s}   {:8s}%  {:25s}   {:20s}   {:40s}  {:30s}   \033[33m{:15s} '.format ( symbol, price_string , _change_2dec ,
                colorme ( recommendation ), 'OSC:' + colorme ( osc_recommendation ), 'mAVE:' + colorme ( mave_recommendation ),
                osc_line,  upgrade_downgrade ),'',txcolors.ENDC)
            print('--------------------------------------------------------------------')

            time.sleep(1)
            #sys.exit(0)


    #####  BUY  list  #####
    print ( buy_list )


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

