import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import flask
import os

from nav import navbar
from inputs import inputs
import stats
server = flask.Flask(__name__)

app = dash.Dash(__name__, server=server, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = 'Covid and Flask'

app.layout = html.Div(children=[
    html.Div(navbar),
    dbc.Container(children=[
        html.H1(children='COVID Tracking'),
        html.Div('Double Click on the Graph to reset', className="text-muted"),
        html.Div(inputs)
    ]
    ),

    # inputs,

    dcc.Graph(id='states-output', config={'scrollZoom': True}),

])


@app.callback(
    # Output(component_id='input-output', component_property='children'),
    Output('states-output', 'figure'),
    # [Input(component_id='my-id', component_property='value')],
    [Input('states-input', 'value')],

)
def update_state(value):
    df = stats.get_states_hist(value)
    new_positive = stats.get_new_metrics(df, 'positive')
    new_deaths = stats.get_new_metrics(df, 'death')
    pos_avg = stats.moving_average(new_positive)
    death_avg = stats.moving_average(new_deaths)

    return {
        'data': [
            {'x': df['date'].tolist(), 'y': new_positive, 'type': 'bar', 'name': 'New Cases',
             'marker': {'color': 'rgb(2, 117, 216)'}},
            {'x': df['date'].tolist(), 'y': new_deaths, 'type': 'bar', 'name': 'New Deaths',
             'marker': {'color': 'rgb(2, 117, 216)'}},
            {'x': df['date'].tolist(), 'y': pos_avg, 'type': 'line', 'name': '7 day Pos avg',
             'marker': {'color': 'rgb(240, 173, 78)'}},
            {'x': df['date'].tolist(), 'y': death_avg, 'type': 'line', 'name': '7 day Death avg',
             'marker': {'color': 'rgb(240, 173, 78)'}}
        ],
        'layout': go.Layout(
            xaxis={'type': 'category', 'title': 'State'},
            yaxis={'title': 'People'},
            title='{} COVID New Cases and Deaths'.format(value),
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


def get_y_measure(df, measure):
    return df[measure].tolist()


def update_output_div(input_value):
    return 'You\'ve entered "{}"'.format(input_value)


def remove_outliers(list):
    return list[list.between(list.quantile(.15), list.quantile(.85))]


if __name__ == '__main__':
    app.run_server(debug=False)
