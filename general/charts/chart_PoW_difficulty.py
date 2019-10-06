# Plot Normalised Difficulty Adjustments

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

BTC.columns
start_date = '01-01-2018'
end_date = today
metric = 'DiffMean'

response = pd.concat([
    BTC[metric], 
    LTC[metric],
    BCH[metric],
    DASH[metric],
    DCR[metric],
    XMR[metric],
    ZEC[metric],
    ETH[metric]
    ], axis=1)

assets = ['BTC','LTC','BCH','DASH','DCR','XMR','ZEC','ETH']
#assets = ['BTC','LTC','BCH','DASH','DCR','ETH']
response.columns=assets

# Isolate data from a specific date
response = response.loc[start_date:end_date]

for i in assets:
    idx = response[i].first_valid_index()
    response[i+'_mod'] = response[[i]]/response.loc[idx,[i]]
    response[i+'_mod'] = response[i+'_mod'].rolling(14).mean()


x_data = [
    response.index,response.index,
    response.index,response.index,
    response.index,response.index,
    response.index,response.index
]

y_data = [
    response['BTC_mod'],response['LTC_mod'],
    response['BCH_mod'],response['DASH_mod'],
    response['DCR_mod'],response['XMR_mod'],
    response['ZEC_mod'],response['ETH_mod']
]

color_data = [
    'rgb(255, 102, 0)',  
    'rgb(214, 214, 194)',
    'rgb(0, 153, 51)',   
    'rgb(51, 204, 255)',
    'rgb(46, 214, 161)', 
    'rgb(255, 153, 0)',  
    'rgb(255, 255, 0)', 
    'rgb(153, 51, 255)' 
]


fig = make_subplots(specs=[[{"secondary_y": False}]])
for i in range(0,8):
    fig.add_trace(go.Scatter(
        x=x_data[i], 
        y=y_data[i],
        mode='lines',
        name=assets[i]#,
        #line=dict(color=color_data[i])
        ))


fig.update_yaxes(
    title_text="<b>Date</b>",type="linear")
fig.update_yaxes(
    title_text="<b>Difficulty Adjustment Growth</b>",type="log",tickformat= ',.0%')
fig.update_layout(template="plotly_dark")
fig.show()