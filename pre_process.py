import pandas as pd
import numpy as np
import util as ut 
import re
from sklearn.preprocessing import MinMaxScaler

def process_dates(grouped_data, ticker):
    start_date = pd.to_datetime(str(grouped_data[ticker].index.values[0])).strftime("%Y/%m/%d")
    last_index = len(grouped_data[ticker].index.values) - 1
    end_date = pd.to_datetime(str(grouped_data[ticker].index.values[last_index])).strftime("%Y/%m/%d")
    dates = pd.date_range(start_date, end_date)
    return dates

def fill_missing_values(df):
    # Drop nan values if all are nan
    df.dropna(how="all", inplace=True)
    # Forward Fill
    df.fillna(method="ffill", inplace=True)
    # Backward Fill
    df.fillna(method="backfill", inplace=True)
    return df

def rename_col(col_list, ticker):
    regx = "adj"
    columns = {}
    for col in col_list:
        if col != 'adj_close':
            columns[col] = re.sub(regx, ticker, col)
        else:
            columns[col] = ticker     
    return columns    

def process_indicators(df):
    # Compute leading indicators
    mom, rsi = ut.leading_indicators(df)
    # Compute lagging indicators
    sma, trima, wma = ut.lagging_indicators(df)
    df["adj_mom"] = mom
    df["adj_rsi"] = rsi
    df["adj_sma"] = sma
    df["adj_trima"] = trima
    df["adj_wma"] = wma
    # add target
    df["adj_pred"] = df["adj_close"].shift(-7)
    return fill_missing_values(df)

def log_transform(x):
    mod = 1
    if np.sign(x) < 0:
        x = abs(x)
        mod = -1
    return mod * np.log(x + 1)

def verify_skewness(df):
    for feature in df.columns.values:
        skewness = df[feature].skew()
        if skewness < -1 or skewness > 1:
            print "high skewness for {}, skewness = {}".format(feature, skewness)
            # apply log  
            df[feature] = df[feature].apply(lambda x: log_transform(x)) 
            print "after transformation ", df[feature].skew()       
    return df

def normalize(raw_features, stock_ticker):
    print "verifying skewness for {}".format(stock_ticker)
    # Check for skewness and apply transformation if necessary
    features = verify_skewness(raw_features)
    scaler = MinMaxScaler()
    # normalize dataset
    data = scaler.fit_transform(features)
    normalized_df = pd.DataFrame(data=data, index=raw_features.index.values, columns=raw_features.columns.values)
    return normalized_df

def dataset(grouped_data, valid_tickers):
    date_index = process_dates(grouped_data, valid_tickers[0])
    df = pd.DataFrame(index=date_index)
    df.index.name = 'date'
    for stock_ticker in valid_tickers:
        temp_df = grouped_data[stock_ticker].copy()
        temp_df.drop("ticker", axis=1, inplace=True)
        # Compute and add technical indicators, target
        process_indicators(temp_df)
        # Drop target in order to normalize the features
        raw_features = temp_df.drop("adj_pred", axis=1)
        # Scale and prepare the dataset for model training 
        normalized_df = normalize(raw_features, stock_ticker)
        # add target to normalized data frame
        normalized_df["adj_pred"] = temp_df["adj_pred"] 
        normalized_df = normalized_df.rename(columns=rename_col(normalized_df.columns.values, stock_ticker))
        df = df.join(normalized_df)   
    return fill_missing_values(df)

# Debugger code
# import code
# code.interact(local=dict(globals(), **locals()))
