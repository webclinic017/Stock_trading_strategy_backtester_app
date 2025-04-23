import dash
from dash import Dash, html, dcc, callback, Output, Input, State
import dash_bootstrap_components as dbc
from dash_bootstrap_components._components.Container import Container

#instantiate dash app
app = Dash(__name__, 
           use_pages = True,
           assets_folder = 'assets',
          external_stylesheets = [dbc.themes.BOOTSTRAP],
          title='Built by Flexxie', 
          meta_tags=[{'name': 'viewport',
                      'content': 'width=device-width, initial-scale=1.0, maximum-scale=1.5, minimum-scale=0.5'}],)


#instantiate app server
server = app.server

#logo source
navbar_logo_src = "./assets/stock-icon.png"
linkedin_logo_src = "./assets/linkedin-logo.png"
github_logo_src = "./assets/github-logo.png"
gmail_logo_src = "./assets/gmail-logo.png"
hand_logo_src = "./assets/waving-hand.svg"

#inline styling for left-sidebar with a fixed height,width and distance from the top
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": "76px",
    "left": 0,
    "bottom": 0,
    "overflow": "auto"    
}
#left-Navigationbar
Navigation_bar= dbc.Navbar([
    dbc.Nav([
        dbc.NavLink([
        html.Div(page["name"], className="ms-2"),
        ], href=page["path"],
           active="exact",
        )
        for page in dash.page_registry.values()
    ],
     vertical=True,
    pills=True,                      
    ),
], color='dark', dark=True, style=SIDEBAR_STYLE)

app.layout= dbc.Container([
    dbc.Row([
        dbc.Navbar([
          dbc.Col(html.Img(src = navbar_logo_src, height = '80px')),
          dbc.Col(dbc.NavbarBrand('BacktesterApp', className = 'ms-2')),
         dbc.Col(style={'width':'200px'}),
        dbc.Col(html.H4('Say hi', style={'color':'#BF9B30'})),
        dbc.Col(html.Img(src = hand_logo_src, height = '50px')),
        dbc.Col(dbc.NavLink(html.Img(src= gmail_logo_src, height='50px'), href='https://felixobioma99@gmail.com')),
        dbc.Col(dbc.NavLink(html.Img(src= linkedin_logo_src,
                style={'height':'50px'}), href='https://www.linkedin.com/in/felix-obioma-nkwuzor-828a20215/')),
        dbc.Col(dbc.NavLink(html.Img(src= github_logo_src, style={'height':'50px'}), href='https://github.com/flex3'))
        ], color='grey', dark=True, fixed='top'),
    ], align = 'center', className = 'g-0'),
    dbc.Row([
        dbc.Col([Navigation_bar], width=2),
        dbc.Col([dash.page_container
                ], width=10)
    ]),
], fluid= True)

#run app
if __name__ == '__main__':
    app.run_server(debug=False)






