#!/usr/bin/env python

try:
    # For Python 3.0 and later
    from urllib.request import urlopen
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import urlopen

import json
import pandas as pd
import sys


def technical_indicator(ticker, api_key, period, type = "ema"):
    response = urlopen("https://financialmodelingprep.com/api/v3/technical_indicator/daily/" + ticker + "?period=" + period + "&type=" + type + "&apikey=" + api_key)
    data = json.loads(response.read().decode("utf-8"))

    if 'Error Message' in data:
        raise ValueError(data['Error Message'])
        
    data_formatted = {}
    for value in data:
        date = value['date']
        
        del value['date']
        data_formatted[date] = value
    
    return pd.DataFrame(data_formatted)


try:
    ticker = sys.argv[1].upper()
except:
    print('usage : '+__file__+' <ticker>')
    sys.exit(1)

api_key = "4d1d8612c6f15e10c2a2327977f81d43"

techindicator = technical_indicator(ticker, api_key, "12")

techindicator.loc['%'] = (techindicator.loc['close']-techindicator.loc['ema'])*100/techindicator.loc['close']

print(techindicator.T.head())