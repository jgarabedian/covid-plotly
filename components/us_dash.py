import dash_html_components as html
import dash_bootstrap_components as dbc


def get_current_total(metric) -> str:
    import requests
    import pandas as pd
    endpoint = 'https://covidtracking.com/api/v1/us/current.json'
    response = requests.get(endpoint)
    df = pd.DataFrame(response.json())
    pos = int(df[metric][0])
    return f"{pos:,}"


us_dash_html = html.Div(children=[
    html.H1(className="display-4", children=[
        'US Total'
    ]),
    dbc.Row(children=
    [
        dbc.Col(
            html.Div(className="border text-center kpi-row", children=[
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
        dbc.Col(html.Div(className="border text-center kpi-row", children=[
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
    )
])
