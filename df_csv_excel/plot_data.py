#!/usr/bin/env python
import pandas as pd
import numpy as np
import os
import plotly.express as px

#####################################################
#           Plot             #
#####################################################
def plot_histgram(df, column_name, parameter_root = 0, parameter_log = False):
    if parameter_log:
        df[f'log_{column_name}'] = df[column_name].apply(lambda x: np.log(x+0.00001))
        df[f'root_{column_name}'] = df[f'root_{column_name}'].apply(lambda x: x.real)
        fig = px.histogram(df, x=f'log_{column_name}')
        fig.show()
    if parameter_root > 0:
        df[f'root_{column_name}'] = df[column_name].apply(lambda x: x**parameter_root)
        df[f'root_{column_name}'] = df[f'root_{column_name}'].apply(lambda x: x.real)
        fig = px.histogram(df, x=f'root_{column_name}')
        fig.show()
    if parameter_root == 0 and parameter_log == False:
        fig = px.histogram(df, x=column_name)
        fig.show()
    