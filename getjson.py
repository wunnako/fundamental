#!/usr/bin/env python

import sys
import pull
import pandas as pd
import json
import os.path
from os import path
import readjson

def checkfile(ticker, filetype):

    file = 'data/'+ ticker + '/' + filetype + '.json'

    if path.exists(file):
        return True
    else:
        return False

def request_json(ticker, filetype):

    data = []

    if checkfile(ticker, filetype):
        if filetype == 'ratios':
            data = readjson.ratios(ticker)
        if filetype == 'income_statement':
            data = readjson.income_statement(ticker)
        if filetype == 'balance_sheet_statement':
            data = readjson.balance_sheet_statement(ticker)
        if filetype == 'key_metrics':
            data = readjson.key_metrics(ticker)
        if filetype == 'cashflow_statement':
            data = readjson.cashflow_statement(ticker)

    else:
        if filetype == 'ratios':
            data = pull.ratios(ticker)
            readjson.write(ticker, data, 'ratios')
        if filetype == 'income_statement':
            data = pull.income_statement(ticker)
            readjson.write(ticker, data, 'income_statement')
        if filetype == 'balance_sheet_statement':
            data = pull.balance_sheet_statement(ticker)
            readjson.write(ticker, data, 'balance_sheet_statement')
        if filetype == 'key_metrics':
            data = pull.key_metrics(ticker)
            readjson.write(ticker, data, 'key_metrics')
        if filetype == 'cashflow_statement':
            data = pull.cashflow_statement(ticker)
            readjson.write(ticker, data, 'cashflow_statement')
    
    return data