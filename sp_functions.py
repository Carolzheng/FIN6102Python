# -*- coding: utf-8 -*-
"""
Created on Sun Sep 15 15:10:15 2019

@author: zheng
"""
import pandas as pd
import matplotlib.pyplot as plt

# in the function definitiong, path is the positional argument, so when you call this function, you must pass a value for path
# end, columns and fmt are the keyword arguments, you can ignore them if the default value suits your needs.
def get_stock_data(path, end=None, columns=None, fmt=None):
    df = pd.read_csv(path)
    df = df.iloc[:end]
    df['Date'] = pd.to_datetime(df['Date'], format=fmt)
    df = df.set_index('Date')
    if columns is None:
        return df
    else:
        df = df[columns]
        return df 

# The reason why we use if __name__ == "__main__" is: we want the following code to run if the current file is the 
# main file that is being executed. But if the file is being imported in other files, we want to aovid executing this block of codes. 
# In the first case, the __name__ of this file will be __main__, so the if condition is met and our code will be executed.
# In the second case, the __name__ of this file will just be the name you gave it (in our case, it's sp_functions), so the 
# if condition is not met, then the block of code will not be executed.
if __name__ == "__main__":
    sp = get_stock_data('data/S&P500.csv', columns=['Adj Close'])
    nky = get_stock_data('data/NKY225.csv', columns=['Adj Close'])
    # the join function will join two dataframe on their indices. We use this to make sure that the two series of data 
    # that we are looking at are being compared (or plotted) for the same dates. 
    data = sp.join(nky, how='outer', lsuffix='_SP', rsuffix='_NKY')
    # There are many ways to fillna, the 'ffill' means forward fill, where we fill the na values with value of 
    # the previous day. if you want to fill na with a constant value (for example 0), you can use df.fillna(value=0)
    data = data.fillna(method='ffill') # value=0
    ax = plt.gca() #gca() means get current axis, it will give you the axis of the current plot
    ax.plot(data['Adj Close_SP'], color='blue')
    ax.legend(['SPX'])
    ax2 = ax.twinx()
    ax2.plot(data['Adj Close_NKY'], color='orange')
    ax2.legend(['NKY'])
