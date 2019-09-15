# checkonchain
Python Modules for studying the on-chain behavior of Bitcoin and Decred

## Purpose of repo
This repo is a collection of analysis code, tools and published articles for analysing the blockchains of Bitcoin and Decred. 

Based on the on-chain signiatures of BTC and DCR, there is a significant heartbeat for both of these chains. These blockchains also represent the strongest store of value candidates based on my fundamental research and opinions to date and thus deserve further research attention.

This repository includes all data and code used to undertake these analyses. 

*Note - I am not a developer, code unlikely to be perfect. Suggestions and ideas welcomed.*

## Goals for these studies
1. Establish additional rigor for my personal fundamental investment thesis for Bitcoin and Decred
2. Analyse the scarcity of both Bitcoin and Decred with inspiration from Plan B stock to flow ratio analysis (@100TrillionUSD)
3. Analyse the behaviour of DCR tickets as a mechanism for scarcity
4. Assess the balance between supply issuance, scarcity, ticket behaviour and transaction flows
5. Establish a set of charting packages with which others can replicate and follow the analysis
6. Develop an online charting package similar to woobull.com to scratch my own itch encomapsing for both Decred and Bitcion.


## Repo Structure
This repo is my first and thus structure will develop over time. All code will be Python unless otherwise noted

```
checkonchain
│   README.md
│   LICENCE    
│
└───general (general tools, calling APIs, coin comparisons etc)
│   │   __init.py__
│   │   coinmetrics.py (pulls community API data from coinmetrics) [50%]
|
└───btconchain
│   │   __init.py__
│   │   file012.txt
│   
└───dcronchain
    │   file021.txt
    │   file022.txt
```







- **Monetary Premiums** - Article and data for [medium article located here.](https://medium.com/@_Checkmatey_/monetary-premiums-can-altcoins-compete-with-bitcoin-54c97a92c6d4)
- **Coinmetrics** - Contains all scripts for extracting data from Coinmetrics
- **Decred_Analysis** - Modules for analysing Decred specific metrics
- **Bitcoin_Analysis** - Modules for analysing Bitcoin specific metrics

## Dependencies
1. [Coinmetrics python toolkit by h4110w33n.](https://github.com/h4110w33n/coinmetrics)
2. [TinyDecred by buck54321](https://github.com/decred/tinydecred)



## Roadmap
**Phase 1 - Write supply curve scripts:**
- Bitcoin (90%)
- Decred (90%)

**Phase 2 - Establish API Calls and Modules for:**
- Coinmetrics V2 (50%)
- dcrdata (via TinyDecred) (50%)
- CoinAPI (0%)
- Glassnode (0%)

**Phase 3 - Compile datasets from API calls into specific analysis**
- Decred staking Distribution - PoW, PoS and Ticket pool
- Transaction volumes and value vs Ticket behaviour
- PoW and PoS difficulty comparisons as driver for value
- Unforgeable costliness (Stock-to-flow, PoW Mining costs, PoS Capital costs, Treasury work cost)
- Realised Cap, Market Cap, Days destroyed


## Donations
BTC - 34cw55q8e71613VMxepGgFXqLcpU52CZig
DCR - DsmQRL9ZPzcVsUda6vN1aSmmCQPXdm7HwVk