#Produce Bitcoin Supply Schedule
#Data Science
import pandas as pd
import numpy as np
import math

"""
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
BITCOIN SUPPLY FUNCTION
btc_supply_schedule.btc_supply_function(end_blockheight)
Returns blk, TotSply, PoWSply, PoSSply, FundSply, Inflation, S2F
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
"""

class btc_supply_schedule:

    #Set constants for Bitcoin
    def __init__(self,blk_max):
        self.initial_sply = 0
        self.initial_W = 0
        self.initial_S = 0*self.initial_sply
        self.initial_F = 0*self.initial_sply
        self.initial_br = 50
        self.br_W = 1.0
        self.br_S = 0.0
        self.br_F = 0.0
        self.halving = 210000
        self.blk_max = blk_max
        self.blk_time = 10 #min
        self.sats = 1e8

    def btc_schedule(self,blk):
        response = int(math.floor(blk/self.halving))
        return response

    def btc_blk_rew(self,blk):
        if blk == 0:
            response = self.initial_sply+self.initial_br
        else:
            response = self.initial_br*(0.5)**self.btc_schedule(blk)
        return response

    def btc_supply_function(self):
        print('...Calculating Bitcoin Supply Curve up to block height ',self.blk_max,'...')
        response=np.zeros((self.blk_max,8))
        response[0,0]=int(0) #block height
        response[0,1]=self.btc_blk_rew(0) #Current Block Reward
        response[0,2]=self.initial_sply #Total Supply
        response[0,3]=self.initial_W #Total PoW Supply
        response[0,4]=self.initial_S #Total PoS Supply
        response[0,5]=self.initial_F #Total Treasury Supply
        response[0,6]=float('inf') #Inflation Rate = Infinity
        response[0,7]=1/1e8#response[0,6] #Stock-to-Flow Ratio - set near zero
        for i in range (1, self.blk_max):
            response[i,0] = int(i)
            response[i,1] = self.btc_blk_rew(i)
            response[i,2] = response[i-1,2]+response[i,1]
            response[i,3] = response[i-1,3]+response[i,1]*self.br_W
            response[i,4] = response[i-1,4]+response[i,1]*self.br_S
            response[i,5] = response[i-1,5]+response[i,1]*self.br_F
            response[i,6] = response[i,1]*(365*24*60/self.blk_time)/response[i,2]
            response[i,7] = 1/response[i,6]
    
        columns=['blk','blk_reward','Sply_ideal','PoWSply_ideal','PoSSply_ideal','FundSply_ideal','inflation_ideal','S2F_ideal']
        df = pd.DataFrame(data=response,columns=columns)
        return df
    
    def btc_halvings(self):
        print('...Calculating Bitcoin halvings...')
        data = np.zeros((34,8))
        for i in range(0,34):
            data[i,0] = int(self.halving*(i)) # start blk
            data[i,1] = float(self.btc_blk_rew(data[i,0])) #blk rew
            if i==0:#start_sply = prev_end + (blk_rew * start_blk)
                data[i,2] = data[i,0]*data[i,1] 
            else:
                data[i,2] = data[i-1,4]
            data[i,3] = self.halving*data[i,1] #btc_added = halving blocks * b_rew
            data[i,4] = data[i,2] +data[i,3] #end_sply = start sply + added
            if data[i,2]==0: # Calculate Inflation as proprtion of circ supply
                data[i,5] = float('Inf')
            else:
                data[i,5] = data[i,3]/data[i,2]
            data[i,6] = data[i,4]/21000000 # End_sply / 21M
            data[i,7] = 1/(data[i,5]/(self.halving*self.blk_time/60/24/365.25))

        columns=['blk','blk_reward','start_sply','sply_added','end_sply','sply_increase','end_pct_totsply','S2F']
        df = pd.DataFrame(data=data,columns=columns)
        return df


    def btc_halvings_stepped(self):
        data = np.zeros((34*2,9))
        cols = ['blk','blk_reward','start_sply','sply_added','end_sply','sply_increase','end_pct_totsply','S2F','y_arb']
        j=-1
        df = self.btc_halvings()
        for i in range(0,len(df.index),2):
            j = j + 1
            for k in range(0,8):
                data[i,k]   =  df.iloc[j,k]
                data[i+1,k] =  df.iloc[j,k]
            if (j % 2) == 0:
                data[i,8]   =  0
                data[i+1,8] =  1e20
            else:
                data[i,8]   =  1e20
                data[i+1,8] =  0   
        return pd.DataFrame(data=data,columns=cols)

#BTC = btc_supply_schedule(1200000).btc_supply_function()
#BTC_half = btc_supply_schedule(0).btc_halvings()
#BTC_step = btc_supply_schedule(0).btc_halvings_stepped()
