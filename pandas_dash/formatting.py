from typing import List, Union

import colorlover
import numpy as np
import pandas as pd
from dash import html


def _make_sparkline(spark_line: List, include_limits: bool = True) -> List:
    if isinstance(spark_line, list):
        spark_line = [v for v in spark_line if not np.isnan(v)]
        if len(spark_line) > 1:
            first_value, last_value = spark_line[0], spark_line[-1]
            min_value, max_value = min(spark_line), max(spark_line)
            value_range = max_value - min_value
            if value_range > 0:
                spark_line = [(v - min_value) * 100 / max_value for v in spark_line]
            elif max_value != 0:
                spark_line = [100]*len(spark_line)
            spark_line = [str(int(v)) for v in spark_line]
            spark_line = ",".join(spark_line)
            spark_line = "{" + spark_line + "}"
            if include_limits:
                spark_line = f"{first_value}{spark_line}{last_value}"
        else:
            spark_line = spark_line[0]
    return spark_line


def sparkline(column: pd.Series, include_limits: bool = True) -> pd.Series:
    return column.apply(_make_sparkline, include_limits=include_limits)


def heatmap(
    data: pd.DataFrame,
    n_bins: int = 5,
    columns: Union[str, List] = "all",
    min_value: float = None,
    max_value: float = None,
    color_scale: str = "Blues",
    legend_height: str = "10px"
) -> List:
    """
    color_scale: One of 'Blues', 'BuGn', 'BuPu', 'GnBu', 'Greens', 'Greys', 'OrRd', 'Oranges',
    'PuBu', 'PuBuGn', 'PuRd', 'Purples', 'RdPu', 'Reds', 'YlGn', 'YlGnBu', 'YlOrBr', 'YlOrRd'
    """
    if columns == "all":
        df_numeric_columns = data.select_dtypes("number")
    else:
        df_numeric_columns = data[columns]
    if min_value is None:
        min_value = df_numeric_columns.min().min()
    if max_value is None:
        max_value = df_numeric_columns.max().max()
    ranges = np.linspace(min_value, max_value, n_bins)
    styles = []
    legend = []
    for i in range(1, n_bins):
        min_bound = ranges[i - 1]
        max_bound = ranges[i]
        backgroundColor = colorlover.scales[str(n_bins)]["seq"][color_scale][i - 1]
        for column in df_numeric_columns:
            filter_query = f"{{{column}}} >= {min_bound}"
            if n_bins - 1 > i:
                filter_query += f" && {{{column}}} < {max_bound}"
            styles.append(
                {
                    "if": {"filter_query": filter_query, "column_id": column},
                    "backgroundColor": backgroundColor,
                }
            )
        legend.append(
            html.Div(
                style={"display": "inline-block", "width": "60px"},
                children=[
                    html.Div(
                        style={
                            "backgroundColor": backgroundColor,
                            "borderLeft": "1px rgb(50, 50, 50) solid",
                            "height": legend_height,
                        }
                    ),
                    html.Small(round(min_bound, 1)),
                ],
            )
        )
    return styles, html.Div(legend)


def data_bars(data: pd.Series) -> List:
    column = data.name
    n_bins = 101
    col_max, col_min = data.max(), data.min()
    ranges = np.linspace(start=col_min, stop=col_max, num=n_bins)
    styles = []
    for i in range(1, n_bins):
        min_bound, max_bound = ranges[i - 1], ranges[i]
        max_bound_percentage = i
        filter_query = f"{{{column}}} >= {min_bound}"
        if n_bins - 1 > max_bound_percentage:
            filter_query += f" && {{{column}}} < {max_bound}"
        styles.append(
            {
                "if": {"filter_query": filter_query, "column_id": column},
                "background": f"""
                    linear-gradient(90deg,
                    #0074D9 0%,
                    #0074D9 {max_bound_percentage}%,
                    white {max_bound_percentage}%,
                    white 100%)
                """,
            }
        )
    return styles


def data_bars_diverging(
    data: pd.Series,
    midpoint: int = None,
    color_above: str = "#3D9970",
    color_below: str = "#FF4136",
) -> List:
    column = data.name
    n_bins = 101
    col_max, col_min = data.max(), data.min()
    ranges = np.linspace(start=col_min, stop=col_max, num=n_bins)
    if midpoint is None:
        midpoint = (col_max + col_min) / 2
    styles = []
    for i in range(1, n_bins):
        min_bound, max_bound = ranges[i - 1], ranges[i]
        min_bound_percentage, max_bound_percentage = i - 1, i
        if max_bound > midpoint:
            background = f"""
                    linear-gradient(90deg,
                    white 0%,
                    white 50%,
                    {color_above} 50%,
                    {color_above} {max_bound_percentage}%,
                    white {max_bound_percentage}%,
                    white 100%)
                """
        else:
            background = f"""
                    linear-gradient(90deg,
                    white 0%,
                    white {min_bound_percentage}%,
                    {color_below} {min_bound_percentage}%,
                    {color_below} 50%,
                    white 50%,
                    white 100%)
                """
        filter_query = f"{{{column}}} >= {min_bound}"
        if (n_bins - 1) > max_bound_percentage:
            filter_query += f" && {{{column}}} < {max_bound}"
        style = {
            "if": {"filter_query": filter_query, "column_id": column},
            "background": background,
        }
        styles.append(style)
    return styles
