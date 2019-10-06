#Compare the behaviour of Decred and Bitcoin
import pandas as pd
import numpy as np
import datetime as date
today = date.datetime.now().strftime('%Y-%m-%d')

from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.io as pio
pio.renderers.default = "browser"

from checkonchain.general.coinmetrics_api import *
from checkonchain.btconchain.btc_schedule import *
from checkonchain.dcronchain.dcr_schedule import *
from checkonchain.dcronchain.dcr_dcrdata_api import *
"""**************************************************************************
                            Part 0 - Code Setup
***************************************************************************"""

"""##### PULL INITIAL DATSETS #####"""
#Pull BTC and DCR data from Coinmetrics
BTC_coin = Coinmetrics_api('btc',"2009-01-03",today,35).add_metrics()
DCR_coin = Coinmetrics_api('dcr',"2016-02-08",today,35).add_metrics()
print('Coinmetrics')
print(BTC_coin.columns)

#Pull BTC and DCR data from Theoretical SUpply Curves
BTC_sply = btc_supply_schedule(1200000).btc_supply_function()
DCR_sply = dcr_supply_schedule(1200000*2-33600*2).dcr_supply_function()
print('Supply')
print(BTC_sply.columns)

"""##### CALCULATE DCR EQUIVALENT BTC BLOCK HEIGHT @ 1.68M BTC #####"""
#Calculate the btc_block where supply = 1.68million BTC
btc_blk_start = int(BTC_sply[BTC_sply['Sply_ideal']==1680000]['blk'])
#Create DCR_Sply column of equivalent btc_blk
#ASSUMES 1BTC block == 2 DCR blocks
DCR_sply['btc_blk'] = btc_blk_start + 0.5*DCR_sply['blk']
#Create XXX_data column absorbing XXX_Sply columns
"""##### COMPILE INTO FINAL DATASETS #####"""
#XXX_real --> COINMETRICS = PARENT
BTC_real = pd.concat([BTC_coin.set_index('blk',drop=False),BTC_sply.set_index('blk')],axis=1,join='inner')
BTC_real = BTC_real.reset_index(drop=True)
DCR_real = pd.concat([DCR_coin.set_index('blk',drop=False),DCR_sply.set_index('blk')],axis=1,join='inner')
DCR_real = DCR_real.reset_index(drop=True)
# Calculate Max-Min step to plot up Bitcoin halvings
BTC_half = btc_supply_schedule(0).btc_halvings_stepped()

#Decred Specific Metrics
# Extract from Modules
DCR_perf = Extract_dcrdata().dcr_performance()
DCR_diff = Extract_dcrdata().dcr_difficulty()
#Create temp dataframe containing just btc_blk and then concat
df_temp = pd.DataFrame(data=DCR_real.set_index('blk',drop=False)['btc_blk'])
DCR_perf = pd.concat([DCR_perf.set_index('blk',drop=False),df_temp],axis=1,join='inner')



"""**************************************************************************
                            Part 1 - Monetary Policy
***************************************************************************"""


"""%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
                CREATE PLOT 01 (TOP)
        SUPPLY CURVES - STACKED AREA CHARTS
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"""
x_data = [
    BTC_sply['blk'],
    DCR_sply['btc_blk'],
    DCR_sply['btc_blk'],
    DCR_sply['btc_blk'],
    DCR_sply['btc_blk']
]
y_data = [
    BTC_sply['Sply_ideal'],
    DCR_sply['Sply_ideal'],
    DCR_sply['PoWSply_ideal'],
    DCR_sply['PoSSply_ideal'],
    DCR_sply['FundSply_ideal']
]
name_data = [
    'BTC Supply',
    'DCR Total Supply',
    'DCR PoW Supply',
    'DCR PoS Supply',
    'DCR Treasury Supply',
]
color_data = [
    'rgb(255, 153, 0)',
    'rgb(46, 214, 161)',
    'rgb(41, 112, 255)',
    'rgb(46, 214, 161)',
    'rgb(237, 109, 71)'
]
fill_data = [
    'tozeroy',
    'tonexty',
    'tonexty',
    'tonexty',
    'tozeroy'
]
opacity_data = [
    0.5,1,0.5,0.5,0.5
]
fig = go.Figure()
for i in range(0,5):
    fig.add_trace(go.Scatter(
        x=x_data[i], 
        y=y_data[i],
        name=name_data[i], 
        fill=fill_data[i],
        #fillcolor=color_data[i],
        #line_color= color_data[i],
        line=dict(
            color=color_data[i],
            width=2
            #opacity=opacity_data[i]
        )))
