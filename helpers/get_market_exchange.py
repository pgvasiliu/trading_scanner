#!/usr/bin/env python

#
# dnf install python3-colorama python3-requests 
#

import os
import sys
import json
import requests
import argparse

from colorama import Fore, Style




def get_market_exchange(ticker):
    absolutepath = os.path.abspath(__file__)
    fileDirectory = os.path.dirname(absolutepath)
    CONFIG_PATH = os.path.dirname(fileDirectory) + '/' + 'config_settings.json'

    with open(CONFIG_PATH) as json_file:
        json_data = json.load(json_file)

    headers = {'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'}

    r = requests.get(json_data['symbol_url'].format(ticker), headers=headers)
    response = {}
    for el in r.json():
        if el['symbol'] == ticker.upper():
            if el['exchange'] in ['NYSE', 'NASDAQ', 'BINANCE', 'BITTREX', "NYSE ARCA & MKT"]:
                if el['exchange'] == "NYSE ARCA & MKT":
                    #print(el['exchange'])
                    exchange = "AMEX"
                else:
                    exchange = el['exchange']
            if el['exchange'] in ['TSE', 'TSX']:
                exchange = "TSX"
    if exchange in ['NYSE', 'NASDAQ', 'ARCA',"AMEX"]:
        screener = "america"
    elif exchange in ['TSE', 'TSX']:
        screener = "canada"
    else:
        screener = "crypto"
    return(screener, exchange)

def main():
    data = '{' + "\n"
    parser = argparse.ArgumentParser()
    parser.add_argument('symbols', nargs='+')

    args=parser.parse_args()

    symbols = sorted ( set (args.symbols) )
    for symbol in symbols:
        undef, exch = get_market_exchange(symbol)
        #print ("%s:%s" % ( symbol, exch ) )
        #print(f"{Fore.GREEN}{symbol}:{Style.RESET_ALL}{exch}")
        data += '    "%s":"%s",\n' % ( symbol, exch )

    # delete last 2 chars from string: , and \n
    data = data[:-2]
    data += "\n" + '}' + "\n"
    print(data); 

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)

