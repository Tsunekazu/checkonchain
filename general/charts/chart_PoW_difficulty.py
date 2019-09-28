# Plot Normalised Difficulty Adjustments
start_date = '01-01-2019'
end_date = today

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

Difficulty = pd.concat([
    BTC['DiffMean'], 
    LTC['DiffMean'],
    BCH['DiffMean'],
    DASH['DiffMean'],
    DCR['DiffMean'],
    XMR['DiffMean'],
    ZEC['DiffMean'],
    ETH['DiffMean']
    ], axis=1)

assets = ['BTC','LTC','BCH','DASH','DCR','XMR','ZEC','ETH']
Difficulty.columns=assets

# Isolate data from a specific date
Difficulty = Difficulty.loc[start_date:end_date]
Difficulty = Difficulty/Difficulty.iloc[0]
Difficulty = Difficulty.rolling(14).mean()
Difficulty.tail(20)

fig = make_subplots(specs=[[{"secondary_y": False}]])
fig.add_trace(go.Scatter(x=Difficulty.index, y=Difficulty['BTC'],mode='lines',name='BTC'))
fig.add_trace(go.Scatter(x=Difficulty.index, y=Difficulty['LTC'],mode='lines',name='LTC'))
fig.add_trace(go.Scatter(x=Difficulty.index, y=Difficulty['BCH'],mode='lines',name='BCH'))
fig.add_trace(go.Scatter(x=Difficulty.index, y=Difficulty['DASH'],mode='lines',name='DASH'))
fig.add_trace(go.Scatter(x=Difficulty.index, y=Difficulty['DCR'],mode='lines',name='DCR'))
fig.add_trace(go.Scatter(x=Difficulty.index, y=Difficulty['XMR'],mode='lines',name='XMR'))
fig.add_trace(go.Scatter(x=Difficulty.index, y=Difficulty['ZEC'],mode='lines',name='ZEC'))
fig.add_trace(go.Scatter(x=Difficulty.index, y=Difficulty['ETH'],mode='lines',name='ETH'))


fig.update_yaxes(
    title_text="<b>Date</b>",type="linear")
fig.update_yaxes(
    title_text="<b>Difficulty Adjustment Growth</b>",type="log",tickformat= ',.0%')
fig.update_layout(template="plotly_dark")
fig.show()