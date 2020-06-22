import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output
import flask
import numpy as np

from components.states_dash import states_dash
import stats
from components.us_dash import get_current_total
from nav import navbar
import plotly.graph_objs as go

server = flask.Flask(__name__)

app = dash.Dash(__name__, server=server, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = 'Covid and Flask'

app.layout = html.Div(children=[
    html.Div(navbar),
    dbc.Container(children=(
        html.P(className="text-muted", children=[
            'Thanks to ',
            html.A(className="text-reset", href="https://covidtracking.com/",
                   target="_blank", children='COVID Tracking'),
            ' for the data.'
        ]),
        html.H1(className="display-4", children=[
            'US Total'
        ]),
        dbc.Row(id="us-container", children=
          [
              dbc.Col(html.Div(className="border text-center", children=[
                  html.H1(id="total-positive", children=[
                      # 'Metric'
                      get_current_total('positive')
                  ]),
                  html.H3(
                      children=[
                          html.Small(className="text-muted", children='Total Positive Cases')
                      ]
                  ),
              ])),
              dbc.Col(html.Div(className="border text-center", children=[
                  html.H1(id="total-death", children=[
                      # 'Metric'
                      get_current_total('death')
                  ]),
                  html.H3(
                      children=[
                        html.Small(className="text-muted", children='Total Deaths')
                      ]
                  ),

              ])),
              dbc.Col(html.Div(className="border text-center", children=[
                  html.H1(id="hosp-currently", children=[
                      # 'Metric'
                      get_current_total('hospitalizedCurrently')
                  ]),
                  html.H3(
                      children=[
                          html.Small(className="text-muted", children='Currently Hospitalized')
                      ]
                  ),
              ])),
          ]
        ),
        html.Hr(),
        html.Div(states_dash)
    )
    ),

])

@app.callback(
    Output('states-output', 'figure'),
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
    title = '{} COVID New Cases and Deaths'.format(value)

    return {
        'data': [
            {'x': stats.format_dates(df['date'].tolist()), 'y': new_positive, 'type': 'bar', 'name': 'New Cases',
             'marker': {'color': 'rgb(2, 117, 216)'}},
            {'x': stats.format_dates(df['date'].tolist()), 'y': new_deaths, 'type': 'bar', 'name': 'New Deaths',
             'marker': {'color': 'rgb(2, 117, 216)'}},
            {'x': stats.format_dates(df['date'].tolist()), 'y': pos_avg, 'type': 'line', 'name': '7 day Pos avg',
             'marker': {'color': 'rgb(240, 173, 78)'}},
            {'x': stats.format_dates(df['date'].tolist()), 'y': death_avg, 'type': 'line', 'name': '7 day Death avg',
             'marker': {'color': 'rgb(240, 173, 78)'}}
        ],
        'layout': go.Layout(
            xaxis={'type': 'date'},
            yaxis={'title': 'People'},
            title=title,
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


if __name__ == '__main__':
    app.run_server(debug=False)
