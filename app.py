import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import stats

app = dash.Dash(__name__)

options = []
for state in stats.get_states():
    state_dict = {'label': state, 'value': state}
    options.append(state_dict)


app.layout = html.Div(children=[
    html.H1(children='COVID Tracking'),

    html.Div(children='''
        Dash: A web application framework for Python.
    '''),

    dcc.Graph(
        id='example-graph',
        figure={
            'data': [
                {'x': stats.get_states(), 'y': stats.get_positive(), 'type': 'bar', 'name': 'States'},
            ],
            'layout': {
                'title': 'COVID Positive Numbers'
            }
        }
    ),

    dcc.Dropdown(id='states-input',
                 options=options,
                 value='NY'),

    dcc.Dropdown(id='input-measure',
                 options=[
                        {'label': 'Positive Cases', 'value': 'positive'},
                        {'label': 'Total Deaths', 'value': 'death'}],
                    value='positive'),

    dcc.Graph(id='states-output'),


])


@app.callback(
    # Output(component_id='input-output', component_property='children'),
    Output('states-output', 'figure'),
    # [Input(component_id='my-id', component_property='value')],
    [Input('states-input', 'value'), Input('input-measure', 'value')],

)
def update_state(value, measure):
    df = stats.get_states_hist(value)

    return {
        'data': [
            {'x': df['date'].tolist(), 'y': get_y_measure(df, measure), 'type': 'line', 'name': 'Date'}
        ],
        'layout': go.Layout(
            xaxis={'type': 'category', 'title': 'State'},
            yaxis={'type': 'log', 'title': 'Positive Cases'},
            title='{} COVID {}'.format(value, measure.capitalize())
        )
    }

def get_y_measure(df, measure):
    return df[measure].tolist()

def update_output_div(input_value):
    return 'You\'ve entered "{}"'.format(input_value)


if __name__ == '__main__':
    app.run_server(debug=True)
