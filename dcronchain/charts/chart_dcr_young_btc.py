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
from checkonchain.btconchain.btc_schedule import *
from checkonchain.dcronchain.dcr_schedule import *
from checkonchain.btconchain.ltc_schedule import *
from checkonchain.dcronchain.dcr_dcrdata_api import *
"""**************************************************************************
                            Part 0 - Code Setup
***************************************************************************"""

"""##### PULL INITIAL DATSETS #####"""
#Pull BTC and DCR data from Coinmetrics
BTC_coin = Coinmetrics_api('btc',"2009-01-03",today,35).add_metrics()
DCR_coin = Coinmetrics_api('dcr',"2016-02-08",today,35).add_metrics()
LTC_coin = Coinmetrics_api('ltc',"2011-10-07",today,35).add_metrics()
print('Coinmetrics')
print(BTC_coin.columns)

#Pull BTC and DCR data from Theoretical SUpply Curves
BTC_sply = btc_supply_schedule(1200000).btc_supply_function()
DCR_sply = dcr_supply_schedule(1200000*2-33600*2).dcr_supply_function()
LTC_sply = ltc_supply_schedule(1200000*4).ltc_supply_function()
print('Supply')
print(BTC_sply.columns)

"""##### CALCULATE DCR EQUIVALENT BTC BLOCK HEIGHT @ 1.68M BTC #####"""
#Calculate the btc_block where supply = 1.68million BTC
dcr_btc_blk_start = int(BTC_sply[BTC_sply['Sply_ideal']==1680000]['blk'])
#Create DCR_Sply column of equivalent btc_blk
#ASSUMES 1BTC block == 2 DCR blocks
DCR_sply['btc_blk'] = dcr_btc_blk_start + 0.5*DCR_sply['blk']
LTC_sply['btc_blk'] = 0.25*LTC_sply['blk']
#Create XXX_data column absorbing XXX_Sply columns
"""##### COMPILE INTO FINAL DATASETS #####"""
#XXX_real --> COINMETRICS = PARENT
BTC_real = pd.concat([BTC_coin.set_index('blk',drop=False),BTC_sply.set_index('blk')],axis=1,join='inner')
BTC_real = BTC_real.reset_index(drop=True)
DCR_real = pd.concat([DCR_coin.set_index('blk',drop=False),DCR_sply.set_index('blk')],axis=1,join='inner')
DCR_real = DCR_real.reset_index(drop=True)
LTC_real = pd.concat([LTC_coin.set_index('blk',drop=False),LTC_sply.set_index('blk')],axis=1,join='inner')
LTC_real = LTC_real.reset_index(drop=True)
# Calculate Max-Min step to plot up Bitcoin halvings
BTC_half = btc_supply_schedule(0).btc_halvings_stepped()

"""##### DECRED SPECIFIC MODULES #####"""
DCR_perf = Extract_dcrdata().dcr_performance()
DCR_diff = Extract_dcrdata().dcr_difficulty()
#Update DCR_performance with date and btc_blk
DCR_perf = pd.concat([DCR_perf.set_index('blk',drop=False),DCR_real[['blk','date','btc_blk']].set_index('blk',drop=True)],axis=1,join='inner')
# Clean DCR hashrate data
DCR_perf = DCR_perf[DCR_perf['pow_hashrate_THs']>1]

"""##### BITCOIN HASHRATE CSV FROM BLOCKCHAIN.COM #####"""
# Blockchain.com hashrate w/ coinmetrics block (UPDATE 5 Oct 2019)
#Note need to add coinmetrics block manually
BTC_hash = pd.read_csv(r"D:\code_development\checkonchain\checkonchain\btconchain\data\btc_blockchaincom_hashrate.csv")
#Drop date and apply
BTC_hash = BTC_hash.drop(BTC_hash.index[1])
BTC_hash = BTC_hash.drop(['date'],axis=1)
BTC_hash = pd.concat([BTC_hash.set_index('blk',drop=False),BTC_real[['blk','date']].set_index('blk',drop=True)],axis=1,join='inner')
BTC_hash = BTC_hash.drop(BTC_hash.index[0])
BTC_hash.reset_index(drop=True)

