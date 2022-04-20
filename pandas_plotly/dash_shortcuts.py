from typing import Dict, Tuple, List

import pandas as pd


@pd.api.extensions.register_dataframe_accessor("pp")
class DashAccessor:
    def __init__(self, pandas_obj):
        self._validate(pandas_obj)
        self._obj = pandas_obj

    @staticmethod
    def _validate(obj):
        if not isinstance(obj, pd.DataFrame):
            raise AttributeError("Must be `pd.DataFrame`.")

    def to_dash_table(
        self,
        separator: str = "_",
        properties: Dict = {},
        column_properties: Dict = {},
    ) -> Tuple:
        df = self._obj.copy()
        column_dicts, new_column_names = [], []
        for column in df.columns:
            if isinstance(column, (list, tuple)):
                column_str = [str(x) for x in column]
                non_empty_column_str = [x for x in column_str if x != ""]
                if "" in column_str:
                    last_non_empty_str = non_empty_column_str[-1]
                    column_str = [x for x in column_str if x != last_non_empty_str] + [
                        last_non_empty_str
                    ]
                column_id = f"{separator}".join(non_empty_column_str)
            else:
                column_id = str(column)
                column_str = column_id
            new_column_names.append(column_id)
            column_dict = {"id": column_id, "name": column_str, **properties}
            if column_id in column_properties:
                column_dict.update(column_properties[column_id])
            column_dicts.append(column_dict)
        df.columns = new_column_names
        df = df.to_dict("records")
        return df, column_dicts

    def to_options(
        self,
        label: str,
        na_remove: bool = True,
        sort: bool = False,
        ascending: bool = True,
        title: str = None,
        disabled: str = None,
    ) -> List:
        df = self._obj.copy()
        df = df.drop_duplicates(subset=[label])
        if na_remove:
            df = df.dropna(subset=[label])
        else:
            df[label] = df[label].fillna("")
        if sort:
            df = df.sort_values(by=label, ascending=ascending)
        options = []
        for index, row in df.iterrows():
            row_label = str(row[label])
            option = {"label": row_label, "value": row_label}
            if title:
                row_title = str(row[title])
                if pd.notnull(row_title):
                    option["title"] = row_title
            if disabled:
                row_disabled = row[disabled]
                if pd.notnull(row_disabled):
                    option["disabled"] = row_disabled
            options.append(option)
        return options
