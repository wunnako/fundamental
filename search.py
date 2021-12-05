#!/usr/bin/env python

try:
    # For Python 3.0 and later
    from urllib.request import urlopen
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import urlopen

import json
import time
import os
import sys

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

for data in quotedata:
    if (data['pe'] != None and data['pe'] < 20):
#		avgpe.avg_pe(data['symbol'], quotedata))
        print(data['symbol'] + '\t' + str(data['price']) + '\t' + str(data['pe']) + '\t' + str(avgpe.avg_pe(data['symbol'], data, api_key)))
    
