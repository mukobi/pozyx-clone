import pandas as pd
import matplotlib as mpl
#mpl.use('Qt5Agg')
import matplotlib.pyplot as plt
import numpy as np
import scipy.optimize as opt
from math import isclose
from scipy.optimize import curve_fit
from scipy import stats
from physProps import *
params = {'mathtext.default': 'regular'}
plt.rcParams.update(params)
#####################################################################

datafile = ['red_toss2.csv', 'yellow_toss2.csv', 'blue_toss2.csv', 'orange_toss.csv']
ball = [redBall, yellowBall, blueBall, orangeBall]
title = ['red ball', 'yellow ball', 'blue ball', 'orange ball']
figname = ['redBall', 'yellowBall', 'blueBall', 'orangeBall']
rows = [slice(417,454,1), slice(359,396,1), slice(172,209,1), slice(2319,2347,1)]

#slice(549,584,1),
for ii in range(4):
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

    da=df2['range'].values*0.001
    di = da[0] # when was the ball released?
    d_final = da[-1] - di # sets land time assuming drop time is zero
    d2 = da - di # sets release time to zero

    t0_new = x2[0]
    xdata = np.array([x2,x2])


    dtGlobal = 0.0000001
    dtGlobal = 0.001



    xx3 = np.linspace(x2[0],x2[-1],100)

    def func3(t, vel, drag):
        dt = dtGlobal

        x=0                 # initial position
        t_curr = t0_new     # inital time
        xlist = [x]
        a = g - ( drag * ( ( rho*(vel)**2 ) /2) * ball[ii].xSectionArea /ball[ii].mass )

    # fix for scalar input
        if not hasattr(t, '__len__') :
            tlist = [0,t]       # make a list out of a single target t value
        else :
            tlist = t

        i = 1           # list index, initialized to 1 since i=0 is initial time, which we already have
    #print('t_curr:',t_curr , 'i:',i ) # show where we are at start
    #while t_curr <= tlist[-1] :
        while not isclose(t_curr, tlist[-1], abs_tol=dt) :
            t_curr += dt
            x = x + vel * dt + (1/2) * a * dt**2
            vel = vel + a * dt

            if vel < 0:
                dragForce = -(drag*((rho*(vel)**2)/2)*ball[ii].xSectionArea)
            else:
                dragForce = drag*((rho*vel**2)/2)*ball[ii].xSectionArea
            a = (Fg-dragForce)/ball[ii].mass

        #xDict[t_curr] = x
            t_next = tlist[i]
        #print('t_curr:', t_curr, 'x:', x, 't_next:', t_next, 'i:',i) # debugging
            if isclose(t_curr, t_next,abs_tol=dt) :
                xlist.append(x)
                i+=1        # go to next target time in list

        return np.array(xlist)


    popt, pcov = curve_fit(func3, x2, d2, bounds=([0,-2], [10,2]))
    print(popt)
    plt.figure()
    x_filt = d2[d2 >= 0]
    plt.plot(x2,d2,'o', label = 'experimental data')
    plt.plot(xx3, func3(xx3, *popt),
            label='fit: initial velocity=%5.3f, drag coefficient=%5.3f' % tuple(popt))
    plt.title("{}".format(figname[ii]))
    plt.xlabel("Time (s)")
    plt.ylabel("Position (m)")
    plt.legend()
    model_data = func3(x2, *popt)
    slope, intercept, r_value, p_value, std_err = stats.linregress(model_data, d2)
    print("r-squared:",r_value**2)
    plt.savefig(figname[ii], bbox_inches='tight')

plt.show()
