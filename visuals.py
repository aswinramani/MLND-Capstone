# import warnings
# warnings.filterwarnings("ignore", category = UserWarning, module = "matplotlib")

# from IPython import get_ipython
# get_ipython().run_line_magic('matplotlib', 'inline')

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def plot_data(df, title="Stock prices", xlabel="Date", ylabel="Prices", kind='line'):
    # plt.figure(figsize=(20,20))
    ax = df.plot(title=title, kind=kind)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.legend(loc='upper left')
    plt.show()

def plot_df(df):
    # x = np.array([0,1,2,3])
    # y = np.array([0.650, 0.660, 0.675, 0.685])
    # my_xticks = ['a', 'b', 'c', 'd']
    # plt.xticks(x, my_xticks)
    # plt.yticks(np.arange(y.min(), y.max(), 0.005))
    features = df.drop([df.columns.values[0], 'NextFortnightPrice'], axis=1)
    prices = df["NextFortnightPrice"]
    X = np.array(features)
    y = np.array(prices)
    X_col = features.columns.values
    plt.xticks(X, X_col)
    # plt.yticks
    plt.plot(X, y)
    # # ax.set_xlabel("Features")
    # # ax.set_ylabel("Prices")
    plt.legend(loc='upper left')
    plt.show()

def plot_histogram(df, feature):
    # for symbol in symbols:
    #     df[symbol].hist(bins=20, label=symbol)
    df.hist(bins=20, label=feature)
    plt.legend(loc='upper right')
    # Calculating mean and std dev in order to visulaize them.
    # mean = df['TSLA'].mean()
    # print "mean = ", mean
    # std = df['TSLA'].std()
    # print "std = ", std
    # print "kurtosis =", df.kurtosis()
    # print "correlation cofficient"
    # print df.corr(method='pearson')
    mean =  df.mean()
    std = df.std()
    skewness = df.skew()
    kurtosis = df.kurtosis()
    plt.axvline(mean, color='y', linestyle='dashed', linewidth=2)
    plt.axvline(mean + std, color='g', linestyle='dashed', linewidth=2)
    plt.axvline(mean - std, color='g', linestyle='dashed', linewidth=2)
    print "mean ", mean
    print "std ", std
    print "skewness ", skewness
    print "kurtosis ", kurtosis 

    # plt.axvline(kurtosis, color='r', linestyle='dashed', linewidth=2)
    # plt.axvline(-kurtosis, color='r', linestyle='dashed', linewidth=2)
    # Histogram for Daily Returns
    plt.show()

# def distribution(data, transformed = False):
#     """
#     Visualization code for displaying skewed distributions of features
#     """
    
#     # Create figure
#     # fig = plt.figure(figsize = (11,5))
#     fig = plt.figure(figsize = (6,5))
#     # f_l = ['MSFT_volume','MSFT_obv']
#     f_l = ['MSFT_obv', 'MSFT_volume']
#     #  'MSFT_high', 'MSFT_volume', 'MSFT',
#     #    'MSFT_sma', 'MSFT_trima', 'MSFT_wma', 'MSFT_dema', 'MSFT_tema',
#     #    'MSFT_t3', 'MSFT_mom', 'MSFT_ppo', 'MSFT_rsi', 'MSFT_cci',
#     #    'MSFT_ult', 'MSFT_mfi', 'MSFT_obv'
#     # Skewed feature plotting
#     for i, feature in enumerate(f_l):
#         ax = fig.add_subplot(1, 2, i+1)
#         ax.hist(data[feature], bins = 25, color = '#00A0A0')
#         ax.set_title("'%s' Feature Distribution"%(feature), fontsize = 14)
#         ax.set_xlabel("Value")
#         ax.set_ylabel("Number of Records")
#         ax.set_ylim((0, 2000))
#         ax.set_yticks([0, 500, 1000, 1500, 2000])
#         ax.set_yticklabels([0, 500, 1000, 1500, ">2000"])

#     # Plot aesthetics
#     if transformed:
#         fig.suptitle("Log-transformed Distributions of Continuous Census Data Features", \
#             fontsize = 16, y = 1.03)
#     else:
#         fig.suptitle("Skewed Distributions of Continuous Census Data Features", \
#             fontsize = 16, y = 1.03)

#     fig.tight_layout()
#     fig.show()