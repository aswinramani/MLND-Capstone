# Stock Price Predictor

## Stock Price Prediction Using Technical Analysis

### Software and Libraries
This project uses the following software and Python libraries:

- [Python 2.7](https://www.python.org/download/releases/2.7/)
- [NumPy](http://www.numpy.org/)
- [Pandas](http://pandas.pydata.org/)
- [Scikit-Learn](http://scikit-learn.org/stable/)
- [Quandl](https://docs.quandl.com/)
- [TA-Lib](https://mrjbq7.github.io/ta-lib/)
- [Arrow](http://arrow.readthedocs.io/)

Please refer to the official websites of the above mentioned libraries to install them.

### Change the directory to src by typing this command
cd src

### Default Settings

To keep things simple, default stock tickers and time period have been implemented. Please follow the instructions given below.

#### Train models using default stock tickers and time period 
python main.py t 
#### Default query will return predictions for all tickers 
python main.py q

### Train models with stock tickers of your choice

python main.py t TICKER1 TICKER2 TICKER3 10y

python main.py q TICKER1 TICKER2 5

### Remove predictions

python main.py r

Note:

Months could be used as training time period as well. By default, if you mention 14 it would be considered as 14 months. 

The word "train" could be used inplace of t to train.

The word "query" could be used inplace of q to query.

The word "remove" could be used inplace of r to remove.



