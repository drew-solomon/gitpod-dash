import dash
from dash import dash_table
from dash import dcc # dash core components
from dash.dependencies import Input, Output
from dash import html

import pandas as pd

df = pd.read_csv('https://bit.ly/elements-periodic-table')

app = dash.Dash(__name__)

#  dropdown menus for index, columns, and values, and datatable
app.layout = html.Div([
    dcc.Dropdown(
        id='index-dropdown',
        options=[{'label': i, 'value': i} for i in df.columns],
        value='Period',
         placeholder="Select an index"
    ),
    dcc.Dropdown(
        id='columns-dropdown',
        options=[{'label': i, 'value': i} for i in df.columns],
        value='Group',
        placeholder="Select columns"
    ),
    dcc.Dropdown(
        id='values-dropdown',
        options=[{'label': i, 'value': i} for i in df.columns],
        value='Element',
        placeholder="Select values"
    ),
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
    Input('index-dropdown', 'selected_index'),
    Input('columns-dropdown', 'selected_columns'),
    Input('values-dropdown', 'selected_values')
    )
def update_pivottable(selected_index, selected_columns, selected_values):
    pivot_table = df.pivot_table(
        index=selected_index,
        columns=selected_columns, 
        values=selected_values,
        aggfunc=identity,
    )
    return pivot_table

app.run_server(debug=True, host="0.0.0.0")
