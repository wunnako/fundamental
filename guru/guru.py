#!/usr/bin/env python

import json
from urllib.request import urlopen
import os.path
import sys

def get13f(cik, date, api_key):

    response = urlopen("https://financialmodelingprep.com/api/v3/form-thirteen/" + cik + "?date=" + date + "&apikey=" + api_key)
    data = json.loads(response.read().decode("utf-8"))
  
    return data
    
def getguruname(cik, api_key):

    response = urlopen("https://financialmodelingprep.com/api/v3/cik/" + cik + "?apikey=" + api_key)
    data = json.loads(response.read().decode("utf-8"))
    
    for value in data:
        name = value['name']
        print(name.strip())
  
    return name

def read():

    file = 'data/guru.json'
    
    with open(file, 'r') as f:
        data = json.load(f)
    f.close()

    return data

def write(data):

    file = 'data/guru.json'
    
    if not os.path.exists(os.path.dirname(file)):
        try:
            os.makedirs(os.path.dirname(file))
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise
    
    with open(file, 'w+') as f:
        json.dump(data, f, indent=4)
    
    return

def addname(data, api_key):

    newdata = []
    for value in data:
        value['name'] = gurudict[value['cik']]
        newdata.append(value)

    return newdata
    
def merge(data, old_data):
    
    for value in old_data:
        if value not in data:
            data.append(value)
        
    return data
        

f = open('/home/wunnakoko/.api/api_key','r')
#f = open('api_key','r')

api_key = f.readline()

try:
    cik = sys.argv[1].upper()
    date = sys.argv[2].upper()
except:
    print('usage : '+__file__+' <cik>  <date-yyyy-mm-dd>')
    sys.exit(1)

data = get13f(cik, date, api_key)

gurudict = {}

gurudict [cik] = getguruname(cik, api_key)

print(gurudict)

data = addname(data,gurudict)

old_data = read()

print(old_data)

if old_data != None:
    data = merge(data, old_data)

write(data)
