#Compare the behaviour of Decred and Bitcoin
import pandas as pd
import numpy as np
import datetime as date
today = date.datetime.now().strftime('%Y-%m-%d')

from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.io as pio
pio.renderers.default = "browser"

from checkonchain.general.coinmetrics_api import *


DCR_coin = Coinmetrics_api('dcr',"2016-02-08",today,35).add_metrics()
DCR_coin.columns

"""%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
                CREATE PLOT
        SUPPLY CURVES AND STOCK TO FLOW RATIOS
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"""
# BTC Theoretical Supply curve
# DCR Theoretical Supply curve
# DCR Theoretical Supply curve (Offset to BTC 1.68million)
# BTC Theoretical S2F
# DCR Theoretical S2F
# DCR Theoretical S2F (Offset to BTC 1.68million)
# BTC Halvings
x_data = [
    DCR_coin['blk']
]
y_data = [
    DCR_coin['SplyCur']
    ]
name_data = [
    'Decred Coin Supply'
    ]
color_data = [
    'rgb(237, 109, 71)'
    ]
dash_data = [
    'solid'
    ]
width_data = [
    5
    ]
opacity_data = [
    1
]

fig = make_subplots(specs=[[{"secondary_y": False}]])

# Constants
img_width = 1600
img_height = 900
scale_factor = 0.5

fig = go.Figure()
for i in [0]:
    fig.add_trace(go.Scatter(
        x=x_data[i], y=y_data[i],
        name=name_data[i],
        opacity=opacity_data[i],
        line=dict(width=width_data[i],color=color_data[i],dash=dash_data[i])))

"""$$$$$$$$$$$$$$$ FORMATTING $$$$$$$$$$$$$$$$"""
# Add figure title
fig.update_layout(title_text="Bitcoin and Decred Monetary Policy")
fig.update_xaxes(
    title_text="<b>Bitcoin Block Height</b>",
    type='linear',
    range=[0,1200000]
    )
fig.update_yaxes(
    title_text="<b>Coin Supply</b>",
    type="linear",
    range=[0,21000000])
fig.update_layout(
    images=[go.layout.Image(
        x=0,
        sizex=img_width * scale_factor,
        y=img_height * scale_factor,
        sizey=img_height * scale_factor,
        xref="x",
        yref="y",
        opacity=1.0,
        layer="below",
        sizing="stretch",
        source="https://raw.githubusercontent.com/michaelbabyn/plot_data/master/bridge.jpg")]
)
fig.update_layout(template="plotly_white")
#fig.update_layout(template="plotly_dark")
fig.show()





import plotly.graph_objects as go

# Create figure
fig = go.Figure()

# Add trace
fig.add_trace(
    go.Scatter(x=[0, 0.5, 1, 2, 2.2], y=[1.23, 2.5, 0.42, 3, 1])
)

# Add images
fig.update_layout(
    images=[
        go.layout.Image(
            source="https://images.plot.ly/language-icons/api-home/python-logo.png",
            xref="x",
            yref="y",
            x=0,
            y=3,
            sizex=2,
            sizey=2,
            sizing="stretch",
            opacity=0.5,
            layer="below")
    ]
)

# Set templates
fig.update_layout(template="plotly_white")

fig.show()