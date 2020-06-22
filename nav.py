import dash_bootstrap_components as dbc

navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("US Dashboard", href="/")),
        dbc.NavItem(dbc.NavLink("State Dashboard", href="/state")),
        dbc.NavItem(dbc.NavLink("State Comparison", href="/compare"))
    ],
    brand="COVID and Flask",
    brand_href="#",
    color="primary",
    expand=True,
    dark=True,
)