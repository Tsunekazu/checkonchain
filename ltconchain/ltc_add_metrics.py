# Calculate a Suite of Bitcoin Specific Metrics
#Data Science
import pandas as pd
import numpy as np
import math
import datetime as date
today = date.datetime.now().strftime('%Y-%m-%d')

from checkonchain.general.coinmetrics_api import * #Coinmetrics.io
from checkonchain.general.regression_analysis import *
from checkonchain.ltconchain.ltc_schedule import *

class ltc_add_metrics():

    def ltc_coin(self):
        df = Coinmetrics_api('ltc',"2011-10-07",today).convert_to_pd()
        df['notes'] = str('')
        return df

    def ltc_sply(self,to_blk):
        df = ltc_supply_schedule(to_blk).ltc_supply_function()

        ltc_s2f_model = regression_analysis().regression_constants()['ltc_s2f']
        df['CapS2Fmodel'] = np.exp(float(ltc_s2f_model['coefficient'])*np.log(df['S2F_ideal'])+float(ltc_s2f_model['intercept']))
        df['PriceS2Fmodel'] = df['CapS2Fmodel']/df['Sply_ideal']
        #Calc S2F Model - Bitcoins Plan B Model
        planb_s2f_model = regression_analysis().regression_constants()['planb']
        df['CapPlanBmodel'] = np.exp(float(planb_s2f_model['coefficient'])*np.log(df['S2F_ideal'])+float(planb_s2f_model['intercept']))
        df['PricePlanBmodel'] = df['CapPlanBmodel']/df['Sply_ideal']
        return df

    def ltc_real(self):
        print('...compiling Litecoin specific metrics (coinmetrics + supply curve)...')
        _coin = self.ltc_coin()
        _blk_max = int(_coin['blk'][_coin.index[-1]])
        _sply = self.ltc_sply(_blk_max)

        # Drop uncessecary columns, Vlookup nearest on blk
        df = pd.merge_asof(_coin,_sply[['blk','blk_reward','Sply_ideal', 'PoWSply_ideal','inflation_ideal','S2F_ideal']],on='blk')
        return df

    def ltc_pricing_models(self):
        print('...Calculating Litecoin pricing models...')
        _real = self.ltc_real()
        df = _real
        #Calc S2F Model - Specific to Litecoin
        btc_s2f_model = regression_analysis().ln_regression(df,'S2F','CapMrktCurUSD','date')['model_params']
        df['CapS2Fmodel'] = np.exp(float(btc_s2f_model['coefficient'])*np.log(df['S2F'])+float(btc_s2f_model['intercept']))
        df['PriceS2Fmodel'] = df['CapS2Fmodel']/df['SplyCur']
        #Calc S2F Model - Bitcoins Plan B Model
        planb_s2f_model = regression_analysis().regression_constants()['planb']
        df['CapPlanBmodel'] = np.exp(float(planb_s2f_model['coefficient'])*np.log(df['S2F'])+float(planb_s2f_model['intercept']))
        df['PricePlanBmodel'] = df['CapPlanBmodel']/df['SplyCur']
        return df

 