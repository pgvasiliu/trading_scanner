# trading_scanner

## Install dependencies

### Fedora

```bash
$ dnf install python3-requests  python3-colorama python3-beautifulsoup4
$ pip3 install tradingview_ta lxml
```

### Pip

```bash
$ pip3 install --user lxml requests colorama beautifulsoup4 tradingview_ta
```

## TODO

- [ ] Resistance / support levels
- [ ] Earnings date
- [ ] TEMA ( 30 ) indicator. TradingView does not return TEMA via the API so we are going to use yahoo to calculate tema.

## Example runs

```bash
$ ./scanner.py config_tickers_canada.json

--------------------------------------------------------------------
   BCE       67.66        0.03    %  NEUTRAL            OSC:NEUTRAL         |   mAVE:NEUTRAL                     OSC:  W%R BUY, MACD SELL,        []                
--------------------------------------------------------------------
   CP        102.85       0.29    %  BUY                OSC:NEUTRAL         |   mAVE:STRONG_BUY                  OSC:  W%R SELL, MACD BUY,        []                
--------------------------------------------------------------------
SELL: CCI crossing -20 from above
   GRT.UN    96.6         -1.20   %  BUY                OSC:NEUTRAL         |   mAVE:STRONG_BUY                  OSC:  MACD BUY,                  []                
--------------------------------------------------------------------
   HXE       27.01        -0.11   %  BUY                OSC:SELL            |   mAVE:STRONG_BUY                  OSC:  W%R SELL, CCI SELL, MACD BUY,   []                
--------------------------------------------------------------------
   L         109.52       -0.83   %  BUY                OSC:SELL            |   mAVE:STRONG_BUY                  OSC:  MACD SELL,                 []                
--------------------------------------------------------------------
   MFC       26.13        -0.04   %  BUY                OSC:NEUTRAL         |   mAVE:STRONG_BUY                  OSC:  CCI SELL, MACD BUY, Stoch.RSI SELL,   []                
--------------------------------------------------------------------
   NEO       16.35        0.12    %  NEUTRAL            OSC:NEUTRAL         |   mAVE:NEUTRAL                     OSC:  MACD BUY,                  []                
--------------------------------------------------------------------
   PD        86.21        -0.51   %  BUY                OSC:SELL            |   mAVE:STRONG_BUY                  OSC:  W%R SELL, CCI SELL, MACD SELL,   []                
--------------------------------------------------------------------
   SRU.UN    32.78        -0.82   %  BUY                OSC:NEUTRAL         |   mAVE:STRONG_BUY                  OSC:  MACD BUY,                  []                
--------------------------------------------------------------------
   SSRM      27.53        0.95    %  BUY                OSC:SELL            |   mAVE:STRONG_BUY                  OSC:  MACD SELL,                 []                
--------------------------------------------------------------------
   VUN       77.36        1.10    %  BUY                OSC:BUY             |   mAVE:BUY                         OSC:  MACD BUY,                  []                
--------------------------------------------------------------------
   ZEB       40.77        0.00    %  NEUTRAL                     OSC:BUY    |   mAVE:SELL                        OSC:  MACD BUY,                  []                
--------------------------------------------------------------------
   ZUB       35.22        0.31    %  SELL               OSC:NEUTRAL         |   mAVE:SELL                        OSC:  MACD BUY,                  []                
--------------------------------------------------------------------


$ ./scanner.py config_tickers_us.json
--------------------------------------------------------------------
BUY no stockastic
BUY w stockastic
   AAPL      174.07       2.27    %  STRONG_BUY         OSC:BUY     |   mAVE:STRONG_BUY                  OSC:  MACD BUY,                  []                
--------------------------------------------------------------------
   ABBV      160.28       1.17    %  BUY                OSC:NEUTRAL |   mAVE:STRONG_BUY                  OSC:  CCI SELL, MACD BUY,        []                
--------------------------------------------------------------------
   ADBE      432.14       2.18    %  SELL               OSC:NEUTRAL |   mAVE:STRONG_SELL                 OSC:  MACD BUY,                  [3/24/2022,Maintains,Goldman Sachs 3/23/2022,Maintains,Oppenheimer 3/23/2022,Maintains,Jefferies 3/23/2022,Maintains,Deutsche Bank 3/23/2022,Maintains,Morgan Stanley ]   
--------------------------------------------------------------------
BUY: AMAZING: EMA10/EMA20 CROSS
   AMD       120.53       5.80    %  BUY                OSC:BUY     |   mAVE:STRONG_BUY                  OSC:  MACD BUY, Stoch.RSI SELL,   []                
--------------------------------------------------------------------
BUY no stockastic
   AMZN      3272.99      0.15    %  BUY                OSC:NEUTRAL |   mAVE:STRONG_BUY                  OSC:  CCI SELL, MACD BUY,        []                
--------------------------------------------------------------------
BUY no stockastic
   APA       40.78        0.17    %  BUY                OSC:NEUTRAL |   mAVE:STRONG_BUY                  OSC:  CCI SELL, MACD BUY,        [3/24/2022,Maintains,Keybanc ]   
--------------------------------------------------------------------
   AXP       188.89       1.54    %  BUY                OSC:BUY     |   mAVE:STRONG_BUY                  OSC:  MACD BUY,                  []                
--------------------------------------------------------------------
SELL: CCI crossing -20 from above
   BKR       38.29        1.86    %  BUY                OSC:NEUTRAL |   mAVE:STRONG_BUY                  OSC:  MACD BUY,                  []                
--------------------------------------------------------------------
   BMO       118.79       0.87    %  BUY                OSC:BUY     |   mAVE:STRONG_BUY                  OSC:  MACD BUY,                  []                
--------------------------------------------------------------------
   BNS       72.78        0.57    %  BUY                OSC:BUY     |   mAVE:STRONG_BUY                  OSC:  MACD BUY,                  []                
--------------------------------------------------------------------
   CAT       222.21       0.02    %  BUY                OSC:NEUTRAL |   mAVE:STRONG_BUY                  OSC:  W%R SELL, MACD BUY,        []                
--------------------------------------------------------------------
   CNQ       63.01        -0.38   %  BUY                OSC:SELL    |   mAVE:STRONG_BUY                  OSC:  W%R SELL, CCI SELL, MACD BUY,   []                
--------------------------------------------------------------------
BUY no stockastic
   COST      558.11       0.74    %  BUY                OSC:NEUTRAL |   mAVE:STRONG_BUY                  OSC:  CCI SELL, MACD BUY,        []                
--------------------------------------------------------------------
BUY: EARLY ---> MACD CROSS
   CVE       16.07        -0.62   %  BUY                OSC:NEUTRAL |   mAVE:STRONG_BUY                  OSC:  MACD BUY,                  []                
--------------------------------------------------------------------
   CVS       108.05       1.74    %  STRONG_BUY         OSC:BUY     |   mAVE:STRONG_BUY                  OSC:  MACD BUY,                  []                
--------------------------------------------------------------------
   DE        432.22       0.16    %  BUY                OSC:NEUTRAL |   mAVE:STRONG_BUY                  OSC:  CCI SELL, MACD BUY,        []                
--------------------------------------------------------------------
   F         16.83        0.90    %  SELL               OSC:NEUTRAL |   mAVE:SELL                        OSC:  MACD BUY,                  []                
--------------------------------------------------------------------
BUY no stockastic
   FB        219.57       2.86    %  BUY                OSC:BUY     |   mAVE:NEUTRAL                              OSC:  MACD BUY,                  []                
--------------------------------------------------------------------
BUY no stockastic
   GOOG      2826.24      2.03    %  STRONG_BUY         OSC:BUY     |   mAVE:STRONG_BUY                  OSC:  MACD BUY,                  []                
--------------------------------------------------------------------
   HD        315.78       -0.40   %  STRONG_SELL        OSC:NEUTRAL |   mAVE:STRONG_SELL                 OSC:  MACD BUY,                  []                
--------------------------------------------------------------------
BUY no stockastic
   ITOT      100.72       1.12    %  BUY                OSC:NEUTRAL |   mAVE:STRONG_BUY                  OSC:  CCI SELL, MACD BUY,        []                
--------------------------------------------------------------------
   JNJ       175.24       0.52    %  STRONG_BUY         OSC:BUY     |   mAVE:STRONG_BUY                  OSC:  MACD BUY,                  []                
--------------------------------------------------------------------
   KBWB      66.33        0.68    %  SELL               OSC:NEUTRAL |   mAVE:SELL                        OSC:  MACD BUY,                  []                
--------------------------------------------------------------------
   KO        60.98        0.96    %  BUY                OSC:BUY     |   mAVE:STRONG_BUY                  OSC:  MACD BUY,                  []                
--------------------------------------------------------------------
   KR        56.75        0.53    %  BUY                OSC:SELL    |   mAVE:STRONG_BUY                  OSC:  MACD SELL,                 []                
--------------------------------------------------------------------
   KRE       70.46        0.97    %  SELL               OSC:BUY     |   mAVE:STRONG_SELL                 OSC:  MACD BUY,                  []                
--------------------------------------------------------------------
   M         26.35        2.41    %  BUY                OSC:BUY     |   mAVE:STRONG_BUY                  OSC:  MACD BUY,                  []                
--------------------------------------------------------------------
   MCD       240.26       1.75    %  NEUTRAL            OSC:BUY     |   mAVE:NEUTRAL                     OSC:  MACD BUY,                  []                
--------------------------------------------------------------------
BUY no stockastic
   MPC       81.39        1.16    %  BUY                OSC:NEUTRAL |   mAVE:STRONG_BUY                  OSC:  MACD BUY,                  []                
--------------------------------------------------------------------
   MRO       25.53        -0.20   %  BUY                OSC:SELL    |   mAVE:STRONG_BUY                  OSC:  W%R SELL, CCI SELL, MACD BUY,   []                
--------------------------------------------------------------------
BUY no stockastic
   MSFT      304.1        1.54    %  BUY                OSC:BUY     |   mAVE:STRONG_BUY                  OSC:  MACD BUY,                  []                
--------------------------------------------------------------------
BUY no stockastic
   NVDA      281.5        9.82    %  STRONG_BUY         OSC:BUY     |   mAVE:STRONG_BUY                  OSC:  MACD BUY,                  []                
--------------------------------------------------------------------
   OKTA      144.5        -2.73   %  SELL               OSC:NEUTRAL |   mAVE:STRONG_SELL                 OSC:  W%R BUY, MACD SELL,        []                
--------------------------------------------------------------------
BUY no stockastic
   ORCL      82.24        2.30    %  BUY                OSC:BUY     |   mAVE:BUY                         OSC:  MACD BUY,                  []                
--------------------------------------------------------------------
   OXY       57.75        -3.49   %  BUY                OSC:SELL    |   mAVE:STRONG_BUY                  OSC:  MACD SELL,                 []                
--------------------------------------------------------------------
   PG        151.08       0.17    %  NEUTRAL            OSC:NEUTRAL |   mAVE:SELL                        OSC:  MACD BUY,                  []                
--------------------------------------------------------------------
   RY        112.21       0.45    %  BUY                OSC:NEUTRAL |   mAVE:STRONG_BUY                  OSC:  MACD BUY,                  []                
--------------------------------------------------------------------
   SCHD      78.7         0.95    %  BUY                OSC:BUY     |   mAVE:STRONG_BUY                  OSC:  MACD BUY,                  []                
--------------------------------------------------------------------
BUY: AMAZING: EMA10/EMA20 CROSS
   SHOP      705          0.20    %  NEUTRAL            OSC:BUY     |   mAVE:SELL                        OSC:  MACD BUY,                  []                
--------------------------------------------------------------------
BUY: EARLY ---> MACD CROSS
   SLB       42.64        0.54    %  BUY                OSC:NEUTRAL |   mAVE:STRONG_BUY                  OSC:  MACD BUY,                  []                
--------------------------------------------------------------------
   SNOW      227.57       2.40    %  NEUTRAL            OSC:NEUTRAL |   mAVE:SELL                        OSC:  MACD BUY,                  [3/24/2022,Maintains,Truist Securities ]   
--------------------------------------------------------------------
BUY no stockastic
   SPY       450.49       1.51    %  BUY                OSC:BUY     |   mAVE:STRONG_BUY                  OSC:  MACD BUY,                  []                
--------------------------------------------------------------------
   TD        80.59        0.21    %  BUY                OSC:BUY     |   mAVE:STRONG_BUY                  OSC:  MACD BUY,                  []                
--------------------------------------------------------------------
BUY no stockastic
   TSLA      1013.92      1.48    %  BUY                OSC:NEUTRAL |   mAVE:STRONG_BUY                  OSC:  CCI SELL, MACD BUY,        []                
--------------------------------------------------------------------
   UAA       17.27        1.89    %  BUY                OSC:BUY     |   mAVE:BUY                         OSC:  MACD BUY,                  []                
--------------------------------------------------------------------
   V         217.31       1.23    %  BUY                OSC:BUY     |   mAVE:STRONG_BUY                  OSC:  MACD BUY,                  []                
--------------------------------------------------------------------
BUY no stockastic
   VLO       96.44        0.96    %  BUY                OSC:NEUTRAL |   mAVE:STRONG_BUY                  OSC:  CCI SELL, MACD BUY,        []                
--------------------------------------------------------------------
BUY no stockastic
   VTI       227.12       1.42    %  BUY                OSC:BUY     |   mAVE:STRONG_BUY                  OSC:  MACD BUY,                  []                
--------------------------------------------------------------------
BUY no stockastic
   VYM       112.48       0.99    %  STRONG_BUY         OSC:BUY     |   mAVE:STRONG_BUY                  OSC:  MACD BUY,                  []                
--------------------------------------------------------------------
   WFC       51.33        0.41    %  NEUTRAL            OSC:NEUTRAL |   mAVE:SELL                        OSC:  MACD BUY,                  []                
--------------------------------------------------------------------
   WMT       142.83       0.62    %  BUY                OSC:NEUTRAL |   mAVE:STRONG_BUY                  OSC:  MACD BUY,                  []                
--------------------------------------------------------------------
   XLE       77.06        0.25    %  BUY                OSC:SELL    |   mAVE:STRONG_BUY                  OSC:  MACD SELL,                 []                
--------------------------------------------------------------------
BUY no stockastic
   XLK       158.31       2.60    %  STRONG_BUY         OSC:BUY     |   mAVE:STRONG_BUY                  OSC:  MACD BUY,                  []                
--------------------------------------------------------------------
   XLP       74.42        0.70    %  BUY                OSC:NEUTRAL |   mAVE:BUY                         OSC:  MACD BUY,                  []                
--------------------------------------------------------------------
   XLU       71.74        1.03    %  STRONG_BUY         OSC:BUY     |   mAVE:STRONG_BUY                  OSC:  MACD BUY,                  []                
--------------------------------------------------------------------
   XOM       83.38        0.30    %  BUY                OSC:SELL    |   mAVE:STRONG_BUY                  OSC:  MACD SELL,                 []                
--------------------------------------------------------------------


$ curl -L https://datahub.io/core/s-and-p-500-companies/r/0.csv -o /tmp/sp500.csv

```
