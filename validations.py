import os
import shutil
import util as ut

def duration(last_element, train=True):
    period = {}
    period['value'] = 0
    period['valid'] = True
    period["train"] = train
    if train:
        period['years'] = False
        period['months'] = False
        try:
            period['value'] = int(last_element)
            period['months'] = True
            if period['value'] > 180 or period['value'] < 60:
                period['valid'] = False
        except ValueError:
            split_input_m = last_element.split('m')
            split_input_y = last_element.split('y')
            if len(split_input_m) > 1:
                try: 
                    period['value'] = int(split_input_m[0])
                except ValueError:
                    period['valid'] = False
                if period['valid']:
                    period['months'] = True
                    if period['value'] > 180 or period['value'] < 60:
                        period['valid'] = False
            elif len(split_input_y) > 1:
                try:
                    period['value'] = int(split_input_y[0])
                except ValueError:
                    period['valid'] = False
                if period['valid']:
                    period['years'] = True
                    if period['value'] > 15 or period['value'] < 5:
                        period['valid'] = False
            else:
                period['valid'] = False
    else:
        period["exceed_limit"] = False
        try:
            period['value'] = int(last_element)
        except ValueError:
            split_input_d = last_element.split('d')
            if len(split_input_d) > 1:
                try:
                    period['value'] = int(split_input_d[0])
                except ValueError:
                    period['valid'] = False
            else:
                period['valid'] = False
        if period['valid']:
            if period['value'] > 7 or period['value'] < 1:
                period["exceed_limit"] = True
                period['valid'] = False
    return period

def group(symbols, ticker_keys):
    stringify_group = ut.stringify(ticker_keys)
    error_message = "Dataset not available for "
    err_list = []
    ticker = {}
    valid_list = []
    ticker["unavailable"] = False
    for symbol in symbols:
        if symbol in stringify_group:
            valid_list.append(symbol)
        else:    
            err_list.append(symbol)
            ticker["unavailable"] = True
    length = len(err_list)
    if length == 1:
        error_message += err_list[0]
    elif length > 1:
        err_item = ""
        for index, value in enumerate(err_list):
            err_item +=  str(index+1) +". " + str(value) + "\n"
        error_message += "\n" + err_item
    ticker["list"] = valid_list    
    ticker["error_message"] = error_message
    return ticker

def qi_tickers(input_list):
    valid = True
    error_message = ""
    if len(input_list) > 2:
        new_ls = list(input_list)
        first_element = input_list[0]
        last_index = len(new_ls) - 1
        last_element = new_ls[last_index]
        new_ls.remove(first_element)
        new_ls.remove(last_element)
        valid_list = []
        for input_item in new_ls:
            for fyle in os.listdir('./predictions'):
                if fyle.endswith(".csv"):
                    if fyle.startswith(input_item):
                        valid_list.append(input_item)
        valid = len(new_ls) == len(valid_list)
        if not valid:
            set1 = set(new_ls)
            set2 = set(valid_list)
            unmatched = list(set1.symmetric_difference(set2)) 
            if len(unmatched) > 1:
                error_message += "invalid tickers \n"
                i = 1
                for unmatched_item in unmatched:
                    error_message += str(i)+". " + unmatched_item + "\n"
                    i+= 1
            else:
                error_message += "invalid ticker {}".format(unmatched[0])
    else:
        error_message += "please mention tickers for querying"
        valid = False
    tickers = {
        "valid": valid,
        "error_message": error_message
    }
    return tickers

def query_interface(input_list):
    value = 0
    valid = True
    use_default = False
    error_message = ""
    directory = './predictions'
    if os.path.exists(directory):
        if len(input_list) > 1:
            last_index = len(input_list) - 1
            period = duration(input_list[last_index], False)
            value = period["value"]
            if not period["valid"]:
                valid = False
                if period["exceed_limit"]:
                    error_message = "invalid querying period min-> 1 max--> 7"
                else:
                    error_message = "please mention stock tickers and querying period properly"
            tickers = qi_tickers(input_list)
            if not tickers["valid"]:
                valid =  False
                error_message = tickers["error_message"]
        elif len(input_list) > 0:
            import sys
            sys.path.insert(0,'./predictions')
            try:
                import default
                use_default = True
            except ImportError:
                error_message = "please mention ticker symbols for querying"
                valid = False
    else:
        error_message = "please train before querying"
        valid = False
    query = {
        "value": value,
        "valid": valid,
        "use_default": use_default,
        "error_message": error_message
    }
    return query

