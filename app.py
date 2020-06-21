import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import stats

app = dash.Dash(__name__)

# df = stats.get_data('https://covidtracking.com/api/v1/states/current.json')
options = []
new_df = stats.get_states_hist('NY')
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
    #
    # dcc.Input(id='my-id', value='initial value', type='text'),
    #
    # html.Div(id='input-output'),

    dcc.Dropdown(id='states-input',
                 options=options,
                 value='NY'),

    # html.Div(id='states-output'),


    dcc.Graph(
        id='states-output',
        figure={
            'data': [
                {'x': new_df['date'].tolist(), 'y': new_df['positive'].tolist(), 'type': 'line', 'name': 'Date'}
            ],
            'layout': go.Layout(
                xaxis={'type': 'category', 'title': 'State'},
                yaxis={'type': 'log', 'title': 'Positive Cases'}
                )
            }
    ),

    # html.H1(children='COVID History'),
    #
    # html.Div(children='''
    #     Historical Numbers in the US
    # '''),
    #
    # dcc.Graph(
    #     id='us-historical',
    #     figure={
    #         'data': [
    #             {'x': stats.get_us_hist_dates(), 'y': stats.get_us_hist_positive(), 'type': 'line', 'name': 'Date'}
    #         ],
    #         'layout': {
    #             'title': 'US Historical Trend'
    #         }
    #     }
    # )
])


@app.callback(
    # Output(component_id='input-output', component_property='children'),
    Output(component_id='states-output', component_property='children'),
    # [Input(component_id='my-id', component_property='value')],
    [Input('states-input', 'value')]

)
def update_state(value):
    df = stats.get_states_hist(value)
    return df
    # return 'You have selected "{}"'.format(value)

def update_output_div(input_value):
    return 'You\'ve entered "{}"'.format(input_value)


if __name__ == '__main__':
    app.run_server(debug=True)
