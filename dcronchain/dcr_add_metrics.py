# Calculate a Suite of Decred Specific Metrics
#Data Science
import pandas as pd
import numpy as np
import math
import datetime as date
today = date.datetime.now().strftime('%Y-%m-%d')

from checkonchain.general.coinmetrics_api import * #Coinmetrics.io
from checkonchain.general.regression_analysis import *
from checkonchain.dcronchain.dcr_schedule import * #DCR Schedule
from checkonchain.dcronchain.dcr_dcrdata_api import * #DCRdata.org

import os
os.getcwd()
os.chdir('D:\code_development\checkonchain\checkonchain')

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
        df['age'] = (df[['date']] - df.loc[0,['date']])/np.timedelta64(1,'D')
        
        print('...adding PriceUSD and CapMrktCurUSD for $0.49 (founders, 8/9-Feb-2016) and Bittrex (10-02-2016 to 16-05-2016)...')
        #Import Early price data --> founders $0.49 for 8/9 Feb 2016 and Bitrex up to 16-May-2016
        df_dcr_earlyprice = pd.read_csv(r"dcronchain\resources\data\dcr_pricedata_2016-02-08_2016-05-16.csv")
        df_dcr_earlyprice['date'] = pd.to_datetime(df_dcr_earlyprice['date'],utc=True)
        df['notes'] = str('')
        for i in df_dcr_earlyprice['date']:
            df.loc[df.date==i,'PriceUSD'] = float(df_dcr_earlyprice.loc[df_dcr_earlyprice.date==i,'PriceUSD'])
            df.loc[df.date==i,'PriceBTC'] = float(df_dcr_earlyprice.loc[df_dcr_earlyprice.date==i,'PriceBTC'])
            df.loc[df.date==i,'CapMrktCurUSD'] = df.loc[df.date==i,'PriceUSD'] * df.loc[df.date==i,'SplyCur']
            df.loc[df.date==i,'notes'] = df_dcr_earlyprice.loc[df_dcr_earlyprice.date==i,'notes']
        return df

    def dcr_sply(self,to_blk):
        df = dcr_supply_schedule(to_blk).dcr_supply_function()

        #Calculate projected S2F Models Valuations
        dcr_s2f_model = regression_analysis().regression_constants()['dcr_s2f']
        df['CapS2Fmodel'] = np.exp(float(dcr_s2f_model['coefficient'])*np.log(df['S2F_ideal'])+float(dcr_s2f_model['intercept']))
        df['PriceS2Fmodel'] = df['CapS2Fmodel']/df['Sply_ideal']
        #Calc S2F Model - Bitcoins Plan B Model
        planb_s2f_model = regression_analysis().regression_constants()['planb']
        df['CapPlanBmodel'] = np.exp(float(planb_s2f_model['coefficient'])*np.log(df['S2F_ideal'])+float(planb_s2f_model['intercept']))
        df['PricePlanBmodel'] = df['CapPlanBmodel']/df['Sply_ideal']        
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
        # Clean DCR hashrate data
        _perf = _perf[_perf['pow_hashrate_THs']>1]
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
        print('...Calculating Decred specific metrics - (coinmetrics + supply curve + dcrdata)...')
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
        df = pd.merge_asof(df,_sply[['blk','blk_reward','Sply_ideal', 'PoWSply_ideal', 'PoSSply_ideal','FundSply_ideal','inflation_ideal','S2F_ideal']],on='blk')
        #Calculate PoS Return on Investment
        df['PoW_Income'] = df['blk_reward']*self.blkrew_ratio[0]*df['window']
        df['PoS_Income'] = df['blk_reward']*self.blkrew_ratio[1]*df['window']
        df['Fund_Income'] = df['blk_reward']*self.blkrew_ratio[2]*df['window']
        return df


    def dcr_pricing_models(self):
        print('...Calculating Decred pricing models...')
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

        #Calc S2F Model - Specific to Decred
        dcr_s2f_model = regression_analysis().ln_regression(df,'S2F','CapMrktCurUSD','date')['model_params']
        df['CapS2Fmodel'] = np.exp(float(dcr_s2f_model['coefficient'])*np.log(df['S2F'])+float(dcr_s2f_model['intercept']))
        df['PriceS2Fmodel'] = df['CapS2Fmodel']/df['SplyCur']
        #Calc S2F Model - Bitcoins Plan B Model
        planb_s2f_model = regression_analysis().regression_constants()['planb']
        df['CapPlanBmodel'] = np.exp(float(planb_s2f_model['coefficient'])*np.log(df['S2F'])+float(planb_s2f_model['intercept']))
        df['PricePlanBmodel'] = df['CapPlanBmodel']/df['SplyCur']

        # Inflow Cap and Inflow Price
        df['CapInflow'] = df['DailyIssuedUSD'].expanding().sum()
        df['PriceInflow'] =df['CapInflow']/df['SplyCur']
        
        # Fee Cap and Fee Price
        df['CapFee'] = df['FeeTotUSD'].expanding().sum()
        df['PriceFee'] =df['CapFee']/df['SplyCur']

        #Calculate Miner Income
        df['MinerIncome'] = df['CapInflow'] + df['CapFee']
        df['FeesPct'] =  df['CapFee']/df['MinerIncome']
        df['MinerCap'] = df['MinerIncome'].expanding().sum()

        return df

    def dcr_oscillators(self):
        print('...Calculating Decred Oscillators...')
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
