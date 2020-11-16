#!/usr/bin/env python

import json
from urllib.request import urlopen

def date_correction(date):

    date = int(date)
    date -= 1
    date = str(date)

    return date

def ratios(ticker, api_key, period="annual"):
    response = urlopen("https://financialmodelingprep.com/api/v3/ratios/" +
                       ticker + "?limit=40&apikey=" + api_key)
    data = json.loads(response.read().decode("utf-8"))
    
    return data
