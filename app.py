import sys
import validations as validate
import util as ut
import pre_process
import model
import pred as predictions

def run():
    input_data = validate.input_data(sys.argv)
    if input_data["success"]:

        # /***** 1. Training *****/

        if input_data["train"]:
            use_default = input_data['period']['value'] <= 0
            if input_data["default"]:
                print input_data["message"]   
            start_date, end_date =  ut.get_dates(use_default, input_data['period']) 
            ticker_list = ut.get_tickers(input_data["default"], input_data['tickers'])   
            ticker_data = validate.stock_data(ut.get_data(ticker_list, start_date, end_date), ticker_list)
            if ticker_data["success"]:
                # Data Preprocessing
                normalized_df = pre_process.dataset(ticker_data["grouped_data"], ticker_data["valid_tickers"])
                # Model Training and Prediction 
                model.train_predict(normalized_df, ticker_data["valid_tickers"], input_data["default"])
            else:
                print ticker_data["error_message"]

        # /***** 2. Querying *****/

        elif input_data["query"]:
            
            if input_data["default"]:
                print input_data["message"] 
            predictions.show(input_data["default"], input_data['tickers'], input_data['period']['value'])

        # /***** 3. Removing *****/

        else:
            print input_data["message"]

    else:
        print input_data["error_message"]
    

if __name__ == '__main__':
    run()

# Debugger Code
# import code
# code.interact(local=dict(globals(), **locals()))