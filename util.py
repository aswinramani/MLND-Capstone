import arrow
import pandas as pd
import numpy as np
import quandl
from talib import SMA, TRIMA, WMA, MOM, RSI
quandl.ApiConfig.api_key = "APIKEY" 

def get_tickers(use_default, tickers):
    # Default tickers
    if use_default or len(tickers) == 0:
        tickers = ["MSFT", "PG", "INTC", "JNJ", "AAPL"]
    return tickers

def get_dates(use_default=True, period={}):
    default_date_format = "YYYY-MM-DD" 
    today = arrow.now()
    # Default Dates for training 
    start_date = today.replace(years=-10, days=-1).format(default_date_format)
    if not use_default: 
        if period["months"]:
            start_date = today.replace(months=-period["value"], days=-1).format(default_date_format)
        elif period["years"]:
            start_date = today.replace(years=-period["value"], days=-1).format(default_date_format)
    end_date = today.replace(days=-1).format(default_date_format)
    # Convert unicode string to string
    return str(start_date), str(end_date) 

def get_global_stats(values):
    global_mean = values.mean()
    global_std = values.std()
    return global_mean, global_std

def lagging_indicators(df):
    adj_close = np.array(df['adj_close'])
    n_days = 21
    sma = SMA(adj_close, timeperiod=n_days)
    trima = TRIMA(adj_close, timeperiod=n_days)
    wma = WMA(adj_close, timeperiod=n_days)
    return sma, trima, wma

def leading_indicators(df):
    adj_close = np.array(df['adj_close'])
    mom = MOM(adj_close, timeperiod=10)
    rsi = RSI(adj_close, timeperiod=14)
    return mom, rsi

def get_normalized_data(df):
    return df/df.ix[0,:] 

def get_data(tickers, start_date, end_date):
    columns = ["date", "ticker","adj_open", "adj_low", "adj_high", "adj_close"]
    data = quandl.get_table("WIKI/PRICES", qopts = { "columns": columns }, ticker = tickers, date = { "gte": start_date, "lte": end_date }, paginate=True)
    return data

def stringify(group):
    stringify_group = [str(i).strip() for i in group]
    return stringify_group

def verify_day(train_end_date):
    end_date = arrow.get(train_end_date)
    end_day = str(end_date.format('dddd'))
    d_format = "YYYY-MM-DD"
    if end_day == "Monday":
        day = {1:1, 2:2, 3:3, 4:4, 5:7, 6:8, 7:9}
    elif end_day == "Tuesday":
        day = {1:1, 2:2, 3:3, 4:6, 5:7, 6:8, 7:9}
    elif end_day == "Wednesday":
        day = {1:1, 2:2, 3:5, 4:6, 5:7, 6:8, 7:9}
    elif end_day == "Thursday":
        day = {1:1, 2:4, 3:5, 4:6, 5:7, 6:8, 7:11}
    elif end_day == "Friday":
        day = {1:3, 2:4, 3:5, 4:6, 5:7, 6:10, 7:11}
    else:
        day = {1:1, 2:2, 3:3, 4:4, 5:5, 6:6, 7:7}
        print "Error: unexpected training end day"        
    dates = []
    for i in range(len(day)):
        dates.append(np.datetime64(end_date.replace(days=day[i+1]).format(d_format)))
    return dates

def get_pred_dates(train_end_date):
    conv_train_end_date = pd.to_datetime(str(train_end_date)).strftime("%Y-%m-%d") 
    dates = verify_day(conv_train_end_date)
    return dates

# Debugger Code
# import code
# code.interact(local=dict(globals(), **locals()))