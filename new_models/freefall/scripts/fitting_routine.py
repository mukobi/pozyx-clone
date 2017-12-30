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

# old: datafile = ['red_drop.csv', 'yellow_drop.csv', 'blue_drop.csv', 'orange_drop.csv', 'rocket_drop.csv']
datafile = ['red_122617.csv', 'yellow_122617.csv', 'blueball2_122617.csv', 'orange_drop.csv', 'rocket_122617.csv']

ball = [redBall, yellowBall, blueBall, orangeBall, rocket]
title = ['red ball', 'yellow ball', 'blue ball', 'orange ball', 'rocket']
figname = ['redBall', 'yellowBall', 'blueBall', 'orangeBall', 'rocket']
rows = [slice(361,399,1), slice(375,420,1), slice(415,456,1), slice(2483,2540,1), slice(554,589,1)]

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

    t0_new = x2[0]
    xdata = np.array([x2,x2])


    dtGlobal = 0.0000001
    dtGlobal = 0.001

    unitConv = 1000 # convert model units from meters to mm

    xx3 = np.linspace(x2[0],x2[-1],100)

    def func3(t, vel, drag):
        dt = dtGlobal
        vel = vel
  #  testint = t/dt
  #  import pdb; pdb.set_trace()
    #print("t is:", t)
    #xDict = {t0:x}
        x=0                 # initial position
        t_curr = t0_new     # inital time
        xlist = [x]
 #   rho = 1.225 # density of air at sea level at 20 degrees C
 #   m = 0.225 # mass of the object in kg
 #   g = -10
 #   Fg = m*g
        a=g
 #   diameter = 0.07083 # cross sectional area
 #   radius = 1/2 * diameter
 #   A = pi*radius**2 # cross sectional area in meters

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


    popt, pcov = curve_fit(func3, x2, d2, bounds=([-5,0], [10,1]))
    print(popt)
    plt.figure()
    x_filt = d2[d2 >= 0]
    plt.plot(x2,d2,'o', label = 'experimental data')
    plt.plot(xx3, func3(xx3, *popt),
            label='fit: initial velocity=%5.3f, drag coefficient=%5.3f' % tuple(popt))
    plt.title("{} forced".format(figname[ii]))
    plt.xlabel("Time (s)")
    plt.ylabel("Position (m)")
    plt.legend()
    model_data = func3(x2, *popt)
    slope, intercept, r_value, p_value, std_err = stats.linregress(model_data, d2)
    print("r-squared:",r_value**2)
    plt.savefig(figname[ii], bbox_inches='tight')

plt.show()
