# read_csv_excel

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Overview

`read_csv_excel` is a Python library that provides a collection of common and customized functions for handling data, particularly CSV and Excel data. It simplifies the process of converting data into Pandas DataFrames, performing statistical analysis, and creating visualizations.

## Features

- CSV and Excel data conversion to Pandas DataFrames.
- Statistical analysis of DataFrames.
- Customized functions for common data handling tasks.
- Plotting functions for data visualization.

## Installation

You can install `read_csv_excel` using pip:

```
pip install df-csv-excel
```

pypi page link is here:(https://pypi.org/project/df-csv-excel/)

## Usage read and process data

```
from df_csv_excel import read_data 

df = read_data.read_data_by_path('a.xlsx')
df['name'] = read_data.get_feature_from_json(df, 'json_column', ['key_name1', 'key_name2', 'key_name3])
df['time_column'] = read_data.foramt_date_column(df, 'date')
```

## Usage plot data

```
from df_csv_excel import read_data, plot_data 

df = read_data.read_data_by_path('a.xlsx')
plot_data.plot_histgram(df, 'column_name')
```

## Contributing
If you have suggestions, enhancements, or find issues, please feel free to contribute! Follow the Contribution Guidelines for more details.


