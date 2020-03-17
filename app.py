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

      
    html.H4("Country Data"),
    dash_table.DataTable(
        id='global-data-table',
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict('records'),
        filter_action="native",
        sort_action="native",
        sort_mode="multi",
        page_size= 10,
        row_selectable='multi',
        style_header={
            'fontWeight': 'bold'
        },
        # Zebra style
        style_data_conditional=[{
            'if': {'row_index': 'odd'},
            'backgroundColor': 'rgb(248, 248, 248)'
        }],
        
        
    ),
    html.Div(id='datatable-interactivity-container'),
])

@app.callback(
    Output('datatable-interactivity-container', "children"),
    [Input('global-data-table', "derived_virtual_data"),
     Input('global-data-table', "derived_virtual_selected_rows")])
def update_graphs(rows, derived_virtual_selected_rows):
    if derived_virtual_selected_rows is None:
        derived_virtual_selected_rows = []

    dff = df if rows is None else pd.DataFrame(rows)

    colors = ['#7FDBFF' if i in derived_virtual_selected_rows else '#0074D9'
              for i in range(len(dff))]

    return [
        dcc.Graph(
            id=column,
            figure={
                "data": [
                    {
                        "x": dff["country"],
                        "y": dff[column],
                        "type": "bar",
                        "marker": {"color": colors},
                    }
                ],
                "layout": {
                    "xaxis": {"automargin": True},
                    "yaxis": {
                        "automargin": True,
                        "title": {"text": column}
                    },
                    "margin": {"t": 30, "l": 10, "r": 10},
                    
                },
            },
        )
        # check if column exists - user may have deleted it
        # If `column.deletable=False`, then you don't
        # need to do this check.
        for column in ["cases", "deaths", "recovered", "todayCases"]
    ]


if __name__ == '__main__':
    app.run_server(debug=True)