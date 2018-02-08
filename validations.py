def duration(last_element):
    period = {}
    period['value'] = 0
    period['years'] = False
    period['months'] = False
    period['valid'] = True
    # period['min'] = False 
    # period['max'] = False
    try:
        period['value'] = int(last_element)
        period['months'] = True
    except ValueError:
        split_input_m = last_element.split('m')
        split_input_y = last_element.split('y')
        if len(split_input_m) > 1:
            period['value'] = int(split_input_m[0])
            period['months'] = True
        elif len(split_input_y) > 1:
            period['value'] = int(split_input_y[0])
            period['years'] = True
        else:
            period['valid'] = False
    return period

def group(symbols, group):
    stringify_group = [str(i).strip() for i in group]
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

def input_data(input_list):
    success = True
    default = False
    error_message = "Error: "
    def_message = None
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
                error_message += "please mention training period"
                success = False
        elif input_list[0] == 'q' or input_list[0] == 'query':
            error_message +=  "query logic needs to be implemented"
            success = False
        else:
            error_message +=  "please mention if you want to train or query. "
            success = False
    elif len(input_list) > 7:
        line_1 =  "Exceeded Maximum permissible arguments\n"
        line_2 =  "Enter a maximum of 7 inputs consisting of\n"
        line_3 = "1.input for mentioning training or query\n 2. Ticker symbols(max 5 allowed),\n 3. Training period"#, and \n3. Prediction Period"
        error_message += line_1 + line_2 + line_3
        success = False
    elif len(input_list) > 0:
        def_message = "Using default ticker symbols and date range. "
        default = True    
    else:
        error_message +=  "please mention if you want to train or query. "
        success = False   
    if success:
        input_list.remove(input_list[0])     
    input_data = {}   
    input_data["tickers"] = input_list
    input_data["period"] = period
    input_data["default"] = default
    input_data["success"] = success
    input_data["def_message"] = def_message
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
        "list": data
    }
    return ticker_data