fig.update_layout(template="plotly_dark",title="Bitcoin and Decred Theoretical Supply Curves")
fig.show()



"""%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
                CREATE PLOT 02
        SUPPLY CURVES AND STOCK TO FLOW RATIOS
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"""
# BTC Theoretical Supply curve
# DCR Theoretical Supply curve
# DCR Theoretical Supply curve (Offset to BTC 1.68million)
# BTC Theoretical S2F
# DCR Theoretical S2F
# DCR Theoretical S2F (Offset to BTC 1.68million)
# BTC Halvings
x_data = [
    BTC_sply['blk'],
    BTC_sply['blk'],
    BTC_real['blk'],
    DCR_sply['btc_blk']+372384,
    DCR_sply['btc_blk']+372384,
    DCR_real['btc_blk']+372384,
    DCR_sply['btc_blk'],
    DCR_sply['btc_blk'],
    DCR_real['btc_blk'],
    BTC_half['blk']
]
y_data = [
    BTC_sply['Sply_ideal'],
    BTC_sply['S2F_ideal'],
    BTC_real['S2F'],
    DCR_sply['Sply_ideal'],
    DCR_sply['S2F_ideal'],
    DCR_real['S2F'],
    DCR_sply['Sply_ideal'],
    DCR_sply['S2F_ideal'],
    DCR_real['S2F'],
    BTC_half['y_arb']
    ]
name_data = [
    'Bitcoin Coin Supply',
    'Bitcoin S2F Ratio',
    'Bitcoin S2F Ratio (Actual)',
    'Decred Coin Supply',
    'Decred S2F Ratio',
    'Decred S2F Ratio (Actual)',
    'Decred Coin Supply (Offset)',
    'Decred S2F Ratio (Offset)',
    'Decred S2F Ratio (Offset, Actual)',
    'BTC Halvings'
    ]
color_data = [
    'rgb(237, 109, 71)','rgb(237, 109, 71)','rgb(237, 109, 71)',
    'rgb(112, 203, 255)','rgb(112, 203, 255)','rgb(112, 203, 255)',
    'rgb(46, 214, 161)','rgb(46, 214, 161)','rgb(46, 214, 161)',
    'rgb(255, 255, 255)' 
    ]
dash_data = [
    'solid','dot','solid',
    'solid','dot','solid',
    'solid','dot','solid',
    'solid'
    ]
width_data = [
    5,5,1,4,4,1,4,4,1,0.5
    ]
opacity_data = [
    1,1,0.75,
    1,1,0.75,
    1,1,0.75,
    0.5
]
name_data[6]

fig = make_subplots(specs=[[{"secondary_y": True}]])
for i in [0,3,6]:
    fig.add_trace(go.Scatter(
        x=x_data[i], y=y_data[i],
        name=name_data[i],
        opacity=opacity_data[i],
        line=dict(width=width_data[i],color=color_data[i],dash=dash_data[i])),
        secondary_y=False)
for i in [1,2,4,5,7,8,9]:
    fig.add_trace(go.Scatter(
        x=x_data[i], y=y_data[i],
        name=name_data[i],
        opacity=opacity_data[i],
        line=dict(width=width_data[i],color=color_data[i],dash=dash_data[i])),
        secondary_y=True)
"""$$$$$$$$$$$$$$$ FORMATTING $$$$$$$$$$$$$$$$"""
# Add figure title
fig.update_layout(title_text="Bitcoin and Decred Monetary Policy")
fig.update_xaxes(
    title_text="<b>Bitcoin Block Height</b>",
    type='linear',
    range=[0,1200000]
    )
fig.update_yaxes(
    title_text="<b>Coin Supply</b>",
    type="linear",
    range=[0,21000000],
    secondary_y=False)
fig.update_yaxes(
    title_text="<b>Stock-to-Flow Ratio</b>",
    type="log",
    range=[-1,5],
    secondary_y=True)
fig.update_layout(template="plotly_dark")
fig.show()




"""%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
                CREATE PLOT 03
SUPPLY AND DEMAND - % of Supply Mined VS Market Cap
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"""

x_data = [
    BTC_real['SplyCur']/21000000,BTC_real['SplyCur']/21000000,
    DCR_real['SplyCur']/21000000,DCR_real['SplyCur']/21000000,
    BTC_half['end_pct_totsply']
]
y_data = [
    BTC_real['CapMrktCurUSD'],BTC_real['CapRealUSD'],
    DCR_real['CapMrktCurUSD'],DCR_real['CapRealUSD'],
    BTC_half['y_arb']
    ]
