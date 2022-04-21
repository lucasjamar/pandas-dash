# Release 0.1.1

## Minor bug fix
* Replaced default args from dict to None since they are mutable.
* Fixed a bug where certain multi-index have nan values.

# Release 0.1.0

## Major features and improvements
* `to_dash_table()` extension to create data and columns from `pd.DataFrame` for `dash_table.DataTable`
* `to_options()` extension to create options for `dcc.DropDown`.
