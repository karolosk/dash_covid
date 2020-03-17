import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import pandas as pd
from datetime import date
from data_retriever import get_all_data, get_all_country_data, get_all_country_data_as_json, get_data_keys, create_data_file


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = 'dash-covid'

server = app.server
global_data = get_all_data()
country_data = get_all_country_data()
create_data_file()
df = pd.read_csv('coronavirus_data_file_' + str(date.today()) + '.csv')


app.layout = html.Div([

    html.Div(
        className="app-header",
        children=[
            html.Div('Coronavirus Data', className="app-header--title"),
            html.Div('Vizualization using Dash',  className="app-header--subtitle"),
        ]
    ),



    html.Div(
        children=[
            html.Div(
                className="total-info",
                children=[
                    html.H4("Global Data"),
                    html.P("Total " + str(global_data[0][0]) + ": " + str(global_data[1][0])),
                    html.P("Total " + str(global_data[0][1]) + ": " + str(global_data[1][1])),
                    html.P("Total " + str(global_data[0][2]) + ": " + str(global_data[1][2])),
                ]
            ),
            
            html.Div(
                className="total-graph",
                children=[
                    dcc.Graph(
                    id='example-graph',
                    figure={
                        'data': [
                            {'x': global_data[0], 'y': global_data[1], 'type': 'bar', 'name': 'Global'},
                        ],
                        'layout': {
                            
                        }
                    }
                ),
                ]
            ),

        ]
    ),

    html.Div(
        children=[
            html.H4("Country Data", className="country-info"),
            dash_table.DataTable(
                id='global-data-table',
                columns=[{"name": i, "id": i} for i in df.columns],
                data=df.to_dict('records'),
                filter_action="native",
                sort_action="native",
                sort_mode="multi",
                style_header={
                    'fontWeight': 'bold'
                },
                # Zebra style
                style_data_conditional=[{
                    'if': {'row_index': 'odd'},
                    'backgroundColor': 'rgb(248, 248, 248)'
                }],
            )
        ]
    ), 

    html.Div(
        className="app-footer",
        children=[
            html.Div('Made with Dash'),
        ]
    ),

    
])

if __name__ == '__main__':
    app.run_server(debug=True)