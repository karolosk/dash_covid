import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash_table.Format import Format
from datetime import date
from data_service import get_all_data, get_data
from who_service import get_timeline
import pandas as pd 

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = 'dash-covid'

server = app.server
global_data = get_all_data()

df = get_data()

app.layout = html.Div([

    html.Div(
        className="app-header",
        children=[
            html.P('Coronavirus Data', className="title"),
            html.P('Visualization using Dash',  className="subtitle"),
        ]
    ),

    html.Div(
        children=[
        
            html.Div(
                className="total-info",
                children=[
                    html.P("TOTAL " + str(global_data[0][0]).upper(), className="total-info-label"),
                    html.P(str(global_data[1][0]), className="total-info-data"),
                    html.P("TOTAL " + str(global_data[0][1]).upper(), className="total-info-label"),
                    html.P(str(global_data[1][1]), className="total-info-data"),
                    html.P("TOTAL " + str(global_data[0][2]).upper(), className="total-info-label"),
                    html.P(str(global_data[1][2]), className="total-info-data"),
                    html.P("UPDATED AT", className="total-info-label"),
                    html.P( global_data[2], className="total-info-date"),
                ]
            ),
            
            html.Div(
                className="total-graph",
                children=[
                    dcc.Graph(
                        id='example-graph',
                        figure={
                            'data': [{'x': global_data[0], 'y': global_data[1], 'type': 'bar', 'name': 'Global'},],
                            'layout': {}
                        },
                    ),
                ]
            ),
        ]
    ),
    
    html.Div(
        children = [
            html.Div(
                className="total-graph",
                children = [
                dcc.Graph(
                        figure=dict(
                            data=[
                                dict(
                                    data = [1,2,3],
                                    name='Cases',
                                    marker=dict(
                                        color='rgb(55, 83, 109)'
                                    )
                                ),
                                dict(
                                    data = get_timeline(),
                                    name='Deaths',
                                    marker=dict(
                                        color='rgb(26, 118, 255)'
                                    )
                                )
                            ],
                            layout=dict(
                                title='Timeline',
                                showlegend=True,
                                legend=dict(
                                    x=0,
                                    y=1.0
                                ),
                                margin=dict(l=40, r=0, t=40, b=30)
                            )
                        ),
                        style={'height': 300},
                        id='my-graph'
                    )
                ]
            )
        ]
    ),

    html.Div(
        children=[
            dash_table.DataTable(
                id='global-data-table',
                columns=[
                        {"name": i, "id": i, 'type': 'numeric', 'format': Format(group=',')} for i in df.columns
                    ],
                data=df.to_dict('records'),
                filter_action="native",
                sort_action="native",
                sort_mode="multi",
                style_cell={'textAlign': 'left'},
                style_header={
                    'fontWeight': 'bold'
                },
                # Zebra style / conditional cell format
                style_data_conditional=[
                    {
                        'if': {'row_index': 'odd'},
                        'backgroundColor': 'rgb(248, 248, 248)'
                    },
                    {
                        'if': {'column_id': 'Country'},
                        'fontWeight': 'bold'
                    },
                    {
                        'if': {
                            'column_id': 'Today Cases',
                            'filter_query': '{Today Cases} != 0'
                        },
                        'backgroundColor': '#FFFBE5',
                        'fontWeight': 'bold'
                    },
                    {
                        'if': {
                            'column_id': 'Today Deaths',
                            'filter_query': '{Today Deaths} != 0'
                        },
                        'backgroundColor': '#FFE5E5',
                        'color': '#B12305',
                        'fontWeight': 'bold'
                    },
                ],
            )
        ],
        className="data-table"
    ), 
    
])

if __name__ == '__main__':
    app.run_server(debug=True)