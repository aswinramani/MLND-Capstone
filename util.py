import arrow
import pandas as pd
import numpy as np
import quandl
from talib import SMA, TRIMA, WMA, DEMA, TEMA, T3, MOM, PPO, CCI, MFI, RSI, ULTOSC, OBV, ADOSC
import code
quandl.ApiConfig.api_key = "APIKEY" 

def get_tickers(use_default, tickers):
    # Default tickers
    if use_default or len(tickers) == 0:
        tickers = ["MSFT", "PG", "INTC", "JNJ", "AAPL"]
        # tickers = ["AAPL"]
    return tickers

def get_dates(use_default=True, period={}):
    default_date_format = "YYYY-MM-DD" 
    today = arrow.now()
    # print "today ", today
    # Default Dates for training 
    start_date = today.replace(years=-5, days=-1).format(default_date_format)
    if not use_default: 
        # print "period, \n", period
        if period["months"]:
            start_date = today.replace(months=-period["value"], days=-1).format(default_date_format)
        elif period["years"]:
            start_date = today.replace(years=-period["value"], days=-1).format(default_date_format)
    end_date = today.replace(days=-1).format(default_date_format)
    # Convert unicode string to string
    return str(start_date), str(end_date) 
    # return "2017-01-01", "2017-12-31"


# def np_to_df(np_array, df, col_list=[]):
    # if len(col_list) > 0:
    #     new_df = pd.DataFrame(data=np_array, index=df.index.values, columns=col_list)
    # else:
def np_to_df(np_array, df):    
    new_df = pd.DataFrame(data=np_array, index=df.index.values)
    return new_df

def get_global_stats(values):
    global_mean = values.mean()
    global_std = values.std()
    return global_mean, global_std

def overlap_studies(df):
    adj_close = np.array(df['adj_close'])
    n_days = 20
    sma = SMA(adj_close, timeperiod=n_days)
    trima = TRIMA(adj_close, timeperiod=n_days)
    wma = WMA(adj_close, timeperiod=n_days)
    dema = DEMA(adj_close, timeperiod=7)
    tema = TEMA(adj_close, timeperiod=5)
    t3 = T3(adj_close, timeperiod=3, vfactor=0.7)
    return sma, trima, wma, dema, tema, t3

def momentum_indicators(df):
    # adj_high = np.array(df["adj_high"])
    # adj_low = np.array(df["adj_low"])
    adj_close = np.array(df['adj_close'])
    # adj_volume = np.array(df['adj_volume'])
    mom = MOM(adj_close, timeperiod=13)
    # ppo = PPO(adj_close, fastperiod=9, slowperiod=21, matype=0)
    ppo = PPO(adj_close, fastperiod=5, slowperiod=14, matype=0)
    rsi = RSI(adj_close, timeperiod=13)
    # cci = CCI(adj_high, adj_low, adj_close, timeperiod=14)
    # ult = ULTOSC(adj_high, adj_low, adj_close, timeperiod1=10, timeperiod2=12, timeperiod3=13)
    # mfi = MFI(adj_high, adj_low, adj_close, adj_volume, timeperiod=13)
    return mom, ppo, rsi#, cci, ult, mfi 

def volume_indicators(df):
    adj_low = np.array(df["adj_low"])
    adj_high = np.array(df["adj_high"]) 
    adj_close = np.array(df['adj_close'])
    adj_volume = np.array(df['adj_volume'])
    obv = OBV(adj_close, adj_volume)
    chaikin_osc = ADOSC(adj_high, adj_low, adj_close, adj_volume, fastperiod=5, slowperiod=14)
    return obv, chaikin_osc

def get_normalized_data(df):
    return df/df.ix[0,:] 

def get_data(tickers, start_date, end_date):
    # columns = ["date", "ticker", "adj_open", "adj_low", "adj_high", "adj_volume", "adj_close"]
    columns = ["date", "ticker","adj_open", "adj_low", "adj_high", "adj_close"]
    data = quandl.get_table("WIKI/PRICES", qopts = { "columns": columns }, ticker = tickers, date = { "gte": start_date, "lte": end_date })
    # print data.head()
    return data

def stringify(group):
    stringify_group = [str(i).strip() for i in group]
    return stringify_group

def verify_day(train_end_date):
    # train_end_date = "2018-02-22"
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