#Calculate the dust limit and estimate future value

# Plotly Libraries (+ force browser charts)
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.io as pio
pio.renderers.default = "browser"

from checkonchain.btconchain.btc_add_metrics import *

#Set Constants
blk_max = 210000*6 #max block height to calculate up to
dustlim = 172 #sats
sats = 1e8 #sats per BTC

#Pull Coinmetrics data
BTC_coin = btc_add_metrics().btc_coin()
BTC_coin = BTC_coin.loc[:,[
    'date','blk',
    'PriceUSD','PriceRealised','SplyCur',
    'BlkCnt','BlkSizeByte','BlkSizeMeanByte	',
    'FeeMeanNtv','FeeMeanUSD',
    'FeeMedNtv','FeeMedUSD',
    'FeeTotNtv','FeeTotUSD',
    'TxCnt','TxTfr'
    ]]


#Calculate Actual Fee performance
BTC_coin['DustPrice']=dustlim/sats * BTC_coin['PriceUSD']
BTC_coin['FeeSatsMean']=BTC_coin['FeeMeanUSD']/BTC_coin['PriceUSD']
BTC_coin['FeeSatsMed']=BTC_coin['FeeMedUSD']/BTC_coin['PriceUSD']
BTC_coin['TxCntSizeByte']=BTC_coin['BlkSizeByte']/BTC_coin['TxCnt']
BTC_coin['TxTfrSizeByte']=BTC_coin['BlkSizeByte']/BTC_coin['TxTfr']
BTC_coin['DustSizeByte']=dustlim
BTC_coin['DustSizeByte']=dustlim
BTC_coin['FeeTxCnt']=BTC_coin['TxCntSizeByte']/sats*BTC_coin['PriceUSD']
BTC_coin['FeeTxTfr']=BTC_coin['TxTfrSizeByte']/sats*BTC_coin['PriceUSD']

BTC_coin['FeeSatsMean']
BTC_coin['FeeMeanNtv']

#Calculate supply function
BTC_sply = btc_add_metrics().btc_sply(blk_max)
BTC_sply['S2F_1sats_byte'] = BTC_sply['PricePlanBmodel'] * dustlim/sats
BTC_sply['S2F_2sats_byte'] = BTC_sply['S2F_1sats_byte'] * 2
BTC_sply['S2F_10sats_byte'] = BTC_sply['S2F_1sats_byte'] * 10
BTC_sply['S2F_30sats_byte'] = BTC_sply['S2F_1sats_byte'] * 30
BTC_sply['S2F_100sats_byte'] = BTC_sply['S2F_1sats_byte'] * 100
BTC_sply['S2F_200sats_byte'] = BTC_sply['S2F_1sats_byte'] * 200



"""%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
CREATE PLOT 01
DUST COMPARED TO FEE LIMITS
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"""

#Create Plot against block height
# Y-axis 1 = Fee (USD)
# Y-axs 2 = BTCUSD Price

# Create Input Dataset
x_data = [
    BTC_sply['blk'],BTC_sply['blk'],BTC_sply['blk'],
    BTC_sply['blk'],BTC_sply['blk'],BTC_sply['blk'],
    BTC_coin['blk'],BTC_coin['blk'],BTC_coin['blk']
    ]

y_data = [
    BTC_sply['S2F_1sats_byte'],BTC_sply['S2F_2sats_byte'],BTC_sply['S2F_10sats_byte'],
    BTC_sply['S2F_30sats_byte'],BTC_sply['S2F_100sats_byte'],BTC_sply['S2F_200sats_byte'],
    BTC_coin['DustPrice'],BTC_coin['FeeMeanUSD'],BTC_coin['FeeMedUSD']
]

names = [
    'S2F 1sats/byte','S2F 2sats/byte','S2F 10sats/byte',
    'S2F 30sats/byte','S2F 100sats/byte','S2F 200sats/byte',
    'Actual Dust Value','Actual Mean Fee','Actual Median Fee'
]

line_size = [
    2,1,1,
    1,1,1,
    2,2,2
]
dash_type = [
    'dash','dash','dash',
    'dash','dash','dash'
]
color_data = [
    'rgb(153, 255, 102)', 'rgb(255, 255, 102)', 'rgb(255, 204, 102)',
    'rgb(255, 153, 102)', 'rgb(255, 102, 102)', 'rgb(255, 80, 80)',
    'rgb(255, 255, 255)', 'rgb(102, 255, 153)', 'rgb(102, 204, 255)'
]

fig_01 = make_subplots(specs=[[{"secondary_y": True}]])
fig_01.update_layout(template="plotly_dark",title="Dust Limits Assuming 172 byte Size")
#Create plots for Fee bands and Actual Performance
for i in range(0,6):
    fig_01.add_trace(go.Scatter(x=x_data[i], y=y_data[i],mode='lines',  name=names[i],line=dict(color=color_data[i], width=line_size[i],dash=dash_type[i])))
