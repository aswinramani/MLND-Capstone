import arrow
import pandas as pd
import quandl
quandl.ApiConfig.api_key = "APIKEY"

def get_tickers(use_default, tickers):
    # Default tickers
    if use_default or len(tickers) == 0:
        tickers = ['AAPL', 'MSFT', 'TWTR', 'FB', 'TSLA']
    return tickers

def get_dates(use_default=True, period={}):
    default_date_format = 'YYYY-MM-DD' 
    today = arrow.now()
    # print "today ", today
    # Default Dates for training 
    start_date = today.replace(years=-1).format(default_date_format)
    if not use_default: 
        # print "period, \n", period
        if period["months"]:
            start_date = today.replace(months=-period["value"]).format(default_date_format)
        elif period["years"]:
            start_date = today.replace(years=-period["value"]).format(default_date_format)
    end_date = today.replace(days=-1).format(default_date_format)
    # Convert unicode string to string
    return str(start_date), str(end_date)    

def get_rolling_stats(values, window=20):
    rolling_obj = values.rolling(window=window, center=False)
    roll_mean = rolling_obj.mean()
    roll_std = rolling_obj.std()
    upper_band = roll_mean + (roll_std*2)
    lower_band = roll_mean - (roll_std*2)
    return roll_mean, roll_std, upper_band, lower_band

def get_normalized_data(df):
    return df/df.ix[0,:] 

def get_data(tickers, start_date, end_date):
    data = quandl.get_table('WIKI/PRICES', qopts = { 'columns': ['date', 'ticker', 'adj_close'] }, ticker = tickers, date = { 'gte': start_date, 'lte': end_date })
    # data = quandl.get_table('WIKI/PRICES', qopts = { 'columns': ['date', 'ticker', 'adj_close'] }, ticker = ['gthj', 'ajhabj'], date = { 'gte': '2016-02-05', 'lte': '2017-02-04' })
    # print data.head()
    return data

# def get_file_path(symbol):  
#     return "data/{}.csv".format(symbol)

# def get_data(symbols, dates):
#     df =  pd.DataFrame(index=dates)
#     for symbol in symbols:
#         file_path = get_file_path(symbol)
#         data_df = pd.read_csv(file_path, index_col='Date', parse_dates=True,  usecols=['Date', 'Adj Close'], na_values=['nan', 'NaN', 'null', 'NULL'])       
#         data_df = data_df.rename(columns={'Adj Close': symbol})
#         df = df.join(data_df)
#     # # Step 1a Drop NaN values
#     df = df.dropna(how="all")
#     df.fillna(method="ffill", inplace=True)
#     # Backward Fill
#     df.fillna(method="bfill", inplace=True)    
#     return df