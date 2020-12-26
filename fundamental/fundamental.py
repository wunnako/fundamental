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
import getjson

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

def income_statement(ticker):

    data = getjson.request_json(ticker,'income_statement')

    if 'Error Message' in data:
        raise ValueError(data['Error Message'])
        
    data_formatted = {}
    
    for value in data:
        date = value['date'][:4]
        month = value['date'][5:7]
        if month == "01":
            date = date_correction(date)

        del value['date']
        del value['symbol']

        data_formatted[date] = value

    return pd.DataFrame(data_formatted)

def balance_sheet_statement(ticker):

    data = getjson.request_json(ticker,'balance_sheet_statement')
    
    if 'Error Message' in data:
        raise ValueError(data['Error Message'])
        
    data_formatted = {}
    
    for value in data:
        date = value['date'][:4]
        month = value['date'][5:7]
        if month == "01":
            date = date_correction(date)

        del value['date']
        del value['symbol']

        data_formatted[date] = value

    return pd.DataFrame(data_formatted)

def cashflow_statement(ticker):

    data = getjson.request_json(ticker,'cashflow_statement')

    if 'Error Message' in data:
        raise ValueError(data['Error Message'])
        
    data_formatted = {}
    
    for value in data:
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

def ratios(ticker):
    
    data = getjson.request_json(ticker,'ratios')

    if 'Error Message' in data:
        raise ValueError(data['Error Message'])
        
    data_formatted = {}
    
    for value in data:
        date = value['date'][:4]
        month = value['date'][5:7]
        if month == "01":
            date = date_correction(date)

        del value['date']
        del value['symbol']

        data_formatted[date] = value

    return pd.DataFrame(data_formatted)

    
def key_metrics_ttm(ticker, api_key):

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

def key_metrics(ticker):

    data = getjson.request_json(ticker,'key_metrics')
    
    if 'Error Message' in data:
        raise ValueError(data['Error Message'])

    data_formatted = {}
    for value in data:
        date = value['date'][:4]
        month = value['date'][5:7]
        if month == "01":
            date = date_correction(date)

        del value['date']
        del value['symbol']

        data_formatted[date] = value

    return pd.DataFrame(data_formatted)

f = open('/home/wunnakoko/.api/api_key','r')
#f = open('api_key','r')

api_key = f.readline()

try:
    ticker = sys.argv[1].upper()
except:
    print('usage : '+__file__+' <ticker>')
    sys.exit(1)

print(ticker)

growth = int(input("Estimated Growth % "))

if growth <= 0:
    growth = 0

discountrate = int(input("Discount Rate % "))

if discountrate <= 0:
    discountrate = 2

quotedata = quote(ticker, api_key)

keymetricsttm = key_metrics_ttm(ticker, api_key)

marketcap = market_cap(ticker, api_key)

print('Name                     ' + str(quotedata['name']))
print('Price                    ' + "${:,.2f}".format(quotedata['price']))
print('PE                       ' + str(quotedata['pe']))
print('Market Cap               ' + "${:,.2f}".format(marketcap['marketCap']))
print('Free Cash Flow Yield TTM ' + "{0:.2f}%".format(keymetricsttm['freeCashFlowYieldTTM']* 100))

incomestatement = income_statement(ticker)

bsstatement = balance_sheet_statement(ticker)

debttoearning = pd.DataFrame()

debttoearning['netIncome'] = incomestatement.loc['netIncome']

debttoearning['totalCurrentLiabilities'] = bsstatement.loc['totalCurrentLiabilities'].map('${:,.2f}'.format)

debttoearning['longTermDebt'] = bsstatement.loc['longTermDebt']

debttoearning['DebtToEarning'] = debttoearning['longTermDebt']/debttoearning['netIncome']

debttoearning = debttoearning.T

debttoearning.loc['netIncome'] = debttoearning.loc['netIncome'].map('${:,.2f}'.format)

debttoearning.loc['longTermDebt'] = debttoearning.loc['longTermDebt'].map('${:,.2f}'.format)

ratio = ratios(ticker)

debttoearning.loc['ROE %'] = (ratio.loc['returnOnEquity']*100).map('{0:.2f}%'.format)

debttoearning.loc['ROIC %'] = (ratio.loc['returnOnCapitalEmployed']*100).map('{0:.2f}%'.format)

debttoearning.loc['ROA %'] = (ratio.loc['returnOnAssets']*100).map('{0:.2f}%'.format)

debttoearning = debttoearning.append(ratio.loc[['currentRatio','freeCashFlowPerShare','priceToFreeCashFlowsRatio'], : ])

keymetrics = key_metrics(ticker)

#if bsstatement.loc['totalCurrentLiabilities'].astype(int) > 0 or bsstatement.loc['totalCurrentLiabilities'] != None:
debttoearning.loc['Acid Test'] = (bsstatement.loc['cashAndShortTermInvestments']+bsstatement.loc['netReceivables'])/bsstatement.loc['totalCurrentLiabilities']

debttoearning = debttoearning.append(keymetrics.loc[['returnOnTangibleAssets','tangibleBookValuePerShare'], : ])

debttoearning.loc['EPS'] = incomestatement.loc['netIncome']/quotedata['sharesOutstanding']

debttoearning.loc["Enterprise Earning Per Share"] = (incomestatement.loc["operatingIncome"] - incomestatement.loc["interestExpense"])/quotedata['sharesOutstanding']

debttoearning.loc['PE Ratio'] = quotedata['price']/debttoearning.loc['EPS']

debttoearning.loc['ZambiValuePerShare'] = (bsstatement.loc['totalStockholdersEquity'] - bsstatement.loc['goodwillAndIntangibleAssets'] - bsstatement.loc['totalLiabilities'])/quotedata['sharesOutstanding']

cashflowstatement = cashflow_statement(ticker)

debttoearning.loc["IntrinsicValue(DCF)"] = discounted_cash_flow(ratio.loc['freeCashFlowPerShare'], growth, discountrate)

debttoearning.loc["IntrinsicValue(10X)"] = ((incomestatement.loc['incomeBeforeTax'] + cashflowstatement.loc['depreciationAndAmortization'] + cashflowstatement.loc['accountsPayables'] + cashflowstatement.loc['accountsReceivables'] + (cashflowstatement.loc['capitalExpenditure']/2))/quotedata['sharesOutstanding']) * 10

# formatting

debttoearning.loc['EPS'] = debttoearning.loc['EPS'].map('${:,.2f}'.format)

debttoearning.loc["IntrinsicValue(10X)"] = debttoearning.loc["IntrinsicValue(10X)"].map('${:,.2f}'.format)

debttoearning.loc['Enterprise Earning Per Share'] = debttoearning.loc['Enterprise Earning Per Share'].map('${:,.2f}'.format)

debttoearning.loc['freeCashFlowPerShare'] = debttoearning.loc['freeCashFlowPerShare'].map('${:,.2f}'.format)

debttoearning.loc["IntrinsicValue(DCF)"] = debttoearning.loc["IntrinsicValue(DCF)"].map('${:,.2f}'.format)

debttoearning.loc["tangibleBookValuePerShare"] = debttoearning.loc["tangibleBookValuePerShare"].map('${:,.2f}'.format)

print(debttoearning.iloc[:,:10])

note = "\n\nAcid test < 1\tCurrent Ratio < 2\tROE > ROIC"

print(note)
#print(incomestatement.loc['incomeBeforeTax'])

#print(cashflowstatement.loc[['depreciationAndAmortization','accountsPayables','accountsReceivables','capitalExpenditure'],:])
