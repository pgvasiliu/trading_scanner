# trading_scanner

INSTALL dependencies:

```bash
dnf install python3-requests  python3-colorama python3-beautifulsoup4   # or pip3 install requests colorama beautifulsoup4
pip3 install tradingview_ta
```
 

```bash

--------------------------------------------------------------------
   BCE       70.35       STRONG_BUY         OSC:BUY       mAVE:STRONG_BUY                  OSC:  MACD BUY,                  []                
--------------------------------------------------------------------
   CP        98.91       BUY                OSC:NEUTRAL   mAVE:STRONG_BUY                  OSC:  CCI SELL, MACD BUY,        []                
--------------------------------------------------------------------
   GRT.UN    94.8        BUY                OSC:BUY       mAVE:BUY                         OSC:  MACD BUY,                  []                
--------------------------------------------------------------------
   HXE       26.45       BUY                OSC:NEUTRAL   mAVE:STRONG_BUY                  OSC:  MACD BUY,                  []                
--------------------------------------------------------------------
   L         114.75      BUY                OSC:SELL      mAVE:STRONG_BUY                  OSC:  W%R SELL, CCI SELL, MACD BUY, RSI SELL,   []                
--------------------------------------------------------------------
   NEO       15.79       SELL               OSC:NEUTRAL   mAVE:SELL                        OSC:  MACD BUY,                  []                
--------------------------------------------------------------------
   PD        85.84       BUY                OSC:NEUTRAL   mAVE:STRONG_BUY                  OSC:  CCI SELL, MACD BUY,        []                
--------------------------------------------------------------------
   SRU.UN    32.93       STRONG_BUY         OSC:NEUTRAL   mAVE:STRONG_BUY                  OSC:  W%R SELL, MACD BUY,        []                
--------------------------------------------------------------------
   SSRM      28.34       BUY                OSC:NEUTRAL   mAVE:STRONG_BUY                  OSC:  CCI SELL, MACD BUY,        []                
--------------------------------------------------------------------
   VUN       73.32       STRONG_SELL        OSC:SELL      mAVE:STRONG_SELL                 OSC:  MACD SELL,                 []                
--------------------------------------------------------------------
   ZEB       40.4        SELL               OSC:SELL      mAVE:SELL                        OSC:  MACD SELL,                 []                
--------------------------------------------------------------------
   ZUB       33.57       SELL               OSC:SELL      mAVE:STRONG_SELL                 OSC:  MACD SELL,                 [] 



$ ./scanner.py config_tickers_us.json

--------------------------------------------------------------------
   WFC       48.47       SELL               OSC:SELL      mAVE:STRONG_SELL                 OSC:  MACD SELL,                 []                
--------------------------------------------------------------------
   XLE       76.85       BUY                OSC:NEUTRAL   mAVE:STRONG_BUY                  OSC:  CCI SELL, MACD BUY,        []                
--------------------------------------------------------------------
   XLK       144.06      STRONG_SELL        OSC:NEUTRAL   mAVE:STRONG_SELL                 OSC:  CCI BUY, MACD SELL,        []                
--------------------------------------------------------------------
   XLP       71.44       STRONG_SELL        OSC:NEUTRAL   mAVE:STRONG_SELL                 OSC:  CCI BUY, MACD SELL,        []                
--------------------------------------------------------------------
   XLU       70.43       BUY                OSC:NEUTRAL   mAVE:STRONG_BUY                  OSC:  CCI SELL, MACD BUY,        []                
--------------------------------------------------------------------
   XOM       84.92       BUY                OSC:NEUTRAL   mAVE:STRONG_BUY                  OSC:  CCI SELL, MACD BUY,        [3/11/2022,Maintains,Wells Fargo ]


$ ./scanner.py config_tickers_canada.json  config_tickers_us.json

[ .... ]



$ curl -L https://datahub.io/core/s-and-p-500-companies/r/0.csv -o /tmp/sp500.csv

```

