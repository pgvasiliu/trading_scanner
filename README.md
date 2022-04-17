# trading_scanner

## Install dependencies

### Fedora

```bash
$ dnf install  python3-devel python3-pip  python3-requests  python3-colorama python3-beautifulsoup4 python3-pandas python3-pandas-datareader
$ pip3 install tradingview_ta lxml pandas pandas-datareader
```

### Pip

```bash
$ pip3 install --user lxml requests colorama beautifulsoup4 tradingview_ta pandas pandas-datareader
```

### Advanced features
```bash

        1. Get build essentials

        $ sudo dnf install python3-devel python3-pip python3-numpy python3-matplotlib python3-yfinance

        2. Build TA-Lib

        $ wget http://sourceforge.net/projects/ta-lib/files/ta-lib/0.4.0/ta-lib-0.4.0-src.tar.gz/download?use_mirror=iweb
        $ tar zxfv ta-lib-0.4.0-src.tar.gz
        $ cd ta-lib
        $ ./configure --prefix=/usr
        $ make
        $ sudo make install

        1.3 Install python wrapper

        $ pip3 install --user Cython
        $ pip3 install --user TA-Lib
        $ pip3 install --user yahoo-fin
        $ pip3 install --user mplfinance mpl-finance

```

## TODO

- [x] Resistance / support levels
- [ ] Volume logic
- [ ] Earnings date
- [ ] TEMA ( 30 ) indicator. TradingView does not return TEMA via the API so we are going to use yahoo to calculate tema.
- [ ] ATR stoploss/take profit

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
   BP        31.05        1.01    %  BUY                OSC:BUY    |   mAVE:STRONG_BUY                  OSC:  MACD BUY,                  []                
         BP # BUY: [w/o stockastic]
--------------------------------------------------------------------
   BTU       25.95        2.77    %  BUY                OSC:NEUTRAL|   mAVE:STRONG_BUY                  OSC:  W%R SELL, MACD BUY,        []                
         BTU # BUY: [w/o stockastic], BUY: [w stockastic]
--------------------------------------------------------------------
   COP       107.5        2.83    %  STRONG_BUY         OSC:BUY    |   mAVE:STRONG_BUY                  OSC:  MACD BUY,                  []                
--------------------------------------------------------------------
   CVX       169.31       1.81    %  BUY                OSC:NEUTRAL         |   mAVE:STRONG_BUY                  OSC:  MACD SELL,                 []                
--------------------------------------------------------------------
   DVN       62.5         1.56    %  BUY                OSC:BUY    |   mAVE:STRONG_BUY                  OSC:  MACD BUY,                  []                
         DVN # BUY: [w/o stockastic]
--------------------------------------------------------------------
   EOG       124.51       2.89    %  STRONG_BUY         OSC:BUY    |   mAVE:STRONG_BUY                  OSC:  MACD BUY,                  [3/24/2022,Downgrades,TD Securities ]   
         EOG # BUY: GOOD [WR 14 cross to overbought], BUY: [w/o stockastic]
--------------------------------------------------------------------
   EXC       45.51        2.34    %  STRONG_BUY         OSC:BUY    |   mAVE:STRONG_BUY                  OSC:  MACD BUY,                  []                
         EXC # BUY: EARLY [MACD CROSS]
--------------------------------------------------------------------
   HAL       21.91        0.97    %  BUY                OSC:BUY    |   mAVE:STRONG_BUY                  OSC:  MACD BUY,                  []                
--------------------------------------------------------------------
   LNG       149.3        5.46    %  STRONG_BUY         OSC:BUY    |   mAVE:STRONG_BUY                  OSC:  MACD BUY,                  []                
--------------------------------------------------------------------
   MGY       25.44        4.26    %  STRONG_BUY         OSC:BUY    |   mAVE:STRONG_BUY                  OSC:  MACD BUY,                  []                
--------------------------------------------------------------------
   MPC       6.92         -2.12   %  SELL               OSC:SELL   |   mAVE:SELL                        OSC:  MACD SELL,                 []                
--------------------------------------------------------------------
   MRO       26.04        2.00    %  BUY                OSC:NEUTRAL|   mAVE:STRONG_BUY                  OSC:  CCI SELL, MACD BUY,        []                
--------------------------------------------------------------------
   MUR       43.15        3.83    %  STRONG_BUY         OSC:BUY    |   mAVE:STRONG_BUY                  OSC:  CCI SELL, MACD BUY,        []                
--------------------------------------------------------------------
   NOG       29.36        5.65    %  STRONG_BUY         OSC:BUY    |   mAVE:STRONG_BUY                  OSC:  MACD BUY,                  [3/25/2022,Maintains,Raymond James ]   
--------------------------------------------------------------------
   OXY       58.71        1.66    %  BUY                OSC:NEUTRAL|   mAVE:STRONG_BUY                  OSC:  MACD SELL,                 []                
--------------------------------------------------------------------
   RIG       5.03         13.54   %  STRONG_BUY         OSC:BUY    |   mAVE:STRONG_BUY                  OSC:  MACD BUY,                  []                
--------------------------------------------------------------------
   SLB       43.68        2.44    %  STRONG_BUY         OSC:BUY    |   mAVE:STRONG_BUY                  OSC:  MACD BUY,                  []                
--------------------------------------------------------------------
   SM        42.48        6.71    %  STRONG_BUY         OSC:BUY    |   mAVE:STRONG_BUY                  OSC:  MACD BUY,                  []                
         SM # BUY: GOOD [CCI20 cross to upper level], BUY: [w/o stockastic], BUY: [w stockastic]
--------------------------------------------------------------------
   USO       80.74        1.24    %  BUY                OSC:NEUTRAL|   mAVE:STRONG_BUY                  OSC:  MACD BUY,                  []                
--------------------------------------------------------------------
   VDE       110.55       2.64    %  STRONG_BUY         OSC:BUY    |   mAVE:STRONG_BUY                  OSC:  MACD BUY,                  []                
         VDE # BUY: GOOD [CCI20 cross to upper level]
--------------------------------------------------------------------
   VLO       97.25        0.84    %  BUY                OSC:NEUTRAL|   mAVE:STRONG_BUY                  OSC:  CCI SELL, MACD BUY,        []                
         VLO # BUY: [w/o stockastic]
--------------------------------------------------------------------
   XLE       78.75        2.19    %  STRONG_BUY         OSC:BUY    |   mAVE:STRONG_BUY                  OSC:  MACD BUY,                  []                
         XLE # BUY: GOOD [CCI20 cross to upper level], BUY: GOOD [WR 14 cross to overbought], BUY: [w/o stockastic], BUY: [w stockastic], BUY: EARLY [MACD CROSS]
--------------------------------------------------------------------
   XOM       85.2         2.18    %  STRONG_BUY         OSC:BUY    |   mAVE:STRONG_BUY                  OSC:  MACD BUY,                  []                
         XOM # BUY: EARLY [MACD CROSS]
--------------------------------------------------------------------
   XOP       138.6        4.75    %  STRONG_BUY         OSC:BUY    |   mAVE:STRONG_BUY                  OSC:  MACD BUY,                  []


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
