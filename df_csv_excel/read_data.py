#!/usr/bin/env python
import pandas as pd
import os, re, warnings

#####################################################
#           Read csv or excel file as df            #
#####################################################
def remove_current_directory_prefix(file_path):
    if file_path.startswith("./"):
        return file_path[2:]
    else:
        return file_path


def read_data_by_path(file_path):
    if file_path:
        file_prefix = remove_current_directory_prefix(file_path)
        _, file_extension = os.path.splitext(file_prefix.lower())

        # Mapping file extensions to corresponding read functions
        read_functions = {'.csv': pd.read_csv, '.xlsx': pd.read_excel}

        if file_extension in read_functions:
            try:
                df_test = read_functions[file_extension](file_path)
                return df_test
            except Exception as e:
                print(f"Error reading file: {e}")
        else:
            print("This function can only handle csv and excel files.")
    return None
     

################################################################
#              Get value from df's json column                 #
################################################################
import json


# function to get value of node in json
def process_json(row, key_names):
    try:
        parsed_json = json.loads(row)
        value = parsed_json
        for key in key_names:
            if key in value:
                value = value[key]
            else:
                return None
        return value
    except (json.JSONDecodeError, TypeError, KeyError):
        return None



def get_feature_from_json(df, json_column_name, key_names):
    df.loc[:, 'json_feature'] = df[json_column_name].apply(process_json, args=(key_names,))
    return df['json_feature'].values



# Example usage:
# parse_dates(df, 'date_column')
# parse_dates(df, 'date_column', format='%d/%m/%Y %H:%M:%S')
def parse_dates(df, date_column_name, format=None):
    if date_column_name not in df.columns:
        raise ValueError(f"'{date_column_name}' column not found in the DataFrame.")
    def apply_date_parser(date_parser, format=None):
        try:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore", UserWarning)
                df['date_column'] = date_parser(df[date_column_name], errors='coerce', format=format)
            return df['date_column'].values
        except Exception as e:
            print(e)
            return None

    if format is None:
        try:
            # Attempt parsing with default settings
            return apply_date_parser(pd.to_datetime)
        except Exception as e:
            # If default parsing fails, try to extract and use the format from the error
            match = re.search(r'Parsing dates in (.+?) format', str(e))
            if match:
                date_format = match.group(1)
                return apply_date_parser(pd.to_datetime, format=date_format)
            else:
                print(e)
                return None
    else:
        # Parse with the specified format
        return apply_date_parser(pd.to_datetime, format=format)




def format_numeric_column(df, numeric_column_name):
    try:
        df['numric_column'] = df[numeric_column_name].apply(lambda x: int(x) if x.isdigit() else 0)
        return df['numric_column'].values
    except Exception as e:
        print(e)
        return None



###############################################################
#                                                             #
#       get email domain and predix from email column         #
#                                                             #
###############################################################
def get_email_host(df, email_column='email'):
    if email_column not in df.columns:
        raise ValueError(f"'{email_column}' column not found in the DataFrame.")
    df[email_column] = df[email_column].fillna('').str.lower()
    df['email_domain'] = ''
    df['email_prefix'] = ''
    # check for non-empty email addresses
    mask_non_empty_email = df[email_column] != ''
    df.loc[mask_non_empty_email, 'email_domain'] = df[mask_non_empty_email][email_column].str.split('@').str[1]
    df.loc[mask_non_empty_email, 'email_prefix'] = df[mask_non_empty_email][email_column].str.split('@').str[0]
    df['email_domain'] = df['email_domain'].str.lower()
    df['email_prefix'] = df['email_prefix'].str.lower()
    return df['email_prefix'].values, df['email_domain'].values



##########################################################
#                                                        #
#       get lastest row base on duplicate column         #
#                                                        #
##########################################################
def get_latest_row_by_column(df, date_column, duplicate_column):
    df[date_column] = pd.to_datetime(df[date_column])
    df_sorted = df.sort_values(date_column, ascending=False)
    df_unique_latest = df_sorted.drop_duplicates(duplicate_column)
    df_unique_latest = df_unique_latest.reset_index(drop=True)
    return df_unique_latest


def greet(name):
    return f"Hello, {name}!"
