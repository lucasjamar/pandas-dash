from dash import Dash, html, dash_table, dcc
import plotly.express as px
import pandas_plotly


# App
app = Dash(__name__, title="Pandas Plotly Dashboard")
server = app.server
gdp = px.data.gapminder()
country_options = gdp.pp.to_options(label="country", title="continent")
flat_data = gdp.head(50)
flat_data, flat_columns = flat_data.pp.to_dash_table()

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
gdp, gdp_columns = gdp.pp.to_dash_table(
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
tips, tips_columns = tips.pp.to_dash_table(
    column_properties={"country": {"presentation": "markdown"}}
)

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
            sort_mode="single",
            filter_action="native",
            merge_duplicate_headers=True,
        ),
        dash_table.DataTable(
            data=tips,
            columns=tips_columns,
            sort_action="native",
            sort_mode="single",
            filter_action="native",
            merge_duplicate_headers=True,
        ),
    ]
)

if __name__ == "__main__":
    app.run_server(debug=True)