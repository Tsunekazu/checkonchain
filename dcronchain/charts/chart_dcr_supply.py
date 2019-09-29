#Plot Decred Supply Curves

data = dcr_supply_function(blk_max)
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



"""
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
Plot % Premne
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
"""
fig=go.Figure()
fig.add_trace(go.Scattergl(x=Sply['blk'], y=Sply['Premne_W'],
    mode='lines',
    name='Premne_W'))
fig.add_trace(go.Scattergl(x=Sply['blk'], y=Sply['Premne_Tot'],
    mode='lines',
    name='Premne_Tot'))

fig.update_layout(
    images=[
        go.layout.Image(
            source="Capture.JPG",
            xref="paper",
            yref="paper",
            sizing="stretch",
            opacity=0.5,
            layer="above"
        )
    ]
)
fig.update_yaxes(
    type="linear",
    range = [0,1]
)
fig.update_layout(template="plotly_white")
fig.show()

"""
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
Plot % particip
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
"""
fig=go.Figure()
fig.add_trace(go.Scattergl(x=tic['blk'], y=tic['part'],
    mode='lines',
    name='part'))
fig.add_trace(go.Scattergl(x=tic['blk'], y=tic['part_tot'],
    mode='lines',
    name='part_tot'))

fig.update_layout(
    images=[
        go.layout.Image(
            source="Capture.JPG",
            xref="paper",
            yref="paper",
            sizing="stretch",
            opacity=0.5,
            layer="above"
        )
    ]
)
fig.update_layout(template="plotly_white")
fig.show()


"""
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
Plot TicPce vs Diff with secondary y-axis
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
"""
fig = make_subplots(specs=[[{"secondary_y": True}]])
# Add traces
""" tic pce """
fig.add_trace(
    go.Scatter(x=tic['blk'], y=tic['pce'], 
    name="tic_pce"),
    secondary_y=False,
)
""" Mean Ntv Tx """
fig.add_trace(
    go.Scatter(x=crd['blk'], y=crd['MeanNtv_28'], 
    name="MeanNtv_28"),
    secondary_y=False,
)
""" Med Ntv Tx """
fig.add_trace(
    go.Scatter(x=crd['blk'], y=crd['MedNtv_28'], 
    name="MedNtv_28"),
    secondary_y=False,
)
#""" Pce """
#fig.add_trace(
#    go.Scatter(x=crd['blk'], y=crd['PriceUSD'], 
#    name="Pce"),
#    secondary_y=False,
#)
""" W Diff """
fig.add_trace(
    go.Scatter(x=crd['blk'], y=crd['DiffMean'], 
    name="DifMean"),
    secondary_y=True,
)
fig.update_layout(
    images=[
        go.layout.Image(
            source="Capture.JPG",
            xref="paper",
            yref="paper",
            sizing="stretch",
            opacity=0.5,
            layer="above"
        )
    ]
)
fig.update_yaxes(
    title_text="<b>pool</b>", 
    type="linear",
    range = [0,150],
    secondary_y=False
)
fig.update_yaxes(
    title_text="<b>Diff</b>", 
    type="log", 
    secondary_y=True
)
fig.update_layout(template="plotly_white")
fig.show()










"""
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
Plot Infl and S2 with secondary y-axis
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
"""

Inf=df.loc[blk_min:blk_max,['blk','inf','S2']]


fig = make_subplots(specs=[[{"secondary_y": True}]])
# Add traces
fig.add_trace(
    go.Scatter(x=Inf['blk'], y=Inf['inf'], 
    name="Inf"),
    secondary_y=False,
)
fig.add_trace(
    go.Scatter(x=Inf['blk'], y=Inf['S2'], 
    name="S2"),
    secondary_y=True,
)
# Add figure title
fig.update_layout(
    title_text="Double Y Axis Example",
    paper_bgcolor='rgba(39,40,34,0)',
    plot_bgcolor='rgba(39,40,34,0)'
)
# Set x-axis title
fig.update_xaxes(title_text="xaxis title")
# Set y-axes titles
fig.update_yaxes(
    title_text="<b>primary Inf</b>",
    type="log",
    #range = [0,2.5],
    secondary_y=False, 
    tickformat = '%',
    tickfont=dict(size=18, family='Courier', color='white'),
    gridcolor='grey',
    gridwidth = 0.5,
    title_font=dict(size=18, family='Courier', color='white')
)
fig.update_yaxes(
    title_text="<b>secondary</b> S2", 
    type="log", 
    secondary_y=True
)
fig.show()
