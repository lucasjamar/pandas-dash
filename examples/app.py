from dash import Dash, html, dash_table, dcc
import plotly.express as px
import pandas_dash as pdd


# App
print(pdd.__version__)
app = Dash(__name__, title="Pandas-Dash")
server = app.server
gdp = px.data.gapminder()
country_options = gdp.dash.to_options(label="country", title="continent")
flat_data = gdp.head(50)
flat_data, flat_columns = flat_data.dash.to_dash_table()

gdp["country"] = (
    "["
    + gdp["country"]
    + "](https://en.wikipedia.org/wiki/"
    + gdp["country"].str.replace(" ", "_")
    + ")"
)
gdp = gdp.sort_values(["continent", "country", "year"])
gdp = (
    gdp.pivot(
        index=["continent", "country"],
        columns="year",
        values=["gdpPercap", "pop"],
    )
    .round(2)
    .reset_index()
)
styling, _ = pdd.heatmap(gdp, n_bins=9)
print(styling)
gdp, gdp_columns = gdp.dash.to_dash_table(
    column_properties={"country": {"presentation": "markdown"}}
)
tips = px.data.tips()
tips = (
    tips.pivot_table(
        index=["day", "time", "size"],
        columns=["sex", "smoker"],
        values=["tip", "total_bill"],
    )
    .reset_index()
    .round(2)
)
tips, tips_columns = tips.dash.to_dash_table()

app.layout = html.Div(
    children=[
        dcc.Dropdown(options=country_options, value="China"),
        dash_table.DataTable(
            data=flat_data,
            columns=flat_columns,
        ),
        dash_table.DataTable(
            data=gdp,
            columns=gdp_columns,
            sort_action="native",
            sort_mode="multi",
            filter_action="native",
            style_data_conditional=styling,
            merge_duplicate_headers=True,
        ),
        dash_table.DataTable(
            data=tips,
            columns=tips_columns,
            sort_action="native",
            sort_mode="multi",
            filter_action="native",
            merge_duplicate_headers=True,
        ),
    ]
)

if __name__ == "__main__":
    app.run_server(debug=True)