name_data = [
    'Bitcoin Market Cap','Bitcoin Realised Cap',
    'Decred Market Cap','Decred Realised Cap',
    'BTC Halvings'
    ]
color_data = [
    'rgb(237, 109, 71)','rgb(237, 109, 71)',
    'rgb(46, 214, 161)','rgb(46, 214, 161)',
    'rgb(255, 255, 255)' 
    ]
dash_data = [
    'solid','dash',
    'solid','dash',
    'dot'
    ]
width_data = [
    2,2,2,2,0.5
    ]


fig = make_subplots(specs=[[{"secondary_y": False}]])
for i in range(0,5):
    fig.add_trace(go.Scatter(
        x=x_data[i], y=y_data[i],
        name=name_data[i],
        line=dict(width=width_data[i],color=color_data[i],dash=dash_data[i])),
        secondary_y=False)

"""$$$$$$$$$$$$$$$ FORMATTING $$$$$$$$$$$$$$$$"""
# Add figure title
fig.update_layout(title_text="Market Capitalisation vs Supply Mined")
fig.update_xaxes(
    title_text="<b>Coin Supply Issued</b>",
    type='linear',
    range=[0,1]
    )
fig.update_yaxes(
    title_text="<b>Coin Market Cap</b>",
    type="log",
    range=[4,12],
    secondary_y=False)
fig.update_layout(template="plotly_dark")
fig.show()




"""%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
                CREATE PLOT 04
        STOCK-TO-FLOW - S2F Market Cap
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"""

x_data = [
    BTC_real['S2F'],
    DCR_real['S2F'],
    BTC_half['S2F'],BTC_real['S2F']
]
y_data = [
    BTC_real['CapMrktCurUSD'],
    DCR_real['CapMrktCurUSD'],
    BTC_half['y_arb'],BTC_real['CapS2Fmodel']
    ]
name_data = [
    'Bitcoin Market Cap',
    'Decred Market Cap',
    'Bitcoin Halvings','Plan B Model'
    ]
color_data = [
    'rgb(237, 109, 71)',
    'rgb(46, 214, 161)',
    'rgb(255,255,255)','rgb(255,255,255)'
    ]
dash_data = [
    'solid',
    'solid',
    'dash','solid'
    ]
size_data = [
    4,4,2,2
    ]

fig = make_subplots(specs=[[{"secondary_y": False}]])
for i in range(0,2):
    fig.add_trace(go.Scatter(
        mode = 'markers',
        x=x_data[i], y=y_data[i],
        name=name_data[i],
        marker=dict(size=size_data[i],color=color_data[i])),
        secondary_y=False)
