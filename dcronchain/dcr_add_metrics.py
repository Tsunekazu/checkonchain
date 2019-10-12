# Calculate a Suite of Decred Specific Metrics
from checkonchain.dcronchain.__init__ import *

"""ROADMAP
Goal:   Distil datasets down into core datasets for development of useful metrics

End Datasets: 
    Native Dataset --> DCR_natv = DCR_perf (by blk) + DCR_diff (smeared + filled backwards for step functions)
        For plotting actual performance over time

    Real Dataset --> DCR_diff (by blk at 144 spacing) + DCR_perf (culled to diff blk) + DCR_coin (vlookup)
        Noting 2x 144 blk windows per day on avg --> 2x coin data per DCR_diff

    Theoretical Performance - by blk
        Supply as base
        Increased discretisation of data
        Average / smearing of conmetrics data
        DCR_path = DCR_sply + smear(DCR_real)

Notes:
    Ticket window (DCR_diff) is step function except for:
        'ticket_count' '
        'missed'
"""

class dcr_add_metrics():

    def __init__(self):
        self.topcapconst = 12 #Top Cap = topcapconst * Avg Cap
        self.blkrew_ratio = [0.6,0.3,0.1] #PoW,PoS,Fund Block Reward Fraction

    def dcr_coin(self):
        df = Coinmetrics_api('dcr',"2016-02-08",today).convert_to_pd()
        return df

    def dcr_sply(self,to_blk):
        df = dcr_supply_schedule(to_blk).dcr_supply_function()
        return df

    def dcr_diff(self):
        df = Extract_dcrdata().dcr_difficulty()
        return df

    def dcr_perf(self):
        df = Extract_dcrdata().dcr_performance()
        return df
    
    def dcr_natv(self):
        #Step 1 - smear tickets bought in window for economic calculations
        _diff = self.dcr_diff()
        _perf = self.dcr_perf()
        _diff['ticket_count_smeared'] = _diff['ticket_count']/144
        # DCR_natv concat diff and perf on blk, dropping useless cols
        df = pd.concat([
            _perf.set_index('blk',drop=True),
            _diff.drop(['time','window','missed'],axis=1).set_index('blk',drop=True)],
            axis=1).reset_index()
        # fill backwards for selected constants (step functions = tic price and diff) and smeared vals
        df[['ticket_count_smeared','ticket_price','pow_diff']]=df[['ticket_count_smeared','ticket_price','pow_diff']].fillna(method='bfill')
        return df

    def dcr_real(self):
        _coin = self.dcr_coin()
        _diff = self.dcr_diff()
        _perf = self.dcr_perf()
        _blk_max = int(_coin['blk'][_coin.index[-1]])
        _sply = self.dcr_sply(_blk_max)

        # Set blk to float (default is int)
        _diff['blk']=_diff.astype({'blk':'float64'})
        _perf['blk']=_perf.astype({'blk':'float64'})
        # Drop uncessecary columns, perf = exact match, Vlookup nearest lower on blk for coin
        df = pd.merge_asof(_diff.drop(['time','missed'],axis=1),_perf.drop(['time','pow_offset'],axis=1),on='blk')
        df = pd.merge_asof(df,_coin,on='blk',direction='backward')
        df = pd.merge_asof(df,_sply[['blk','blk_reward','Sply_ideal', 'PoWSply_ideal', 'PoSSply_ideal','FundSply_ideal']],on='blk')
        #Calculate PoS Return on Investment
        df['PoW_Income'] = df['blk_reward']*self.blkrew_ratio[0]*df['window']
        df['PoS_Income'] = df['blk_reward']*self.blkrew_ratio[1]*df['window']
        df['Fund_Income'] = df['blk_reward']*self.blkrew_ratio[2]*df['window']
        return df


    def dcr_pricing_models(self):
        _real = self.dcr_real()
        df = _real
        #Calculate Ticket Based Valuation Metrics
        # Ticket Cap = cummulative USD put into tickets
        df['ticket_dcr_cost'] = df['ticket_count'] * df['ticket_price']
        df['ticket_usd_cost'] = df['ticket_dcr_cost'] * df['PriceUSD']
        df['CapTicket'] = df['ticket_usd_cost'].cumsum()
        df['CapTicketPrice'] = df['CapTicket'] / df['SplyCur']
        
        #Calculate Aggregate Ticket Risk-Reward
        #Risk = 28 to 142 day volatility of ticket value
        #Reward = PoS_Income
        df['dcr_hodl_rating'] = (df['ticket_usd_cost'].rolling(28).mean() / df['PoS_Income'])
        df['dcr_hodl_rating_tot'] = df['dcr_hodl_rating']*df['SplyCur']
        df['dcr_hodl_rating_pool'] = df['dcr_hodl_rating']*df['ticket_pool_value']/1e8
        df['dcr_hodl_rating_posideal'] = df['dcr_hodl_rating']*df['SplyCur']*self.blkrew_ratio[1]


        # Average Cap and Average Price
        df['CapAvg'] = df['CapMrktCurUSD'].fillna(0.0001) #Fill not quite to zero for Log charts/calcs
        df['CapAvg'] = df['CapAvg'].expanding().mean()
        df['PriceAvg'] = df['CapAvg']/df['SplyCur']
        # Delta Cap and Delta Price
        df['CapDelta'] = df['CapRealUSD'] - df['CapAvg']
        df['PriceDelta'] =df['CapDelta']/df['SplyCur']
        # Top Cap and Top Price
        df['CapTop'] = df['CapAvg']*self.topcapconst
        df['PriceTop'] =df['CapTop']/df['SplyCur']

        #Calc S2F Model
        s2f_model = self.dcr_regression('S2F','CapMrktCurUSD')['model_params']
        df['CapS2Fmodel'] = np.exp(s2f_model['coefficient']*np.log(df['S2F'])+s2f_model['intercept'])
        df['PriceS2Fmodel'] = df['CapS2Fmodel']/df['SplyCur']

        # Inflow Cap and Inflow Price
        df['CapInflow'] = df['DailyIssuedUSD'].expanding().sum()
        df['PriceInflow'] =df['CapInflow']/df['SplyCur']
        
        # Fee Cap and Fee Price
        df['CapFee'] = df['FeeTotUSD'].expanding().sum()
        df['PriceFee'] =df['CapFee']/df['SplyCur']

        #Calculate Miner Income
        df['MinerIncome'] = df['CapInflow'] + df['CapFee']
        df['FeesPct'] =  df['CapFee']/df['MinerIncome']

        return df

    def dcr_oscillators(self):
        _real = self.dcr_real()
        df = _real        
        #Calc - NVT_28, NVT_90, NVTS, RVT_28, RVT_90, RVTS
        df['NVT_28'] = df['CapMrktCurUSD'].rolling(28).mean()/ df['TxTfrValUSD'].rolling(28).mean()
        df['NVT_90'] = df['CapMrktCurUSD'].rolling(90).mean()/df['TxTfrValUSD'].rolling(90).mean()
        df['NVTS']   = df['CapMrktCurUSD']/ df['TxTfrValUSD'].rolling(28).mean()
        df['RVT_28'] = df['CapRealUSD'].rolling(28).mean()/ df['TxTfrValUSD'].rolling(28).mean()
        df['RVT_90'] = df['CapRealUSD'].rolling(90).mean()/df['TxTfrValUSD'].rolling(90).mean()
        df['RVTS']   = df['CapRealUSD']/ df['TxTfrValUSD'].rolling(28).mean()

        return df


    def dcr_regression(self,x_metric,y_metric):
        from sklearn.linear_model import LinearRegression
        _coin = self.dcr_coin()

        #Subset of coin, drop na values
        df = _coin[['blk','date',x_metric,y_metric]].dropna(axis=0)
        df = df.reset_index(drop=True)

        x=np.array(np.log(df[x_metric])).reshape((-1,1))
        y=np.array(np.log(df[y_metric]))
        regression_model = LinearRegression().fit(x, y)
        
        #Calculate progression of rsq over time 
        df['rsq']=0
        for i in range(0,len(df.index)):
            #Calculate S2F RSQ development
            df.loc[i,['rsq']]=LinearRegression().fit(
                np.log(df.loc[:i,[x_metric]]),
                np.log(df.loc[:i,[y_metric]])
                ).score(
                    np.log(df.loc[:i,[x_metric]]),
                    np.log(df.loc[:i,[y_metric]])
                    )

        #Calculate r_sq, intercept and coefficient of models
        model_params = pd.DataFrame(
            index=['regression_model'],
            data={
                'rsq':[regression_model.score(x,y)], 
                'intercept': [regression_model.intercept_],
                'coefficient':[float(regression_model.coef_)]
                })
        return {
            'regression_model': regression_model, 
            'model_params':model_params, 
            'rsq_develop':df
            }




