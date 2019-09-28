# Plot Coin Valuation Models
BTC = Coinmetrics_api('btc',"2009-01-03",today,35).add_metrics()
DCR = Coinmetrics_api('dcr',"2016-02-08",today,12).add_metrics()

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
    go.Scatter(x=asset['date'], y=asset['NVT_28'], 
    name="NVT_28"),
    secondary_y=True
)
fig.add_trace(
    go.Scatter(x=asset['date'], y=asset['NVT_90'], 
    name="NVT_90"),
    secondary_y=True
)
fig.add_trace(
    go.Scatter(x=asset['date'], y=asset['NVTS'], 
    name="NVTS"),
    secondary_y=True
)
fig.add_trace(
    go.Scatter(x=asset['date'], y=asset['RVT_28'], 
    name="RVT_28"),
    secondary_y=True
)
fig.add_trace(
    go.Scatter(x=asset['date'], y=asset['RVT_90'], 
    name="RVT_90"),
    secondary_y=True
)
fig.add_trace(
    go.Scatter(x=asset['date'], y=asset['RVTS'], 
    name="RVTS"),
    secondary_y=True
)

"""$$$$$$$$$$$$$$$ FORMATTING $$$$$$$$$$$$$$$$"""
# Add figure title
fig.update_layout(
    title_text="Network Valuation Models", template="plotly_dark")
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
    type="log",
    #range=[0,50],
    secondary_y=True
)
fig.show()




