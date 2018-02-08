import sys
import code
import pandas as pd 
import validations as validate
import util as ut
# import visuals as vs

def run():
    input_data = validate.input_data(sys.argv)
    if input_data['success']:
        use_default = input_data['period']['value'] <= 0
        if input_data["default"]:
            print input_data["def_message"]   
        start_date, end_date =  ut.get_dates(use_default, input_data['period']) 
        ticker_list = ut.get_tickers(input_data["default"], input_data['tickers'])   
        ticker_data = validate.stock_data(ut.get_data(ticker_list, start_date, end_date), ticker_list)
        # Debugger Code
        # code.interact(local=dict(globals(), **locals()))
        if ticker_data["success"]:
            print ticker_data["list"].head()
        else:
            print ticker_data["error_message"]
        # vs.plot_data(get_normalized_data(df_data))
 
              
    else:
        print input_data["error_message"]
    

if __name__ == '__main__':
    run()