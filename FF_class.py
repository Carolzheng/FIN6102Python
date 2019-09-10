# -*- coding: utf-8 -*-
"""
Created on Sat Aug 17 15:20:35 2019

@author: zheng


"""
import pandas as pd
import numpy as np
import statsmodels.api as sm
from statsmodels.tools.tools import add_constant

class DataHandler:
    def __init__(self, path_x, path_y, date_fmt='%Y%m'):
        self.df_x = self.get_data(path_x, date_fmt)
        self.df_y = self.get_data(path_y, date_fmt)
        self.df_results=pd.DataFrame()
        assert (self.df_x.index == self.df_y.index).all()
        
    @staticmethod
    def get_data(path, fmt='%Y%m'):
        df = pd.read_csv(path)
        df = df[df['Date'].apply(lambda x: x.isdigit())]
        df = df.set_index('Date')
        df.index = pd.to_datetime(df.index,format=fmt)
        return df
    
    def get_training_data(self,start, end, y_index=0, add_constant_to_x=True):
        x = self.df_x.loc[start:end].values[:, :-1]
        rf = self.df_x.loc[start:end].values[:, -1]
        y = self.df_y.loc[start:end]
        if type(y_index) is int:
            y = y.iloc[:, y_index]
        elif type(y_index) is str:
            y = y.loc[:, y_index]
        else:
            raise IndexError("y_list should be all integer or all string")
        y =y.values
        y = y-rf
        if add_constant_to_x:
            x = add_constant(x, prepend=True, has_constant='raise')
        return x, y

    def record_results(self, params, tvalues, name=None, y_index=None):
        if name is None:
            name = self.df_y.columns[y_index]
        me_name, bm_name = name.split(" ")
        if me_name == 'SMALL':
            me_name = 'ME1'
        elif me_name == 'BIG':
            me_name = 'ME5'
        if bm_name == 'LoBM':
            bm_name = 'BM1'
        elif bm_name == 'HiBM':
            bm_name = 'BM5'
        self._get_temp_df(params, 'params', me_name, bm_name)
        self._get_temp_df(tvalues, 'tvalue', me_name, bm_name)
    
    def _get_temp_df(self, value, feature_name, me_name, bm_name):
        temp_df=pd.DataFrame(data=[value], columns=['alpha', 'b', 's', 'h'])
        temp_df['feature'] = feature_name
        temp_df['ME']=me_name
        temp_df['BM']=bm_name
        self.df_results = self.df_results.append(temp_df)
        
    def get_FF_format(self):
        if self.df_results.empty:
            raise ValueError("No data recorded for results")
        else:
            results = self.df_results.drop(columns=['alpha'])
            results = results.pivot_table(index=['feature','BM'], columns=['ME'], values=['b','s','h'])
            results = results.T
            results = results.reindex(['b', 's', 'h'],level=0)
            results = results.sort_index(axis=1,level=1)
            return results
        
        
if __name__ == "__main__":
    path_x = 'data/FF_Three_Factor_Monthly.csv'
    path_y = 'data/25_Portfolios_5x5.csv'
    start_date = pd.to_datetime('196307',format='%Y%m')
    end_date = pd.to_datetime('199112',format='%Y%m')
    dh = DataHandler(path_x, path_y)
    for i in range(25):
        x, y = dh.get_training_data(start_date, end_date, y_index=i)
        model = sm.OLS(y, x)
        res = model.fit()
        dh.record_results(res.params, res.tvalues, y_index=i)
    results = dh.get_FF_format()