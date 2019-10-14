#Data Science
import pandas as pd
import numpy as np
import math


from checkonchain.btconchain.btc_add_metrics import *
from checkonchain.dcronchain.dcr_add_metrics import *
from checkonchain.ltconchain.ltc_add_metrics import *
from checkonchain.general.regression_analysis import *

#Plotly Libraries
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.io as pio
pio.renderers.default = "browser"

BTC_sply = btc_add_metrics().btc_sply(1200000) #Theoretical Supply curve
BTC_real = btc_add_metrics().btc_pricing_models() #Actual Performance
BTC_half = btc_supply_schedule(0).btc_halvings_stepped()

DCR_sply = dcr_add_metrics().dcr_sply(1200000*2-33600*2) #Theoretical Supply curve
DCR_real = dcr_add_metrics().dcr_pricing_models() #Actual Market Performance
DCR_natv = dcr_add_metrics().dcr_natv() #Actual On-chain Performance
dcr_btc_blk_start = int(BTC_sply[BTC_sply['Sply_ideal']==1680000]['blk'])
DCR_sply['btc_blk'] = dcr_btc_blk_start + 0.5*DCR_sply['blk']
DCR_real['btc_blk'] = dcr_btc_blk_start + 0.5*DCR_real['blk']

LTC_sply = ltc_add_metrics().ltc_sply(1200000*2) #Theoretical Supply curve
LTC_real = ltc_add_metrics().ltc_real() #Actual Performance


import os
os.getcwd()
os.chdir('D:\code_development\checkonchain\checkonchain')
BTC_real.to_csv(r"dcronchain\resources\data\BTC_real.csv")
DCR_real.to_csv(r"dcronchain\resources\data\DCR_real.csv")
LTC_real.to_csv(r"dcronchain\resources\data\LTC_real.csv")






x_data = [
    BTC_sply['blk'],
    DCR_sply['btc_blk']
]
y_data = [
    BTC_sply['Sply_ideal'],
    DCR_sply['Sply_ideal']
    ]
name_data = [
    'Bitcoin',
    'Decred'
    ]
color_data = [
    'rgb(237, 109, 71)',
    'rgb(46, 214, 161)'
    ]
dash_data = [
    'solid',
    'solid'
    ]
size_data = [
    4,4
    ]
legend_data = [
    True,True
]

fig = make_subplots(specs=[[{"secondary_y": False}]])
for i in range(0,2):
    fig.add_trace(go.Scatter(
        x=x_data[i], y=y_data[i],
        name=name_data[i],
        showlegend=legend_data[i],
        line=dict(width=size_data[i],color=color_data[i],dash=dash_data[i])),
        secondary_y=False)

"""$$$$$$$$$$$$$$$ FORMATTING $$$$$$$$$$$$$$$$"""
# Add figure title
fig.update_layout(title_text="Market Capitalisation vs Stock-to-Flow Ratio")
fig.update_xaxes(
    title_text="<b>Stock-to-Flow Ratio</b>",
    type='log',
    range=[-1,2]
    )
fig.update_yaxes(
    title_text="<b>Coin Market Cap</b>",
    type="log",
    range=[4,12],
    secondary_y=False)
fig.update_layout(template="plotly_dark")
fig.show()