"""**************************************************************************
                            Part 1 - Monetary Policy
***************************************************************************"""
class dcrbtc_monetary_policy():
    
    def __init__(self):
        pass

    def chart_dcrbtc_sply_area(self):
        """%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
                        CREATE PLOT 01
                SUPPLY CURVES - STACKED AREA CHARTS
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"""
        x_data = [
            BTC_sply['blk'],
            DCR_sply['btc_blk'],
            DCR_sply['btc_blk'],
            DCR_sply['btc_blk'],
            DCR_sply['btc_blk'],

        ]
        y_data = [
            BTC_sply['Sply_ideal'],
            DCR_sply['Sply_ideal'],
            DCR_sply['PoWSply_ideal'],
            DCR_sply['PoSSply_ideal'],
            DCR_sply['FundSply_ideal']
        ]
        name_data = [
            'BTC Supply',
            'DCR Total Supply',
            'DCR PoW Supply',
            'DCR PoS Supply',
            'DCR Treasury Supply',
        ]
        color_data = [
            'rgb(255, 153, 0)',
            'rgb(46, 214, 161)',
            'rgb(41, 112, 255)',
            'rgb(46, 214, 161)',
            'rgb(237, 109, 71)'
        ]
        fill_data = [
            'tozeroy',
            'tonexty',
            'tonexty',
            'tonexty',
            'tozeroy'
        ]
        opacity_data = [
            0.5,1,0.5,0.5,0.5
        ]
        fig = go.Figure()
        for i in range(0,5):
            fig.add_trace(go.Scatter(
                x=x_data[i], 
                y=y_data[i],
                name=name_data[i], 
                fill=fill_data[i],
                #fillcolor=color_data[i],
                #line_color= color_data[i],
                line=dict(
                    color=color_data[i],
                    width=2
                    #opacity=opacity_data[i]
                )))
        fig.update_layout(template="plotly_dark",title="Bitcoin and Decred Theoretical Supply Curves")
        
        return fig


    def chart_dcrbtc_sply_s2f(self):
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
            BTC_sply['blk'],
            BTC_sply['blk'],
            BTC_real['blk'],
            DCR_sply['btc_blk']+372384,
            DCR_sply['btc_blk']+372384,
            DCR_real['btc_blk']+372384,
            DCR_sply['btc_blk'],
            DCR_sply['btc_blk'],
            DCR_real['btc_blk'],
            BTC_half['blk']
        ]
        y_data = [
            BTC_sply['Sply_ideal'],
            BTC_sply['S2F_ideal'],
            BTC_real['S2F'],
            DCR_sply['Sply_ideal'],
            DCR_sply['S2F_ideal'],
            DCR_real['S2F'],
            DCR_sply['Sply_ideal'],
            DCR_sply['S2F_ideal'],
            DCR_real['S2F'],
            BTC_half['y_arb']
            ]
        name_data = [
            'Bitcoin Coin Supply',
            'Bitcoin S2F Ratio',
            'Bitcoin S2F Ratio (Actual)',
            'Decred Coin Supply',
            'Decred S2F Ratio',
            'Decred S2F Ratio (Actual)',
            'Decred Coin Supply (Offset)',
            'Decred S2F Ratio (Offset)',
            'Decred S2F Ratio (Offset, Actual)',
            'BTC Halvings'
            ]
        color_data = [
            'rgb(237, 109, 71)','rgb(237, 109, 71)','rgb(237, 109, 71)',
            'rgb(112, 203, 255)','rgb(112, 203, 255)','rgb(112, 203, 255)',
            'rgb(46, 214, 161)','rgb(46, 214, 161)','rgb(46, 214, 161)',
            'rgb(255, 255, 255)' 
            ]
        dash_data = [
            'solid','dot','solid',
            'solid','dot','solid',
            'solid','dot','solid',
            'solid'
            ]
        width_data = [
            5,5,1,4,4,1,4,4,1,0.5
            ]
        opacity_data = [
            1,1,0.75,
            1,1,0.75,
            1,1,0.75,
            0.5
        ]
        name_data[6]

        fig = make_subplots(specs=[[{"secondary_y": True}]])
        for i in [0,3,6]:
            fig.add_trace(go.Scatter(
                x=x_data[i], y=y_data[i],
                name=name_data[i],
                opacity=opacity_data[i],
                line=dict(width=width_data[i],color=color_data[i],dash=dash_data[i])),
                secondary_y=False)
        for i in [1,2,4,5,7,8,9]:
            fig.add_trace(go.Scatter(
                x=x_data[i], y=y_data[i],
                name=name_data[i],
                opacity=opacity_data[i],
                line=dict(width=width_data[i],color=color_data[i],dash=dash_data[i])),
                secondary_y=True)
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
            range=[0,21000000],
            secondary_y=False)
        fig.update_yaxes(
            title_text="<b>Stock-to-Flow Ratio</b>",
            type="log",
            range=[-1,5],
            secondary_y=True)
        fig.update_layout(template="plotly_dark")
        return fig


    def chart_dcrbtc_sply_marketcap(self):
        """%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
                        CREATE PLOT 03
            SUPPLY AND DEMAND - % of Supply Mined VS Market Cap
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"""

        BTC_sply['CapS2Fmodel_ideal'] = np.exp(3.31954*np.log(BTC_sply['S2F_ideal'])+14.6227)
        DCR_sply['CapS2Fmodel_ideal'] = np.exp(3.31954*np.log(DCR_sply['S2F_ideal'])+14.6227)
        LTC_sply['CapS2Fmodel_ideal'] = np.exp(3.31954*np.log(LTC_sply['S2F_ideal'])+14.6227)
        x_data = [
            BTC_real['SplyCur']/21e6,BTC_real['SplyCur']/21e6,BTC_sply['Sply_ideal']/21e6,
            DCR_real['SplyCur']/21e6,DCR_real['SplyCur']/21e6,DCR_sply['Sply_ideal']/21e6,
            LTC_real['SplyCur']/84e6,LTC_real['SplyCur']/84e6,LTC_sply['Sply_ideal']/84e6,
            BTC_half['end_pct_totsply']
        ]
        y_data = [
            BTC_real['CapMrktCurUSD'],BTC_real['CapRealUSD'],BTC_sply['CapS2Fmodel_ideal'],
            DCR_real['CapMrktCurUSD'],DCR_real['CapRealUSD'],DCR_sply['CapS2Fmodel_ideal'],
            LTC_real['CapMrktCurUSD'],LTC_real['CapRealUSD'],LTC_sply['CapS2Fmodel_ideal'],
            BTC_half['y_arb']
            ]
        name_data = [
            'Bitcoin Market Cap','Bitcoin Realised Cap','Bitcoin S2F Model',
            'Decred Market Cap','Decred Realised Cap','Decred S2F Model',
            'Litecoin Market Cap','Litecoin Realised Cap','Litecoin S2F Model',
            'BTC Halvings'
            ]
        color_data = [
            'rgb(237, 109, 71)','rgb(237, 109, 71)','rgb(237, 109, 71)',
            'rgb(46, 214, 161)','rgb(46, 214, 161)','rgb(46, 214, 161)',
            'rgb(255, 192, 0)','rgb(255, 192, 0)','rgb(255, 192, 0)',
            'rgb(255, 255, 255)' 
            ]
        dash_data = [
            'solid','dash','solid',
            'solid','dash','solid',
            'solid','dash','solid',
            'dot'
            ]
        width_data = [
            2,2,1,
            2,2,1,
            2,2,1,
            0.5
            ]
        opacity_data = [
            1,1,0.5,
            1,1,0.5,
            1,1,0.5,
            1
        ]
        legend_data = [
            True,True,True,
            True,True,True,
            True,True,True,
            True
        ]

        fig = make_subplots(specs=[[{"secondary_y": False}]])
        for i in range(0,10):
            fig.add_trace(go.Scatter(
                x=x_data[i], y=y_data[i],
                name=name_data[i],
                opacity=opacity_data[i],
                showlegend=legend_data[i],
                line=dict(width=width_data[i],color=color_data[i],dash=dash_data[i])),
                secondary_y=False)

        """$$$$$$$$$$$$$$$ FORMATTING $$$$$$$$$$$$$$$$"""
        # Add figure title
        fig.update_layout(title_text="Market Capitalisation vs Supply Mined")
        fig.update_xaxes(
            title_text="<b>Coin Supply Issued</b>",
            type='linear',
            range=[0,1]
            )
        fig.update_yaxes(
            title_text="<b>Coin Market Cap</b>",
            type="log",
            range=[4,15],
            secondary_y=False)
        fig.update_layout(template="plotly_dark")
        return fig


    def chart_dcrbtc_s2f_model(self):
        """%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
                        CREATE PLOT 04
                STOCK-TO-FLOW - S2F Market Cap
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"""

        x_data = [
            BTC_real['S2F'],
            DCR_real['S2F'],
            LTC_real['S2F'],
            BTC_half['S2F'],BTC_real['S2F']
        ]
        y_data = [
            BTC_real['CapMrktCurUSD'],
            DCR_real['CapMrktCurUSD'],
            LTC_real['CapMrktCurUSD'],
            BTC_half['y_arb'],BTC_real['CapS2Fmodel']
            ]
        name_data = [
            'Bitcoin Market Cap',
            'Decred Market Cap',
            'Litecoin Market Cap',
            'Bitcoin Halvings','Plan B Model'
            ]
        color_data = [
            'rgb(237, 109, 71)',
            'rgb(46, 214, 161)',
            'rgb(255, 192, 0)',
            'rgb(255,255,255)','rgb(255,255,255)'
            ]
        dash_data = [
            'solid',
            'solid',
            'solid',
            'dash','solid'
            ]
        size_data = [
            4,4,4,2,2
            ]
        legend_data = [
            True,True,True,
            True,True
        ]
        fig = make_subplots(specs=[[{"secondary_y": False}]])
        for i in range(0,3):
            fig.add_trace(go.Scatter(
                mode = 'markers',
                x=x_data[i], y=y_data[i],
                name=name_data[i],
                showlegend=legend_data[i],
                marker=dict(size=size_data[i],color=color_data[i])),
                secondary_y=False)
        for i in range(3,4):
            fig.add_trace(go.Scatter(
                x=x_data[i], y=y_data[i],
                name=name_data[i],
                showlegend=legend_data[i],
                line=dict(width=size_data[i],color=color_data[i],dash=dash_data[i])),
                secondary_y=False)

        """$$$$$$$$$$$$$$$ FORMATTING $$$$$$$$$$$$$$$$"""
        # Add figure title
        fig.update_layout(title_text="Market Capitalisation vs Stock-to-Flow Ratio")
        fig.update_xaxes(
            title_text="<b>Stock-to-Flow Ratio</b>",
            type='log',
            range=[-1,2]
            )
        fig.update_yaxes(
            title_text="<b>Coin Market Cap</b>",
            type="log",
            range=[4,12],
            secondary_y=False)
        fig.update_layout(template="plotly_dark")
        return fig


