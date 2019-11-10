# -*- coding: utf-8 -*-
"""
Created on Mon Nov  4 19:01:47 2019

@author: zheng
"""
import numpy as np
import pandas as pd
from scipy.optimize import minimize
from sp_functions import get_stock_data
import matplotlib.pyplot as plt
from pandas.tseries.offsets import MonthEnd

class DataHandler:
    def __init__(self, init_trade_date='2016/12/31', final_trade_date='2019/06/30'):
        self.data = self.read_full_data()
        self.init_date = pd.to_datetime(init_trade_date)
        self.final_date = pd.to_datetime(final_trade_date)
        self.current_date = self._calibrate_date(self.init_date)
        print("Starting from", self.current_date)
        self.is_terminated = False
        self.port_return = pd.DataFrame(index=[self.current_date+pd.DateOffset(-1)], data=[1], columns=['Port Return'])
    
    def read_full_data(self):
        df_stock = get_stock_data('data/S&P500.csv', columns=['Adj Close'])
        df_bond = get_stock_data('data/IUSB.csv', columns=['Adj Close'])
        df_gold = get_stock_data('data/GLD.csv', columns=['Adj Close'])
        data =df_stock.join(df_bond, how='inner', lsuffix='_Stock',rsuffix='_Bond')
        data = data.join(df_gold, how='inner', rsuffix='_Gold')
        data.columns= ['Stock', 'Bond', 'Gold']
        data = data.pct_change()
        data = data.dropna() 
        return data
    
    def get_training_data(self):
        start_date = self.current_date - pd.DateOffset(years=2)
        x = self.data.loc[start_date:self.current_date]
        return x
    
    def move_forward(self):
        self.current_date = self.current_date + pd.DateOffset(-1) + MonthEnd(2)
        if self.current_date >= self.final_date:
            self.is_terminated = True
        self.current_date = self._calibrate_date(self.current_date)
        print("Moving to Date", self.current_date)      
        
    def _calibrate_date(self, date):
        while date not in self.data.index:
            date = date + pd.DateOffset(-1)
        return date
    
    def record_results(self, action):
        next_reb_date = self._calibrate_date(self.current_date + pd.DateOffset(-1) + MonthEnd(2))
        stock_return  = self.data.loc[self.current_date:next_reb_date+pd.DateOffset(1)].copy()
        stock_cum_return = (stock_return  + 1).cumprod()
        temp_port = np.sum(stock_cum_return * action, axis=1)*self.port_return.iloc[-1].values
        temp_port = temp_port.to_frame()
        temp_port.columns=self.port_return.columns
        self.port_return = self.port_return.append(temp_port)
        
    def plot_portfolio(self):
        plt.plot(self.port_return)
        plt.plot((self.data.loc[self.port_return.index[0]:]+1).cumprod())
        plt.legend(['port_return']+list(self.data.columns))
        plt.show()
    
    
class RiskParityModel:
    def __init__(self, num_assets):
        self.num_assets = num_assets
        self.trained = False
        
    def train(self, x):
        cov = np.cov(x.T)
        self.cov = cov
        self.trained = True
    
    @staticmethod
    def _cal_risk_contrib(w, cov):
        sigma_p = np.sqrt(np.dot(np.dot(w.T,cov), w))
        risk_contrib = w * np.dot(cov, w) / sigma_p
        risk_contrib_pct = risk_contrib/sigma_p
        return risk_contrib_pct
    
    def get_best_action(self):
        n = self.num_assets
        assert self.trained
        cov = self.cov
        self.trained = False
        def opt(w):
            risk_pct = self._cal_risk_contrib(w, cov)
            loss = np.sum(np.square(risk_pct - np.array([1/n]*n, ndmin=2)))
            return loss
        init_w = np.array([1/n]*n, ndmin=2)
        bounds = [[0, 1]]*n
        cons = [{'type':'eq', 'fun': lambda x: np.sum(x)-1}]
        res = minimize(opt, init_w, constraints = cons, bounds=bounds)
        return res.x
    
class MinVarianceModel:
    def __init__(self, num_assets):
        self.num_assets = num_assets
        self.trained = False
        
    def train(self, x):
        cov = np.cov(x.T)
        self.cov = cov
        self.trained = True
    
    @staticmethod
    def _cal_port_sigma(w, cov):
        sigma_p = np.sqrt(np.dot(np.dot(w.T,cov), w))
        return sigma_p
    
    def get_best_action(self):
        n = self.num_assets
        assert self.trained
        cov = self.cov
        self.trained = False
        def opt(w):
            sigma_p = self._cal_port_sigma(w, cov)
            return sigma_p
        init_w = np.array([1/n]*n, ndmin=2)
        bounds = [[0, 1]]*n
        cons = [{'type':'eq', 'fun': lambda x: np.sum(x)-1}]
        res = minimize(opt, init_w, constraints = cons, bounds=bounds)
        return res.x

    
if __name__ == "__main__":
    dh = DataHandler()
    m = RiskParityModel(num_assets=3)
    terminate = False
    while True:
        x = dh.get_training_data()
        m.train(x)
        w = m.get_best_action()
        dh.record_results(w)
        terminate = dh.is_terminated
        if terminate:
            break
        dh.move_forward()
    dh.plot_portfolio()
