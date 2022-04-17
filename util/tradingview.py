#############################
#####  TRADINGVIEW API  #####
#############################

from tradingview_ta import TA_Handler, Interval

interval = Interval.INTERVAL_1_DAY

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

