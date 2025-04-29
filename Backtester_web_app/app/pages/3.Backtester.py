import dash
from dash import Dash, html, dash_table, dcc, callback, Output, Input, State
import dash_bootstrap_components as dbc
from dash_bootstrap_components._components.Container import Container
import strategy_selector

#instantiate web page
dash.register_page(__name__, name='Backtest Strategies')

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
              dbc.Col(html.Div([html.Label('Input startDate'),dcc.DatePickerSingle(id = 'start-date', date = '2023-01-01')],
            style = {'text-align':'center'})),
             dbc.Col(html.Div([html.Label('Input endDate'),dcc.DatePickerSingle(id = 'end-date', date ='2023-12-29')],
            style = {'text-align':'center'})),
             dbc.Col(dbc.Button('Submit',id='date-inputerbutton',
                n_clicks=0, style={'background-color':'black'}))
          ], style={'marginBottom':'20px'}),
          #prepare layout for selecting the trading strategies to backtest
         dbc.Row([
         html.Div([
        html.H5('Select trading strategies to backtest(Cash=1000, Commission=0.1%)'),
        dcc.Dropdown(id='backtester-dropdown', options=[
        {'label':html.Pre('1. buy and hold when ema(50period) crosses above the middle bollinger\nsell when ema crosses below the middle bollinger.',
                         style={'marginTop':'20px'}),'value':'EmaBband'},
        {'label':html.Pre('2. buy if closingprice is above the middle bolinger and rsi>20 and 60\nsell if closingprice is in reverse and rsi < 80 and 60.',
                         style={'marginTop':'20px'}), 'value':'BbandRsi'},
        {'label':html.Pre('3. buy if shorter ema(10period) crosses above a longer ema(20period) and rsi(7period)>60\nsell if in reverse.',
                         style={'marginTop':'20px'}), 'value':'EmaRsi'},
        {'label':html.Pre('4. buy if shorter sma(10period) crosses above a longer sma(20period) and rsi(7period)>60\nsell if in reverse.',
                         style={'marginTop':'20px'}), 'value':'RsiSma'},
        {'label':html.Pre('5. buy if rsi(7periods) > 20 and 60\nsell if rsi < 80 and 60.',
                         style={'marginTop':'20px'}), 'value':'SimpleRsi'},
        {'label':html.Pre('6. buy if shorter ema(10period) crosses above a longer ema(20period)\nsell if in reverse.',
                         style={'marginTop':'20px'}), 'value':'SimpleEma'},
        {'label':html.Pre('7. buy if closingprice > sma(20period), sell if closingprice < sma.',
                          style={'marginTop':'20px'}), 'value':'SmaPrice'}
                 ])
             ])    
         ]),
            dbc.Row([
             html.Pre(id='backtester-output')
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
        )
                ], vertical=True, navbar=True),
            style=right_sidebar, color ='dark', dark = True)
        ], width=3),
    ], fluid=True),
], style={"margin-top":"110px"})
@callback(
    Output(component_id='backtester-output', component_property='children'),
    Input(component_id='ticker-dropdown', component_property='value'),
    Input(component_id='date-inputerbutton', component_property='n_clicks'),
    State(component_id='start-date', component_property='date'),
    State(component_id='end-date', component_property='date'),
    Input(component_id='backtester-dropdown', component_property='value')
)
def run_backtester(ticker, clicks, start_date, end_date, strategy):
    ss= strategy_selector
    if clicks is None:
        start_date = None
        end_date = None
    else:
        start_date = start_date
        end_date = end_date
    #run the backtester algorithm
    if strategy == 'EmaBband':
        return ss.bband_ema_strategy(ticker=ticker, start_date=start_date, end_date=end_date)
    elif strategy == 'BbandRsi':
        return ss.bband_rsi_strategy(ticker=ticker, start_date=start_date, end_date=end_date)
    elif strategy == 'EmaRsi':
        return ss.ema_rsi_strategy(ticker=ticker, start_date=start_date, end_date=end_date)
    elif strategy == 'RsiSma':
        return ss.rsi_sma_strategy(ticker=ticker, start_date=start_date, end_date=end_date)
    elif strategy == 'SimpleRsi':
        return ss.rsi_strategy(ticker=ticker, start_date=start_date, end_date=end_date)
    elif strategy == 'SimpleEma':
        return ss.ema_strategy(ticker=ticker, start_date=start_date, end_date=end_date)
    elif strategy == 'SmaPrice':
        return ss.sma_closeprice_strategy(ticker=ticker, start_date=start_date, end_date=end_date)
