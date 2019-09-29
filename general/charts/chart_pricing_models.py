# Plot Coin Pricing Models

BTC = Coinmetrics_api('btc',"2009-01-03",today,35).add_metrics()
DCR = Coinmetrics_api('dcr',"2016-02-08",today,12).add_metrics()

asset = BTC

fig = make_subplots(specs=[[{"secondary_y": True}]])
# Add traces
"""$$$$$$$$$$$$$$$ PRIMARY AXIS $$$$$$$$$$$$$$$$"""
fig.add_trace(
    go.Scatter(x=asset['date'], y=asset['PriceUSD'], 
    name="Price USD"),
    secondary_y=False
)
fig.add_trace(
    go.Scatter(x=asset['date'], y=asset['PriceRealised'], 
    name="Realised Price"),
    secondary_y=False
)
fig.add_trace(
    go.Scatter(x=asset['date'], y=asset['PriceAvg'], 
    name="Average Price"),
    secondary_y=False
)
fig.add_trace(
    go.Scatter(x=asset['date'], y=asset['PriceDelta'], 
    name="Delta Price"),
    secondary_y=False
)
fig.add_trace(
    go.Scatter(x=asset['date'], y=asset['PriceTop'], 
    name="Top Price"),
    secondary_y=False
)
fig.add_trace(
    go.Scatter(x=asset['date'], y=asset['PriceUSD'].rolling(200).mean(), 
    name="200DMA"),
    secondary_y=False
)
fig.add_trace(
    go.Scatter(x=asset['date'], y=asset['PriceS2Fmodel'].rolling(90).mean(), 
    name="Plan B S2F Price (BTC)"),
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
    title_text="Network Valuation Models"
)
# Set x-axis title
fig.update_xaxes(title_text="Date")
# Set y-axes titles
fig.update_yaxes(
    title_text="<b>Network Pricing Models (USD)</b>",
    type="log",
    range=[-1,6],
    secondary_y=False
)
fig.update_yaxes(
    title_text="<b>NVT | RVT Ratio</b>", 
    type="log",
    #range=[0,50],
    secondary_y=True
)
fig.update_layout(template="plotly_dark")
fig.show()



