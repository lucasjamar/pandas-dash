# Pandas Plotly

![Python version](https://img.shields.io/badge/python-3.7%20%7C%203.8%20%7C%203.9%20%7C%203.10-blue.svg)
[![PyPI version](https://badge.fury.io/py/pandas-plotly.svg)](https://pypi.org/project/pandas-plotly/)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/lucasjamar/kedro/pandas-plotly/main/LICENSE.md)

Tools for working with Pandas, Plotly, and Dash.

[See examples](https://github.com/lucasjamar/pandas-plotly/main/examples/app.py)

## Available extensions for `Dash`:
* `df.pp.to_dash_table()` for getting the `data` and `columns` for `dash_table` from a flat or multi-index `pd.DataFrame`.
* `df.pp.to_options("my_column")` for creating `dcc.Dropdown` options from the column of a `pd.DataFrame`.

## Extensions for `Plotly` coming soon