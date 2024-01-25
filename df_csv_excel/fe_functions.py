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
