import dash_core_components as dcc
import dash_html_components as html
from inputs import inputs


states_dash = html.Div(
    children=[
        html.Div('Double Click on the Graph to reset',
                 className="text-muted"),
        html.Div(inputs),
        html.Div(
            children=[
                dcc.Graph(id="states-output",
                      config={'scrollZoom': True})
            ]
        )
    ]
)





