#!/usr/bin/env python

import json
import os.path

def ratios(ticker):

    file = 'data/'+ ticker + '/ratios.json'
    
    with open(file, 'r') as f:
        data = json.load(f)
    f.close()

    return data
    
def income_statement(ticker):

    file = 'data/'+ ticker + '/income_statement.json'
    
    with open(file, 'r') as f:
        data = json.load(f)
    f.close()

    return data

def balance_sheet_statement(ticker):

    file = 'data/'+ ticker + '/balance_sheet_statement.json'
    
    with open(file, 'r') as f:
        data = json.load(f)
    f.close()

    return data

def cashflow_statement(ticker):

    file = 'data/'+ ticker + '/cashflow_statement.json'
    
    with open(file, 'r') as f:
        data = json.load(f)
    f.close()

    return data

def key_metrics(ticker):

    file = 'data/'+ ticker + '/key_metrics.json'
    
    with open(file, 'r') as f:
        data = json.load(f)
    f.close()

    return data

def write(ticker, data, data_type):

    file = 'data/'+ ticker + '/' + data_type + '.json'
    
    if not os.path.exists(os.path.dirname(file)):
        try:
            os.makedirs(os.path.dirname(file))
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise
    
    with open(file, 'w+') as f:
        json.dump(data, f, indent=4)

    return