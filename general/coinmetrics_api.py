# Import Coinmetrics API
import coinmetrics
import pandas as pd
import numpy as np

# Initialize a reference object, in this case `cm` for the Community API
cm = coinmetrics.Community()

#Pull Asset Data
#'asset'
# start timestamp 'yyyy-mm-dd'
# end timestamp 'yyyy-mm-dd'
# top cap constant (Top cap = Average Cap * Const)
# BTC = Coinmetrics_api('btc',"2009-01-03",today,35).add_metrics()
# BTC.head(5)

"""
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
Coinmetrics API calls
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
"""
class Coinmetrics_api:
       
    def __init__(self,asset,begin_timestamp,end_timestamp,topcapconst):
        # List all available metrics for BTC.
        self.asset = asset
        self.begin_timestamp=begin_timestamp
        self.end_timestamp=end_timestamp
        self.topcapconst = topcapconst

    def collect_data(self):
        available_data_types = cm.get_available_data_types_for_asset(self.asset)
        metric_list = str((','.join(available_data_types))) #setup complete metric list
        #print(metric_list)
        asset_data = cm.get_asset_data_for_time_range(self.asset, metric_list, self.begin_timestamp, self.end_timestamp)
        return asset_data
    
    def convert_to_pd(self):
        asset_data = Coinmetrics_api.collect_data(self)
        df = coinmetrics.cm_to_pandas(asset_data)
        #df.index = df.index.map(lambda x: str(x)[:-14])
        #df.index = pd.to_datetime(df.index)
        #df.index = df.index.strftime("%d-%m-%Y")
        df.index.name = 'date'
        df.reset_index(inplace=True)
        df['date'] = pd.to_datetime(df['date'])
        return df.fillna(0.0001) #Fill not quite to zero for Log charts/calcs

    def add_metrics(self):
        #Add metrics for block, btc_block, inflation rate, S2F Ratio
        df = Coinmetrics_api.convert_to_pd(self)
        
        #Calc - block height
        df['blk']=df['BlkCnt'].cumsum()
        
        #Calc - approx btc block height (Noting BTC blocks were mined from 9/Jan/09)
        df['btc_blk_est'] = (df['date'] - pd.to_datetime(np.datetime64('2009-01-09'),utc=True))
        df['btc_blk_est'] = df['btc_blk_est']/np.timedelta64(1,'D') #convert from timedelta to Days (float)
        df['btc_blk_est'] = df['btc_blk_est']*(24*6) #Note - corrected for neg values in loop below
        
        #Realised Price
        df['PriceRealised'] = df['CapRealUSD']/df['SplyCur']
        # Average Cap and Average Price
        df['CapAvg'] = df['CapMrktCurUSD'].expanding().mean()
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


"""Coinmetrics Community API"""



# NVTAdj
# NVTAdj90
# PriceBTC
# PriceUSD
# ROI1yr
# ROI30d
# SplyCur
# TxCnt
# TxTfr
# TxTfrValAdjNtv
# TxTfrValAdjUSD
# TxTfrValMeanNtv
# TxTfrValMeanUSD
# TxTfrValMedNtv
# TxTfrValMedUSD
# TxTfrValNtv
# TxTfrValUSD
# VtyDayRet180d
# VtyDayRet30d
# VtyDayRet60d

"""Blockchain Metrics"""
# date
# AdrActCnt
# BlkCnt
# BlkSizeByte
# BlkSizeMeanByte
# blk
# btc_blk_est

"""Network Valuation Models"""
#CapMrktCurUSD      - Market Cap
#CapRealUSD         - Realised Cap
#CapAvg             - Average Cap (All Time Average of Market Cap)


"""Network Pricing Models"""
#PriceUSD           - Coin Price USD
#PriceRealised      - Realised Price USD
#PriceAvg           - All time Average Price USD 

"""Network Value Metrics"""
# CapMVRVCur        - Ratio of Market Cap to Realised Cap


"""Miner Metrics"""
# DiffMean          - Average Difficulty
# FeeMeanNtv        - Mean Fee paid in Native Coins (Daily)
# FeeMeanUSD        - Mean Fee paid in USD (Daily)
# FeeMedNtv         - Median Fee paid in Native Coins (Daily)
# FeeMedUSD         - Mean Fee paid in USD (Daily)
# FeeTotNtv         - Total Fees paid in Native Coins (Daily)
# FeeTotUSD         - Total Fees paid in Native Coins (Daily)
# IssContNtv        - Daily Issued Native Coins to Miners/Validators
# IssContPctAnn     - Annualised Inflation Rate
# IssContUSD        - Daily Issued USD to Miners/Validators
# IssTotNtvDaily    - Issued Native Coins to Miners/Validators (Daily)
# IssTotUSD         - Daily Issued USD Value to Miners/Validators (Daily)