import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import plotly.graph_objs as go
from plotly.subplots import make_subplots
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

fig = {
    'data': [
        {'x': dates,
         'y': newPos, 'type': 'bar',
         'name': 'New Cases',
         'marker': {'color': 'rgb(2, 117, 216)'}},
        {'x': dates,
         'y': posAvg, 'type': 'line',
         'name': '7 day Pos avg',
         'marker': {'color': 'rgb(240, 173, 78)'}},
        {'x': dates,
         'y': newDeath, 'type': 'bar',
         'name': 'New Deaths',
         'marker': {'color': 'rgb(217, 83, 79)'}},
        {'x': dates,
         'y': deathAvg, 'type': 'line',
         'name': '7 day Death avg',
         'marker': {'color': 'rgb(240, 173, 78)'}}
    ],
    'layout': go.Layout(
        xaxis = {'type': 'date'},
        yaxis = {'title': 'People'},
        title='US COVID Cases',
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

# testing rate
df['testing_rate'] = df['positive'] / df['totalTestResults']
fig2 = go.Figure()

fig2 = make_subplots(specs=[[{"secondary_y": True}]])

fig2.add_trace(go.Bar(
    x=stats.format_dates(df['date'].tolist()),
    y=df['totalTestResults'],
    name='Total Tests',
    marker_color='rgb(2, 117, 216)'
),
    secondary_y=False
)

fig2.add_trace(go.Scatter(
    x=stats.format_dates(df['date'].tolist()),
    y=df['testing_rate'],
    name='Positive Rate',
    mode='lines+markers',
    line=dict(color='rgb(217, 83, 79)')
),
    secondary_y=True
)

fig2.update_layout(
    yaxis=dict(
        title='Total Tests',
        gridcolor='lightgrey'
    ),
    yaxis2=dict(
        title='% Positive Rate',
        side='right'
    ),
    yaxis2_tickformat='%',
    plot_bgcolor='white',
    title='Tests vs. Positive Rate',
    xaxis=dict(
        showgrid=True
    ),
    hovermode='x'
)

us_dash_html = html.Div(children=[
    html.H1(className="display-4", children=[
        'US Total'
    ]),
    dbc.Row(children=
    [
        dbc.Col(
            html.Div(className="border rounded text-center kpi-row", children=[
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
        dbc.Col(html.Div(className="border rounded text-center kpi-row", children=[
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
        dbc.Col(html.Div(className="border text-center kpi-row", children=[
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
        dbc.Col(html.Div(className="border text-center kpi-row", children=[
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
        dbc.Col(html.Div(className="border text-center kpi-row", children=[
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
                    children=[
                        dcc.Graph(
                            id="us-hist",
                            figure=fig,
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
                    children=[
                        dcc.Graph(
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
