#!/usr/bin/env python
import pandas as pd


#####################################################
#           Read csv or excel file as df            #
#####################################################
def remove_current_directory_prefix(file_path):
    # Check if the file path starts with "./"
    if file_path.startswith("./"):
        # Remove the leading "./" and return the modified path
        return file_path[2:]
    else:
        # If the path doesn't start with "./", return it unchanged
        return file_path


def read_data_by_path(file_path):
    if file_path is not None:
        file_predix = remove_current_directory_prefix(file_path)
        file_predix = file_path.split('.')[1]
        if file_predix == 'csv':
            df_test = pd.read_csv(file_path)
        if file_predix == 'xlsx':
            df_test = pd.read_excel(file_path)
        else:
            print(f"this function can only handle csv and excel file.")
            df_test = None
        return df_test  
    return None

     

################################################################
#              Get value from df's json column                 #
################################################################
import json

# function to get value of node in json
def process_json(row, key_name):
    try:
        parsed_json = json.loads(row)
        if key_name in parsed_json:
            return parsed_json[key_name]
        else:
            return None
    except (json.JSONDecodeError, TypeError):
        return None

def get_feature_from_json(df, json_column_name, key_name):
    df['json_feature'] = df[json_column_name].apply(process_json, args=(key_name,))
    return df['json_feature'].values


def greet(name):
    return f"Hello, {name}!"
