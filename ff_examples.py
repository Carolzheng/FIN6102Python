# -*- coding: utf-8 -*-
"""
Created on Sun Sep 15 16:15:14 2019

@author: zheng
"""

from sp_functions import get_stock_data
import pandas as pd
import statsmodels.api as sm
import numpy as np

# read data using the function defined in sp_functions
df_x = get_stock_data(path='data/FF_Three_Factor_Monthly.csv', end=-1, fmt='%Y%m')
df_y = get_stock_data(path='data/25_Portfolios_5x5.csv', end=-1, fmt='%Y%m')

start = pd.to_datetime('196307', format='%Y%m')
end = pd.to_datetime('199112', format='%Y%m')
# to replicate the original implemetation in Fama French paper, we only take the data samples from 196307 to 199112.
df_x = df_x.loc[start:end]
df_y = df_y.loc[start:end]
# we would like to make sure that the index of df_x is the same as the index of df_y so that our regression samples are from 
# the same period of time.
assert (df_x.index == df_y.index).all()

factors = df_x.iloc[:, :3].values
rf = df_x.iloc[:, -1].values
# add a constant to the independent variables so that the linear regression is done with intercepts.
factors = np.insert(factors, obj=0, values=1, axis=1)
results = pd.DataFrame()
for i in range(25):
    port_return = df_y.iloc[:, i].values
    port_excess_return  = port_return -rf
    model=sm.OLS(endog=port_excess_return, exog=factors)
    res = model.fit()
    # create a temporary dataframe to store the values. To identify the meaning of each value, we need to know which 
    # coefficient it is ('a' or 'b' or 's' or 'h'), whether it is params or tvalues, and which portfolio it is representing.
    # Therefore, we have to add columns, index and a 'port' column to help us understand the values stored.
    temp_df = pd.DataFrame(data=[res.params], index=['params'], columns=['a', 'b', 's', 'h'])
    temp_df['port'] = df_y.columns[i]
    # unlike list, when you append value to dataframe, you have to store the returned value.
    results = results.append(temp_df)
    temp_df = pd.DataFrame(data=[res.tvalues], index=['tvalues'], columns=['a', 'b', 's', 'h'])
    temp_df['port'] = df_y.columns[i]
    results = results.append(temp_df)
    # res.summary() will give you a general description of the regression results.
    #print(res.summary())
