# Import Coinmetrics API
import coinmetrics
import pandas as pd
import datetime as dt
from datetime import date
from functools import reduce

#Plotly libraries
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

# Initialize a reference object, in this case `cm` for the Community API
cm = coinmetrics.Community()

# Usage Examples ############################################################


"""
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
Initial API calls
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
"""
today = datetime.datetime.now().strftime('%Y-%m-%d')
# List the assets Coin Metrics has data for.
supported_assets = cm.get_supported_assets()
#print("supported assets:\n", supported_assets)
#available_data_types = cm.get_available_data_types_for_asset('btc')
#print("available data types:\n", available_data_types)

#metric_list = ('"'+','.join(available_data_types)+'"') #setup complete metric list
#print(metric_list)
class Coinmetrics_df:
       
    def __init__(self,asset,begin_timestamp,end_timestamp):
        # List all available metrics for BTC.
        self.asset = asset
        self.begin_timestamp=begin_timestamp
        self.end_timestamp=end_timestamp

    def collect_data(self):
        available_data_types = cm.get_available_data_types_for_asset(self.asset)
        metric_list = str((','.join(available_data_types))) #setup complete metric list
        #print(metric_list)
        asset_data = cm.get_asset_data_for_time_range(self.asset, metric_list, self.begin_timestamp, self.end_timestamp)
        return asset_data
    
    def convert_to_pd(self):
        asset_data = Coinmetrics_df.collect_data(self)
        df = coinmetrics.cm_to_pandas(asset_data)
        #df.index = df.index.map(lambda x: str(x)[:-14])
        #df.index = pd.to_datetime(df.index)
        #df.index = df.index.strftime("%d-%m-%Y")
        df.index.name = 'date'
        df.reset_index(inplace=True)
        df['date'] = pd.to_datetime(df['date'])
        #df['date'] = df['date'].dt.strftime('%d-%m-%Y')
        return df

    def add_metrics(self):
        #Add metrics for block, btc_block, inflation rate, S2F Ratio
        df = Coinmetrics_df.convert_to_pd(self)
        df['blk']=df['BlkCnt'].cumsum()
        df['btc_blk'] = df.loc[0,['date']]# - dt.datetime(2009,1,9)))*(24*6)
        return df


#Pull BTC Data, reduce down to mining related Fees and Income 
#BTC = Coinmetrics_df('btc',"2009-01-03",today).convert_to_pd()
#LTC = Coinmetrics_df('ltc',"2011-10-07",today).convert_to_pd()
#BCH = Coinmetrics_df('bch',"2017-08-01",today).convert_to_pd()
#DASH = Coinmetrics_df('dash',"2014-01-19",today).convert_to_pd()
#DCR = Coinmetrics_df('dcr',"2016-02-08",today).convert_to_pd()
#XMR = Coinmetrics_df('xmr',"2014-04-18",today).convert_to_pd()
#ZEC = Coinmetrics_df('zec',"2016-10-28",today).convert_to_pd()
#ETH = Coinmetrics_df('eth',"2015-07-30",today).convert_to_pd()

DCR = Coinmetrics_df('dcr',"2016-02-08",today).add_metrics()
DCR.dtypes
DCR.tail(5)

DCR['btc_blk']= pd.to_datetime('2009-01-03')
DCR['check'] = DCR['date'] - DCR['btc_blk']



DCR['btc_blk']=DCR['date']-pd.Timestamp('2009-01-09')

DCR['btc_blk'] = DCR.loc[10,['date']]
DCR['btc_blk'] = DCR.loc[0,['date']] - pd.Timestamp('2009-01-09')

DCR.dtypes


DCR['dcr_btc']  = DCR["CapMrktCurUSD"]/ BTC["CapMrktCurUSD"]
DCR['dcr_ltc']  = DCR["CapMrktCurUSD"]/ LTC["CapMrktCurUSD"]
DCR['dcr_bch']  = DCR["CapMrktCurUSD"]/ BCH["CapMrktCurUSD"]
DCR['dcr_dash'] = DCR["CapMrktCurUSD"]/DASH["CapMrktCurUSD"]
DCR['dcr_xmr']  = DCR["CapMrktCurUSD"]/ XMR["CapMrktCurUSD"]
DCR['dcr_zec']  = DCR["CapMrktCurUSD"]/ ZEC["CapMrktCurUSD"]
DCR['dcr_eth']  = DCR["CapMrktCurUSD"]/ ETH["CapMrktCurUSD"]




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