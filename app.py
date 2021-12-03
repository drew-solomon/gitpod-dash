import dash
from dash import dash_table
from dash import dcc # dash core components
from dash.dependencies import Input, Output
from dash import html

import pandas as pd

# read csv of periodic table
df = pd.read_csv('https://bit.ly/elements-periodic-table')

app = dash.Dash(__name__)

#  dropdown menus for index, columns, and values, and datatable
app.layout = html.Div([
    dcc.Dropdown(
        id='index-dropdown',
        options=[{'label': i, 'value': i} for i in df.columns],
         placeholder="Select an index"
    ),
    dcc.Dropdown(
        id='columns-dropdown',
        options=[{'label': i, 'value': i} for i in df.columns],
        placeholder="Select columns"
    ),
    dcc.Dropdown(
        id='values-dropdown',
        options=[{'label': i, 'value': i} for i in df.columns],
        placeholder="Select values"
    ),
    dash_table.DataTable(
        id='table',
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict('records')
    )
])


# callback function to update pivot table based on selected inputs
@app.callback(
    Output('table', 'data'),
    Output('table', 'columns'),
    Input('index-dropdown', 'value'),
    Input('columns-dropdown', 'value'),
    Input('values-dropdown', 'value')
    )
def update_pivottable(selected_index, selected_columns, selected_values):
    # define the identity function
    def identity(x): return x
    pivot_table = df.pivot_table(
        index=selected_index,
        columns=selected_columns, 
        values=selected_values,
        aggfunc=identity,
    )
    # pivot table dict
    pivot_table_dict = pivot_table.to_dict('records')
    # pivot table columns
    pivot_table_columns = [{"name": i, "id": i} for i in pivot_table.columns]
    return pivot_table_dict, pivot_table_columns

app.run_server(debug=True, host="0.0.0.0")
