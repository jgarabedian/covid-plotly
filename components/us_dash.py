import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import numpy as np
import stats



def get_current_total(metric) -> str:
    import requests
    import pandas as pd
    endpoint = 'https://covidtracking.com/api/v1/us/current.json'
    response = requests.get(endpoint)
    df = pd.DataFrame(response.json())
    pos = int(df[metric][0])
    return f"{pos:,}"


df = stats.get_us_hist()
newPos = stats.get_new_metrics(df, 'positive')
posAvg = stats.moving_average(newPos)
newDeath = stats.get_new_metrics(df, 'death')
deathAvg = stats.moving_average(newDeath)
dates = stats.format_dates(df['date'])

fig1 = go.Figure()

fig1.add_trace(go.Bar(
    x=stats.format_dates(df['date'].tolist()),
    y=newPos,
    name='New Cases',
    marker=dict(
        color='rgb(2, 117, 216)'
    )
))

fig1.add_trace(go.Bar(
    x=stats.format_dates(df['date'].tolist()),
    y=newDeath,
    name='New Deaths',
    marker=dict(
        color='rgb(217, 83, 79)'
    )
))

fig1.add_trace(go.Scatter(
    x=stats.format_dates(df['date'].tolist()),
    y=posAvg,
    name='7 Day Pos Avg',
    mode='lines+markers',
    line=dict(color='rgb(240, 173, 78)')
))

fig1.add_trace(go.Scatter(
    x=stats.format_dates(df['date'].tolist()),
    y=deathAvg,
    name='7 Day Death Avg',
    mode='lines+markers',
    line=dict(color='rgb(91, 192, 222)')
))

fig1.update_layout(
    xaxis=dict(
        type='date'
    ),
    yaxis=dict(
        title='People',
        gridcolor='lightgrey'
    ),
    title='New Cases and Deaths',
    plot_bgcolor='white',
    hovermode='x unified'
)

# new tests
new_tests = stats.get_new_metrics(df, 'totalTestResults')

# testing rate
np.seterr(divide='ignore', invalid='ignore')
testing_rate = np.array(newPos) / np.array(new_tests)
rate_avg = stats.moving_average(testing_rate)
fig2 = go.Figure()

fig2 = make_subplots(specs=[[{"secondary_y": True}]])

fig2.add_trace(go.Bar(
    x=stats.format_dates(df['date'].tolist()),
    y=new_tests,
    name='New Tests',
    marker_color='rgb(2, 117, 216)'
),
    secondary_y=False
)

fig2.add_trace(go.Scatter(
    x=stats.format_dates(df['date'].tolist()),
    y=rate_avg,
    name='7 Day Pos Rate Avg',
    mode='lines+markers',
    line=dict(color='rgb(217, 83, 79)')
),
    secondary_y=True
)

fig2.update_layout(
    yaxis=dict(
        title='New Tests',
        gridcolor='lightgrey'
    ),
    yaxis2=dict(
        title='% Positive Rate',
        side='right'
    ),
    yaxis2_tickformat=',.1%',
    plot_bgcolor='white',
    title='Tests vs. Positive Rate',
    xaxis=dict(
        showgrid=True
    ),
    hovermode='x unified'
)

ymax = max(new_tests)

fig2.update_yaxes(
    showspikes=True,
    range=[0, ymax],
    secondary_y=False
)

us_dash_html = html.Div(children=[
    html.H1(className="display-4", children=[
        'US Total'
    ]),
    dbc.Row(children=
    [
        dbc.Col(
            html.Div(className="border rounded text-center kpi-row bg-white shadow", children=[
                html.H1(id="total-positive", children=[
                    # 'Metric'
                    get_current_total('positive')
                ]),
                html.H3(
                    children=[
                        html.Small(className="text-muted", children='Total Positive Cases')
                    ]
                ),
            ]),
            md=12,
            lg=6,
            xl=4,
            sm=12),
        dbc.Col(html.Div(className="border text-center kpi-row bg-white shadow", children=[
            html.H1(id="vent-currently", children=[
                # 'Metric'
                get_current_total('recovered')
            ]),
            html.H3(
                children=[
                    html.Small(className="text-muted", children='Total Recovered')
                ]
                ),
            ]),
            md=12,
            lg=6,
            xl=4,
            sm=12
            ),
        dbc.Col(html.Div(className="border rounded text-center kpi-row bg-white shadow", children=[
            html.H1(id="total-death", children=[
                # 'Metric'
                get_current_total('death')
            ]),
            html.H3(
                children=[
                    html.Small(className="text-muted", children='Total Deaths')
                ]
            ),
            ]),
            md=12,
            lg=6,
            xl=4,
            sm=12),
        dbc.Col(html.Div(className="border text-center kpi-row bg-white shadow", children=[
            html.H1(id="hosp-currently", children=[
                # 'Metric'
                get_current_total('hospitalizedCurrently')
            ]),
            html.H3(
                children=[
                    html.Small(className="text-muted", children='Currently Hospitalized')
                ]
                ),
            ]),
            md=12,
            lg=6,
            xl=4,
            sm=12
            ),
        dbc.Col(html.Div(className="border text-center kpi-row bg-white shadow", children=[
            html.H1(id="icu-currently", children=[
                # 'Metric'
                get_current_total('inIcuCurrently')
            ]),
            html.H3(
                children=[
                    html.Small(className="text-muted", children='Currently in ICU')
                ]
                ),
            ]),
            md=12,
            lg=6,
            xl=4,
            sm=12
            ),
        dbc.Col(html.Div(className="border text-center kpi-row bg-white shadow", children=[
            html.H1(id="vent-currently", children=[
                # 'Metric'
                get_current_total('onVentilatorCurrently')
            ]),
            html.H3(
                children=[
                    html.Small(className="text-muted", children='Currently on Ventilator')
                ]
                ),
            ]),
            md=12,
            lg=6,
            xl=4,
            sm=12
            )
        ],
        justify="center"
    ),
    html.Div(
        dbc.Row(
            justify="center",
            children=[
                dbc.Col(
                    className="mb-2",
                    children=[
                        dcc.Graph(
                            className="shadow",
                            id="us-hist",
                            figure=fig1,
                            config={'scrollZoom': True}
                        )
                    ]
                )
            ]
        )
    ),
    html.Div(
        dbc.Row(
            justify="center",
            children=[
                dbc.Col(
                    className="mb-2",
                    children=[
                        dcc.Graph(
                            className="shadow",
                            id="us-testing",
                            figure=fig2,
                            config={'scrollZoom': True}
                        )
                    ]
                )
            ]
        )
    )
])
