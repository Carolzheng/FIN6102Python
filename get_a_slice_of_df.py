# -*- coding: utf-8 -*-
"""
Created on Sun Sep  8 15:41:42 2019

@author: zheng
"""
import pandas as pd
sp = pd.read_csv('data/S&P500.csv')
sp['Date'] = pd.to_datetime(sp['Date'])
sp = sp.set_index('Date')
sp_adj_close = sp['Adj Close']
# get columns of data
a = sp['Open']
columns_to_get=['Open', 'Low']
b = sp[columns_to_get]

# get rows of data
date0 = pd.to_datetime('2014/07/14')
date1 = pd.to_datetime('2014/07/18')
dates = [date0, date1]
c = sp.loc[date0]
d = sp.loc[dates]
e = sp.loc[dates, columns_to_get]
f = sp.loc[date0:date1, columns_to_get]

#get date by integer location
h = sp.iloc[0:5, 1:3]
# be careful: changing a slice from the original data could change the original data in some cases.
j = b.iloc[0:5,0:2]
j.iloc[0,0]=9999
k = sp.iloc[0:5, 0:2]
k.iloc[0, 0]=9999
# use copy if you don't want to change the original data
m = b.iloc[0:5, 0:2].copy()
m.iloc[0, 0] = 8888