#!/usr/bin/env python

import json
from urllib.request import urlopen

#f = open('/home/wunnakoko/.api/api_key','r')
f = open('api_key','r')

api_key = f.readline()

def ratios(ticker, period="annual"):

    response = urlopen("https://financialmodelingprep.com/api/v3/ratios/" +
                       ticker + "?limit=40&apikey=" + api_key)
    data = json.loads(response.read().decode("utf-8"))
    
    return data


def income_statement(ticker, period="annual"):

    response = urlopen("https://financialmodelingprep.com/api/v3/income-statement/" +
                       ticker + "?period=" + period + "&apikey=" + api_key)
    data = json.loads(response.read().decode("utf-8"))
    
    return data


def balance_sheet_statement(ticker, period="annual"):

    response = urlopen("https://financialmodelingprep.com/api/v3/balance-sheet-statement/" +
                       ticker + "?period=" + period + "&apikey=" + api_key)
    data = json.loads(response.read().decode("utf-8"))
    
    return data

def cashflow_statement(ticker, period="annual"):

    response = urlopen("https://financialmodelingprep.com/api/v3/cash-flow-statement/" +
                       ticker + "?period=" + period + "&apikey=" + api_key)
    data = json.loads(response.read().decode("utf-8"))
    
    return data

def key_metrics(ticker, period="annual"):

    response = urlopen("https://financialmodelingprep.com/api/v3/key-metrics/" +
                       ticker + "?period=" + period + "&apikey=" + api_key)
    data = json.loads(response.read().decode("utf-8"))
    
    return data