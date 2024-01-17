#!/usr/bin/env python
import pandas as pd
import numpy as np
import os
import plotly.express as px
import scipy.stats as stats
import matplotlib.pyplot as plt
from scipy.stats import shapiro, anderson



#####################################################
#                 Plot histgram                    #
#####################################################
def plot_histgram(df, column_name, parameter_root = 0, parameter_log = False):
    if parameter_log:
        df[f'log_{column_name}'] = df[column_name].apply(lambda x: np.log(x+0.00001))
        fig = px.histogram(df, x=f'log_{column_name}')
    if parameter_root > 0:
        df[f'root_{column_name}'] = df[column_name].apply(lambda x: x**parameter_root)
        df[f'root_{column_name}'] = df[f'root_{column_name}'].apply(lambda x: x.real)
        fig = px.histogram(df, x=f'root_{column_name}')
    if parameter_root == 0 and parameter_log == False:
        fig = px.histogram(df, x=column_name)
    fig.show()



def check_normal_distribution(df, column_name):
    if column_name in df.column.values:
        data = df[column_name]
        plt.figure(figsize=(12, 6))
        # Histogram
        plt.subplot(1, 2, 1)
        plt.hist(data, bins='auto', color='#0504aa', alpha=0.7, rwidth=0.85)
        plt.title('Histogram')
        # QQ Plot
        plt.subplot(1, 2, 2)
        stats.probplot(data, dist="norm", plot=plt)
        plt.title('QQ Plot')
        plt.show()
        # Shapiro-Wilk test
        stat, p_value = shapiro(data)
        # Anderson-Darling test
        result = anderson(data)
        return {
            "mean": data.mean(),
            "Standard Deviation": data.std(),
            "Skewness": data.skew(),
            "Kurtosis": data.kurtosis(),
            "Shapiro-Wilk Test": {
                "Statistic": stat,
                "p-value": p_value
            },
            "Anderson-Darling Test": {
                "Statistic": result.statistic,
                "Critical Values": result.critical_values
            }
        }
    else:
        print(f'There is no {column_name} in the dataframe, the dataframe has columns: {df.column.values}')

    