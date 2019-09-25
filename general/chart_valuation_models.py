# Plot Coin Valuation Models
import checkonchain.general.coinmetrics_api
import datetime as date
import plotly.io as pio
pio.renderers.default = "browser"

today = date.datetime.now().strftime('%Y-%m-%d')
#Pull Asset Data
#'asset'
# start timestamp 'yyyy-mm-dd'
# end timestamp 'yyyy-mm-dd'
# top cap constant (Top cap = Average Cap * Const)

BTC = Coinmetrics_df('btc',"2009-01-03",today,35).add_metrics()
LTC = Coinmetrics_df('ltc',"2011-10-07",today,35).add_metrics()
BCH = Coinmetrics_df('bch',"2017-08-01",today,35).add_metrics()
DASH = Coinmetrics_df('dash',"2014-01-19",today,35).add_metrics()
DCR = Coinmetrics_df('dcr',"2016-02-08",today,35).add_metrics()
#XMR = Coinmetrics_df('xmr',"2014-04-18",today,35).add_metrics()
#ZEC = Coinmetrics_df('zec',"2016-10-28",today,35).add_metrics()
#ETH = Coinmetrics_df('eth',"2015-07-30",today,35).add_metrics()


asset = DCR

fig = make_subplots(specs=[[{"secondary_y": True}]])
# Add traces
"""$$$$$$$$$$$$$$$ PRIMARY AXIS $$$$$$$$$$$$$$$$"""
fig.add_trace(
    go.Scatter(x=asset['date'], y=asset['CapMrktCurUSD'], 
    name="Market Cap"),
    secondary_y=False,
)
fig.add_trace(
    go.Scatter(x=asset['date'], y=asset['CapRealUSD'], 
    name="Realised Cap"),
    secondary_y=False,
)
fig.add_trace(
    go.Scatter(x=asset['date'], y=asset['CapAvg'], 
    name="Average Cap"),
    secondary_y=False,
)
fig.add_trace(
    go.Scatter(x=asset['date'], y=asset['CapDelta'], 
    name="Delta Cap"),
    secondary_y=False
)
fig.add_trace(
    go.Scatter(x=asset['date'], y=asset['CapTop'], 
    name="Top Cap"),
    secondary_y=False
)
fig.add_trace(
    go.Scatter(x=asset['date'], y=asset['CapFee'], 
    name="Fee Cap"),
    secondary_y=False
)
fig.add_trace(
    go.Scatter(x=asset['date'], y=asset['CapInflow'], 
    name="Inflow Cap"),
    secondary_y=False
)
fig.add_trace(
    go.Scatter(x=asset['date'], y=asset['CapDiffRegression'], 
    name="Difficulty Regression"),
    secondary_y=False
)
fig.add_trace(
    go.Scatter(x=asset['date'], y=asset['MinerIncome'], 
    name="Cummulative Miner Income"),
    secondary_y=False
)
fig.add_trace(
    go.Scatter(x=asset['date'], y=asset['CapS2Fmodel'], 
    name="Plan B S2F Model (BTC)"),
    secondary_y=False
)



"""$$$$$$$$$$$$$$$ SECONDARY AXIS $$$$$$$$$$$$$$$$"""
fig.add_trace(
    go.Scatter(x=asset['date'], y=asset['NVT_90'], 
    name="NVT_28"),
    secondary_y=True
)
fig.add_trace(
    go.Scatter(x=asset['date'], y=asset['RVT_90'], 
    name="RVT_28"),
    secondary_y=True
)
fig.add_trace(
    go.Scatter(x=asset['date'], y=asset['NVT_90'], 
    name="NVT_90"),
    secondary_y=True
)
fig.add_trace(
    go.Scatter(x=asset['date'], y=asset['RVT_90'], 
    name="RVT_90"),
    secondary_y=True
)
fig.add_trace(
    go.Scatter(x=asset['date'], y=asset['NVT_90'], 
    name="NVTS"),
    secondary_y=True
)
fig.add_trace(
    go.Scatter(x=asset['date'], y=asset['RVT_90'], 
    name="RVTS"),
    secondary_y=True
)

"""$$$$$$$$$$$$$$$ FORMATTING $$$$$$$$$$$$$$$$"""
# Add figure title
fig.update_layout(
    title_text="Network Valuation Models"
)
# Set x-axis title
fig.update_xaxes(title_text="Date")
# Set y-axes titles
fig.update_yaxes(
    title_text="<b>Network Valuation (USD)</b>",
    type="log",
    range=[5,12],
    secondary_y=False
)
fig.update_yaxes(
    title_text="<b>NVT | RVT Ratio</b>", 
    type="linear",
    range=[0,50],
    secondary_y=True
)
fig.show()




