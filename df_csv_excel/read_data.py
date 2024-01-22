#!/usr/bin/env python
import pandas as pd
import os

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
    df['json_feature'] = df[json_column_name].apply(process_json, args=(key_names,))
    return df['json_feature'].values



def foramt_date_column(df, date_column_name, format=None):
    # format='%Y-%m-%d %H:%M:%S'
    if format is None:
        df['date_column'] = pd.to_datetime(df[date_column_name], errors='coerce')
    else:
        try:
            df['date_column'] = pd.to_datetime(df[date_column_name], errors='coerce', format=format)
            return df['date_column'].values
        except Exception as e:
            print(e)
            return None



def format_numeric_column(df, numeric_column_name):
    try:
        df['numric_column'] = df[numeric_column_name].apply(lambda x: int(x) if x.isdigit() else 0)
        return df['numric_column'].values
    except Exception as e:
        print(e)
        return None



def greet(name):
    return f"Hello, {name}!"
