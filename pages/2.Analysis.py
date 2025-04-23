import dash
from dash import Dash, html, dash_table, dcc, callback, Output, Input, State
import dash_bootstrap_components as dbc
from dash_bootstrap_components._components.Container import Container
from charts import chart_selector

#instantiate web page
dash.register_page(__name__, name='Make Analysis')

#style right-sidebar for controls
right_sidebar= {
    "position": "fixed",
    "top": 0,
    "right": 0,
    "bottom": 0,
    "overflow": "auto"    
}
#setup page layout
layout= html.Div([
    dbc.Container([
        dbc.Col([
          dbc.Row([
              dbc.Col(html.Div([html.Label('Input startDate'),dcc.Input(id = 'start-date', type='text',
            minLength=10, maxLength=10, value = '2023-01-01',
            placeholder = 'yyyy-mm-dd',style = {'border-radius':'50px', 'text-align':'center'})],
            style = {'text-align':'center'})),
             dbc.Col(html.Div([html.Label('Input endDate'),dcc.Input(id = 'end-date', type='text', minLength=10,maxLength=10,
              value='2023-12-31', placeholder = 'yyyy-mm-dd',style ={'border-radius':'50px', 'text-align':'center'})],
            style = {'text-align':'center'})),
             dbc.Col(dbc.Button('Submit',id='date-inputerbutton',
                n_clicks=0, style={'background-color':'black'}))
          ]),
          dbc.Row([
              dcc.Graph(id='output-chart', figure={})
          ])
        ], width=9),
        dbc.Col([
            dbc.Navbar(
                dbc.Nav([
                    dbc.NavItem(
          html.Div([
              html.Label('Select Stock', style={'color':'#BF9B30'}),
              dcc.Dropdown(id='ticker-dropdown', options=[
            {'label':'MSFT', 'value':'MSFT'},
            {'label':'AAPL', 'value':'AAPL'},
            {'label':'META', 'value':'META'},
            {'label':'AMZN', 'value':'AMZN'},
            {'label':'TSLA', 'value':'TSLA'},
            {'label':'GOOGL', 'value':'GOOGL'},
            {'label':'WMT', 'value':'WMT'},
            {'label':'NVDA', 'value':'NVDA'},
            {'label':'AMZN', 'value':'AMZN'},
            {'label':'ORCL', 'value':'ORCL'},
            {'label':'JMIA', 'value':'JMIA'},
            {'label':'IHS', 'value':'IHS'}
              ], clearable=False, value='MSFT',
                           style={'border-radius':'50px', 'width':'185px', 'background-color':'grey'})
          ], style={'text-align':'center','font-weight':'bold'})  
        ),
      dbc.NavItem(
          html.Div([
              html.Label('Select Chart', style={'color':'#BF9B30'}),
              dcc.Dropdown(id='analytics-chart', options=[
                 {'label':'Candlestick-Chart', 'value':'Candlestick'},
                 {'label':'EMA-RSI', 'value':'EMA-RSI'},
                 {'label':'BollingerBands', 'value':'Bollingerbands'},
                 {'label':'SMA-RSI', 'value':'SMA-RSI'},
                 {'label':'Macd-Adx', 'value':'Macd-Adx'},
                  {'label':'Returns', 'value':'Returns'},
                  
              ], clearable=False, value='Candlestick',
                           style={'border-radius':'50px', 'width':'185px', 'margin-top':'0px'})
          ], style={'text-align':'center','font-weight':'bold'})  
        ),
                ], vertical=True, navbar=True),
            style=right_sidebar, color ='dark', dark = True)
        ], width=4),
    ], fluid=True),
], style={"margin-top":"89px"})
#create callbacks to output chart
@callback(
    Output(component_id='output-chart', component_property='figure'),
    Input(component_id='ticker-dropdown', component_property='value'),
    Input(component_id='analytics-chart', component_property='value'),
    State(component_id='start-date', component_property='value'),
    State(component_id='end-date', component_property='value'),
    Input(component_id='date-inputerbutton', component_property='n_clicks')
)
def display_chart(ticker,chart,start_date, end_date,n_clicks):
    charts = chart_selector()
    display_chart = None
    if chart == 'Candlestick':
        display_chart= charts.plot_price_only(ticker=ticker, start_date=start_date, end_date=end_date)
    elif chart == 'EMA-RSI':
        display_chart= charts.plot_ema_rsi(ticker=ticker, start_date=start_date, end_date=end_date)
    elif chart == 'SMA-RSI':
        display_chart= charts.plot_sma_rsi(ticker=ticker, start_date=start_date, end_date=end_date)
    elif chart == 'Bollingerbands':
        display_chart= charts.plot_bollinger(ticker=ticker, start_date=start_date, end_date=end_date)
    elif chart == 'Macd-Adx':
        display_chart= charts.plot_macd_adx(ticker=ticker, start_date=start_date, end_date=end_date)
    elif chart == 'Returns':
        display_chart= charts.plot_return(ticker=ticker, start_date=start_date, end_date=end_date)
    return display_chart
