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
BTC_data = Coinmetrics_df('btc',"2009-01-03",today).convert_to_pd()
BTC_data.tail(15)
