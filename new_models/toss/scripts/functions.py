import pandas as pd
import numpy as np

def horizontalCompensate(datafile, rows):
    df=pd.read_csv(datafile, delimiter=',', usecols = [0,1,28])
    df.columns = ['index', 'time', 'range']
    df2 = df.ix[rows].dropna() #index range pertaining to data of interest

    xa=df2['time'].values
    xi = xa[0] # when was the ball released?
    x_final = xa[-1] - xi # sets land time assuming drop time is zero
    x2 = xa - xi # sets release time to zero

    da=df2['range'].values*0.001
    di = da[0] # when was the ball released?
    d_final = da[-1] - di # sets land time assuming drop time is zero
    d2 = da - di # sets release time to zero
    df3 = df.ix[168:216].dropna()
    x3=df3['time'].values
    d3 = df3['range'].values*0.001
    dt = x3[-1] - x3[0]
    new_v = d2[-1] / dt
    new_x = new_v * dt
    newd = np.sqrt( d2**2 - new_x**2 )
    newRange = newd[~np.isnan(newd)] # compensated range

    x4 = df['time'].ix[169:214].values
    newRange_mod = df['range'].ix[169:214].values*0.001
    adj_newRange_mod = newRange_mod - newRange_mod[0] # adjusted to start at zero
    adj_x4_mod = x4 - 11.23917484 #adjusted to start at zero
    return


