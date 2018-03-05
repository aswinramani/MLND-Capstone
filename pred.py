import pandas as pd
import util as ut

def show(use_default, ticker_list, period):
    tickers = ticker_list
    if use_default:
        tickers = ut.get_tickers(True, [])
        period =  7
    for ticker in tickers:
        df = pd.read_csv("predictions/{}.csv".format(ticker), index_col='date', nrows=period)           
        print df 
        print "\n"

# Debugger  code
# import code
# code.interact(local=dict(globals(), **locals()))