from scipy.stats import chi2_contingency
import pandas as pd
import numpy as np
from difflib import SequenceMatcher
import re
import matplotlib.pyplot as plt



def significant_association_chi_square(df, column_category, column_target, alpha = 0.05):
    """
    Check for significant association between a categorical feature and a binary target using the Chi-Square test.

    :param df: The pandas DataFrame containing the data.
    :type df: pandas.DataFrame

    :param column_category: The name of the categorical feature column.
    :type column_category: str

    :param column_target: The name of the binary target column.
    :type column_target: str

    :param alpha: The significance level for the Chi-Square test.
    :type alpha: float, optional, default: 0.05

    :return: True if there is a significant association, False if the variables are independent.
    :rtype: bool
    """
    if column_category not in df.columns or column_target not in df.columns:
        raise ValueError(f"One or more specified columns not found in the DataFrame.")
    contingency_table = pd.crosstab(df[column_category], df[column_target])
    chi2, p, _, _ = chi2_contingency(contingency_table)
    if p < alpha:
        # significant association
        return True
    else:
        # independent
        return False




# Calculate Jaccard similarity scores between two specified columns in a DataFrame.
def get_similarity(df, column_str_1, column_str_2):
    """
    Calculate Jaccard similarity scores between two specified columns in a DataFrame.

    Parameters:
    - df (pd.DataFrame): The input DataFrame.
    - column_str_1 (str): The name of the first column.
    - column_str_2 (str): The name of the second column.

    Returns:
    - np.ndarray: An array of Jaccard similarity scores.

    Raises:
    - ValueError: If the DataFrame is empty or if one or more specified columns are not found.
    """
    # Check for empty DataFrame
    if df.empty:
        raise ValueError("DataFrame is empty.")

    # Check for column existence
    if column_str_1 not in df.columns or column_str_2 not in df.columns:
        raise ValueError("One or more specified columns not found in the DataFrame.")

    def jaccard_similarity(str1, str2):
        # Check for missing or empty values
        if not str1 or not str2:
            return 0.0
        a = set(str1)
        b = set(str2)
        c = a.intersection(b)
        return float(len(c)) / (len(a) + len(b) - len(c))

    # Use .loc for assignment
    df.loc[:, 'similarity_score'] = df.apply(lambda row: jaccard_similarity(row[column_str_1], row[column_str_2]), axis=1)

    # Return similarity scores as a NumPy array
    return df['similarity_score'].values




################################   
#         calculate IV         #
################################
def calculate_iv(data, feature, target, num_bins=10):
    """
    Calculate Information Value (IV) for a given feature in a binary classification model.

    Parameters:
    -----------
    data : pandas.DataFrame
        The input DataFrame containing the feature and target columns.
    feature : str
        The name of the feature column for which IV is calculated.
    target : str
        The name of the binary target column.
    num_bins : int, optional
        The number of bins to discretize the continuous feature, default is 10.

    Returns:
    --------
    total_iv : float
        The total Information Value (IV) for the feature.
    pivot_table : pandas.DataFrame
        A DataFrame containing counts, percentages, WoE, and IV for each bin and target label.
    plot : matplotlib.pyplot
        The grouped bar chart showing counts for each bin and label.

    Raises:
    -------
    ValueError
        If one or both target values have zero counts for some levels of the feature,
        or if zero percentages are detected.

    Example:
    --------
    # Assuming 'df' is your DataFrame and 'feature_column' is the feature you want to evaluate
    # 'target_column' is your binary target column
    total_iv, pivot_table, plot = calculate_iv(df, 'email_firstname_score', 'Anomaly', num_bins=10)

    if total_iv is not None:
        print(f"Information Value (IV) for the feature: {total_iv}")
        # Show the plot
        plot.show()
    else:
        print("Unable to calculate Information Value. Please check the data and parameters.")

    """
    # Discretize the continuous feature into bins
    data[feature+'_bins'] = pd.cut(data[feature], bins=num_bins, labels=False)

    # Create a DataFrame with the counts of each unique value in the binned feature
    data['count'] = 1
    grouped_data = data.groupby([feature+'_bins', target]).agg({'count': 'sum'}).reset_index()

    # Check if there are any levels in the feature with zero counts for both target values
    if grouped_data[grouped_data[target] == 0].empty or grouped_data[grouped_data[target] == 1].empty:
        raise ValueError(f"Warning: One or both target values have zero counts for some levels of the feature.")

    # Pivot the table to get counts for each target value
    pivot_table = grouped_data.pivot(index=feature+'_bins', columns=target, values='count').fillna(0)

    # Calculate WoE and IV with a small constant added to avoid division by zero
    epsilon = 0.001
    pivot_table['total'] = pivot_table[0] + pivot_table[1]
    pivot_table['percentage'] = (pivot_table['total'] / pivot_table['total'].sum()).round(4)
    pivot_table['good_percentage'] = ((pivot_table[0] + epsilon) / pivot_table[0].sum()).round(4)
    pivot_table['bad_percentage'] = ((pivot_table[1] + epsilon) / pivot_table[1].sum()).round(4)

    # Check if any of the percentages are zero
    if (pivot_table['good_percentage'] == 0).any() or (pivot_table['bad_percentage'] == 0).any():
        raise ValueError(f"Warning: Zero percentages detected. Adjust the epsilon value and check the data.")

    pivot_table['WoE'] = np.log((pivot_table['good_percentage'] + epsilon) / (pivot_table['bad_percentage'] + epsilon))
    pivot_table['IV'] = (pivot_table['WoE'] * (pivot_table['good_percentage'] - pivot_table['bad_percentage'])).sum()

    # Calculate the total IV for the feature
    total_iv = pivot_table['IV'].sum()
     
    # bar chart
    plt.figure(figsize=(10, 6))
    bar_width = 0.4

    # Bar chart for bad_percentage
    plt.bar(np.arange(len(pivot_table)), pivot_table[0.0], width=bar_width, label='Label 0.0', color='blue')

    # Bar chart for good_percentage (shifted to the right by bar_width)
    plt.bar(np.arange(len(pivot_table)) + bar_width, pivot_table[1.0], width=bar_width, label='Label 1.0', color='orange')

    plt.xlabel('Bins')
    plt.ylabel('Count')  # Updated ylabel
    plt.title('Bar Chart of Counts for Each Bin and Label')
    plt.legend()

    return total_iv, pivot_table, plt