#Consolidate Coinmetrics with Supply Curve and Ticket Data
from checkonchain.dcronchain.__init__ import *
from checkonchain.dcronchain.dcr_add_metrics import *

#Plotly libraries
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

#number of 'Lifetimes to Print
lifetimes = 1

#Coinmetrics Data
DCR_real = dcr_add_metrics().dcr_pricing_models()
DCR_coin = Coinmetrics_api('dcr',"2016-02-08",today,12).add_metrics()
blk_max = int(DCR_coin['blk'][DCR_coin.index[-1]]*lifetimes)

#Supply Curve Data
DCR_sply = dcr_supply_schedule(blk_max).dcr_supply_function()

#dcrdata.org
DCR_diff = Extract_dcrdata().dcr_difficulty()
DCR_perf = Extract_dcrdata().dcr_performance()


print('Coinmetrics')
print(DCR_coin.columns)
print('Supply Curve')
print(DCR_sply.columns)
print('Difficulty')
print(DCR_diff.columns)
print('Performance')
print(DCR_perf.columns)


DCR_sply['PriceS2Fmodel'] = np.exp(3.31954*np.log(DCR_sply['S2F_ideal'])+14.6227)/DCR_sply['Sply_ideal']

DCR_coin['PriceS2Fmodel'].tail(5)

"""%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
CREATE PLOT 01 (TOP)
DECRED PRICING MODELS
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"""
#Create Plot against block height
# Y-axis 1 = USD Price
# Y-axs 2 = Supply Curves

# Create Input Dataset for TOP PLOT
x_data_1 = [
    DCR_coin['blk'],DCR_coin['blk'],DCR_coin['blk'],
    DCR_coin['blk'],DCR_coin['blk'],DCR_coin['blk'],
    DCR_coin['blk'],DCR_sply['blk'],DCR_diff['blk']
    ]

y_data_1 = [
    DCR_coin['PriceUSD'],DCR_coin['PriceRealised'],DCR_coin['PriceAvg'],
    DCR_coin['PriceDelta'],DCR_coin['PriceTop'],DCR_coin['PriceInflow'],
    DCR_coin['PriceS2Fmodel'],DCR_sply['PriceS2Fmodel'],DCR_diff['ticket_price']
]
#STAKER INFLOW!!!!!
names_1 = [
    'Price USD','Realised Price','Average Price',
    'Delta Price','Top Price','Price Miner Inflow',
    'Actual S2F Model','Theoretical S2F Model','Ticket Price (DCR)'
]
line_size_1 = [
    2,2,1,
    1,1,1,
    1,1,1
]
dash_type_1 = [
    'solid','solid','dash',
    'dash','dash','dash',
    'dot','dash','dash'
]
opacity_1 = [
    1,1,0.75,
    0.75,0.75,0.75,
    0.75,0.75,1
]
color_data_1 = [
    'rgb(255, 255, 255)', 'rgb(102, 255, 153)', 'rgb(102, 204, 255)',
    'rgb(153, 255, 102)', 'rgb(255, 255, 102)', 'rgb(255, 204, 102)',
    'rgb(255, 153, 102)', 'rgb(255, 102, 102)', 'rgb(255, 80, 80)'
]


"""%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
CREATE PLOT 01 (Bottom)
DECRED OSCILLATORS
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"""
#Create Plot against block height
# Y-axis 1 = NVT | RVT RATIO

# Create Input Dataset for TOP PLOT
x_data_2 = [
    DCR_coin['blk'],DCR_coin['blk'],DCR_coin['blk'],
    DCR_coin['blk'],DCR_coin['blk'],DCR_coin['blk']
    ]

y_data_2 = [
    DCR_coin['NVT_28'],DCR_coin['NVT_90'],DCR_coin['NVTS'],
    DCR_coin['RVT_28'],DCR_coin['RVT_90'],DCR_coin['RVTS']
]
#STAKER INFLOW!!!!!
names_2 = [
    'NVT 28D','NVT 90D','NVTS',
    'RVT 29D','RVT 90D','RVTS'
]
line_size_2 = [
    1,1,1,
    1,1,1
]
dash_type_2 = [
    'dot','dash','solid',
    'dot','dash','solid'
]
opacity_2 = [
    1,1,1,
    1,1,1
]
color_data_2 = [
    'rgb(153, 255, 102)', 'rgb(255, 255, 102)', 'rgb(255, 204, 102)',
    'rgb(255, 153, 102)', 'rgb(255, 102, 102)', 'rgb(255, 80, 80)'
]


fig = make_subplots(
    rows=2,cols=1,
    shared_xaxes=True, 
    vertical_spacing=0.05,
    row_heights=[0.7,0.3],
    specs=[[{"secondary_y": True}],[{}]]
    )

"""Create Pricing Model Plots"""
for i in range(0,9):
    fig.add_trace(go.Scatter(
        mode='lines',
        x=x_data_1[i], 
        y=y_data_1[i],
        name=names_1[i],
        opacity=opacity_1[i],
        line=dict(
            width=line_size_1[i],
            color=color_data_1[i],
            dash=dash_type_1[i]
            )),
        secondary_y=False,
        row=1,col=1)


"""Create NVT Plots"""
for i in range(0,6):
    fig.add_trace(go.Scatter(
        mode='lines',
        x=x_data_2[i], 
        y=y_data_2[i],
        name=names_2[i],
        opacity=opacity_2[i],
        line=dict(
            width=line_size_2[i],
            color=color_data_2[i],
            dash=dash_type_2[i]
            )),
        secondary_y=False,
        row=2,col=1)

fig.update_layout(template="plotly_dark",title="Decred Pricing Models")
fig.update_xaxes(row=2,col=1)
fig.update_xaxes(
    row=2,col=1,
    title_text="<b>Block Height</b>",
    type="linear",
    range=[0,blk_max],
    rangeslider=dict(visible=True),
    rangeselector=dict(
        buttons=list([
            dict(count=1,
                    label="1m",
                    step="month",
                    stepmode="backward"),
            dict(count=6,
                    label="6m",
                    step="month",
                    stepmode="backward"),
            dict(count=1,
                    label="YTD",
                    step="year",
                    stepmode="todate"),
            dict(count=1,
                    label="1y",
                    step="year",
                    stepmode="backward"),
            dict(step="all")
        ])
    )
    )
fig.update_yaxes(
    row=1,col=1,
    title_text="<b>DCR Price (USD)</b>",
    type="log",
    secondary_y=False,
    range=[-1,4]
    )
fig.update_yaxes(
    row=2,col=1,
    title_text="<b>NVT | RVT Ratio</b>",
    type="linear",
    secondary_y=False,
    range=[0,80],
    dtick=10
    )

fig.show()




