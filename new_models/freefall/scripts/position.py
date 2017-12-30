import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import scipy.optimize as opt
from scipy.optimize import curve_fit
from math import pi
from physProps import redBall, yellowBall, blueBall, orangeBall, rocket

params = {'mathtext.default': 'regular'}
plt.rcParams.update(params)
#####################################################################
datafile = ['red_drop.csv', 'yellow_drop.csv', 'blue_drop.csv', 'orange_drop.csv', 'rocket_drop.csv']
ball = [redBall, yellowBall, blueBall, orangeBall, rocket]
title = ['red ball', 'yellow ball', 'blue ball', 'orange ball', 'rocket']
figname = ['redBall.pdf', 'yellowBall.pdf', 'blueBall.pdf', 'orangeBall.pdf', 'rocket.pdf'
]
rows = [slice(185,220,1), slice(159,192,1), slice(382,415,1), slice(2483,2540,1), slice(437,469,1)]

for ii in range(5):
    g = -9.81
    Fg = g * ball[ii].mass
    rho = 1.225

    df=pd.read_csv(datafile[ii], delimiter=',', usecols = [0,1,28])

    df.columns = ['index', 'time', 'range']


    df2 = df.ix[rows[ii]].dropna() #index range pertaining to data of interest

    xa=df2['time'].values
    xi = xa[0] # when was the ball released?
    x_final = xa[-1] - xi # sets land time assuming drop time is zero
    x2 = xa - xi # sets release time to zero

    da=df2['range'].values*-0.001
    di = da[0] # when was the ball released?
    d_final = da[-1] - di # sets land time assuming drop time is zero
    d2 = da - di # sets release time to zero
    ######################################################################################
    if datafile[ii] == 'rocket_launch.csv':
#        horizontalCompensate('rocket_launch.csv', slice(168,216,))

        df3 = df.ix[168:216].dropna() # for newRange calculations
        x3=df3['time'].values
        raw_d3=df3['range'].values*0.001
        d3 = raw_d3 - raw_d3[0]

        dt = x3[-1] - x3[0]   # rocket's time in the air
        s = d3[-1] - d3[0]    # final distance from anchor - initial distance from anchor
        new_v = s / dt          # for discounting horizontal motion
        new_x = new_v * dt      # for discounting horizontal motion

        newd = np.sqrt(d2**2 - new_x**2) # total range discounting horizontal motion
        plain_newRange = newd[~np.isnan(newd)]
        newRange = plain_newRange - plain_newRange[0]

#        new_time = df['time'].ix[169:214].values
        new_time = df2['time'].ix[167:216].values
#        newRange_mod = df['range'].ix[169:214].values*0.001

#        adj_newRange_mod = newRange_mod  - newRange_mod[0]

        adj_time = new_time - new_time[0]
#        import pdb; pdb.set_trace()
    else:
        pass

    ################################### create the models ################################
    N = 100 # allows you to create each model out of 100 points
    if datafile [ii] == 'rocket_launch.csv':
        plt.figure()
        plt.plot(adj_time, newRange, 'o')
        def func(x,a,b,c):
            return a*(x**2) + b*x + c
        pfit, success = opt.curve_fit(func,adj_time,newRange)
        xx = np.linspace(adj_time[0],adj_time[-1],100)
        plt.plot(xx,func(xx,*pfit),'--', alpha=.8)
        gravity = 'a = {} m/s$^2$'.format(np.around(pfit[0]*-2, 3))
        print(gravity)
        plt.figtext(0.445,0.20, gravity, style='italic')
        plt.tight_layout()
    else:
        plt.figure()
        plt.plot(x2, d2, 'o')
        def func(x,a,b,c):
            return a*(x**2) + b*x + c
        pfit, success = opt.curve_fit(func,x2,d2)
        xx = np.linspace(x2[0],x2[-1],100)
        plt.plot(xx,func(xx,*pfit),'--', alpha=.8)
        print(pfit)
        gravity = 'a = {} m/s$^2$'.format(np.around(pfit[0]*-2, 3))
        print(gravity)
        plt.figtext(0.445,0.20, gravity, style='italic')
        plt.tight_layout()



    plt.xlabel("Time (s)")
    plt.ylabel("Position (s)")
    plt.title("{} Position".format(title[ii]))
    plt.legend()
    plt.savefig(figname[ii], dpi=800, bbox_inches='tight')

#import pdb; pdb.set_trace()


plt.show()
        #plt.savefig("modelP_orange_freefall.pdf", bbox_inches='tight')
