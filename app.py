import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import flask
import numpy as np

from nav import navbar
from inputs import inputs
import stats
server = flask.Flask(__name__)

app = dash.Dash(__name__, server=server, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = 'Covid and Flask'

app.layout = html.Div(children=[
    html.Div(navbar),
    dbc.Container(children=[
        html.P(className="text-muted", children=[
            'Thanks to ',
            html.A(className="text-reset", href="https://covidtracking.com/",
                   target="_blank", children='COVID Tracking'),
            ' for the data.'
        ]),
        html.Div('Double Click on the Graph to reset', className="text-muted"),
        html.Div(inputs),
        html.Div(children=[
            dcc.Graph(id='states-output', config={'scrollZoom': True}, animate=True)
        ]

        )
    ]
    ),

    # inputs,



])


@app.callback(
    # Output(component_id='input-output', component_property='children'),
    Output('states-output', 'figure'),
    # [Input(component_id='my-id', component_property='value')],
    [Input('states-input', 'value')],

)
def update_state(value: str):
    """
    :name update_state
    :desc run when new state is selected from dropdown
    :param value: str - state abbr
    :return: figure
    """
    df = stats.get_states_hist(value)
    new_positive = stats.get_new_metrics(df, 'positive')
    new_deaths = stats.get_new_metrics(df, 'death')
    pos_avg = stats.moving_average(new_positive)
    death_avg = stats.moving_average(new_deaths)
    # title = '{} COVID New Cases and Deaths'.format(value)

    return {
        'data': [
            {'x': format_dates(df['date'].tolist()), 'y': new_positive, 'type': 'bar', 'name': 'New Cases',
             'marker': {'color': 'rgb(2, 117, 216)'}},
            {'x': format_dates(df['date'].tolist()), 'y': new_deaths, 'type': 'bar', 'name': 'New Deaths',
             'marker': {'color': 'rgb(2, 117, 216)'}},
            {'x': format_dates(df['date'].tolist()), 'y': pos_avg, 'type': 'line', 'name': '7 day Pos avg',
             'marker': {'color': 'rgb(240, 173, 78)'}},
            {'x': format_dates(df['date'].tolist()), 'y': death_avg, 'type': 'line', 'name': '7 day Death avg',
             'marker': {'color': 'rgb(240, 173, 78)'}}
        ],
        'layout': go.Layout(
            xaxis={'type': 'date'},
            yaxis={'title': 'People', 'range': [0, np.nanmax(new_positive)]},
            title='New COVID Cases and Deaths',
            legend=dict(
                x=.01,
                y=.75,
                traceorder="normal",
                font=dict(
                    family="sans-serif",
                    size=12,
                    color="black"
                ),
                bordercolor="Black",
                borderwidth=1
            )
        )
    }


def get_y_measure(df: list, measure: str) -> list:
    # Convert the df column to a list
    return df[measure].tolist()


def format_dates(list_col) -> list:
    # Convert yyyymmdd to date for axis
    from datetime import datetime
    new_list = []
    for i in list_col:
        date_object = datetime.strptime(str(i),'%Y%m%d')
        new_list.append(date_object.strftime('%Y-%m-%d'))
    return new_list


if __name__ == '__main__':
    app.run_server(debug=False)
