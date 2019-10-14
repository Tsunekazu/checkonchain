# Calculate a Suite of Bitcoin Specific Metrics
#Data Science
import pandas as pd
import numpy as np
import math
import datetime as date
today = date.datetime.now().strftime('%Y-%m-%d')

from checkonchain.general.coinmetrics_api import *
from checkonchain.general.regression_analysis import *
from checkonchain.btconchain.btc_schedule import *


class btc_add_metrics():

    def __init__(self):
        self.topcapconst = 35 #Top Cap = topcapconst * Avg Cap
        self.blkrew_ratio = [1.0] #PoW Reward Fraction

    def btc_coin(self):
        df = Coinmetrics_api('btc',"2009-01-03","2019-10-07").convert_to_pd()
        df['age'] = (df[['date']] - df.loc[0,['date']])/np.timedelta64(1,'D')
        #Add in Plan B Data for Price and Market Cap
        #Create dataframe with Plan B price data before Coinmetrics has it
        print('...adding monthly Plan B PriceUSD and CapMrktCurUSD 2009-10...')
        planB_data = [
            ['01-10-2009',0.000763941940412529],
            ['01-11-2009',0.002],
            ['01-12-2009',0.002],
            ['01-01-2010',0.002],
            ['01-02-2010',0.002],
            ['01-03-2010',0.003],
            ['01-04-2010',0.0035],
            ['01-05-2010',0.0041],
            ['01-06-2010',0.04],
            ['01-07-2010',0.07]
            ]
        df_planB = pd.DataFrame(data=planB_data,columns=['date','PriceUSD'])
        df_planB['date'] = pd.to_datetime(df_planB['date'],utc=True)
        #Populate Price and Market Cap
        df['notes'] = str('')
        for i in df_planB['date']:
            df.loc[df.date==i,'PriceUSD'] = float(df_planB.loc[df_planB.date==i,'PriceUSD'])
            df.loc[df.date==i,'CapMrktCurUSD'] = df.loc[df.date==i,'PriceUSD'] * df.loc[df.date==i,'SplyCur']
            df.loc[df.date==i,'notes'] = 'PriceUSD and CapMrktCurUSD from Plan B data (@100TrillionUSD)'
        return df


    def btc_sply(self,to_blk):
        df = btc_supply_schedule(to_blk).btc_supply_function()
        #Calculate projected S2F Models Valuations
        btc_s2f_model = regression_analysis().regression_constants()['btc_s2f']
        df['CapS2Fmodel'] = np.exp(float(btc_s2f_model['coefficient'])*np.log(df['S2F_ideal'])+float(btc_s2f_model['intercept']))
        df['PriceS2Fmodel'] = df['CapS2Fmodel']/df['Sply_ideal']
        #Calc S2F Model - Bitcoins Plan B Model
        planb_s2f_model = regression_analysis().regression_constants()['planb']
        df['CapPlanBmodel'] = np.exp(float(planb_s2f_model['coefficient'])*np.log(df['S2F_ideal'])+float(planb_s2f_model['intercept']))
        df['PricePlanBmodel'] = df['CapPlanBmodel']/df['Sply_ideal']
        return df


    def btc_real(self):
        print('...compiling Bitcoin specific metrics (coinmetrics + supply curve)...')
        _coin = self.btc_coin()
        _blk_max = int(_coin['blk'][_coin.index[-1]])
        _sply = self.btc_sply(_blk_max)

        # Drop uncessecary columns, Vlookup nearest on blk
        df = pd.merge_asof(_coin,_sply[['blk','blk_reward','Sply_ideal', 'PoWSply_ideal','inflation_ideal','S2F_ideal']],on='blk')
        return df

    def btc_pricing_models(self):
        print('...Calculating Bitcoin pricing models...')
        _real = self.btc_real()
        df = _real

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

        #Calc S2F Model - Specific to Bitcoin
        btc_s2f_model = regression_analysis().ln_regression(df,'S2F','CapMrktCurUSD','date')['model_params']
        df['CapS2Fmodel'] = np.exp(float(btc_s2f_model['coefficient'])*np.log(df['S2F'])+float(btc_s2f_model['intercept']))
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

        #Moving Averages
        df['PriceUSD_128DMA'] = df['PriceUSD'].rolling(128).mean()
        df['PriceUSD_200DMA'] = df['PriceUSD'].rolling(200).mean()
        return df

    def btc_oscillators(self):
        print('...Calculating Bitcoin Oscillators...')
        _pricing = self.btc_pricing_models()
        df = _pricing        
        #Calc - NVT_28, NVT_90, NVTS, RVT_28, RVT_90, RVTS
        df['NVT_28'] = df['CapMrktCurUSD'].rolling(28).mean()/ df['TxTfrValUSD'].rolling(28).mean()
        df['NVT_90'] = df['CapMrktCurUSD'].rolling(90).mean()/df['TxTfrValUSD'].rolling(90).mean()
        df['NVTS']   = df['CapMrktCurUSD']/ df['TxTfrValUSD'].rolling(28).mean()
        df['RVT_28'] = df['CapRealUSD'].rolling(28).mean()/ df['TxTfrValUSD'].rolling(28).mean()
        df['RVT_90'] = df['CapRealUSD'].rolling(90).mean()/df['TxTfrValUSD'].rolling(90).mean()
        df['RVTS']   = df['CapRealUSD']/ df['TxTfrValUSD'].rolling(28).mean()

        #Mayer Multiple
        df['MayerMultiple'] = df['PriceUSD']/df['PriceUSD_200DMA']

        return df

#BTC = btc_add_metrics().btc_coin()