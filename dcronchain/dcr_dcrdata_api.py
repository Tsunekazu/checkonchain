#Extract key ticket data from dcrdata

""" DATA IS EXTRACTED FROM DCRDATA.ORG IN TWO MODULES
1) dcr_difficulty()  ---> For both PoS and PoW. Rows by Ticket window
blk, window, time, ticket_count, ticket_price, missed, pow_diff

2) dcr_performance() ---> data by block height on actual blockchain performance 
  blk, time, circulation, ticket_pool, ticket_count, pow_hashrate, pow_work, pow_offset
"""

#Data Science
import pandas as pd
import numpy as np

#Project specific modules
import json
from tinydecred.pydecred.dcrdata import DcrdataClient

client = DcrdataClient("https://alpha.dcrdata.org/")

class Extract_dcrdata():

    def __init__(self):
        pass
    
    def dcr_difficulty(self):
        #Extract Ticket Price - WINDOW (~2600)
        tic_pce = pd.DataFrame(client.chart("ticket-price", bin="block"))
        tic_pce.columns = ['ticket_count','ticket_price','time','window']
        tic_pce['ticket_price']= tic_pce['ticket_price']/ 1e8 #Change from Atoms to DCR

        #Missed Votes - WINDOW (~2600)
        tic_miss = pd.DataFrame(client.chart("missed-votes", bin="block", axis="time"))
        tic_miss.columns = ['missed','offset','time','window']

        #Extract Mining Difficulty - WINDOW (~2600)
        pow_dif = pd.DataFrame(client.chart("pow-difficulty", bin="block", axis="time"))
        pow_dif.columns = ['pow_diff','time','window']

        #Combine into single dataset
        response=tic_pce.join(pow_dif['pow_diff'],how='outer')
        response=response.join(tic_miss['missed'],how='outer')

        #Add block height and rearrange
        response['blk'] = (response.index+1)*response['window']
        response=response[['blk','window','time','ticket_count','ticket_price','missed','pow_diff']]
        response.tail(5)

        return response

    def dcr_difficulty_step(self):
        response = Extract_dcrdata().dcr_performance()
        
        return response

    def dcr_performance(self):
        #Ticket Stake Participation
        tic_stake_part = pd.DataFrame(client.chart("stake-participation", bin="block", axis="time"))
        tic_stake_part.columns = ['axis','bin','circulation','ticket_pool','time']
        tic_stake_part['circulation']= tic_stake_part['circulation']/ 1e8
        tic_stake_part['participation'] = tic_stake_part['ticket_pool']/tic_stake_part['circulation']
        
        #Ticket Pool Value
        tic_pool = pd.DataFrame(client.chart("ticket-pool-size", bin="block", axis="time"))
        tic_pool.columns = ['axis','bin','ticket_count','time']

        #Mining Hashrate
        min_hash = pd.DataFrame(client.chart("hashrate", bin="block", axis="time"))
        min_hash.columns = ['axis','bin','pow_offset','pow_hashrate','time']

        #Total Work
        tot_work = pd.DataFrame(client.chart("chainwork", bin="block", axis="time"))
        tot_work.columns = ['axis','bin','time','pow_work']        

        #Combine into single dataset
        response=tic_stake_part.join(tic_pool['ticket_count'],how='outer')
        response=response.join(min_hash[['pow_hashrate','pow_offset']],how='outer')
        response=response.join(tot_work[['pow_work']],how='outer')
        response['blk'] = response.index
        response = response[['blk','time','circulation','ticket_pool','ticket_count','pow_hashrate','pow_work','pow_offset']]
        return response

#a = Extract_dcrdata().dcr_difficulty()
#a.head(5)
#b = Extract_dcrdata().dcr_performance()
#b.tail(5)
