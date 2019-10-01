#Consolidate Coinmetrics with Supply Curve and Ticket Data

#Data Science
import pandas as pd
import numpy as np
import datetime as date
today = date.datetime.now().strftime('%Y-%m-%d')

#Internal Modules
from checkonchain.general.coinmetrics_api import *
from checkonchain.dcronchain.dcr_dcrdata_api import *
from checkonchain.dcronchain.dcr_schedule import *

#Plotly libraries
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

#number of 'Lifetimes to Print
lifetimes = 1.5

#Coinmetrics Data
DCR_data = Coinmetrics_api('dcr',"2016-02-08",today,12).add_metrics()
blk_max = int(DCR_data['blk'][DCR_data.index[-1]]*lifetimes)

#Supply Curve Data
DCR_sply = dcr_supply_schedule(blk_max).dcr_supply_function()

#dcrdata.org
DCR_diff = Extract_dcrdata().dcr_difficulty()
DCR_perf = Extract_dcrdata().dcr_performance()

print('Coinmetrics')
print(DCR_data.columns)
print('Supply Curve')
print(DCR_sply.columns)
print('Difficulty')
print(DCR_diff.columns)
print('Performance')
print(DCR_perf.columns)

DCR_sply['PriceS2Fmodel'] = np.exp(3.31954*np.log(DCR_sply['S2F'])+14.6227)/DCR_sply['SplyCur']

DCR_data['PriceS2Fmodel'].tail(5)

"""%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
CREATE PLOT 01
DUST COMPARED TO FEE LIMITS
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"""

#Create Plot against block height
# Y-axis 1 = USD Price
# Y-axs 2 = Supply Curves

# Create Input Dataset
x_data = [
    DCR_data['blk'],DCR_data['blk'],DCR_data['blk'],
    DCR_data['blk'],DCR_data['blk'],DCR_data['blk'],
    DCR_data['blk'],DCR_sply['blk'],DCR_diff['blk']
    ]

y_data = [
    DCR_data['PriceUSD'],DCR_data['PriceRealised'],DCR_data['PriceAvg'],
    DCR_data['PriceDelta'],DCR_data['PriceTop'],DCR_data['PriceInflow'],
    DCR_data['PriceS2Fmodel'],DCR_sply['PriceS2Fmodel'],DCR_diff['ticket_price']
]
#STAKER INFLOW!!!!!
names = [
    'Price USD','Realised Price','Average Price',
    'Delta Price','Top Price','Price Miner Inflow',
    'Actual S2F Model','Theoretical S2F Model','Ticket Price (DCR)'
]
line_size = [
    2,2,1,
    1,1,1,
    1,1,1
]
dash_type = [
    'solid','solid','dash',
    'dash','dash','dash',
    'dot','dash','dash'
]
opacity = [
    1,1,0.75,
    0.75,0.75,0.75,
    0.75,0.75,1
]
color_data = [
    'rgb(255, 255, 255)', 'rgb(102, 255, 153)', 'rgb(102, 204, 255)',
    'rgb(153, 255, 102)', 'rgb(255, 255, 102)', 'rgb(255, 204, 102)',
    'rgb(255, 153, 102)', 'rgb(255, 102, 102)', 'rgb(255, 80, 80)'
]

# WHITE         'rgb(255, 255, 255)'
# MINT GREEN    'rgb(102, 255, 153)'
# BLUE          'rgb(0, 153, 255)'
# YELLOW        'rgb(102, 102, 153)'
# RED           'rgb(255, 80, 80)'
# PURPLE        'rgb(102, 102, 153)'
# PALE BLUE     'rgb(102, 153, 255)'
#
# Red --> Green Grade
# Red           'rgb(255, 80, 80)'
# Orange        'rgb(255, 102, 102)'
# Orange-Yel    'rgb(255, 153, 102)'
# Yellow        'rgb(255, 204, 102)'
# Yel-Green     'rgb(255, 255, 102)'
# Green         'rgb(153, 255, 102)'


fig = make_subplots(specs=[[{"secondary_y": True}]])
fig.update_layout(template="plotly_dark",title="Decred Pricing Models")
for i in range(0,9):
    fig.add_trace(go.Scatter(
        x=x_data[i], 
        y=y_data[i],
        name=names[i],
        opacity=opacity[i],
        line=dict(
            width=line_size[i],
            dash=dash_type[i],
            color=color_data[i])),
        secondary_y=False)

fig.update_xaxes(
    title_text="<b>Block Height</b>",
    type="linear",
    range=[0,blk_max]
    )
fig.update_yaxes(
    title_text="<b>DCR Price (USD)</b>",
    type="log",
    secondary_y=False,
    range=[-1,4]
    )
#fig.update_yaxes(
#    title_text="<b>BTCUSD Price</b>",
#    tickformat = '$0:.2f',
#    type="log",
#    secondary_y=True,
#    range=[-2,8],
#    color='rgb(102, 102, 153)'
#    )
fig.show()