def input_data(input_list):
    train = True
    query = False
    remove = False
    success = True
    default = False
    error_message = "Error: "
    message = None
    period = {}
    period["value"] = 0
    input_list.remove(input_list[0])
    # print "length ", len(input_list)
    if len(input_list) > 1 and len(input_list) < 8:
        if input_list[0] == 't' or input_list[0] == 'train':
            last_index = len(input_list) - 1
            period = duration(input_list[last_index])
            if period['valid']:
                if period['value'] > 0:
                    input_list.remove(input_list[last_index])
            else:
            # if not period['valid']:
                if period["months"]:
                    error_message += "Min value for months --> 60 and Max --> 180"
                    success = False
                elif period["years"]:
                    error_message += "Min value for years --> 5 and Max --> 15"
                    success = False
                else:    
                    error_message += "please mention training period"
                    success = False
        elif input_list[0] == 'q' or input_list[0] == 'query':
            qi = query_interface(input_list)
            period["value"] = qi["value"]
            train = False
            query = True
            if qi["valid"]:
                last_index = len(input_list) - 1
                input_list.remove(input_list[last_index])
            else:
                error_message += qi["error_message"] 
                success = False                
        else:
            error_message +=  "please mention if you want to train or query. "
            success = False
    elif len(input_list) > 7:
        line_1 =  "Exceeded Maximum permissible arguments\n"
        line_2 =  "Enter a maximum of 7 inputs consisting of\n"
        line_3 = "1.input for mentioning training or query \n 2. Ticker symbols(max 5 allowed),\n 3. Training period"#, and \n3. Prediction Period"
        error_message += line_1 + line_2 + line_3
        success = False
    elif len(input_list) > 0 and ( input_list[0] == 't' or input_list[0] == 'train' ):
        message = "Using default ticker symbols and date range. "
        default = True
    elif len(input_list) > 0 and ( input_list[0] == 'q' or input_list[0] == 'query' ):
        train = False
        query = True
        qi = query_interface(input_list)
        if not qi["valid"]:
            error_message += qi["error_message"] 
            success = False
        elif qi["use_default"]:
            message = "Using default querying"
            default = qi["use_default"]
    elif len(input_list) > 0 and ( input_list[0] == 'r' or input_list[0] == 'remove' ):
        remove = True
        train = False
        try: 
            shutil.rmtree("./predictions")
            message = "Predicted files have been removed successfully"
        except OSError:
            error_message += "oops! no predictions have been made yet..."
            success = False
    else:
        error_message +=  "please mention if you want to train or query. "
        success = False   
    if success:
        input_list.remove(input_list[0])     
    input_data = {}   
    input_data["train"] = train
    input_data["query"] = query
    input_data["remove"] = remove
    input_data["tickers"] = input_list
    input_data["period"] = period
    input_data["default"] = default
    input_data["success"] = success
    input_data["message"] = message
    input_data["error_message"] = error_message
    return input_data

def stock_data(data, ticker_list):
    success = True
    error_message = None
    value = []
    if not data.empty:
        data.set_index(keys='date', inplace=True)
        grouped_data = dict(tuple(data.groupby(by='ticker')))
        ticker = group(ticker_list, grouped_data.keys())
        if ticker["unavailable"]:
            error_message = ticker["error_message"]
            success = False
        else:
           value = ticker["list"]      
    else:
        success = False
        error_message = "Dataset not available for all ticker symbols"
    
    ticker_data = {
        "success": success,
        "valid_tickers": value,
        "error_message": error_message,
        "list": data,
        "grouped_data": grouped_data
    }
    return ticker_data

def learner_names(reg):
    reg_name = reg.__class__.__name__
    try:
        reg_name += "_" + reg.__dict__['kernel'] 
    except KeyError:
        try:
            reg_name += "_" + str(reg.__dict__['n_neighbors'])
        except KeyError:
            try:
                reg_name += "_" + str(reg.__dict__['base_estimator'])
            except KeyError:
                try:
                    reg_name += "_" + str(reg.__dict__['solver'])
                except KeyError:
                    pass
                pass
            pass
    return reg_name   