# Import the Coinmetrics API
import coinmetrics
import pandas as pd
import datetime
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
        df.index = df.index.map(lambda x: str(x)[:-14])
        df.index = pd.to_datetime(df.index)
        df.index = df.index.strftime("%d-%m-%Y %H:%M:%S")
        df.index.name = 'datetime'
        return df

#Pull BTC Data, reduce down to mining related Fees and Income 
BTC_data = Coinmetrics_df('btc',"2009-01-03",today)
BTC=BTC_data.convert_to_pd()
BTC = BTC[
    ['BlkCnt','SplyCur','PriceUSD','CapMrktCurUSD','CapRealUSD',
    'FeeTotNtv','IssContNtv','IssContUSD','IssTotNtv','IssTotUSD']
]
BTC[['blk']] = BTC[['BlkCnt']].cumsum()
BTC['blk_rew_MC'] = BTC['IssTotUSD']/BTC['CapMrktCurUSD']
BTC['blk_rew_RC'] = BTC['IssTotUSD']/BTC['CapRealUSD']


#print(BTC.tail(10))

fig = make_subplots(specs=[[{"secondary_y": True}]])
# Add traces
fig.add_trace(
    go.Scatter(x=BTC['blk'], y=BTC['PriceUSD'], 
    name="Price"),
    secondary_y=False,
)
fig.add_trace(
    go.Scatter(x=BTC['blk'], y=BTC['blk_rew_MC'], 
    name="blk_rew_MC"),
    secondary_y=True,
)
fig.add_trace(
    go.Scatter(x=BTC['blk'], y=BTC['blk_rew_RC'], 
    name="blk_rew_RC"),
    secondary_y=True,
)
# Add figure title
fig.update_layout(
    title_text="Issued Mining Rewards"
)
# Set x-axis title
fig.update_xaxes(title_text="Date",range =[100000,600000])
# Set y-axes titles
fig.update_yaxes(title_text="<b>BTC Price</b>",type="log", secondary_y=False)

fig.update_yaxes(
    title_text="<b>Miner Income (USD)</b>", 
    type="log",
    tickformat = "{:.2%}%",
    secondary_y=True,
    range =[-5,-1.698970004]
)


fig.show()