dcrbtc_monetary_policy().chart_dcrbtc_sply_area().show()
dcrbtc_monetary_policy().chart_dcrbtc_sply_s2f().show()
dcrbtc_monetary_policy().chart_dcrbtc_sply_marketcap().show()
dcrbtc_monetary_policy().chart_dcrbtc_s2f_model().show()


class ltcbtc_monetary_policy():
    
    def __init__(self):
        pass

    def chart_ltcbtc_sply_area(self):
        """%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
                        CREATE PLOT 01
                SUPPLY CURVES - STACKED AREA CHARTS
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"""
        x_data = [
            BTC_sply['blk'],
            LTC_sply['btc_blk']
        ]
        y_data = [
            BTC_sply['Sply_ideal'],
            LTC_sply['Sply_ideal']
        ]
        name_data = [
            'BTC Total Supply',
            'LTC Total Supply'
        ]
        color_data = [
            'rgb(255, 153, 0)',
            'rgb(255, 192, 0)'
        ]
        fill_data = [
            'tonexty',
            'tozeroy'
        ]
        opacity_data = [
            1,1
        ]
        fig = go.Figure()
        for i in range(0,1):
            fig.add_trace(go.Scatter(
                x=x_data[i], 
                y=y_data[i],
                name=name_data[i], 
                fill=fill_data[i],
                #fillcolor=color_data[i],
                #line_color= color_data[i],
                line=dict(
                    color=color_data[i],
                    width=2
                    #opacity=opacity_data[i]
                )))
        fig.update_layout(template="plotly_dark",title="Bitcoin and Litecoin Theoretical Supply Curves")
        
        return fig


    def chart_ltcbtc_sply_s2f(self):
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
            BTC_sply['blk'],
            BTC_sply['blk'],
            BTC_real['blk'],
            LTC_sply['btc_blk']+148500,
            LTC_sply['btc_blk']+148500,
            LTC_real['btc_blk']+148500,
            LTC_sply['btc_blk'],
            LTC_sply['btc_blk'],
            LTC_real['btc_blk'],
            BTC_half['blk']
        ]
        y_data = [
            BTC_sply['Sply_ideal'],
            BTC_sply['S2F_ideal'],
            BTC_real['S2F'],
            LTC_sply['Sply_ideal'],
            LTC_sply['S2F_ideal'],
            LTC_real['S2F'],
            LTC_sply['Sply_ideal'],
            LTC_sply['S2F_ideal'],
            LTC_real['S2F'],
            BTC_half['y_arb']
            ]
        name_data = [
            'Bitcoin Coin Supply',
            'Bitcoin S2F Ratio',
            'Bitcoin S2F Ratio (Actual)',
            'Litecoin Coin Supply',
            'Litecoin S2F Ratio',
            'Litecoin S2F Ratio (Actual)',
            'Litecoin Coin Supply (Offset)',
            'Litecoin S2F Ratio (Offset)',
            'Litecoin S2F Ratio (Offset, Actual)',
            'BTC Halvings'
            ]
        color_data = [
            'rgb(237, 109, 71)','rgb(237, 109, 71)','rgb(237, 109, 71)',
            'rgb(255, 192, 0)','rgb(255, 192, 0)','rgb(255, 192, 0)',
            'rgb(250, 38, 53)','rgb(250, 38, 53)','rgb(250, 38, 53)',
            'rgb(255, 255, 255)' 
            ]
        dash_data = [
            'solid','dot','solid',
            'solid','dot','solid',
            'solid','dot','solid',
            'solid'
            ]
        width_data = [
            5,5,1,4,4,1,4,4,1,0.5
            ]
        opacity_data = [
            1,1,0.75,
            1,1,0.75,
            1,1,0.75,
            0.5
        ]
        name_data[6]

        fig = make_subplots(specs=[[{"secondary_y": True}]])
        for i in [0,3,6]:
            fig.add_trace(go.Scatter(
                x=x_data[i], y=y_data[i],
                name=name_data[i],
                opacity=opacity_data[i],
                line=dict(width=width_data[i],color=color_data[i],dash=dash_data[i])),
                secondary_y=False)
        for i in [1,2,4,5,7,8,9]:
            fig.add_trace(go.Scatter(
                x=x_data[i], y=y_data[i],
                name=name_data[i],
                opacity=opacity_data[i],
                line=dict(width=width_data[i],color=color_data[i],dash=dash_data[i])),
                secondary_y=True)
        """$$$$$$$$$$$$$$$ FORMATTING $$$$$$$$$$$$$$$$"""
        # Add figure title
        fig.update_layout(title_text="Bitcoin and Litecoin Monetary Policy")
        fig.update_xaxes(
            title_text="<b>Bitcoin Block Height</b>",
            type='linear',
            range=[0,1200000]
            )
        fig.update_yaxes(
            title_text="<b>Coin Supply</b>",
            type="linear",
            range=[0,21000000],
            secondary_y=False)
        fig.update_yaxes(
            title_text="<b>Stock-to-Flow Ratio</b>",
            type="log",
            range=[-1,5],
            secondary_y=True)
        fig.update_layout(template="plotly_dark")
        return fig


    def chart_ltcbtc_sply_marketcap(self):
        """%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
                        CREATE PLOT 03
            SUPPLY AND DEMAND - % of Supply Mined VS Market Cap
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"""

        x_data = [
            BTC_real['SplyCur']/21000000,BTC_real['SplyCur']/21000000,
            LTC_real['SplyCur']/84000000,LTC_real['SplyCur']/84000000,
            BTC_half['end_pct_totsply']
        ]
        y_data = [
            BTC_real['CapMrktCurUSD'],BTC_real['CapRealUSD'],
            LTC_real['CapMrktCurUSD'],LTC_real['CapRealUSD'],
            BTC_half['y_arb']
            ]
        name_data = [
            'Bitcoin Market Cap','Bitcoin Realised Cap',
            'Litecoin Market Cap','Litecoin Realised Cap',
            'BTC Halvings'
            ]
        color_data = [
            'rgb(237, 109, 71)','rgb(237, 109, 71)',
            'rgb(255, 192, 0)','rgb(255, 192, 0)',
            'rgb(255, 255, 255)' 
            ]
        dash_data = [
            'solid','dash',
            'solid','dash',
            'dot'
            ]
        width_data = [
            2,2,2,2,0.5
            ]


        fig = make_subplots(specs=[[{"secondary_y": False}]])
        for i in range(0,5):
            fig.add_trace(go.Scatter(
                x=x_data[i], y=y_data[i],
                name=name_data[i],
                line=dict(width=width_data[i],color=color_data[i],dash=dash_data[i])),
                secondary_y=False)

        """$$$$$$$$$$$$$$$ FORMATTING $$$$$$$$$$$$$$$$"""
        # Add figure title
        fig.update_layout(title_text="Market Capitalisation vs Supply Mined")
        fig.update_xaxes(
            title_text="<b>Coin Supply Issued</b>",
            type='linear',
            range=[0,1]
            )
        fig.update_yaxes(
            title_text="<b>Coin Market Cap</b>",
            type="log",
            range=[4,12],
            secondary_y=False)
        fig.update_layout(template="plotly_dark")
        return fig


    def chart_ltcbtc_s2f_model(self):
        """%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
                        CREATE PLOT 04
                STOCK-TO-FLOW - S2F Market Cap
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"""

        x_data = [
            BTC_real['S2F'],
            LTC_real['S2F'],
            BTC_half['S2F'],BTC_real['S2F']
        ]
        y_data = [
            BTC_real['CapMrktCurUSD'],
            LTC_real['CapMrktCurUSD'],
            BTC_half['y_arb'],BTC_real['CapS2Fmodel']
            ]
        name_data = [
            'Bitcoin Market Cap',
            'Litecoin Market Cap',
            'Bitcoin Halvings','Plan B Model'
            ]
        color_data = [
            'rgb(237, 109, 71)',
            'rgb(255, 192, 0)',
            'rgb(255,255,255)','rgb(255,255,255)'
            ]
        dash_data = [
            'solid',
            'solid',
            'dash','solid'
            ]
        size_data = [
            4,4,2,2
            ]

        fig = make_subplots(specs=[[{"secondary_y": False}]])
        for i in range(0,2):
            fig.add_trace(go.Scatter(
                mode = 'markers',
                x=x_data[i], y=y_data[i],
                name=name_data[i],
                marker=dict(size=size_data[i],color=color_data[i])),
                secondary_y=False)
        for i in range(2,4):
            fig.add_trace(go.Scatter(
                x=x_data[i], y=y_data[i],
                name=name_data[i],
                line=dict(width=size_data[i],color=color_data[i],dash=dash_data[i])),
                secondary_y=False)

        """$$$$$$$$$$$$$$$ FORMATTING $$$$$$$$$$$$$$$$"""
        # Add figure title
        fig.update_layout(title_text="Market Capitalisation vs Stock-to-Flow Ratio")
        fig.update_xaxes(
            title_text="<b>Stock-to-Flow Ratio</b>",
            type='log',
            range=[-1,2]
            )
        fig.update_yaxes(
            title_text="<b>Coin Market Cap</b>",
            type="log",
            range=[4,12],
            secondary_y=False)
        fig.update_layout(template="plotly_dark")
        return fig


