#Produce Decred Supply Schedule
from checkonchain.dcronchain import *
import pandas as pd
import numpy as np
import math

"""
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
DECRED SUPPLY FUNCTION
dcr_supply_schedule.dcr_supply_function(end_blockheight)
Returns blk, TotSply, PoWSply, PoSSply, FundSply, Inflation, S2F
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
"""

class dcr_supply_schedule:

    #Set constants for DECRED
    def __init__(self,blk_max):
        self.initial_sply = 1.68e6
        self.initial_W = 0
        self.initial_S = 0.5*self.initial_sply
        self.initial_F = 0.5*self.initial_sply
        self.initial_br = 31.19582664
        self.br_W = 0.6
        self.br_S = 0.3
        self.br_F = 0.1
        self.halving = 6144
        self.blk_min = 1
        self.blk_max = blk_max
        self.blk_time = 5 #min
        self.atoms = 1e8

    def dcr_schedule(self,blk):
        response = int(math.floor(blk/self.halving))
        return response

    def dcr_blk_rew(self,blk):
        if blk == 0:
            response = self.initial_sply
        else:
            response = self.initial_br*(100/101)**self.dcr_schedule(blk)
        return response

    def dcr_supply_function(self):
        response=np.zeros((self.blk_max,8))
        response[0,0]=int(0) #block height
        response[0,1]=self.dcr_blk_rew(0) #Current Block Reward
        response[0,2]=self.initial_sply #Total Supply
        response[0,3]=self.initial_W #Total PoW Supply
        response[0,4]=self.initial_S #Total PoS Supply
        response[0,5]=self.initial_F #Total Treasury Supply
        response[0,6]=self.dcr_blk_rew(0)*(365*24*60/self.blk_time)/self.initial_sply #Inflation Rate
        response[0,7]=1/response[0,6] #Stock-to-Flow Ratio 
        for i in range (1, self.blk_max):
            response[i,0] = int(i)
            response[i,1] = self.dcr_blk_rew(i)
            response[i,2] = response[i-1,2]+self.dcr_blk_rew(i)
            response[i,3] = response[i-1,3]+self.dcr_blk_rew(i)*self.br_W
            response[i,4] = response[i-1,4]+self.dcr_blk_rew(i)*self.br_S
            response[i,5] = response[i-1,5]+self.dcr_blk_rew(i)*self.br_F
            response[i,6] = self.dcr_blk_rew(i)*(365*24*60/self.blk_time)/response[i,2]
            response[i,7] = 1/response[i,6]
    
        columns=['blk','blk_reward','SplyCur','PoWSplyCur','PoSSplyCur','FundSplyCur','inflation','S2F']
        df = pd.DataFrame(data=response,columns=columns)
        return df

DCR=dcr_supply_schedule(38000).dcr_supply_function()