import dash
from dash import Dash, html
import dash_bootstrap_components as dbc
from dash_bootstrap_components._components.Container import Container

#instantiate web page
dash.register_page(__name__ ,assets_folder = 'assets', path= '/', name= 'About')

#app layout
layout= html.Div([
    dbc.Container([
        dbc.Row([
                html.H1(['Holla there !!']),
                html.Hr(),
                html.H5([
                    "This is a demo web app for analysing stocks and backtesting trading strategies to:", html.Br(),
                    "> Minimise loses during bad days.", html.Br(),
                    "> Optimize gains during the good days.",html.Br(),
                    "> Fully manage your trading capital", html.Br()
                ],
                style={'font-weight':'bold'}),
               html.H5([
               "How to use the app?",html.Br(),
            "1. In the Make Analysis page,",html.Br(),
            "The user simply selects a stock ticker, a given date range then any particular chart from the dropdown menu",html.Br(),
            "for some basic technical analysis if you so desire.",html.Br(),
           "2. Proceed to the Backtest Strategies page to choose from a dropdown of simulated strategies suitable to your trading goals.",html.Br(),
            "Offcourse, after having selected your desired stock and trading year.",html.Br(),
            "Ok! thats basically all. We used postgres for the database and the generous twelvedata api for all the data brouhaha needed", html.Br(),
              "Reach out to me on linkedin, star the project on github (Click the image on the Navbar).",html.Br(),
               "Wishing you an insightful analysis!!!!"
               ], style={'font-weight':'Bold'})
        ]),
    ], fluid= True)   
],style= {"margin-top":"100px", "margin-left":"60px"})
