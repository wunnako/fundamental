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

def date_correction(date):

    date = int(date)
    date -= 1
    date = str(date)

    return date

def quote(ticker, api_key):
    response = urlopen("https://financialmodelingprep.com/api/v3/quote/" + ticker + "?apikey=" + api_key)
    data = json.loads(response.read().decode("utf-8"))

    if 'Error Message' in data:
        raise ValueError(data['Error Message'])
        
    data_formatted = {}
    for value in data:
        data_formatted = value
    
    return data_formatted

def income_statement(ticker, api_key, period="annual"):
    response = urlopen("https://financialmodelingprep.com/api/v3/income-statement/" +
                       ticker + "?period=" + period + "&apikey=" + api_key)
    data = json.loads(response.read().decode("utf-8"))

    if 'Error Message' in data:
        raise ValueError(data['Error Message'])
        
    data_formatted = {}
    
    for value in data:
        if period == "quarter":
            date = value['date'][:7]
        else:
            date = value['date'][:4]
            month = value['date'][5:7]
            if month == "01":
                date = date_correction(date)

        del value['date']
        del value['symbol']

        data_formatted[date] = value

    return pd.DataFrame(data_formatted)

def balance_sheet_statement(ticker, api_key, period="annual"):
    response = urlopen("https://financialmodelingprep.com/api/v3/balance-sheet-statement/" +
                       ticker + "?period=" + period + "&apikey=" + api_key)
    data = json.loads(response.read().decode("utf-8"))

    if 'Error Message' in data:
        raise ValueError(data['Error Message'])
        
    data_formatted = {}
    
    for value in data:
        if period == "quarter":
            date = value['date'][:7]
        else:
            date = value['date'][:4]
            month = value['date'][5:7]
            if month == "01":
                date = date_correction(date)

        del value['date']
        del value['symbol']

        data_formatted[date] = value

    return pd.DataFrame(data_formatted)

def cashflow_statement(ticker, api_key, period="annual"):
    response = urlopen("https://financialmodelingprep.com/api/v3/cash-flow-statement/" +
                       ticker + "?period=" + period + "&apikey=" + api_key)
    data = json.loads(response.read().decode("utf-8"))

    if 'Error Message' in data:
        raise ValueError(data['Error Message'])
        
    data_formatted = {}
    
    for value in data:
        if period == "quarter":
            date = value['date'][:7]
        else:
            date = value['date'][:4]
            month = value['date'][5:7]
            if month == "01":
                date = date_correction(date)

        del value['date']
        del value['symbol']

        data_formatted[date] = value

    return pd.DataFrame(data_formatted)

def market_cap(ticker, api_key):
    response = urlopen("https://financialmodelingprep.com/api/v3/market-capitalization/" + ticker + "?apikey=" + api_key)

    data = json.loads(response.read().decode("utf=8"))

    if 'Error Message' in data:
        raise ValueError(data['Error Message'])

    data_formatted = ()

    for value in data:
        data_formatted = value


    return data_formatted


def ratios(ticker, api_key, period="annual"):
    response = urlopen("https://financialmodelingprep.com/api/v3/ratios/" +
                       ticker + "?limit=40&apikey=" + api_key)
    data = json.loads(response.read().decode("utf-8"))

    if 'Error Message' in data:
        raise ValueError(data['Error Message'])
        
    data_formatted = {}
    
    for value in data:
        if period == "quarter":
            date = value['date'][:7]
        else:
            date = value['date'][:4]
            month = value['date'][5:7]
            if month == "01":
                date = date_correction(date)

        del value['date']
        del value['symbol']

        data_formatted[date] = value

    return pd.DataFrame(data_formatted)
    
def key_metrics_ttm(ticker, api_key):
    """
    Description
    ----
    Gives information about key metrics of a company overtime which includes
    i.a. PE ratio, Debt to Equity, Dividend Yield and Average Inventory.

    Input
    ----
    ticker (string)
        The company ticker (for example: "NFLX")
    api_key (string)
        The API Key obtained from https://financialmodelingprep.com/developer/docs/
    period (string)
        Data period, this can be "annual" or "quarter".

    Output
    ----
    data (dataframe)
        Data with variables in rows and the period in columns.
    """
    response = urlopen("https://financialmodelingprep.com/api/v3/key-metrics-ttm/" + ticker + "?apikey=" + api_key)
    data = json.loads(response.read().decode("utf-8"))

    if 'Error Message' in data:
        raise ValueError(data['Error Message'])

    data_formatted = {}
    for value in data:
        data_formatted = value

    return data_formatted
	
