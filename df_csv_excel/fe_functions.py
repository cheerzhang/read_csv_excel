from scipy.stats import chi2_contingency
import pandas as pd



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