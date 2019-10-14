#Modules for Linear Regression Analysis
from checkonchain.general.__init__ import *
from sklearn.linear_model import LinearRegression


class regression_analysis():

    def __init__(self):
        pass

    def regression_constants(self):
        planb = pd.DataFrame(data={
            'Details':['BTC_PlanBModel'],
            'rsq':[0.947328],
            'intercept':[14.6227],
            'coefficient':[3.31954]
            })
        btc_s2f = pd.DataFrame(data={
            'Details':['BTC_S2F_MrktCap_20191013'],
            'rsq':[0.901453],
            'intercept':[13.837495],
            'coefficient':[3.496456]
            })
        btc_diff = pd.DataFrame(data={
            'Details':['BTC_DiffMean_MrktCap_20191013'],
            'rsq':[0.934309],
            'intercept':[10.697469],
            'coefficient':[0.498638]
            })

        dcr_s2f = pd.DataFrame(data={
            'Details':['DCR_S2F_MrktCap_20191014'],
            'rsq':[0.675775],
            'intercept':[15.911287],
            'coefficient':[2.42636]
            })
        dcr_diff = pd.DataFrame(data={
            'Details':['DCR_DiffMean_MrktCap_20191013'],
            'rsq':[0.50967],
            'intercept':[12.310519],
            'coefficient':[0.322534]
            })

        ltc_s2f = pd.DataFrame(data={
            'Details':['LTC_S2F_MrktCap_20191013'],
            'rsq':[0.461942],
            'intercept':[16.95225],
            'coefficient':[1.694044]
            })
        ltc_diff = pd.DataFrame(data={
            'Details':['LTC_DiffMean_MrktCap_20191013'],
            'rsq':[0.745483],
            'intercept':[14.193707],
            'coefficient':[0.494897]
            })
        return {
            'planb':planb,
            'btc_s2f':btc_s2f,
            'btc_diff':btc_diff,
            'dcr_s2f':dcr_s2f,
            'dcr_diff':dcr_diff,
            'ltc_s2f':ltc_s2f,
            'ltc_diff':ltc_diff,            
            }
    
    def ln_regression(self,dataframe,x_metric,y_metric,time_metric):
        self.dataframe = dataframe
        self.x_metric = x_metric
        self.y_metric = y_metric
        self.time_metric = time_metric #arbitrary for charting
        print('...Calculating ln-ln Linear Regression for '+self.x_metric+'-'+self.y_metric+'...')

        #Subset of dataset, drop na values
        df = self.dataframe[[self.time_metric,self.x_metric,self.y_metric]].dropna(axis=0)
        df = df.reset_index(drop=True)

        #Create arrays for x and y in regression
        x=np.array(np.log(df[self.x_metric])).reshape((-1,1))
        y=np.array(np.log(df[self.y_metric]))
        regression_model = LinearRegression().fit(x, y)
        
        #Calculate r_sq, intercept and coefficient of model
        model_params = pd.DataFrame(
            index=['regression_model'],
            data={
                'rsq':[regression_model.score(x,y)], 
                'intercept': [regression_model.intercept_],
                'coefficient':[float(regression_model.coef_)]
                })
        print(model_params)
        return {
            'model': regression_model, 
            'model_params':model_params
            }
        
    def rsq_progression(self,dataframe,x_metric,y_metric,time_metric):
        self.dataframe = dataframe
        self.x_metric = x_metric
        self.y_metric = y_metric
        self.time_metric = time_metric #arbitrary for charting
        print('...Calculating R-Square Progression for '+self.x_metric+'-'+self.y_metric+'...')
        #Calculate progression of rsq over time
        df = self.dataframe[[self.time_metric,self.x_metric,self.y_metric]].dropna(axis=0)
        df = df.reset_index(drop=True)
        df['rsq_'+self.x_metric]=0

        for i in range(0,len(df.index)):
            #Calculate S2F RSQ development
            df.loc[i,['rsq_'+self.x_metric]]=LinearRegression().fit(
                np.log(df.loc[:i,[self.x_metric]]),
                np.log(df.loc[:i,[self.y_metric]])
                ).score(
                    np.log(df.loc[:i,[self.x_metric]]),
                    np.log(df.loc[:i,[self.y_metric]])
                    )
        print('RSQ Complete')
        return {
            'rsq_develop':df
            }


#from checkonchain.general.coinmetrics_api import *
#BTC_coin = Coinmetrics_api('btc',"2009-01-03",today).convert_to_pd()
#BTC_regr = regression_analysis().ln_regression(BTC_coin,'DiffMean','CapMrktCurUSD','date')
#BTC_rsq = regression_analysis().rsq_progression(BTC_coin,'DiffMean','CapMrktCurUSD','date')
#BTC_rsq
#
#DCR_coin = Coinmetrics_api('dcr',"2016-02-08",today).convert_to_pd()
#DCR_regr = regression_analysis().ln_regression(DCR_coin,'DiffMean','CapMrktCurUSD','date')
#DCR_rsq = regression_analysis().rsq_progression(DCR_coin,'DiffMean','CapMrktCurUSD','date')
#DCR_rsq
#
#LTC_coin = Coinmetrics_api('ltc',"2011-10-07",today).convert_to_pd()
#LTC_regr = regression_analysis().ln_regression(LTC_coin,'S2F','CapMrktCurUSD','date')
#LTC_rsq = regression_analysis().rsq_progression(LTC_coin,'DiffMean','CapMrktCurUSD','date')
#LTC_rsq

