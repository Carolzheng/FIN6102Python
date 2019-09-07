# -*- coding: utf-8 -*-
"""
Created on Sun Aug 25 16:41:34 2019

@author: zheng
"""
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def get_stock_data(path, start=None, end=None, columns=None):
    df = pd.read_csv(path)
    df = df.iloc[start:end]
    df = df.set_index('Date')
    df.index = pd.to_datetime(df.index)
    if columns is None:
        return df
    else:
        return df[columns]
if __name__ == "__main__":
    np.random.seed(123)
    # plot price of sp
    adj_close= get_stock_data('data/S&P500.csv',columns=['Adj Close'])
    plt.plot(adj_close)
    plt.title('Adj Close')
    plt.legend(['S&P500'])
    plt.show()
    # calculate and plot daily return of sp
    daily_return  = adj_close.pct_change()
    daily_return  = daily_return.dropna()
    daily_return_array = daily_return.values
    plt.hist(daily_return_array, bins=50)
    plt.title('S&P Daily Return')
    plt.legend(['S&P500'])
    plt.show()
    # calculate mean and std of sp
    mean = np.mean(daily_return_array)
    std = np.std(daily_return_array, ddof=1)
    # assuming normally iid of return ,simulate the stock price
    n = len(daily_return_array)
    s0 = adj_close.iloc[0, 0]
    r = np.random.randn(n, 50)*std + mean
    cum_r = np.cumprod(1+r, axis=0)
    s = s0 * cum_r
    s=np.insert(s, 0, s0, axis=0)
    sp_simulated = pd.DataFrame(data=s, index=adj_close.index)
    cum_mean = np.cumprod(np.ones(1258) * mean+1)
    cum_mean = np.insert(cum_mean, 0, 1)
    s_mean = s0 * cum_mean
    plt.plot(sp_simulated)
    plt.plot(sp_simulated.index, s_mean, color='r', linewidth=4,label='Mean Return')
    plt.title('Simulated S&P 500 return')
    plt.legend()
    plt.show()
