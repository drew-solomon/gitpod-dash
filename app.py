import dash
from dash import dash_table
from dash import dcc # dash core components
from dash.dependencies import Input, Output, State
from dash import html
import numpy as np

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
    html.Button(id='submit-button-state', n_clicks=0, children='Create pivot table'),
    dash_table.DataTable(
        id='table',
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict('records')
    )
])

# define the identity function
def identity(x): return x

# callback function to update pivot table based on selected inputs
@app.callback(
    Output('table', 'data'),
    Output('table', 'columns'),
    Input('submit-button-state', 'n_clicks'),
    State('index-dropdown', 'value'),
    State('columns-dropdown', 'value'),
    State('values-dropdown', 'value')
    )
def update_pivottable(n_clicks, selected_index, selected_columns, selected_values):
    print(n_clicks)
    print("index:", selected_index)
    print("columns:", selected_columns)
    print("values:", selected_values)
    pivot_table = df.pivot_table(
        index=selected_index,
        columns=selected_columns, 
        values=selected_values,
        aggfunc=identity,
    )
    print(pivot_table)
    # pivot table dict
    pivot_table_dict = pivot_table.to_dict('records')
    pivot_table_columns = [{"name": i, "id": i} for i in pivot_table.columns]
    #print("COLUMNS", pivot_table_columns)
    #print("VALUES", pivot_table.values)
    return pivot_table_dict, pivot_table_columns

app.run_server(debug=True, host="0.0.0.0")
