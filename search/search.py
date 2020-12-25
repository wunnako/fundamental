#!/usr/bin/env python

try:
    # For Python 3.0 and later
    from urllib.request import urlopen
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import urlopen

import json
import time

def quote(ticker, api_key):
    try:
        response = urlopen("https://financialmodelingprep.com/api/v3/quote/" + ticker + "?apikey=" + api_key)
    except HTTPError:
        time.sleep(1)
        response = urlopen("https://financialmodelingprep.com/api/v3/quote/" + ticker + "?apikey=" + api_key)
        
    data = json.loads(response.read().decode("utf-8"))

    if 'Error Message' in data:
        raise ValueError(data['Error Message'])
        
    data_formatted = {}
    for value in data:
        data_formatted = value
    
    return data_formatted

f = open('/home/wunnakoko/.api/api_key','r')
#f = open('api_key','r')

api_key = f.readline()

with open('tickerlist', 'r') as finput:
    tickers = finput.read().splitlines()

finput.close()

tickers = set(tickers)

print(tickers)

with open('tickerlist', 'w') as fout:
    for item in tickers:
        fout.write("%s\n" % item)

checklist = {}

for ticker in tickers:
    quotedata = quote(ticker, api_key)
    
    if quotedata['pe'] != None and quotedata['pe'] < 16:
        checklist[ticker] = quotedata['pe']

for check in checklist:
    print(check + '\t' + "{:,.2f}".format(checklist[check]))
