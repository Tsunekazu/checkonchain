#Consolidate Ticket Data

#Data Science
import pandas as pd
import numpy as np
import datetime as date
today = date.datetime.now().strftime('%Y-%m-%d')

#Internal Modules
from checkonchain.general.coinmetrics_api import *
from checkonchain.dcronchain.dcr_dcrdata_api import *
from checkonchain.dcronchain.dcr_schedule import *

#Plotly libraries
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

#number of 'Lifetimes to Print
lifetimes = 1

#Coinmetrics Data
DCR_coin = Coinmetrics_api('dcr',"2016-02-08",today,12).add_metrics()
blk_max = int(DCR_coin['blk'][DCR_coin.index[-1]]*lifetimes)

#Supply Curve Data
DCR_sply = dcr_supply_schedule(blk_max).dcr_supply_function()

#dcrdata.org
DCR_diff = Extract_dcrdata().dcr_difficulty()
DCR_perf = Extract_dcrdata().dcr_performance()


print('Coinmetrics')
print(DCR_coin.columns)
print('Supply Curve')
print(DCR_sply.columns)
print('Difficulty')
print(DCR_diff.columns)
print('Performance')
print(DCR_perf.columns)

DCR_diff.tail(5)
DCR_perf.tail(5)

#DCR_diff is per window = 144 blocks
#DCR_perf is per block = full block height history

#Step 1 - Spread DCR_diff data over DCR_perf --> Window to per block
# Ticket_count is divided over 144 blocks
# Missed divided over 144 blocks
# Remaining metrics are step function
DCR_diff['ticket_count_avg144']=DCR_diff['ticket_count']/144
DCR_diff['missed_avg144']=DCR_diff['missed']/144
DCR_data = pd.concat([
    DCR_perf.set_index('blk',drop=False),
    DCR_diff.set_index('blk',drop=True)],
    axis=1)

del DCR_data.index.name
DCR_data=DCR_data.fillna(method='ffill')
DCR_data=DCR_data.fillna(0)
DCR_data[143990:144010]
DCR_data[1000:1050]


DCR_coin['blk']
DCR_perf.dtypes


fig = make_subplots()
fig.add_trace(go.Scatter(mode='lines',x=DCR_data['blk'], y=DCR_data['pow_hashrate']))
fig.show()