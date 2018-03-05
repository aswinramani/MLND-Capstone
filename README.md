# Machine Learning Engineer Nanodegree

## Build a Stock Price Predictor

### List of Important Libraries that were used for this project

1. Pandas (DataFrame data structure and its functions)
2. Numpy (Arrays, DateTime objects, Log Transformation)
3. Quandl (Stock data)
4. TA-Lib (For computing Technical Indicators)
5. Sklearn  (MinMaxScaler, Algorithms, R-squared score, GridSearchCV, TimeSeriesSplit) 
6. Arrow (uses training period to figure out the start and end dates)

Please refer to the official websites of the above mentioned libraries to install them.

### Default Settings

To keep things simple, default stock tickers and time period have been implemented. Please follow the instructions given below.

#### Train models using default stock tickers and time period 
python app.py t 
#### Default query will return predictions for all tickers 
python app.py q

### Train models with stock tickers of your choice

python app.py t TICKER1 TICKER2 TICKER3 10y
python app.py q TICKER1 TICKER2 5

### Remove predictions

python app.py r

Note:

Months could be used as training time period as well. By default, if you mention 14 it would be considered as 14 months. 

The word "train" could be used inplace of t to train.

The word "query" could be used inplace of q to query.

The word "remove" could be used inplace of r to remove.



