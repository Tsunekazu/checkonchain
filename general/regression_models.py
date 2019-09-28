def regression_analysis(self):
    df = Coinmetrics_df.add_metrics(self)
    df['CapDiffRegression'] = 10**(0.4981*np.log10(df['DiffMean'])+4.6509)
    df['PriceDiffRegression'] =df['CapDiffRegression']/df['SplyCur']
    df['CapS2Fmodel'] = np.exp(3.31954*np.log(df['S2F'])+14.6227)
    df['PriceS2Fmodel'] = df['CapS2Fmodel']/df['SplyCur']