ltcbtc_monetary_policy().chart_ltcbtc_sply_area().show()
ltcbtc_monetary_policy().chart_ltcbtc_sply_s2f().show()
ltcbtc_monetary_policy().chart_ltcbtc_sply_marketcap().show()
ltcbtc_monetary_policy().chart_ltcbtc_s2f_model().show()

"""**************************************************************************
                            Part 2 - Proof of Work
***************************************************************************"""

class dcrbtc_pow_security():

    def __init__(self):
        pass

    def chart_dcrbtc_btc_premine(self):
        """%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
                        CREATE PLOT
        Bitcoin premine + hashrate up to 1.68 Million Supply
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"""
        
        #Typical CPU hashrates from 2009
        # https://en.bitcoin.it/wiki/Non-specialized_hardware_comparison
        # https://en.wikipedia.org/wiki/List_of_Intel_Core_i7_microprocessors#Nehalem_microarchitecture_(1st_generation)
        core_i7_920 = [[0,19.2e6],[21e6,19.2e6]]
        core_i7_920 = pd.DataFrame(data=core_i7_920,columns=['sply_arb','hashrate_Hs'])
        core_i7_920

        #Calculate early Bitcoin sub-set up to supply of 1.68million
        #Establish the grounds for a low premine
        BTC_early = BTC_real[BTC_real['SplyCur']<(1.68e6*2)]
        BTC_early = BTC_early[BTC_early['blk']>0]
        BTC_early = pd.concat([BTC_early.set_index('blk',drop=False),BTC_hash],axis=1,join='inner')

        x_data = [
            BTC_early['SplyCur'],
            BTC_early['SplyCur'],
            core_i7_920['sply_arb'],
            [1.68e6,1.68e6]

        ]
        y_data = [
            BTC_early['DiffMean'],
            BTC_early['pow_hashrate_THs']*1e12,
            core_i7_920['hashrate_Hs'],
            [0,1e10]
            ]

        name_data = [
            'Bitcoin Difficulty',
            'Bitcoin Hashrate',
            '1x Core i7 920 Hashrate (4/8 p/t)',
            'Satoshi 1.68M Premine?'
            ]
        color_data = [
            'rgb(237, 109, 71)',
            'rgb(20, 169, 233)',
            'rgb(250, 38, 53)',
            'rgb(250, 38, 53)'

            ]
        dash_data = [
            'solid',
            'solid',
            'dash',
            'dash'
            ]
        width_data = [
            4,4,4,4
            ]

        fig = make_subplots(specs=[[{"secondary_y": True}]])
        for i in [0]:
            fig.add_trace(go.Scatter(
                mode = 'lines',
                x=x_data[i], y=y_data[i],
                name=name_data[i],
                #yaxis=axis_data[i],
                line=dict(width=width_data[i],color=color_data[i],dash=dash_data[i])),
                secondary_y=False)
        for i in [1,2,3]:
            fig.add_trace(go.Scatter(
                mode = 'lines',
                x=x_data[i], y=y_data[i],
                name=name_data[i],
                line=dict(width=width_data[i],color=color_data[i],dash=dash_data[i])),
                secondary_y=True)
        """$$$$$$$$$$$$$$$ FORMATTING $$$$$$$$$$$$$$$$"""
        # Add figure title
        fig.update_layout(title_text="How large was Bitcoin's Early Premine?")
        fig.update_xaxes(
            title_text="<b>Bitcoin Supply Mined</b>",
            type='linear',
            range=[0,2e6]
            )
        fig.update_yaxes(
            title_text="<b>Bitcoin Difficulty</b>",
            type="log",
            titlefont=dict(color='rgb(237, 109, 71)'),
            tickfont=dict(color='rgb(237, 109, 71)'),
            secondary_y=False)
        fig.update_yaxes(
            title_text="<b>Hashrate (H/s)</b>",
            type="log",
            range=[5,9],
            titlefont=dict(color='rgb(20, 169, 233)'),
            tickfont=dict(color='rgb(20, 169, 233)'),
            secondary_y=True)
        fig.update_layout(template="plotly_dark")
        return fig

    def chart_dcrbtc_powdiffhash_date(self):
        """%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
                        CREATE PLOT 
        Hashrate and Difficulty Adjustment VS BITCOIN BLOCK HEIGHT
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"""
        x_data = [
            BTC_real['date'],
            DCR_real['date'],
            DCR_real['date'],
            BTC_hash['date'],
            DCR_perf['date']
        ]
        y_data = [
            BTC_real['DiffMean']/BTC_real.loc[BTC_real['DiffMean'].first_valid_index(),'DiffMean'],
            DCR_real['DiffMean']/DCR_real.loc[DCR_real['DiffMean'].first_valid_index(),'DiffMean'],
            DCR_real['DiffMean']*100/60/DCR_real.loc[DCR_real['DiffMean'].first_valid_index(),'DiffMean'],
            BTC_hash['pow_hashrate_THs'],
            DCR_perf['pow_hashrate_THs']
            ]
        name_data = [
            'Bitcoin Difficulty',
            'Decred Difficulty (Offset)',
            'Decred Difficulty (Offset x1.667)',
            'Bitcoin Hashrate',
            'Decred Hashrate (Offset)'
            ]
        color_data = [
            'rgb(239, 125, 50)',
            'rgb(1, 255, 116)',
            'rgb(41, 112, 255)',
            'rgb(239, 125, 50)',
            'rgb(1, 255, 116)'
            ]

        dash_data = [
            'solid',
            'solid',
            'solid',
            'dash',
            'dash'
            ]
        width_data = [
            4,4,4,4,4
            ]

        fig = make_subplots(specs=[[{"secondary_y": True}]])
        for i in [0,1,2]:
            fig.add_trace(go.Scatter(
                mode = 'lines',
                x=x_data[i], y=y_data[i],
                name=name_data[i],
                #yaxis=axis_data[i],
                line=dict(width=width_data[i],color=color_data[i],dash=dash_data[i])),
                secondary_y=False)
        for i in [3,4]:
            fig.add_trace(go.Scatter(
                mode = 'lines',
                x=x_data[i], y=y_data[i],
                name=name_data[i],
                #yaxis=axis_data[i],
                line=dict(width=width_data[i],color=color_data[i],dash=dash_data[i])),
                secondary_y=True)
        """$$$$$$$$$$$$$$$ FORMATTING $$$$$$$$$$$$$$$$"""
        # Add figure title
        fig.update_layout(title_text="Proof of Work Security Comparison")
        fig.update_xaxes(
            title_text="<b>Bitcoin Block Height</b>",
            type='date'
            )
        fig.update_yaxes(
            title_text="<b>PoW Difficulty Growth</b>",
            type="log",
            tickformat= ',.0%',
            range=[0,18],
            secondary_y=False)
        fig.update_yaxes(
            title_text="<b>Hashrate (TH/s)</b>",
            type="log",
            range=[-9,9],
            secondary_y=True)
        fig.update_layout(template="plotly_dark")
        
        return fig

    def chart_dcrbtc_powdiffhash_sply(self):
        """%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
                        CREATE PLOT 07
        Hashrate and Difficulty Adjustment VS COIN SUPPLY
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"""

        # Filter BTC hashrate for blk > 0 and combine with BTC_real (coin + sply)
        BTC_real2 = BTC_real[BTC_real['blk']>0]
        BTC_hash2 = BTC_hash[BTC_hash['blk']>0]
        BTC_plot = pd.concat([BTC_real2.set_index('blk',drop=False),BTC_hash2.set_index('blk')],axis=1,join='inner')

        # Plot against coin supply
        # Yaxis 1 = Difficulty Adjustment Growth
        # Yaxis 2 = Hashrate

        #Calculate columns for Difficulty Growth (to normalise)
        # Scale up DCR hashrate by 10/6 as equivalent hashrate to BTC with 100% PoW
        BTC_plot['Diff_Growth'] = BTC_plot['DiffMean']/float(BTC_plot.loc[BTC_plot['DiffMean'].first_valid_index(),['DiffMean']])
        DCR_real['Diff_Growth'] = DCR_real['DiffMean']/float(DCR_real.loc[DCR_real['DiffMean'].first_valid_index(),['DiffMean']])
        DCR_real['Diff_Growth_10-6'] = DCR_real['Diff_Growth']*10/6

        DCR_perf.columns
        x_data = [
            BTC_plot['SplyCur']/21e6, #BTC Diff Growth
            DCR_real['SplyCur']/21e6, #DCR Diff Growth
            DCR_real['SplyCur']/21e6, #DCR Diff Growth * 10/6
            BTC_plot['SplyCur']/21e6, #BTC Hashrate
            DCR_perf['circulation']/21e6 #DCR Hashrate
        ]
        #Difficulty / First valid Difficulty --> Growth
        y_data = [
            BTC_plot['Diff_Growth'],
            DCR_real['Diff_Growth'],
            DCR_real['Diff_Growth_10-6'],
            BTC_plot['pow_hashrate_THs'],
            DCR_perf['pow_hashrate_THs']
            ]

        name_data = [
            'Bitcoin Difficulty',
            'Decred Difficulty',
            'Decred Difficulty (x1.667)',
            'Bitcoin Hashrate',
            'Decred Hashrate'
            ]
        color_data = [
            'rgb(239, 125, 50)',
            'rgb(1, 255, 116)',
            'rgb(41, 112, 255)',
            'rgb(239, 125, 50)',
            'rgb(1, 255, 116)'
            ]

        dash_data = [
            'solid',
            'solid',
            'solid',
            'dash',
            'dash'
            ]
        width_data = [
            4,4,4,4,4
            ]

        fig = make_subplots(specs=[[{"secondary_y": True}]])
        for i in [0,1,2]:
            fig.add_trace(go.Scatter(
                mode = 'lines',
                x=x_data[i], y=y_data[i],
                name=name_data[i],
                line=dict(width=width_data[i],color=color_data[i],dash=dash_data[i])),
                secondary_y=False)
        for i in [3,4]:
            fig.add_trace(go.Scatter(
                mode = 'lines',
                x=x_data[i], y=y_data[i],
                name=name_data[i],
                line=dict(width=width_data[i],color=color_data[i],dash=dash_data[i])),
                secondary_y=True)
        """$$$$$$$$$$$$$$$ FORMATTING $$$$$$$$$$$$$$$$"""
        # Add figure title
        fig.update_layout(title_text="Proof of Work Security")
        fig.update_xaxes(
            title_text="<b>Total Supply Minted</b>",
            type='linear',
            range=[0,1],
            tickformat= ',.0%'
            )
        fig.update_yaxes(
            title_text="<b>PoW Difficulty Growth</b>",
            type="log",
            tickformat= ',.0%',
            range=[0,18],
            secondary_y=False)
        fig.update_yaxes(
            title_text="<b>Hashrate (TH/s)</b>",
            type="log",
            range=[-9,9],
            secondary_y=True)
        fig.update_layout(template="plotly_dark")
        
        return fig


dcrbtc_pow_security().chart_dcrbtc_btc_premine().show()
dcrbtc_pow_security().chart_dcrbtc_powdiffhash_date().show()
dcrbtc_pow_security().chart_dcrbtc_powdiffhash_sply().show()










#Dual Axis

#axis_data = [
#    "y","y2","y2"
#]
#
#fig = go.Figure()
#fig.update_layout(
#    xaxis=dict(
#        title="<b>Bitcoin Block Height</b>",
#        type='linear'
#    ),
#    yaxis=dict(
#        title="Bitcoin Difficulty Growth",
#        type='log',
#        #range=[0,15],
#        #tickformat= ',.0%')
#        titlefont=dict(color=color_data[0]),
#        tickfont=dict(color=color_data[0]),
#    ),
#    yaxis2=dict(
#        title="Decred Difficulty Growth",
#        type='log',
#        #range=[0,15],
#        titlefont=dict(color=color_data[1]),
#        tickfont=dict(color=color_data[1]),
#        anchor="free",
#        overlaying="y",
#        side="left",
#        position=0.05
#    )
#)