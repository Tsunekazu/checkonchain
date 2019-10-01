#Extract Market Cap and Compare Growth of DCR to top coins

BTC = Coinmetrics_api('btc',"2009-01-03",today,35).convert_to_pd()
LTC = Coinmetrics_api('ltc',"2011-10-07",today,35).convert_to_pd()
BCH = Coinmetrics_api('bch',"2017-08-01",today,35).convert_to_pd()
DASH = Coinmetrics_api('dash',"2014-01-19",today,35).convert_to_pd()
DCR = Coinmetrics_api('dcr',"2016-02-08",today,35).convert_to_pd()
XMR = Coinmetrics_api('xmr',"2014-04-18",today,35).convert_to_pd()
ZEC = Coinmetrics_api('zec',"2016-10-28",today,35).convert_to_pd()
ETH = Coinmetrics_api('eth',"2015-07-30",today,35).convert_to_pd()



DCR['dcr_btc']  = DCR["CapMrktCurUSD"]/ BTC["CapMrktCurUSD"]
DCR['dcr_ltc']  = DCR["CapMrktCurUSD"]/ LTC["CapMrktCurUSD"]
DCR['dcr_bch']  = DCR["CapMrktCurUSD"]/ BCH["CapMrktCurUSD"]
DCR['dcr_dash'] = DCR["CapMrktCurUSD"]/DASH["CapMrktCurUSD"]
DCR['dcr_xmr']  = DCR["CapMrktCurUSD"]/ XMR["CapMrktCurUSD"]
DCR['dcr_zec']  = DCR["CapMrktCurUSD"]/ ZEC["CapMrktCurUSD"]
DCR['dcr_eth']  = DCR["CapMrktCurUSD"]/ ETH["CapMrktCurUSD"]
DCR.tail(5)

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
fig.update_layout(template="plotly_dark")
fig.show()