import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash_table.Format import Format
import pandas as pd 
from service.service import get_global_data, get_table_data, get_timeline_dataframe


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
external_scripts = [

]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server


app.index_string = """<!DOCTYPE html>
<html>
    <head>
        <script async src="https://www.googletagmanager.com/gtag/js?id=UA-161477467-1"></script>
        <script>
        window.dataLayer = window.dataLayer || [];
        function gtag(){dataLayer.push(arguments);}
        gtag('js', new Date());

        gtag('config', 'UA-161477467-1');
        </script>

        {%metas%}
        <title>dash-covid</title>
        {%favicon%}
        {%css%}
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>"""


global_data = get_global_data()
datatable_dataframe = get_table_data()
timeline_data = get_timeline_dataframe()

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
                                    x= timeline_data.index.values.tolist(),
                                    y=timeline_data['deaths'].tolist(),
                                    name='Deaths',
                                    marker=dict(
                                        color='rgb(177, 35, 5)'
                                    )
                                ),
                                dict(
                                    x= timeline_data.index.values.tolist(),
                                    y=timeline_data['recovered'].tolist(),
                                    name='Recovered',
                                    marker=dict(
                                        color='rgb(126, 170, 121)'
                                    )
                                ),
                                dict(
                                    x= timeline_data.index.values.tolist(),
                                    y=timeline_data['confirmed'].tolist(),
                                    name='Cases',
                                    marker=dict(
                                        color='rgb(26, 118, 255)'
                                    ),
                                )
                            ],
                            layout=dict(
                                title='Timeline',
                                showlegend=True,
                                xaxis=dict(
                                    showticklabels=False
                                ),
                                legend=dict(
                                    x=0,
                                    y=1.0
                                ),
                                margin=dict(l=40, r=0, t=40, b=30)
                            )
                        ),
                        id='timeline-graph'
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
                        {"name": i, "id": i, 'type': 'numeric', 'format': Format(group=',')} for i in datatable_dataframe.columns
                    ],
                data=datatable_dataframe.to_dict('records'),
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