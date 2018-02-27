import code
import os
import numpy as np
import pandas as pd
import validations as validate
from time import time
import util as ut
from sklearn.model_selection import TimeSeriesSplit
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.svm import SVR
from sklearn.neural_network import MLPRegressor
# from sklearn.ensemble import AdaBoostRegressor, BaggingRegressor
from sklearn.metrics import mean_squared_error, r2_score, median_absolute_error
import warnings
warnings.filterwarnings(action="ignore", module="scipy", message="^internal gelsd")

def learners_list():
    # extra = ExtraTreesRegressor()
    lr = LinearRegression()
    # knn_a = KNeighborsRegressor()
    # dt = DecisionTreeRegressor()
    svr_l = SVR(kernel='linear')
    mlp = MLPRegressor(solver='lbfgs')
    # ada_l = AdaBoostRegressor(base_estimator=lr)
    # BaggingRegressor
    # ada_svr_l = AdaBoostRegressor(base_estimator=svr_l)
    # ada_mlp = AdaBoostRegressor(base_estimator=mlp)
    # mlp_b = MLPRegressor(shuffle=False)
    # mlp_c = MLPRegressor(solver="sgd", shuffle=False, learning_rate="invscaling", early_stopping=True, validation_fraction=0.2)
    # mlp_d = MLPRegressor(solver="sgd", shuffle=False, learning_rate="adaptive", early_stopping=True, validation_fraction=0.2)
    return [lr, svr_l, mlp]#, ada_l]
    # return [ada_l, ada_svr_l, ada_mlp]

def sample_train_predict(reg, X_train, y_train, X_test, y_test, sample_size):

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
    rmse = mean_squared_error(y_test, predictions_test)
    mae = median_absolute_error(y_test, predictions_test)
    # print "{} trained on {} samples.".format(learner.__class__.__name__, len(y_train))
    results = {
        "1_r2": r2,
        "2_rmse": rmse,
        "3_mae": mae,
        "4_train_time": train_time,
        "5_pred_time": pred_time,
    }
    return results
     
def split(features, target):
    results = {}
    X = np.array(features)
    y = np.array(target)
    sample = []
    total_size = len(y)
    r2_score_results = {}
    # print total_size
    for reg in learners_list():
        reg_name = reg.__class__.__name__
        # reg_name = validate.learner_names(reg)
        results[reg_name] = {}
        tss = TimeSeriesSplit(n_splits=3)
        i = 0
        for train_index, test_index in tss.split(X, y=y):
            # print "train_index {}, test_index {}".format(train_index, test_index) 
            X_train, X_test = X[train_index], X[test_index]
            y_train, y_test = y[train_index], y[test_index]
            sample_size = int(round(round(len(y_train)+len(y_test), 2)/total_size, 2) * 100)
            results[reg_name][i] = sample_train_predict(reg, X_train, y_train, X_test, y_test, sample_size)
            if sample_size == 100:
                r2_score_results[reg_name] = results[reg_name][i]["1_r2"]
            sample.append(sample_size)
            i += 1
    for i in results.items():
        print "\n" + i[0] + "\n"
        print pd.DataFrame(i[1]).rename(columns={0: str(sample[0])+"%", 1: str(sample[1])+"%", 2:str(sample[2])+"%"})
    return r2_score_results

def split_train_results(results):
    bench_mark = dict((key,value) for key, value in results.iteritems() if key == 'LinearRegression')
    alg = dict((key,value) for key, value in results.iteritems() if key != 'LinearRegression')
    max_val = max(alg.values())
    pred_alg = dict((key,value) for key, value in alg.iteritems() if value == max_val)
    return bench_mark, pred_alg

def predict(bench_mark, pred_alg, pred_dates, df_train, df_pred, target_col_name):
    ticker = target_col_name.split("_")[0]
    col_1 = ticker+'_'+bench_mark.keys()[0]
    col_2 = ticker+'_'+pred_alg.keys()[0]
    df = pd.DataFrame(index=pred_dates, columns=[col_1, col_2])
    df.index.name = 'date'
    X_train = df_train.drop(target_col_name, axis=1)
    y_train = df_train[target_col_name]
    X_pred = df_pred.drop(target_col_name, axis=1)
    for reg in learners_list():
        if reg.__class__.__name__ == bench_mark.keys()[0]:
            # print "\nbm ", bench_mark.keys()[0]
            reg.fit(np.array(X_train), np.array(y_train))
            bm_predictions = reg.predict(np.array(X_pred))
            df[col_1] = bm_predictions
        if reg.__class__.__name__ == pred_alg.keys()[0]:
            # print "\npred_alg", pred_alg.keys()[0]
            reg.fit(np.array(X_train), np.array(y_train))
            pred_alg_predictions = reg.predict(np.array(X_pred))
            df[col_2] = pred_alg_predictions
    file_name = "{}.csv".format(ticker)
    directory = './predictions'
    if not os.path.exists(directory):
        os.mkdir(directory)
    file_path = os.path.join(directory, file_name)
    df.round(decimals=2).to_csv(file_path, encoding='utf-8')
    # df.to_csv(file_path, sep='\t', encoding='utf-8')
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
        bench_mark, pred_alg = split_train_results(results)
        pred_dates = ut.get_pred_dates(df_pred.index.values[len(df_pred.index.values) - 1])
        predict(bench_mark, pred_alg, pred_dates, df_train, df_pred, target_col_name)
    if default_tickers:
        def_file = open("./predictions/default.py", "w")
        def_file.close() 
# Debugger code
# code.interact(local=dict(globals(), **locals()))