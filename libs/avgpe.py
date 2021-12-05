#!/usr/bin/env python

import pandas as pd
import getjson
from numpy import average

def date_correction(date):

    date = int(date)
    date -= 1
    date = str(date)

    return date

def income_statement(ticker, api_key):

    data = getjson.request_json(ticker,'income_statement', api_key)

    if 'Error Message' in data:
        raise ValueError(data['Error Message'])
        
    data_formatted = {}
    
    for value in data:
        date = value['date'][:4]
        month = value['date'][5:7]
        if month == "01" or month == "02":
            date = date_correction(date)

        del value['date']
        del value['symbol']

        data_formatted[date] = value

    return pd.DataFrame(data_formatted)

def avg_pe(ticker, quotedata, api_key):

	incomestatement = income_statement(ticker, api_key)

	avgeps = average( incomestatement.loc['eps'], weights = incomestatement.loc['weightedAverageShsOut'])
		
	return quotedata['price']/avgeps