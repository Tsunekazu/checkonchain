#Calculate Additional Metrics
import pandas as pd
import numpy as np
import datetime as date
today = date.datetime.now().strftime('%Y-%m-%d')

from checkonchain.general.coinmetrics_api import *

class btc_metrics:
    
    def __init__(self):   
        pass
    
    def btc_metrics(self):
        #Add metrics for block, btc_block, inflation rate, S2F Ratio
        df = Coinmetrics_api.convert_to_pd(self)
        
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

        #Calc - NVT_28, NVT_90, NVTS, RVT_28, RVT_90, RVTS
        df['NVT_28'] = df['CapMrktCurUSD'].rolling(28).mean()/ df['TxTfrValUSD'].rolling(28).mean()
        df['NVT_90'] = df['CapMrktCurUSD'].rolling(90).mean()/df['TxTfrValUSD'].rolling(90).mean()
        df['NVTS']   = df['CapMrktCurUSD']/ df['TxTfrValUSD'].rolling(28).mean()
        df['RVT_28'] = df['CapRealUSD'].rolling(28).mean()/ df['TxTfrValUSD'].rolling(28).mean()
        df['RVT_90'] = df['CapRealUSD'].rolling(90).mean()/df['TxTfrValUSD'].rolling(90).mean()
        df['RVTS']   = df['CapRealUSD']/ df['TxTfrValUSD'].rolling(28).mean()

        #Calc - Daily Issuance
        for i in range(0,len(df.index)):
            #Correct btc_blk_est
            df.loc[i,'btc_blk_est'] = max(0,df.loc[i,'btc_blk_est'])
            
            if i == 0:
                df.loc[i,'DailyIssuedNtv'] = df.loc[i,'SplyCur']
            else:
                df.loc[i,'DailyIssuedNtv'] = df.loc[i,'SplyCur'] - df.loc[i-1,'SplyCur']
        
        # Calc - inflation Rate,  S2F, S2F Model, S2F Price
        df['DailyIssuedUSD'] = df['DailyIssuedNtv'] * df['PriceUSD']            
        df['inf_pct_ann'] = df['DailyIssuedNtv']*365/df['SplyCur']
        df['S2F'] = 1/df['inf_pct_ann']
        df['CapS2Fmodel'] = np.exp(3.31954*np.log(df['S2F'])+14.6227)
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