def discounted_cash_flow(cf, growth=15, discountrate=6, n=10):

	dcf = cf
	
	for i in range(n):
		cf = cf*(pow((1+(growth/100)),1))
		dcf += cf/(pow((1+(discountrate/100)),(i+1)))

	return dcf

def key_metrics(ticker, api_key, period="annual"):
    """
    Description
    ----
    Gives information about key metrics of a company overtime which includes
    i.a. PE ratio, Debt to Equity, Dividend Yield and Average Inventory.

    Input
    ----
    ticker (string)
        The company ticker (for example: "NFLX")
    api_key (string)
        The API Key obtained from https://financialmodelingprep.com/developer/docs/
    period (string)
        Data period, this can be "annual" or "quarter".

    Output
    ----
    data (dataframe)
        Data with variables in rows and the period in columns.
    """
    response = urlopen("https://financialmodelingprep.com/api/v3/key-metrics/" +
                       ticker + "?period=" + period + "&apikey=" + api_key)
    data = json.loads(response.read().decode("utf-8"))

    if 'Error Message' in data:
        raise ValueError(data['Error Message'])

    data_formatted = {}
    for value in data:
        if period == "quarter":
            date = value['date'][:7]
        else:
            date = value['date'][:4]
            month = value['date'][5:7]
            if month == "01":
                date = date_correction(date)

        del value['date']
        del value['symbol']

        data_formatted[date] = value

    return pd.DataFrame(data_formatted)

f = open('/home/wunnakoko/.api/api_key','r')

api_key = f.readline()

try:
    ticker = sys.argv[1].upper()
except:
    print('usage : '+__file__+' <ticker>')
    sys.exit(1)

print(ticker)

growth = int(input("Estimated Growth % "))

quotedata = quote(ticker, api_key)

marketcap = market_cap(ticker, api_key)

print('name             ' + str(quotedata['name']))
print('price            ' + "${:,.2f}".format(quotedata['price']))
print('pe               ' + str(quotedata['pe']))
print('market cap       ' + "${:,.2f}".format(marketcap['marketCap']))

incomestatement = income_statement(ticker, api_key)

bsstatement = balance_sheet_statement(ticker, api_key)

debttoearning = pd.DataFrame()

debttoearning['netIncome'] = incomestatement.loc['netIncome']

debttoearning['longTermDebt'] = bsstatement.loc['longTermDebt']

debttoearning['DebtToEarning'] = debttoearning['longTermDebt']/debttoearning['netIncome']

debttoearning = debttoearning.T

ratio = ratios(ticker, api_key)

debttoearning = debttoearning.append(ratio.loc[['currentRatio','freeCashFlowPerShare','returnOnEquity','returnOnCapitalEmployed','returnOnAssets'], : ])

keymetrics = key_metrics(ticker, api_key)

#debttoearning = debttoearning.append(keymetrics.loc[['returnOnTangibleAssets','tangibleBookValuePerShare'], : ])

debttoearning.loc['EPS'] = incomestatement.loc['netIncome']/quotedata['sharesOutstanding']

debttoearning.loc['PE Ratio'] = quotedata['price']/debttoearning.loc['EPS']

debttoearning.loc['ROE %'] = debttoearning.loc['returnOnEquity']*100

debttoearning.loc['ROIC %'] = debttoearning.loc['returnOnCapitalEmployed']*100

debttoearning.loc['ROA %'] = debttoearning.loc['returnOnAssets']*100

debttoearning.loc['ZambiValuePerShare'] = (bsstatement.loc['totalStockholdersEquity'] - bsstatement.loc['goodwillAndIntangibleAssets'] - bsstatement.loc['totalLiabilities'])/quotedata['sharesOutstanding']

cashflowstatement = cashflow_statement(ticker, api_key)

if growth > 0:
	debttoearning.loc["IntrinsicValue(DCF)"] = discounted_cash_flow(ratio.loc['freeCashFlowPerShare'], growth)
else:
	debttoearning.loc["IntrinsicValue(DCF)"] = discounted_cash_flow(ratio.loc['freeCashFlowPerShare'])

debttoearning.loc["IntrinsicValue(10X)"] = ((incomestatement.loc['incomeBeforeTax'] + cashflowstatement.loc['depreciationAndAmortization'] + cashflowstatement.loc['accountsPayables'] + cashflowstatement.loc['accountsReceivables'] + (cashflowstatement.loc['capitalExpenditure']/2))/quotedata['sharesOutstanding']) * 10

print(debttoearning)

#print(incomestatement.loc['incomeBeforeTax'])

#print(cashflowstatement.loc[['depreciationAndAmortization','accountsPayables','accountsReceivables','capitalExpenditure'],:])
