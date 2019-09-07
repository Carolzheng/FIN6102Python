# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


############Please fill in the blank functions to run the whole program#######
def get_stock_data(path, columns=None):
    """
    :param path: path to the .csv file containing stock information
    :param columns: the columns from the original dataframe to be returned, if None return all data
    :return:
    """
    print("Retrieving Data...")
    df = pd.read_csv(path)
    df = df.set_index('Date')
    if columns is None:
        return df
    else:
        return df[columns]


def get_daily_return(df_adj_close):
    """
    :param df_adj_close: pandas series data that contains the adjusted close price of an asset
    :return: the mean and standard deviation as implied in the df_adj_close
    """

    ####### Fill this function to return the daily return mean and std########
    print("Calculating mean and standard deviation...")




    ##########################################################################
    return mean, std


def simulate_stock_price(df_adj_close, num_simulations=50):
    """
    :param df_adj_close: pandas series object that contains the adjusted close price
    :param num_simulations: number of simulations to be generated
    :return: df_simulation: the simulated close price dataframe
             df_mean: the dataframe containing the price series should the stock has not volatility and daily return
                      equals the expected daily return implied in df_adj_close
    """
    mean, std = get_daily_return(df_adj_close)
    s0 = df_adj_close.iloc[0]
    length = len(df_adj_close)
    ##### Complete this function for price simulation#################
    print("Simulating...")





    ###################################################################

    return df_simulation, df_mean


def plot_simulation_with_mean(df_simulation, df_mean, title="Simulation"):
    """
    :param df_simulation: dataframe containing the simulated close price for an asset
    :param df_mean: dataframe containing the mean-return price series for an asset
    :param title: title of the plot, default "Simulation"
    """
    assert df_simulation.index == df_mean.index
    ##### Complete this function for plot both the simulated price and mean price#################
    print("Plotting simulation...")




    ##############################################################################################
    plt.show()


def plot_volume_data(df_volume, title="Volume"):
    """
    :param df_volume: pandas series that contains volume data, indexed by dates
    :param title: title of the plot, default "Volume"
    :return:
    """
    ##### Complete this function for plot both the simulated price and mean price#################
    print("Plotting volume data...")



    ##############################################################################################
    plt.show()


if __name__ == "__main__":
    np.random.seed(123)
    df_adj_close = get_stock_data('data/S&P500.csv', columns='Adj Close')
    df_volume = get_stock_data('data/S&P500.csv', columns='Volume')
    print("Data Retrived")
    df_simulation, df_mean = simulate_stock_price(df_adj_close, num_simulations=100)
    plot_simulation_with_mean(df_simulation, df_mean)
    plot_volume_data(df_volume)

