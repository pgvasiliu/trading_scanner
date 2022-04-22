# trading_scanner

## Install dependencies

### Fedora

```bash
$ dnf install  python3-devel python3-pip  python3-requests  python3-colorama python3-beautifulsoup4 python3-pandas python3-pandas-datareader
$ pip3 install tradingview_ta lxml pandas pandas-datareader
```

### Pip

```bash
$ pip3 install -r requirements.txt
```

### Building TA-Lib package

To use the TA-Lib python pip package you would need the [previous 0.4.0](https://github.com/mrjbq7/ta-lib#dependencies) library first

**Get build essentials**

```bash
$ sudo dnf install python3-devel python3-pip python3-numpy python3-matplotlib python3-yfinance
```

**Build TA-Lib**

```bash
$ wget http://sourceforge.net/projects/ta-lib/files/ta-lib/0.4.0/ta-lib-0.4.0-src.tar.gz/download?use_mirror=iweb
$ tar zxfv ta-lib-0.4.0-src.tar.gz
$ cd ta-lib
$ ./configure --prefix=/usr
$ make
$ sudo make install
```

**Install python wrappers**

```bash
$ pip3 install --user Cython
$ pip3 install --user TA-Lib
$ pip3 install --user yahoo-fin
$ pip3 install --user mplfinance mpl-finance
```

## TODO

- [x] Resistance / support levels
- [x] ATR bands ( a.k.a. Keltner channel = stop loss/take profit )
- [x] Earnings date
- [x] Fibonnacci levels
- [ ] Volume logic
- [ ] 1 year price target
- [x] TEMA ( 30 ) indicator. TradingView does not return TEMA via the API so we are going to use yahoo to calculate tema.
- [ ] Strategies and backtesting

## Example runs

```bash
$ ./scanner.py config_tickers_canada.json
--------------------------------------------------------------------
   BCE       67.92        0.38    %  BUY                OSC:NEUTRAL|   mAVE:BUY                         OSC:  W%R BUY, MACD SELL,        []                
-------------------------------------------------------------------
   BMO       149.15       0.24    %  BUY                OSC:NEUTRAL|   mAVE:STRONG_BUY                  OSC:  MACD BUY,                  []                
--------------------------------------------------------------------
   BNS       91.97        0.87    %  NEUTRAL            OSC:NEUTRAL|   mAVE:SELL                        OSC:  MACD SELL,                 []                
         BNS # BUY: EARLY [CCI cross -100 from below]
--------------------------------------------------------------------
   CM        157.88       -0.58   %  SELL               OSC:SELL   |   mAVE:SELL                        OSC:  MACD SELL,                 []                
--------------------------------------------------------------------
   CP        103.32       0.46    %  BUY                OSC:BUY    |   mAVE:STRONG_BUY                  OSC:  MACD BUY,                  []                
--------------------------------------------------------------------
   GRT.UN    95.87        -0.76   %  BUY                OSC:NEUTRAL|   mAVE:BUY                         OSC:  MACD BUY,                  []                
--------------------------------------------------------------------
   HXE       27.7         2.55    %  STRONG_BUY         OSC:BUY    |   mAVE:STRONG_BUY                  OSC:  MACD BUY,                  []                
--------------------------------------------------------------------
   L         109.47       -0.05   %  BUY                OSC:NEUTRAL|   mAVE:STRONG_BUY                  OSC:  MACD SELL,                 []                
--------------------------------------------------------------------
   MFC       26.34        0.80    %  BUY                OSC:NEUTRAL|   mAVE:STRONG_BUY                  OSC:  MACD BUY,                  []                
         MFC # BUY: GOOD [WR 14 cross to overbought], BUY: [w/o stockastic]
--------------------------------------------------------------------
   NEO       15.87        -2.94   %  SELL               OSC:NEUTRAL|   mAVE:STRONG_SELL                 OSC:  MACD BUY,                  []                
--------------------------------------------------------------------
   OVV       68.7         4.39    %  STRONG_BUY         OSC:BUY    |   mAVE:STRONG_BUY                  OSC:  MACD BUY,                  []                
--------------------------------------------------------------------
   PD        87.8         1.84    %  BUY                OSC:BUY    |   mAVE:STRONG_BUY                  OSC:  MACD BUY,                  []                
         PD # BUY: EARLY [MACD CROSS]
--------------------------------------------------------------------
   RY        141.28       0.56    %  STRONG_BUY         OSC:BUY    |   mAVE:STRONG_BUY                  OSC:  MACD BUY,                  []                
--------------------------------------------------------------------
   SRU.UN    33.04        0.79    %  BUY                OSC:NEUTRAL|   mAVE:STRONG_BUY                  OSC:  MACD BUY,                  []                
--------------------------------------------------------------------
   SSRM      27.47        -0.22   %  BUY                OSC:SELL   |   mAVE:STRONG_BUY                  OSC:  MACD SELL,                 []                
--------------------------------------------------------------------
   SU        42.41        2.91    %  STRONG_BUY         OSC:BUY    |   mAVE:STRONG_BUY                  OSC:  MACD BUY,                  []                
         SU # BUY: GOOD [CCI20 cross to upper level], BUY: [w/o stockastic], BUY: [w stockastic]
--------------------------------------------------------------------
   TD        101.81       0.91    %  BUY                OSC:BUY    |   mAVE:STRONG_BUY                  OSC:  MACD BUY,                  []                
--------------------------------------------------------------------
   VET       29.2         5.68    %  BUY                OSC:NEUTRAL|   mAVE:STRONG_BUY                  OSC:  MACD SELL,                 []                
--------------------------------------------------------------------
   VUN       77.15        -0.27   %  BUY                OSC:NEUTRAL|   mAVE:BUY                         OSC:  W%R SELL, CCI SELL, MACD BUY,   []                
         VUN # BUY: AMAZING [EMA10/EMA20 CROSS FROM BELOW], SELL: BEAR CROSS [soon 200, 50 EMA]
--------------------------------------------------------------------
   ZEB       41           0.56    %  BUY                OSC:BUY    |   mAVE:BUY                         OSC:  MACD BUY,                  []                
--------------------------------------------------------------------
   ZUB       35.71        1.39    %  BUY                OSC:BUY    |   mAVE:BUY                         OSC:  MACD BUY,                  []                
         ZUB # BUY: GOOD [WR 14 cross to overbought]
--------------------------------------------------------------------


$ ./scanner.py tickers/sectors/energy.json
--------------------------------------------------------------------
   APA       43.68        0.16    %  BUY                OSC:SELL   |   mAVE:STRONG_BUY                  OSC:  W%R SELL, MACD SELL,       []                
         APA # BUY: [w/o stockastic], BUY: [w stockastic]
             SupRes   [APA] ---> ['16.15', '18.41', '19.67', '21.09', '22.44', '23.65', '25.17', '28.67', '31.02', '32.32', '34.27', '36.46', '38.52', '43.88']
             Fibona   [APA] ---> {'0': '15.90', '0.236': '22.46', '0.382': '26.51', '0.5': '29.79', '0.618': '33.07', '0.786': '37.74', '1': '43.68', '1.618': '60.85', '2.618': '88.63', '3.618': '116.40', '4.236': '133.57'}
             ATR_band [APA] ---> (37.36) 43.68  (45.12)
--------------------------------------------------------------------
   BKR       37.29        0.19    %  STRONG_BUY         OSC:NEUTRAL|   mAVE:STRONG_BUY                  OSC:  MACD SELL,                 []                
         BKR # SELL: GOOD [Mom cross above 0]
             SupRes   [BKR] ---> ['18.20', '22.86', '24.57', '25.79', '27.27', '29.28', '32.58', '35.08', '38.41', '39.78']
             Fibona   [BKR] ---> {'0': '18.94', '0.236': '23.61', '0.382': '26.50', '0.5': '28.83', '0.618': '31.16', '0.786': '34.49', '1': '38.72', '1.618': '50.94', '2.618': '70.72', '3.618': '90.50', '4.236': '102.73'}
             ATR_band [BKR] ---> (33.39) 37.29  (39.03)
--------------------------------------------------------------------
   BP        31.29        0.26    %  BUY                OSC:NEUTRAL|   mAVE:STRONG_BUY                  OSC:  W%R SELL, CCI SELL, MACD BUY,   []                
         BP # BUY: [w/o stockastic], BUY: [w stockastic]
             SupRes   [BP] ---> ['23.13', '24.22', '26.16', '26.93', '27.96', '28.60', '29.64', '30.34', '31.24']
             Fibona   [BP] ---> {'0': '22.31', '0.236': '24.83', '0.382': '26.39', '0.5': '27.66', '0.618': '28.92', '0.786': '30.71', '1': '33.00', '1.618': '39.61', '2.618': '50.31', '3.618': '61.01', '4.236': '67.62'}
             ATR_band [BP] ---> (28.58) 31.29  (31.71)
--------------------------------------------------------------------


$ ./get_market_exchange.py HAL BTU SLB XLE MRO OXY VDE RIG SM NOG LNG XOP  MGY MUR XOM CVX HAL COP EOG EXC DVN BP VLO USO MPC APA BKR
{
    "APA":"NASDAQ",
    "BKR":"NASDAQ",
    "BP":"NYSE",
    "BTU":"NYSE",
    "COP":"NYSE",
    "CVX":"NYSE",
    "DVN":"NYSE",
    "EOG":"NYSE",
    "EXC":"NASDAQ",
    "HAL":"NYSE",
    "LNG":"AMEX",
    "MGY":"NYSE",
    "MPC":"TSX",
    "MRO":"NYSE",
    "MUR":"NYSE",
    "NOG":"NYSE",
    "OXY":"NYSE",
    "RIG":"NYSE",
    "SLB":"NYSE",
    "SM":"NYSE",
    "USO":"AMEX",
    "VDE":"AMEX",
    "VLO":"NYSE",
    "XLE":"AMEX",
    "XOM":"NYSE",
    "XOP":"AMEX"
}


$ curl -L https://datahub.io/core/s-and-p-500-companies/r/0.csv -o /tmp/sp500.csv

```
