#!/usr/bin/env python

import json
import os.path
import pull

ticker = input("Ticker = ").upper()

data_type = ['ratios','balance_sheet_statement','cashflow_statement','income_statement','key_metrics']

for type in data_type:

    file = 'data/'+ ticker + '/' + type + '.json'
     
    data = []

    with open(file, 'r') as f:
        data = json.load(f)
    f.close()    
    
    if type == 'ratios':
        data1 = pull.ratios(ticker)
    if type == 'income_statement':
        data1 = pull.income_statement(ticker)
    if type == 'balance_sheet_statement':
        data1 = pull.balance_sheet_statement(ticker)
    if type == 'key_metrics':
        data1 = pull.key_metrics(ticker)
    if type == 'cashflow_statement':
        data1 = pull.cashflow_statement(ticker)

    date_array = []

    for value in data:    
        date_array.append(value['date'])

    print(date_array)
    print(data1)

    for value in data1:
        if value['date'] in date_array:
            print("exists")
        else:
            data.append(value)
            
    data = sorted(data, key=lambda k: k['date'], reverse=True)

    with open(file, 'w') as f:
        json.dump(data, f, indent=4)