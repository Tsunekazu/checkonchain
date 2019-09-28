#Produce Decred Supply Schedule
"""
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
DECRED SUPPLY FUNCTION
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
"""
#Set constants for DECRED
initial_sply = 1.68e6
initial_W = 0
initial_S = 0.5*initial_sply
initial_F = 0.5*initial_sply
initial_br = 31.19582664
br_W = 0.6
br_S = 0.3
br_F = 0.1
halving = 6144
blk_min = 1
blk_max = 368000
blk_time = 5 #min
atoms = 1e8

def dcr_schedule(blk):
    response = int(math.floor(blk/halving))
    return response

def dcr_blk_rew(blk):
    #for i in range(0,blk): 
    if blk == 0:
        response = initial_sply
    else:
        response = initial_br*(100/101)**dcr_schedule(blk)
    return response

def supply_function(blk):
    response=np.zeros((blk,8))
    response[0,0]=int(0)
    response[0,1]=initial_sply
    response[0,2]=initial_W
    response[0,3]=initial_S
    response[0,4]=initial_F
    response[0,5]=dcr_blk_rew(0)
    response[0,6]=dcr_blk_rew(0)*(365*24*60/blk_time)/initial_sply
    response[0,7]=1/response[0,6]   
    for i in range (1, blk):
        response[i,0] = int(i)
        response[i,1] = response[i-1,1]+dcr_blk_rew(i)
        response[i,2] = response[i-1,2]+dcr_blk_rew(i)*br_W
        response[i,3] = response[i-1,3]+dcr_blk_rew(i)*br_S
        response[i,4] = response[i-1,4]+dcr_blk_rew(i)*br_F
        response[i,5] = dcr_blk_rew(i)
        response[i,6] = dcr_blk_rew(i)*(365*24*60/blk_time)/response[i,1]
        response[i,7] = 1/response[i,6]
    return response

#print(dcr_b_rew(blk_max))
























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
