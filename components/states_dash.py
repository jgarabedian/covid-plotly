import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from inputs import inputs


def get_current_state(state: str, metric: str) -> str:
    import requests
    endpoint = "".join(['https://covidtracking.com/api/v1/states/', state.lower(), '/current.json'])
    response = requests.get(endpoint)
    df = response.json()
    pos = df[metric]
    if pos is None:
        return 0
    else:
        return f"{int(pos):,}"


states_dash = html.Div(
    children=[
        html.H1(className="display-4", id="dash-title"),
        dbc.Row(
            children=[
                dbc.Col(
                    html.Div(className="border text-center kpi-row bg-white shadow rounded",
                             children=[
                                 html.H1(id="total-positive"),
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
                dbc.Col(
                    html.Div(className="border text-center kpi-row bg-white shadow rounded",
                             children=[
                                 html.H1(id="total-recovered"),
                                 html.H3(
                                     children=[
                                         html.Small(className="text-muted", children='Total Recovered')
                                     ]
                                 ),
                             ]),
                    md=12,
                    lg=6,
                    xl=4,
                    sm=12),
                dbc.Col(
                    html.Div(className="border text-center kpi-row bg-white shadow rounded",
                             children=[
                                 html.H1(id="total-death"),
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
                dbc.Col(
                    html.Div(className="border text-center kpi-row bg-white shadow rounded",
                             children=[
                                 html.H1(id="hosp-currently"),
                                 html.H3(
                                     children=[
                                         html.Small(className="text-muted", children='Currently Hospitalized')
                                     ]
                                 ),
                             ]),
                    md=12,
                    lg=6,
                    xl=4,
                    sm=12),
                dbc.Col(
                    html.Div(className="border text-center kpi-row bg-white shadow rounded",
                             children=[
                                 html.H1(id="icu-currently"),
                                 html.H3(
                                     children=[
                                         html.Small(className="text-muted", children='Currently in ICU')
                                     ]
                                 ),
                             ]),
                    md=12,
                    lg=6,
                    xl=4,
                    sm=12),
                dbc.Col(
                    html.Div(className="border text-center kpi-row bg-white shadow rounded",
                             children=[
                                 html.H1(id="vent-currently"),
                                 html.H3(
                                     children=[
                                         html.Small(className="text-muted", children='Currently on Ventilator')
                                     ]
                                 ),
                             ]),
                    md=12,
                    lg=6,
                    xl=4,
                    sm=12)
            ],
            justify="center"
        ),
        html.Div('Double Click on the Graph to reset',
                 className="text-muted"),
        html.Div(inputs),
        dbc.Row(
            dbc.Col(
                className="mb-2",
                children=[
                    dcc.Graph(id="states-output",
                              className="shadow",
                            config={'scrollZoom': True})
                ]

            )
        ),
        dbc.Row(
            dbc.Col(html.Div(
                'The rate of positive tests is a good indicator of '
                'the effect testing is having on overall numbers.',
                className="text-muted")
            )
        ),
        dbc.Row(
            justify="center",
            children=[
                dbc.Col(
                    className="mb-2",
                    children=[
                        dcc.Graph(
                            className="shadow",
                            id="total-tests",
                            config={'scrollZoom': True}
                        )
                    ]
                )
            ]
        )
    ]
)
