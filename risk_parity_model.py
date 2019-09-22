# -*- coding: utf-8 -*-
"""
Created on Fri Sep 20 22:39:50 2019

@author: zheng
"""
import numpy as np
import pandas as pd
from scipy.optimize import minimize
from sp_functions import get_stock_data
import matplotlib.pyplot as plt

df_stock = get_stock_data('data/S&P500.csv', columns=['Adj Close'])
df_bond = get_stock_data('data/IUSB.csv', columns=['Adj Close'])
df_gold = get_stock_data('data/GLD.csv', columns=['Adj Close'])
data =df_stock.join(df_bond, how='inner', lsuffix='_Stock',rsuffix='_Bond')
data = data.join(df_gold, how='inner', rsuffix='_Gold')
data = data.pct_change()
data.dropna(how='any', inplace=True)

def calculate_risk_contribution(w, cov):
    sigma_p = np.sqrt(np.dot(np.dot(w.T,cov), w))
    risk_contrib = w * np.dot(cov, w) / sigma_p # * stand for elementwise product
    risk_contrib_pct = risk_contrib/sigma_p
    return risk_contrib_pct

def get_risk_parity_weight(n ,cov):
    def opt(w):
        risk_pct = calculate_risk_contribution(w, cov)
        loss = np.sum(np.square(risk_pct - np.array([1/n]*n, ndmin=2)))
        return loss
    init_w = np.array([1/n]*n, ndmin=2)
    bounds = [[0, 1]]*n
    cons = [{'type':'eq', 'fun': lambda x: np.sum(x)-1}]                        #constraints
    res = minimize(opt, init_w, constraints = cons, bounds=bounds)
    return res.x

train_x = data.iloc[:800]
cov = np.cov(train_x.T)
n = data.shape[1]
w_star = get_risk_parity_weight(n, cov)
risk_pct = calculate_risk_contribution(w_star, cov)