"""##### CALCULATE DCR DATAFRAMES #####"""

#DCR_coin = dcr_add_metrics().dcr_coin()
#DCR_sply = dcr_add_metrics().dcr_sply(387187)
#DCR_perf = dcr_add_metrics().dcr_perf()
#DCR_diff = dcr_add_metrics().dcr_diff()
#DCR_natv = dcr_add_metrics().dcr_natv()
#DCR_real = dcr_add_metrics().dcr_real()
DCR_pricing = dcr_add_metrics().dcr_pricing_models()
#print('DCR_coin - by date')
#print(DCR_coin.columns)
#print('DCR_sply - by blk')
#print(DCR_sply.columns)
#print('DCR_perf - by blk')
#print(DCR_perf.columns)
#print('DCR_diff - by ticket window')
#print(DCR_diff.columns)
#print('DCR_natv - by blk')
#print(DCR_natv.columns)
#print('DCR_real - by ticket window')
#print(DCR_real.columns)




from checkonchain.dcronchain.charts import *
x_data = [
    DCR_pricing['blk'],DCR_pricing['blk'],
    DCR_pricing['blk'],DCR_pricing['blk'],DCR_pricing['blk']
        ]
y_data = [
    DCR_pricing['CapTicket'],DCR_pricing['CapMrktCurUSD'],
    DCR_pricing['dcr_hodl_rating_tot'],
    DCR_pricing['dcr_hodl_rating_pool'],
    DCR_pricing['dcr_hodl_rating_posideal']
    ]
