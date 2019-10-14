# Import Coinmetrics API

#Project specific Modules
from checkonchain.general.__init__ import *
import coinmetrics

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
       
    def __init__(self,asset,begin_timestamp,end_timestamp):
        print('...Fetching Coinmetrics API for '+asset+'...')
        # List all available metrics for BTC.
        self.asset = asset
        self.begin_timestamp=begin_timestamp
        self.end_timestamp=end_timestamp
        self.topcapconst = 35

    def collect_data(self):
        available_data_types = cm.get_available_data_types_for_asset(self.asset)
        metric_list = str((','.join(available_data_types))) #setup complete metric list
        #print(metric_list)
        asset_data = cm.get_asset_data_for_time_range(self.asset, metric_list, self.begin_timestamp, self.end_timestamp)
        return asset_data
    
    def convert_to_pd(self):
        asset_data = Coinmetrics_api.collect_data(self)
        df = coinmetrics.cm_to_pandas(asset_data)
        
        #Extract Data as column for ease of application
        df.index.name = 'date'
        df.reset_index(inplace=True)
        df['date'] = pd.to_datetime(df['date'])
        
        
        #Calc - block height
        df['blk']=df['BlkCnt'].cumsum()
        
        #Realised Price (Only if present, excludes XMR and ZEC et al.)
        if 'CapRealUSD' in df:
            df['PriceRealised'] = df['CapRealUSD']/df['SplyCur']
        
        #Calc - approx btc block height (Noting BTC blocks were mined from 9/Jan/09)
        df['btc_blk_est'] = (df['date'] - pd.to_datetime(np.datetime64('2009-01-09'),utc=True))
        df['btc_blk_est'] = df['btc_blk_est']/np.timedelta64(1,'D') #convert from timedelta to Days (float)
        df['btc_blk_est'] = df['btc_blk_est']*(24*6) #Note - corrected for neg values in loop below

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

        return df
    
    
    def add_metrics(self):
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

        #Calc S2F Model
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

"""#############################  
    Coinmetrics Community API
BTC = Coinmetrics_api('btc',"2009-01-03","2019-10-07").convert_to_pd()  
################################"""

"""Example Calculations"""
#BTC = Coinmetrics_api('btc',"2009-01-03","2019-10-07").convert_to_pd()
#LTC = Coinmetrics_api('ltc',"2011-10-07",today).convert_to_pd()
#BCH = Coinmetrics_api('bch',"2017-08-01",today).convert_to_pd()
#DASH = Coinmetrics_api('dash',"2014-01-19",today).convert_to_pd()
#DCR = Coinmetrics_api('dcr',"2016-02-08",today).convert_to_pd()
#XMR = Coinmetrics_api('xmr',"2014-04-18",today).convert_to_pd()
#ZEC = Coinmetrics_api('zec',"2016-10-28",today).convert_to_pd()
#ETH = Coinmetrics_api('eth',"2015-07-30",today).convert_to_pd()

"""Time Metrics"""
# date               -datetime64[ns, UTC]
# blk                -ADDED METRIC - block height (Sum of BlkCnt)
# btc_blk_est        -ADDED METRIC - Estimated Bitcoin block-height (Assumes 10min block-times)

"""Blockchain Metrics"""
# AdrActCnt          -Active Addresses
# BlkCnt             -Block Count (Daily)
# BlkSizeByte        -Block Size (Bytes)
# BlkSizeMeanByte    -Block Size Average (Bytes)
# SplyCur            -Current Coin Supply
# inf_pct_ann        -ADDED METRIC - Inflation % annual
# S2F                -ADDED METRIC - Stock-to-Flow Ratio

"""Network Valuation Models"""
# CapMrktCurUSD      - Market Cap
# CapRealUSD         - Realised Cap

"""Network Pricing Models"""
# PriceUSD           - Coin Price USD
# PriceRealised      - Realised Price USD

"""Network Valuation Oscillators"""
# CapMVRVCur         - MVRV Ratio - Market Cap / Realised Cap
# NVTAdj             - NVT Ratio (Adjusted Volume)
# NVTAdj90           - NVT Ratio 90D MA (Adjusted Volume)

"""Transaction Flow Metrics"""
# TxCnt              -Count of Transactions
# TxTfrCnt           -Count of Transaction Transfers (Cleaned Data)
# TxTfrValAdjNtv     -Native Units Transferred (Adjusted Data)
# TxTfrValAdjUSD     -USD Value Transferred (Adjusted Data)
# TxTfrValNtv        -Total Native Units Value Transferred
# TxTfrValUSD        -Total USD Value Transferred
# TxTfrValMeanNtv    -Mean Native Units Transferred
# TxTfrValMeanUSD    -Mean USD Value Transferred
# TxTfrValMedNtv     -Median Native Units Transferred
# TxTfrValMedUSD     -Median USD Value Transferred

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
# DailyIssuedNtv    - ADDED METRIC - Daily Issued Native Units (Sply_n - Sply_n-1)
# DailyIssuedUSD    - ADDED METRIC - Daily Issued USD Value (Sply_n - Sply_n-1)

"""Market Specific Metrics"""
# ROI1yr
# ROI30d
# VtyDayRet180d
# VtyDayRet30d
# VtyDayRet60d