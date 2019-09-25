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
LTC = Coinmetrics_df('ltc',"2011-10-07",today).add_metrics()
BCH = Coinmetrics_df('bch',"2017-08-01",today).add_metrics()
DASH = Coinmetrics_df('dash',"2014-01-19",today).add_metrics()
DCR = Coinmetrics_df('dcr',"2016-02-08",today).add_metrics()
#XMR = Coinmetrics_df('xmr',"2014-04-18",today).add_metrics()
#ZEC = Coinmetrics_df('zec',"2016-10-28",today).add_metrics()
#ETH = Coinmetrics_df('eth',"2015-07-30",today).add_metrics()


DCR['dcr_btc']  = DCR["CapMrktCurUSD"]/ BTC["CapMrktCurUSD"]
DCR['dcr_ltc']  = DCR["CapMrktCurUSD"]/ LTC["CapMrktCurUSD"]
DCR['dcr_bch']  = DCR["CapMrktCurUSD"]/ BCH["CapMrktCurUSD"]
DCR['dcr_dash'] = DCR["CapMrktCurUSD"]/DASH["CapMrktCurUSD"]
#DCR['dcr_xmr']  = DCR["CapMrktCurUSD"]/ XMR["CapMrktCurUSD"]
#DCR['dcr_zec']  = DCR["CapMrktCurUSD"]/ ZEC["CapMrktCurUSD"]
#DCR['dcr_eth']  = DCR["CapMrktCurUSD"]/ ETH["CapMrktCurUSD"]


fig = make_subplots(specs=[[{"secondary_y": True}]])
fig.add_trace(go.Scattergl(x=DCR.index, y=DCR['dcr_btc'],mode='lines',name='BTC'))
fig.add_trace(go.Scattergl(x=DCR.index, y=DCR['dcr_ltc'],mode='lines',name='LTC'))
fig.add_trace(go.Scattergl(x=DCR.index, y=DCR['dcr_bch'],mode='lines',name='BCH'))
fig.add_trace(go.Scattergl(x=DCR.index, y=DCR['dcr_dash'],mode='lines',name='DASH'))
fig.add_trace(go.Scattergl(x=DCR.index, y=DCR['dcr_xmr'],mode='lines',name='XMR'))
fig.add_trace(go.Scattergl(x=DCR.index, y=DCR['dcr_zec'],mode='lines',name='ZEC'))
fig.add_trace(go.Scattergl(x=DCR.index, y=DCR['dcr_eth'],mode='lines',name='ETH'))


fig.update_yaxes(
    title_text="<b>Date</b>",type="linear")
fig.update_yaxes(
    title_text="<b>DCR / Coin Market Cap</b>",type="log")
fig.update_layout(template="plotly_white")
fig.show()