name_data = [
    'ticket_cap','market_cap',
    'dcr_hodl_rating_tot','dcr_hodl_rating_pool','dcr_hodl_rating_posideal'
    ]
color_data = [
    'rgb(237, 109, 71)','rgb(46, 214, 161)',
    'rgb(41, 112, 255)','rgb(65, 191, 83)','rgb(112, 203, 255)'
    ]
dash_data = [
    'solid','solid','solid','solid','solid'
    ]
width_data = [
    2,2,2,2,2
    ]
opacity_data = [
    1,1,1,1,1
    ]
legend_data = [
    True,True,True,True,True
    ]

fig = make_subplots(specs=[[{"secondary_y": False}]])
for i in range(0,5):
    fig.add_trace(go.Scatter(
        x=x_data[i], y=y_data[i],
        name=name_data[i],
        opacity=opacity_data[i],
        showlegend=legend_data[i],
        line=dict(width=width_data[i],color=color_data[i],dash=dash_data[i])),
        secondary_y=False)

"""$$$$$$$$$$$$$$$ FORMATTING $$$$$$$$$$$$$$$$"""
# Add figure title
fig.update_layout(title_text="Decred Total Ticket Investment")
fig.update_xaxes(
    title_text="<b>Decred Block Height</b>",
    type='linear'
    #range=[0,1]
    )
fig.update_yaxes(
    title_text="<b>Valuation Metric</b>",
    type="log",
    #range=[4,15],
    secondary_y=False)
fig.update_layout(template="plotly_dark")
fig.show()
