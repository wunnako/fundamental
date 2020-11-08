import pandas as pd
import datetime as dt
import pandas_datareader.data as web
import sys
import numpy as np

def computeRSI (data, time_window):
    diff = data.diff(1).dropna()        # diff in one field(one day)

    #this preservers dimensions off diff values
    up_chg = 0 * diff
    down_chg = 0 * diff
    
    # up change is equal to the positive difference, otherwise equal to zero
    up_chg[diff > 0] = diff[ diff>0 ]
    
    # down change is equal to negative deifference, otherwise equal to zero
    down_chg[diff < 0] = diff[ diff < 0 ]
    
    # check pandas documentation for ewm
    # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.ewm.html
    # values are related to exponential decay
    # we set com=time_window-1 so we get decay alpha=1/time_window
    up_chg_avg   = up_chg.ewm(com=time_window-1 , min_periods=time_window).mean()
    down_chg_avg = down_chg.ewm(com=time_window-1 , min_periods=time_window).mean()
    
    rs = abs(up_chg_avg/down_chg_avg)
    rsi = 100 - 100/(1+rs)
    return rsi

def get_data (ticker, start, end):

	df = web.DataReader(ticker, 'yahoo', start, end)
	df.reset_index(inplace=True)
	df.set_index("Date", inplace=True)
	return df

try:
    ticker = sys.argv[1].upper()
except:
    print('usage : '+__file__+' <ticker>')
    sys.exit(1)

start = dt.datetime(2020, 1, 1)
end = dt.datetime.now()
#ticker = "MU"
df = get_data (ticker, start, end)

df['12dayEMA'] = df['Adj Close'].ewm(span=12, adjust=False).mean()

df['26dayEMA'] = df['Adj Close'].ewm(span=26, adjust=False).mean()

df['UpDown'] = np.where((df['12dayEMA'] >= df['26dayEMA']), "Up", "Down")

df['RSI'] = computeRSI(df['Adj Close'], 14)


#view DataFrame 
print(df.tail())