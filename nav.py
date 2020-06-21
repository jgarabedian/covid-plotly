import dash_bootstrap_components as dbc

navbar = dbc.NavbarSimple(
    # children=[
    #     dbc.NavItem(dbc.NavLink("Page 1", href="#")),
    # ],
    brand="COVID and Flask",
    brand_href="#",
    color="primary",
    expand=True,
    dark=True,
)