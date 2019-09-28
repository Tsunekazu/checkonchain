import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.io as pio
pio.renderers.default = "browser"


data = supply_function(blk_max)
columns=['blk','tot','W','S','F','br','inf','S2']
df = pd.DataFrame(data=data,columns=columns)





"""
Sply=df[['tot','W','S','F']]
print(Sply.tail(5))
print(Sply.loc[10000:10010]) #index rows using .loc using only one set of []
print(Sply[['W','S']]) #index columns using using double  set of [[]] and no .loc
print(Sply.loc[10000:10010,['W','S']]) # Index rows AND Columns (note cols in double [])
"""

Sply=df.loc[blk_min:blk_max,['blk','tot','W','S','F']]
Sply['Premne_W'] = initial_S / Sply['W']
Sply['Premne_Tot'] = initial_S / Sply['tot']


tic = pd.read_csv("D:\code_development\checkonchain\checkonchain\scrap\dcr_difficulty.csv")
tic.head(0)
tic.columns=['blk','blk2', 'time', 'circ', 'pool','count', 'pow_hashrate', 'pow_work', 'pow_offset']
tic['pce']=tic['pool']/tic['count']
tic['part_tot']=tic['pool']/21e6
tic['pool'] = tic['pool']/1e8
tic.tail(5)

"""
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
Plot Sply curves
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
"""

#Plot as an express line chart
#fig = px.line(Sply,x='blk',y='W')
#fig.show()

"""traces from Sply"""
fig = make_subplots(specs=[[{"secondary_y": True}]])
fig.add_trace(go.Scattergl(x=Sply['blk'], y=Sply['W'],mode='lines',name='PoW'))
fig.add_trace(go.Scattergl(x=Sply['blk'], y=Sply['S'],mode='lines',name='PoS'))
fig.add_trace(go.Scattergl(x=Sply['blk'], y=Sply['F'],mode='lines',name='Treasury'))
"""traces from tic"""
fig.add_trace(go.Scattergl(x=tic['blk'], y=tic['pool'],mode='lines',name='Ticket Pool'))
fig.update_yaxes(
    title_text="<b>Block Height</b>",type="linear")
fig.update_yaxes(
    title_text="<b>Supply (DCR)</b>",type="linear")
fig.update_layout(template="plotly_white")
fig.show()





'''$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$'''




fig = make_subplots(specs=[[{"secondary_y": True}]])
# Add traces
fig.add_trace(
    go.Scatter(x=Sply['blk'], y=Sply['W'], 
    name="PoW Sply"),
    secondary_y=False,
)
fig.add_trace(
    go.Scatter(x=Sply['blk'], y=Sply['S'], 
    name="PoS Sply"),
    secondary_y=False,
)
fig.add_trace(
    go.Scatter(x=tic['blk'], y=tic['pool'], 
    name="Tic Pool"),
    secondary_y=False,
)
fig.add_trace(
    go.Scatter(x=tic['blk'], y=tic['pow_hashrate'], 
    name="PoW Hashrate"),
    secondary_y=True
)
# Add figure title
fig.update_layout(
    title_text="Supply and Hashrate"
)
# Set x-axis title
fig.update_xaxes(title_text="Block Height")
# Set y-axes titles
fig.update_yaxes(
    title_text="<b>Supply (DCR)</b>",
    type="linear",
    secondary_y=False
)
fig.update_yaxes(
    title_text="<b>PoW Hashrate</b>", 
    type="log", 
    secondary_y=True
)
fig.show()


