# Plot Normalised Difficulty Adjustments against Coin Supply

#DataScience
import pandas as pd
import numpy as np
import datetime as date
today = date.datetime.now().strftime('%Y-%m-%d')

#Internal Modules
from checkonchain.general.coinmetrics_api import *

#Plotly libraries
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.io as pio
pio.renderers.default = "browser"


BTC = Coinmetrics_api('btc',"2009-01-03",today,35).convert_to_pd()
BTC.set_index(['date'], inplace=True)
LTC = Coinmetrics_api('ltc',"2011-10-07",today,35).convert_to_pd()
LTC.set_index(['date'], inplace=True)
BCH = Coinmetrics_api('bch',"2017-08-01",today,35).convert_to_pd()
BCH.set_index(['date'], inplace=True)
DASH = Coinmetrics_api('dash',"2014-01-19",today,35).convert_to_pd()
DASH.set_index(['date'], inplace=True)
DCR = Coinmetrics_api('dcr',"2016-02-08",today,35).convert_to_pd()
DCR.set_index(['date'], inplace=True)
XMR = Coinmetrics_api('xmr',"2014-04-18",today,35).convert_to_pd()
XMR.set_index(['date'], inplace=True)
ZEC = Coinmetrics_api('zec',"2016-10-28",today,35).convert_to_pd()
ZEC.set_index(['date'], inplace=True)
ETH = Coinmetrics_api('eth',"2015-07-30",today,35).convert_to_pd()
ETH.set_index(['date'], inplace=True)

BTC.columns
metric = 'CapMrktCurUSD'

assets = ['BTC','LTC','BCH','DASH','DCR','XMR','ZEC','ETH']

response = pd.concat([
    BTC[metric], 
    LTC[metric],
    BCH[metric],
    DASH[metric],
    DCR[metric],
    XMR[metric],
    ZEC[metric],
    ETH[metric]
    ], axis=1)
response.columns=assets

for i in assets:
    idx = response[i].first_valid_index()
    response[i+'_mod'] = response[[i]]#/response.loc[idx,[i]]
    response[i+'_mod'] = response[i+'_mod'].rolling(90).mean()

sply = pd.concat([
    BTC['S2F'], 
    LTC['S2F'],
    BCH['S2F'],
    DASH['S2F'],
    DCR['S2F'],
    XMR['S2F'],
    ZEC['S2F'],
    ETH['S2F']
    ], axis=1)
sply.columns=assets

x_data = [
    sply['BTC'],sply['LTC'],
    sply['BCH'],sply['DASH'],
    sply['DCR'],sply['XMR'],
    sply['ZEC'],sply['ETH'],
    BTC['S2F']
]

y_data = [
    response['BTC_mod'],response['LTC_mod'],
    response['BCH_mod'],response['DASH_mod'],
    response['DCR_mod'],response['XMR_mod'],
    response['ZEC_mod'],response['ETH_mod'],
    np.exp(3.31954*np.log(BTC['S2F'])+14.6227)
]

color_data = [
    'rgb(239, 125, 50)',  
    'rgb(250, 38, 53)',
    'rgb(114, 49, 163)',   
    'rgb(0, 153, 255)',
    'rgb(46, 214, 161)', 
    'rgb(255, 102, 0)',  
    'rgb(255, 192, 0)', 
    'rgb(216, 216, 216)',
    'rgb(255, 255, 255)'
]

name_data = ['BTC','LTC','BCH','DASH','DCR','XMR','ZEC','ETH','S2F Model']

fig = make_subplots(specs=[[{"secondary_y": False}]])
for i in range(0,9):
    fig.add_trace(go.Scatter(
        x=x_data[i], 
        y=y_data[i],
        mode='markers',
        name=name_data[i],
        marker=dict(size=4,color=color_data[i])
        ))


fig.update_xaxes(
    title_text="<b>Stock-to-Flow Ratio</b>",type="log",range=[-1,2])
fig.update_yaxes(
    title_text="<b>Market Cap (USD)</b>",type="log",range=[5,12])
fig.update_layout(template="plotly_dark")
fig.show()