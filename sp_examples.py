# -*- coding: utf-8 -*-
"""
Created on Sun Sep  8 14:43:16 2019

@author: zheng
"""


import pandas as pd

import matplotlib.pyplot as plt
import numpy as np
import time
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

# time.time() will record the time when this line is executed, we use this to record how much time it takes 
# to run from t to t1 (defined below)
t = time.time()
s=[s0]
total_s=[]
# use two for loops for generating 200 series (the j for loop) of 1259 prices (the i for loop)
for j in range(200):
    for i in range(n):
        r = np.random.randn()*std_np + mean_np
        current_s=s[-1]*(1+r)
        s.append(current_s)
    total_s.append(s)
    s=[s0]
total_s = np.array(total_s)  
total_s = total_s.T  
t1 = time.time()
print("time for loops,", t1-t)
# plt.plot(total_s)

t = time.time()
# generate all the return data that we are going to use simultaneously to increase efficiency
r = np.random.randn(n, 200)*std_np + mean_np
# np.cumprod will calculate the cumulative product for a given series.
cum_r = np.cumprod(1+r, axis=0)
s = s0 * cum_r
s = np.insert(s, obj=0, values=s0, axis=0)
df_simulation = pd.DataFrame(data=s, index=sp_adj_close.index)
t1 = time.time()
print("time for cumprod,", t1-t)
plt.plot(df_simulation)

# we add mean_np to np.zeros([n]) to generate a series of shape [n] but with value mean_np.
mean_return = np.zeros([n]) + mean_np
s_mean = s0 * np.cumprod(1+mean_return, axis=0) 
s_mean = np.insert(s_mean, obj=0, values=s0, axis=0)
df_mean = pd.DataFrame(data=s_mean, index=sp_adj_close.index)
plt.plot(df_mean, color='red', linewidth=4, label='Mean Return')
plt.legend()