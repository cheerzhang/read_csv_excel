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
    if column_name in df.columns.values:
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
            },
            "fig": plt
        }
    else:
        print(f'There is no {column_name} in the dataframe, the dataframe has columns: {df.columns.values}')
        return  None


#############################################################
#           Binary Classification Result                    #
#############################################################
from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, recall_score, f1_score, roc_curve, auc


def binary_classification_eval(df, true_column, predict_column):
    """
    Evaluate binary classification performance.

    Parameters:
    - df (pd.DataFrame): DataFrame containing the true and predicted labels.
    - true_column (str): Name of the column containing true class labels.
    - predict_column (str): Name of the column containing predicted class labels.

    Returns:
    - dict: Dictionary containing evaluation metrics.
    """
    # Ensure columns exist in the DataFrame
    assert true_column in df.columns, f"{true_column} column not found in DataFrame."
    assert predict_column in df.columns, f"{predict_column} column not found in DataFrame."

    # Extract true and predicted labels
    y_true = df[true_column].values
    y_pred = df[predict_column].values

    # Compute confusion matrix
    cm = confusion_matrix(y_true, y_pred)

    # Calculate evaluation metrics
    accuracy = accuracy_score(y_true, y_pred)
    precision = precision_score(y_true, y_pred)
    recall = recall_score(y_true, y_pred)
    f1 = f1_score(y_true, y_pred)

    # Compute ROC curve
    fpr, tpr, thresholds = roc_curve(y_true, y_pred)
    
    # Calculate KS statistic
    ks = max(tpr - fpr)

    # Calculate Gini coefficient
    gini = 2 * auc(fpr, tpr) - 1

    # Create a dictionary to store the results
    metrics_dict = {
        'Confusion_Matrix': cm,
        'Accuracy': accuracy,
        'Precision': precision,
        'Recall': recall,
        'F1_Score': f1,
        'KS_Statistic': ks,
        'Gini_Coefficient': gini
    }

    return metrics_dict, tpr, fpr
    

