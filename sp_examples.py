# -*- coding: utf-8 -*-
"""
Created on Sun Sep  8 14:43:16 2019

@author: zheng
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
# absolute path
# sp = pd.read_csv('/Users/zheng/OneDrive/Docs/Carol/CUHKSZ/2019/FIN6102Python/data/S&P500.csv')
# relative path
sp = pd.read_csv('data/S&P500.csv')
sp['Date'] = pd.to_datetime(sp['Date'])
sp = sp.set_index('Date')
#date = sp['Date']
sp_adj_close = sp['Adj Close']
plt.plot(sp_adj_close)
plt.title('Adj Close')
plt.legend(['S&P500'])
plt.show()
sp_daily = sp_adj_close.pct_change()
sp_daily = sp_daily.dropna()
plt.hist(sp_daily,bins=50)
plt.title('S&P Daily Return')
plt.legend(['S&P500'])
plt.show()
# calculate using pandas
mean_pd = sp_daily.mean()
std_pd = sp_daily.std()

# calculate using for loops
mean_sum=0
for x in sp_daily:
    mean_sum = mean_sum + x
mean_for = mean_sum/len(sp_daily)

std_sum=0
for x in sp_daily:
    std_sum = std_sum + np.square(x-mean_for)
std_for = np.sqrt(std_sum/(len(sp_daily)-1))

sp_daily_value = sp_daily.values
mean_np = np.mean(sp_daily_value)
std_np = np.std(sp_daily_value, ddof=1)

n=len(sp_daily)
s0 = sp_adj_close.iloc[0]
s=[s0]
for i in range(n):
    r = np.random.randn()*std_np + mean_np
    current_s=s[-1]*(1+r)
    s.append(current_s)
s = np.array(s)
plt.plot(s)
