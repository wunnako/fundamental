#!/usr/bin/env python

import sys
import pull
import pandas as pd
import json
import os.path
from os import path

def read_json(file):

    try:
        path.exists(file)
        with open(file, 'r') as f:
            data = json.load(f)
        f.close()
    except:
        data = None

    return data

def dedup(data):
    clean = []
    for item in data:
        if item not in clean:
            clean.append(item)
    return clean

api_key = "4d1d8612c6f15e10c2a2327977f81d43"

try:
    ticker = sys.argv[1].upper()
except:
    print('usage : '+__file__+' <ticker>')
    sys.exit(1)

print(ticker)

if not os.path.exists(ticker):
        os.makedirs(ticker)

filename = ticker + '/ratios.json'

base = read_json(filename)

ratio = pull.ratios(ticker, api_key)

if base != None:
#    i = 0
    print("in loop")
#    while i < len (base):
    for i in range(len(base)):
        ratio.append(base[i])
#        i += 1

ratio = dedup(ratio)

with open(filename, 'w') as f:
    json.dump(ratio, f, indent=4)