for i in range(2,4):
    fig.add_trace(go.Scatter(
        x=x_data[i], y=y_data[i],
        name=name_data[i],
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



"""**************************************************************************
                            Part 2 - Proof of Work
***************************************************************************"""

# Blockchain.com hashrate w/ coinmetrics block (UPDATE 5 Oct 2019)
BTC_hash = pd.read_csv(r"D:\code_development\checkonchain\checkonchain\btconchain\data\btc_blockchaincom_hashrate.csv")
# Clean DCR hashrate data
DCR_perf = DCR_perf[DCR_perf['pow_hashrate']>1]

"""%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
                CREATE PLOT 05
        Hashrate and Difficulty Adjustment
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"""
DCR_real.columns
DCR_perf.columns
DCR_diff.columns
BTC_hash.columns

x_data = [
    BTC_real['blk'],
    DCR_real['btc_blk'],
    DCR_real['btc_blk'],
    BTC_hash['blk'],
    DCR_perf['btc_blk']
]
y_data = [
    BTC_real['DiffMean']/BTC_real.loc[6,'DiffMean'],
    DCR_real['DiffMean']/DCR_real.loc[1,'DiffMean'],
    DCR_real['DiffMean']*100/60/DCR_real.loc[1,'DiffMean'],
    BTC_hash['hashrate_THs'],
    DCR_perf['pow_hashrate']
    ]
name_data = [
    'Bitcoin Difficulty',
    'Decred Difficulty',
    'Decred Difficulty (Offset x 10/6)',
    'Bitcoin Hashrate',
    'Decred Hashrate'
    ]
color_data = [
    'rgb(237, 109, 71)',
    'rgb(46, 214, 161)',
    'rgb(255, 214, 161)',
    'rgb(255, 153, 0)',
    'rgb(112, 203, 255)'
    ]
dash_data = [
    'solid',
    'solid',
    'dot',
    'solid',
    'solid'
    ]
width_data = [
    4,4,4,4,4
    ]

fig = make_subplots(specs=[[{"secondary_y": True}]])
for i in [0,1,2]:
    fig.add_trace(go.Scatter(
        mode = 'lines',
        x=x_data[i], y=y_data[i],
        name=name_data[i],
        #yaxis=axis_data[i],
        line=dict(width=width_data[i],color=color_data[i])),
        secondary_y=False)
for i in [3,4]:
    fig.add_trace(go.Scatter(
        mode = 'lines',
        x=x_data[i], y=y_data[i],
        name=name_data[i],
        #yaxis=axis_data[i],
        line=dict(width=width_data[i],color=color_data[i])),
        secondary_y=True)
"""$$$$$$$$$$$$$$$ FORMATTING $$$$$$$$$$$$$$$$"""
# Add figure title
fig.update_layout(title_text="Proof of Work Security")
fig.update_xaxes(
    title_text="<b>Bitcoin Block Height</b>",
    type='linear'
    )
fig.update_yaxes(
    title_text="<b>PoW Difficulty Growth</b>",
    type="log",
    tickformat= ',.0%',
    secondary_y=False)
fig.update_yaxes(
    title_text="<b>Hashrate (TH/s)</b>",
    type="log",
    secondary_y=True)
fig.update_layout(template="plotly_dark")
fig.show()





"""%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
                CREATE PLOT 05
        Hashrate and Difficulty Adjustment
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"""
DCR_real.columns
DCR_perf.columns
DCR_diff.columns
BTC_hash.columns

x_data = [
    BTC_real['SplyCur']/21000000,
    DCR_real['SplyCur']/21000000,
    DCR_real['SplyCur']/21000000
]
y_data = [
    BTC_real['DiffMean']/BTC_real.loc[6,'DiffMean'],
    DCR_real['DiffMean']/DCR_real.loc[1,'DiffMean'],
    DCR_real['DiffMean']*100/60/DCR_real.loc[1,'DiffMean']
    ]
name_data = [
    'Bitcoin Difficulty',
    'Decred Difficulty (Offset)',
    'Decred Difficulty (Offset x 10/6)'
    ]
color_data = [
    'rgb(237, 109, 71)',
    'rgb(46, 214, 161)',
    'rgb(255, 214, 161)'
    ]
dash_data = [
    'solid',
    'solid',
    'dot'
    ]
width_data = [
    4,4,4
    ]

fig = make_subplots(specs=[[{"secondary_y": True}]])
for i in [0,1,2]:
    fig.add_trace(go.Scatter(
        mode = 'lines',
        x=x_data[i], y=y_data[i],
        name=name_data[i],
        #yaxis=axis_data[i],
        line=dict(width=width_data[i],color=color_data[i])),
        secondary_y=False)
"""$$$$$$$$$$$$$$$ FORMATTING $$$$$$$$$$$$$$$$"""
# Add figure title
fig.update_layout(title_text="Proof of Work Security")
fig.update_xaxes(
    title_text="<b>Total Supply Minted</b>",
    type='linear',
    tickformat= ',.0%'
    )
fig.update_yaxes(
    title_text="<b>PoW Difficulty Growth</b>",
    type="log",
    tickformat= ',.0%',
    secondary_y=False)
fig.update_layout(template="plotly_dark")
fig.show()




#Dual Axis

#axis_data = [
#    "y","y2","y2"
#]
#
#fig = go.Figure()
#fig.update_layout(
#    xaxis=dict(
#        title="<b>Bitcoin Block Height</b>",
#        type='linear'
#    ),
#    yaxis=dict(
#        title="Bitcoin Difficulty Growth",
#        type='log',
#        #range=[0,15],
#        #tickformat= ',.0%')
#        titlefont=dict(color=color_data[0]),
#        tickfont=dict(color=color_data[0]),
#    ),
#    yaxis2=dict(
#        title="Decred Difficulty Growth",
#        type='log',
#        #range=[0,15],
#        titlefont=dict(color=color_data[1]),
#        tickfont=dict(color=color_data[1]),
#        anchor="free",
#        overlaying="y",
#        side="left",
#        position=0.05
#    )
#)