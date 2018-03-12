import os
import numpy as np
import pandas as pd
from time import time
import data.util as ut
from sklearn.model_selection import TimeSeriesSplit, GridSearchCV
from sklearn.linear_model import LinearRegression
from sklearn.kernel_ridge import KernelRidge
from sklearn.svm import SVR, LinearSVR
from sklearn.neural_network import MLPRegressor
from sklearn.metrics import r2_score, make_scorer
import warnings
warnings.filterwarnings(action="ignore", module="scipy", message="^internal gelsd")

def learners_list():
    lr = LinearRegression()
    lsvr = LinearSVR()
    krr = KernelRidge(kernel='rbf', gamma=0.1)
    svr = SVR(kernel='rbf', gamma=0.1, C=1e3)
    mlp = MLPRegressor(solver='lbfgs', shuffle=False)
    return [lr, lsvr, mlp, svr, krr]

def sample_train_predict(reg, X_train, y_train, X_test, y_test):
    # print reg
    start = time() # Get start time
    learner = reg.fit(X_train, y_train)                   
    end = time() # Get end time
    train_time = end - start

    start = time() # Get start time
    predictions_test = learner.predict(X_test)
    end = time() # Get end time
    pred_time = end - start
    # metrics
    r2 = r2_score(y_test, predictions_test)
    results = {
        "1_r2": r2,
        "2_train_time": train_time,
        "3_pred_time": pred_time
    }
    return results
     
def split(features, target):
    results = {}
    X = np.array(features)
    y = np.array(target)
    sample = []
    total_size = len(y)
    r2_score_results = {}
    for reg in learners_list():
        reg_name = reg.__class__.__name__
        results[reg_name] = {}
        tss = TimeSeriesSplit(n_splits=3)
        i = 0
        for train_index, test_index in tss.split(X, y=y):
            X_train, X_test = X[train_index], X[test_index]
            y_train, y_test = y[train_index], y[test_index]
            sample_size = int(round(round(len(y_train)+len(y_test), 2)/total_size, 2) * 100)
            results[reg_name][i] = sample_train_predict(reg, X_train, y_train, X_test, y_test)
            if sample_size == 100:
                r2_score_results[reg_name] = results[reg_name][i]["1_r2"]
            sample.append(sample_size)
            i += 1
    for i in results.items():
        print "\n" + i[0] + "\n"
        print pd.DataFrame(i[1]).rename(columns={0: str(sample[0])+"%", 1: str(sample[1])+"%", 2:str(sample[2])+"%"})
    return r2_score_results

def apply_grid_search(pred_alg, features, target, r2):
    X = np.array(features)
    y = np.array(target)
    pred_alg_name = pred_alg.keys()[0]
    total_size = len(y)
    non_linear = True
    for reg in learners_list():
        if reg.__class__.__name__ == pred_alg_name:
            regressor = reg
            if reg.__class__.__name__ == "KernelRidge":
                params = {"alpha": [1e0, 0.1, 1e-2, 1e-3],"gamma": np.logspace(-2, 2, 5)}
            elif reg.__class__.__name__ == "SVR":
                params =  {"C": [1e0, 1e1, 1e2, 1e3],"gamma": np.logspace(-2, 2, 5)}
            elif reg.__class__.__name__ == "MLPRegressor":
                params = {'solver' : ['lbfgs', 'sgd', 'adam'],"alpha": [1e0, 0.1, 1e-2, 1e-3], 'shuffle': [False]}
            else:
                non_linear = False 
    estimator = regressor
    if non_linear:            
        scorer = make_scorer(r2_score)             
        grid_obj = GridSearchCV(regressor, params, scoring=scorer)
        tss = TimeSeriesSplit(n_splits=2)
        for train_index, test_index in tss.split(X, y=y):
            X_train, X_test = X[train_index], X[test_index]
            y_train, y_test = y[train_index], y[test_index]
            sample_size = int(round(round(len(y_train)+len(y_test), 2)/total_size, 2) * 100)
            if sample_size == 100:
                grid_fit = grid_obj.fit(X_train, y_train)
                grid_predictions_test = grid_fit.predict(X_test)
                best_est_r2 = r2_score(y_test, grid_predictions_test)
        if best_est_r2 > r2:
            estimator = grid_fit.best_estimator_
        print "unoptimized ",  r2
        print "optimized ", best_est_r2
    return estimator

def split_train_results(results, features, target):
    alg = dict((key,value) for key, value in results.iteritems() if key != 'LinearRegression')
    max_val = max(alg.values())
    pred_alg = dict((key,value) for key, value in alg.iteritems() if value == max_val)
    estimator = apply_grid_search(pred_alg, features, target, max_val)
    return pred_alg, estimator

def predict(pred_alg, estimator, pred_dates, df_train, df_pred, target_col_name):
    ticker = target_col_name.split("_")[0]
    col_1 = ticker+'_LinearRegression'
    col_2 = ticker+'_'+pred_alg.keys()[0]
    df = pd.DataFrame(index=pred_dates, columns=[col_1, col_2])
    df.index.name = 'date'
    X_train = df_train.drop(target_col_name, axis=1)
    y_train = df_train[target_col_name]
    X_pred = df_pred.drop(target_col_name, axis=1)
    # Benchmark
    lin_reg = LinearRegression()
    lin_reg.fit(np.array(X_train), np.array(y_train))
    bm_predictions = lin_reg.predict(np.array(X_pred))
    df[col_1] = bm_predictions
    # Best Algorithm
    estimator.fit(np.array(X_train), np.array(y_train))
    pred_alg_predictions = estimator.predict(np.array(X_pred))                  
    df[col_2] = pred_alg_predictions
    file_name = "{}.csv".format(ticker)
    directory = '../predictions'
    if not os.path.exists(directory):
        os.mkdir(directory)
    file_path = os.path.join(directory, file_name)
    df.round(decimals=2).to_csv(file_path, encoding='utf-8')

def train_predict(df, ticker_list, default_tickers):
    for ticker in ticker_list:
        print "\nrunning model training for {}".format(ticker)
        cols = [col for col in df.columns if ticker in col]
        target_col_name = ticker+'_pred'
        df_train = df[cols].drop(df[cols].tail(7).index.values)
        df_pred = df[cols].tail(7)
        features = df_train.drop(target_col_name, axis=1)
        target = df_train[target_col_name]
        results = split(features, target)
        pred_alg, estimator = split_train_results(results, features, target)
        pred_dates = ut.get_pred_dates(df_pred.index.values[len(df_pred.index.values) - 1])
        predict(pred_alg, estimator, pred_dates, df_train, df_pred, target_col_name)
    if default_tickers:
        def_file = open("../predictions/default.py", "w")
        def_file.close() 
    else:
        directory = '../predictions'
        if os.path.exists(directory):
            file_name = "default.py"
            try:
                os.remove(os.path.join(directory, file_name))
            except OSError:
                pass    
            
# Debugger code
# import code
# code.interact(local=dict(globals(), **locals()))