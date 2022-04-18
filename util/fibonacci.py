
def fib_retracement(p1, p2):
    list =[0, 0.236, 0.382, 0.5, 0.618, 0.786, 1, 1.618, 2.618, 3.618, 4.236]
    dict = {}
    dist = p2 - p1
    for val in list:
        dict[str(val) ] =  "%.2f" % (p2 - dist*val)
    return dict
#Fibonacci Retracement ends here

def fib (symbol):
    #import pandas as pd
    from util.yahoo        import download_yahoo

    data = download_yahoo ( symbol )
    #Calculate the max and min close price
    maximum_price = data['Close'].max()
    minimum_price = data['Close'].min()

    #print ( minimum_price, maximum_price )

    #print ( fib_retracement ( maximum_price, minimum_price ) )
    return fib_retracement ( maximum_price, minimum_price )

