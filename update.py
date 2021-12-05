#!/usr/bin/env python

import sys
import os

sys.path.insert(1, 'libs')
import avgpe

def getDirList(path):

    dir_content = os.listdir(path)
    
    return dir_content

if __name__ == '__main__':
    #f = open('/home/wunnakoko/.api/api_key','r')
    f = open('api_key','r')

    api_key = f.readline()

    path = 'data'

    tickers = getDirList(path)	
    
    for ticker in tickers:
        avgpe.check(ticker, api_key)