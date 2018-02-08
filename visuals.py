# import warnings
# warnings.filterwarnings("ignore", category = UserWarning, module = "matplotlib")

# from IPython import get_ipython
# get_ipython().run_line_magic('matplotlib', 'inline')

import pandas as pd
import matplotlib.pyplot as plt

def plot_data(df, title="Stock prices", xlabel="Date", ylabel="Prices", kind='line'):
    # plt.figure(figsize=(20,20))
    ax = df.plot(title=title, kind=kind)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.legend(loc='upper left')
    plt.show()

def distribution(data, transformed = False):
    """
    Visualization code for displaying skewed distributions of features
    """
    
    # Create figure
    fig = plt.figure(figsize = (11,5));

    # Skewed feature plotting
    # for i, feature in enumerate(['capital-gain','capital-loss']):
    col_list = list(data.columns.values)
    # print col_list
    # print type(col_list)
    for i, feature in enumerate(list(data.columns.values)):
        # print " data[feature] ", data[feature]
        # print "i ", i
        # print "shape ", data[feature].shape
        # rows = data[feature].shape[0]
        # cols = data[feature].shape[1]

        ax = fig.add_subplot(1, 1, 1)
        ax.hist(data[feature], bins = 25, color = '#00A0A0')
        ax.set_title("'%s' Feature Distribution"%(feature), fontsize = 14)
        # ax.set_xlabel("Value")
        # ax.set_ylabel("Number of Records")
        ax.set_xlabel("Dates")
        ax.set_ylabel("Prices")
        # ax.set_ylim((0, 2000))
        # ax.set_yticks([0, 500, 1000, 1500, 2000])
        # ax.set_yticklabels([0, 500, 1000, 1500, ">2000"])

    # Plot aesthetics
    # if transformed:
    #     fig.suptitle("Log-transformed Distributions of Continuous Census Data Features", \
    #         fontsize = 16, y = 1.03)
    # else:
        # fig.suptitle("Skewed Distributions of Continuous Census Data Features", \
        #     fontsize = 16, y = 1.03)

    fig.tight_layout()
    fig.show()