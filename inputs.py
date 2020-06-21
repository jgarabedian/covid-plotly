import dash_bootstrap_components as dbc
import dash_html_components as html
import stats

options: list = []
for state in stats.get_states():
    state_dict = {'label': state, 'value': state}
    options.append(state_dict)

state_dropdown = dbc.Select(
    id="states-input",
    options=options,
    value="AK"
)

inputs = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(html.Div(state_dropdown)),
            ]
        )
    ]
)
