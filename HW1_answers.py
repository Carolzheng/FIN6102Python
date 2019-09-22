# -*- coding: utf-8 -*-
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
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
    df.index = pd.to_datetime(df.index)
    if columns is None:
        return df
    else:
        return df[columns]


def get_daily_return_stats(df_adj_close):
    """
    :param df_adj_close: dataframe containing the adjusted close price of an asset
    :return: the mean and standard deviation as implied in the close price dataframe
    """

    ####### Fill this function to return the daily return mean and std########
    print("Calculating mean and standard deviation...")
    df_daily_return = df_adj_close.pct_change()
    df_daily_return = df_daily_return.dropna()
    mean = df_daily_return.mean()
    std = df_daily_return.std()
    ##########################################################################
    return mean, std


def simulate_stock_price(df_adj_close, num_simulations=10):
    """
    :param df_adj_close: dataframe containing only one column: adjusted close price
    :param num_simulations: number of simulations to be generated
    :return: df_simulation: the simulated close price dataframe
             df_mean: the dataframe containing the price series should the stock has not volatility and daily return
                      equals the expected daily return implied in df_adj_close
    """
    mean, std = get_daily_return_stats(df_adj_close)
    s0 = df_adj_close.iloc[0]
    length = len(df_adj_close)
    ##### Complete this function for price simulation#################
    print("Simulating...")
    ret_series = np.random.randn(length-1, num_simulations)* std + mean
    price_series = np.cumprod(ret_series + 1, axis=0) * s0
    price_series = np.insert(price_series, obj=0, values=s0, axis=0)
    df_simulation = pd.DataFrame(data=price_series, index=df_adj_close.index)
    cum_mean = np.cumprod(np.ones(length-1) * mean + 1)
    cum_mean = np.insert(cum_mean, obj=0, values=1, axis=0)
    s_mean = s0 * cum_mean
    df_mean = pd.DataFrame(data=s_mean, index=df_adj_close.index)
    ###################################################################
    return df_simulation, df_mean


def plot_simulation_with_mean(df_simulation, df_mean, title="Simulation"):
    """
    :param df_simulation: dataframe containing the simulated close price for an asset
    :param df_mean: dataframe containing the mean-return price series for an asset
    :param title: title of the plot, default "Simulation"
    """
    assert (df_simulation.index == df_mean.index).all()
    ##### Complete this function for plot both the simulated price and mean price#################
    print("Plotting simulation...")
    plt.plot(df_simulation)
    plt.plot(df_mean, color='r', linewidth=4, label='Mean Return')
    plt.title(title)
    plt.legend()
    ##############################################################################################
    plt.show()

def plot_volume_data(df_volume, title="Volume"):
    """
    :param df_volume: dataframe containing only one column: volume, indexed by dates
    :param title: title of the plot, default "Volume"
    :: plot an area chart of the volume data
    """
    ##### Complete this function to plot volume data as shadows#################
    print("Plotting volume data...")
    plt.fill_between(x=df_volume.index, y1=df_volume)
    plt.title(title)
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