for i in range(6,9):
    fig_01.add_trace(go.Scatter(x=x_data[i], y=y_data[i],mode='lines',  name=names[i],line=dict(color=color_data[i], width=line_size[i])))

fig_01.add_trace(go.Scatter(
    x=BTC_coin['blk'], y=BTC_coin['PriceUSD'],
    name="BTCUSD Price",line=dict(width=2,color='rgb(102, 102, 153)')),
    secondary_y=True)
fig_01.add_trace(go.Scatter(
    x=BTC_sply['blk'], y=BTC_sply['PricePlanBmodel'],
    name="S2F Model Price",line=dict(width=1,color='rgb(102, 153, 255)')),
    secondary_y=True)

fig_01.update_xaxes(
    title_text="<b>Block Height</b>",
    type="linear",
    range=[70000,blk_max]
    )
fig_01.update_yaxes(
    title_text="<b>Fee Value (USD)</b>",
    tickformat = '$0:.2f',
    type="log",
    secondary_y=False,
    range=[-6,4]
    )
fig_01.update_yaxes(
    title_text="<b>BTCUSD Price</b>",
    tickformat = '$0:.2f',
    type="log",
    secondary_y=True,
    range=[-2,8],
    color='rgb(102, 102, 153)'
    )
fig_01.show()


"""%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
CREATE PLOT 02 
FEE RATE OVER TIME IN SATS
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"""

fig_02 = make_subplots(specs=[[{"secondary_y": True}]])
fig_02.update_layout(template="plotly_dark",title="Fee Rates")
fig_02.add_trace(go.Scatter(
    x=BTC_coin['blk'], y=BTC_coin['FeeMeanNtv'].rolling(14).mean()*sats/dustlim,
    name="Mean Fee Rate",line=dict(width=2,color='rgb(102, 255, 153)')),
    secondary_y=False)
fig_02.add_trace(go.Scatter(
    x=BTC_coin['blk'], y=BTC_coin['FeeMedNtv'].rolling(14).mean()*sats/dustlim,
    name="Median Fee Rate",line=dict(width=2,color='rgb(255, 204, 102)')),
    secondary_y=False)

fig_02.add_trace(go.Scatter(
    x=BTC_coin['blk'], y=BTC_coin['PriceUSD'],
    name="BTCUSD Price",line=dict(width=2,color='rgb(255, 255, 255)')),
    secondary_y=True)
fig_02.add_trace(go.Scatter(
    x=BTC_sply['blk'], y=BTC_sply['PricePlanBmodel'],
    name="S2F Model Price",line=dict(width=2,dash='dash',color='rgb(102, 153, 255)')),
    secondary_y=True)

fig_02.update_xaxes(
    title_text="<b>Block Height</b>",
    type="linear",
    range=[70000,blk_max]
    )
fig_02.update_yaxes(
    title_text="<b>Fee Value (sats)</b>",
    type="log",
    secondary_y=False,
    range=[0,4]
    )
fig_02.update_yaxes(
    title_text="<b>BTCUSD Price</b>",
    tickformat = '$0:.2f',
    type="log",
    secondary_y=True,
    range=[-2,8],
    color='rgb(102, 102, 153)'
    )
fig_02.show()



"""%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
CREATE PLOT 03
AVERAGE TRANSACTION SIZE
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"""
fig_03 = make_subplots(specs=[[{"secondary_y": False}]])
fig_03.update_layout(template="plotly_dark",title="Average Transaction Size (bytes)")
#Create plot for average and median transaction size in bytes
fig_03.add_trace(go.Scatter(
    x=BTC_coin['blk'], y=BTC_coin['TxCntSizeByte'].rolling(14).mean(),
    name="Average Transaction Size",line=dict(width=1,color='rgb(255, 204, 102)')),
    secondary_y=False)
fig_03.update_xaxes(
    title_text="<b>Block Height</b>",
    type="linear",
    range=[0,blk_max]
    )
fig_03.update_yaxes(
    title_text="<b>Average Transaction Size (byte)</b>",
    type="linear",
    color='rgb(255, 204, 102)',
    secondary_y=False,
    range=[100,2000]
    )
fig_03.show()
    


"""%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
CREATE PLOT 04
BLOCKCHAIN SIZE
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"""
fig_04 = make_subplots(specs=[[{"secondary_y": False}]])
fig_04.update_layout(template="plotly_dark")
#Create plot for average and median transaction size in bytes
fig_04.add_trace(go.Scatter(
    x=BTC_coin['blk'], y=BTC_coin['BlkSizeByte'].cumsum()/1048576,
    name="Blockchain Size (MB)",
    line=dict(color='rgb(255, 204, 102)',width=3)),
    secondary_y=False)
fig_04.update_xaxes(
    title_text="<b>Block Height</b>",
    type="linear",
    range=[0,600000]
    )
fig_04.update_yaxes(
    title_text="<b>Blockchain Size (MB)</b>",
    type="log",
    secondary_y=False
    )
fig_04.show()