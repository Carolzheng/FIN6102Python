# -*- coding: utf-8 -*-
"""
Created on Sun Nov 10 09:53:25 2019

@author: zheng
"""
from risk_parity_rolling import DataHandler, RiskParityModel, MinVarianceModel



if __name__ == "__main__":
    model = "MinVariance"
    ##############Don't Change anything below####################
    if model == "RiskParity":
        UseModel = RiskParityModel
    elif model == "MinVariance":
        UseModel = MinVarianceModel
    else:
        raise ValueError("Invalid Model")
    dh = DataHandler()
    m = UseModel(num_assets=3)
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