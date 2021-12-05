#!/usr/bin/env python

from urllib.request import urlopen
import json
import time
import os
import sys
import pandas as pd

sys.path.insert(1, 'libs')
import avgpe

def quote(ticker, api_key):
    try:
        response = urlopen("https://financialmodelingprep.com/api/v3/quote/" + ticker + "?apikey=" + api_key)
    except HTTPError:
        time.sleep(1)
        response = urlopen("https://financialmodelingprep.com/api/v3/quote/" + ticker + "?apikey=" + api_key)
        
    data = json.loads(response.read().decode("utf-8"))
    
    if 'Error Message' in data:
        raise ValueError(data['Error Message'])
        
    return data

def getDirList(path):

    dir_content = os.listdir(path)
    
    return dir_content
    

if __name__ == '__main__':
    #f = open('/home/wunnakoko/.api/api_key','r')
    f = open('api_key','r')

    api_key = f.readline()

    path = 'data'

    tickers = getDirList(path)

    tick = None

    for ticker in tickers:
        if tick == None:
            tick = ticker
        else:
            tick = tick + ',' + ticker

    quotedata = quote(tick, api_key)
    
    pe_limit = 15.0
    
    result_list = []

    for data in quotedata:
        if (data['pe'] != None):
            result_list.append([data['symbol'], data['price'], data['pe'], avgpe.avg_pe(data['symbol'], data, api_key)])
    
    result_df = pd.DataFrame(result_list, columns = ['Ticker', 'Price', 'PE', 'WeightedAverage_PE'])
    
    final_df = result_df[(result_df['PE'] <= pe_limit) & (result_df['WeightedAverage_PE'] <= pe_limit) & (result_df['WeightedAverage_PE'] > 0)]
    
    print(final_df.reset_index())
    
