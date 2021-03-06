import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output
import flask
import numpy as np

np.seterr(divide='ignore', invalid='ignore')

from components.states_dash import states_dash, get_current_state
from components.us_dash import us_dash_html
import stats
import CONSTANTS
from components.nav import navbar
import plotly.graph_objs as go
from plotly.subplots import make_subplots

server = flask.Flask(__name__)

meta_tags = {
    "name": "Covid and Flask",
    "description": "A site utilizing Flask and Plotly to analyze COVID-19 Information."
}

app = dash.Dash(__name__, server=server,
                external_stylesheets=[dbc.themes.BOOTSTRAP],
                meta_tags=[meta_tags],
                suppress_callback_exceptions=True)
app.title = 'Covid and Flask'

app.index_string = """<!DOCTYPE html>
<html>
    <head>
        <!-- Global site tag (gtag.js) - Google Analytics -->
        <script async src="https://www.googletagmanager.com/gtag/js?id=UA-150551765-3"></script>
        <script>
          window.dataLayer = window.dataLayer || [];
          function gtag(){dataLayer.push(arguments);}
          gtag('js', new Date());
        
          gtag('config', 'UA-150551765-3');
        </script>

        {%metas%}
        <title>{%title%}</title>
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

state_acronyms = list(CONSTANTS.US_STATE_ABBR.values())
key_list = list(CONSTANTS.US_STATE_ABBR.keys())
app.layout = html.Div(
    children=[
        dcc.Location(id='url', refresh=False),
        html.Div(navbar),
        dbc.Container(
            fluid=True,
            className="bg-light",
            children=(
                html.P(className="text-muted", children=[
                    'Thanks to ',
                    html.A(className="text-reset", href="https://covidtracking.com/",
                           target="_blank", children='COVID Tracking'),
                    ' for the data.'
                ]),
                html.Div(id="dash-content")
            )
        ),
    ])


@app.callback(dash.dependencies.Output('dash-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def update_dash(pathname):
    if pathname == '/':
        return us_dash_html
    if pathname == '/state':
        return states_dash
    else:
        return us_dash_html


@app.callback(
    [
        Output('dash-title', 'children'),
        Output('states-output', 'figure'),
        Output('total-positive', 'children'),
        Output('total-death', 'children'),
        Output('total-recovered', 'children'),
        Output('hosp-currently', 'children'),
        Output('icu-currently', 'children'),
        Output('vent-currently', 'children'),
        Output('total-tests', 'figure')
    ],
    [Input('states-input', 'value')],

)
def update_state(value: str):
    """
    :name update_state
    :desc run when new state is selected from dropdown
    :param value: str - state abbr
    :return: figure
    """
    import pandas as pd
    df = stats.get_states_hist(value)
    df['newPos'] = np.asarray(stats.get_new_metrics(df, 'positive'))
    df['newTests'] = np.asarray(stats.get_new_metrics(df, 'totalTestResults'))
    # df = df2[(df2['newPos'] > 0) & (df2['newTests'] > 0)]

    # print(df2)
    # df = df2
    new_pos = stats.get_new_metrics(df, 'positive')
    new_positive = stats.get_new_metrics(df, 'positive')
    new_deaths = stats.get_new_metrics(df, 'death')
    pos_avg = stats.moving_average(new_positive)
    death_avg = stats.moving_average(new_deaths)
    title = '{} COVID New Cases and Deaths'.format(value)

    current_pos = get_current_state(value, 'positive')
    current_death = get_current_state(value, 'death')
    current_recovered = get_current_state(value, 'recovered')
    current_hosp = get_current_state(value, 'hospitalizedCurrently')
    current_icu = get_current_state(value, 'inIcuCurrently')
    current_vent = get_current_state(value, 'onVentilatorCurrently')

    state_name = key_list[state_acronyms.index(value)]

    dashTitle = state_name + " Dashboard"

    fig3 = go.Figure()

    # New positives
    fig3.add_trace(go.Bar(
        x=stats.format_dates(df['date'].tolist()),
        y=new_positive,
        name='New Cases',
        marker=dict(
            color='rgb(2, 117, 216)'
        )
    ))

    fig3.add_trace(go.Bar(
        x=stats.format_dates(df['date'].tolist()),
        y=new_deaths,
        name='New Deaths',
        marker=dict(
            color='rgb(217, 83, 79)'
        )
    ))

    fig3.add_trace(go.Scatter(
        x=stats.format_dates(df['date'].tolist()),
        y=pos_avg,
        name='7 Day Pos Avg',
        mode='lines+markers',
        line=dict(color='rgb(240, 173, 78)')
    ))

    fig3.add_trace(go.Scatter(
        x=stats.format_dates(df['date'].tolist()),
        y=death_avg,
        name='7 Day Death Avg',
        mode='lines+markers',
        line=dict(color='rgb(91, 192, 222)')
    ))

    fig3.update_layout(
        xaxis=dict(
            type='date'
        ),
        yaxis=dict(
            title='People',
            gridcolor='lightgrey'
        ),
        title=title,
        plot_bgcolor='white',
        hovermode='x unified'
    )

    # testing rate
    np.seterr(divide='ignore', invalid='ignore')
    new_tests = stats.get_new_metrics(df, 'totalTestResults')
    testing_rate = np.array(new_pos) / np.array(new_tests)
    df['testing_rate'] = df['newPos'] / df['newTests']
    rate_avg = stats.moving_average(testing_rate)
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
        y=pd.Series(rate_avg).fillna(0).tolist(),
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
        yaxis2_tickformat=',.2%',
        yaxis2_range=[0, max(rate_avg)],
        plot_bgcolor='white',
        title='Tests vs. Positive Rate',
        xaxis=dict(
            showgrid=True
        ),
        hovermode='x unified'
    )
    ymax = max(df['newTests'].dropna())
    fig2.update_yaxes(
        showspikes=True,
        range=[0, ymax],
        secondary_y=False
    )

    tuple_return = (dashTitle, fig3, current_pos,
                    current_death, current_recovered,
                    current_hosp, current_icu,
                    current_vent, fig2)

    return tuple_return


if __name__ == '__main__':
    app.run_server(debug=True)
