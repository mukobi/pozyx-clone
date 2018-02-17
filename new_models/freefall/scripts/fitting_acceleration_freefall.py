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

params2 = {'legend.fontsize': 9,
          'legend.handlelength': 1}
plt.rcParams.update(params)
plt.rcParams.update(params2)
#####################################################################

datafile = ['red_122617.csv', 'yellow_122617.csv', 'blueball2_122617.csv', 'orange_drop.csv', 'rocket_122617.csv']

ball = [redBall, yellowBall, blueBall, orangeBall, rocket]
title = ['red ball', 'yellow ball', 'blue ball', 'orange ball', 'rocket']
figname = ['redBall.pdf', 'yellowBall.pdf', 'blueBall.pdf', 'orangeBall.pdf', 'rocket.pdf']
rows = [slice(363,397,1), slice(376,407,1), slice(416,454,1), slice(2485,2540,1), slice(557,588,1)]

for ii in range(5):
    g = -9.81
    Fg = g * ball[ii].mass
    rho = 1.225

#    df=pd.read_csv(datafile[ii], delimiter=',', usecols = [0,1,28])
    datafileThis = datafile[ii]
    print( "Working on datafile: ", datafileThis)
    df=pd.read_csv(datafileThis, delimiter=',', usecols = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28])

    df.columns = ['index', 'time', 'difference','hz','aveHz','pressure','xAcc','yAcc','zAcc','xMag','yMag','zMag','xAngVel','yAngVel','zAngVel','yaw','roll','pitch','xQuat','yQuat','zQuat','wQuat','xLinAcc','yLinAcc','zLinAcc','xGrav','yGrav','zGrav','range']
    #df.columns = ['index', 'time', 'range']
    #print( df['time'] )

    df2 = df.ix[rows[ii]].dropna() #index range pertaining to data of interest

    unitConv = 1./100.
    xLinAcc = df2.xLinAcc.values *unitConv
    yLinAcc = df2.yLinAcc.values *unitConv
    zLinAcc = df2.zLinAcc.values *unitConv
    linAcc = np.sqrt(xLinAcc**2 + yLinAcc**2 + zLinAcc**2)*-1.
    df2['linAcc'] = linAcc

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
####################################################################################################
    '''
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
    '''
#######################################################################################################
    '''
    if datafile[ii] == 'rocket_launch.csv':
        xx3 = np.linspace(adj_time[0],adj_time[-1],100)
    '''
    xx3 = np.linspace(x2[0],x2[-1],100)

    def func4(t, vel, drag):
        dt = dtGlobal

        x=0                 # initial position
        t_curr = t0_new     # inital time

        a = g - ( drag * ( ( rho*(vel)**2 ) /2) * ball[ii].xSectionArea /ball[ii].mass )

        alist = [a]
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
            #x = x + vel * dt + (1/2) * a * dt**2
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
                alist.append(a)
                i+=1        # go to next target time in list

        return np.array(alist)
    '''
    if datafile[ii] == 'rocket_launch.csv':
        popt, pcov = curve_fit(func3, adj_time, newRange, bounds=([0,0], [20,2]))
        plt.figure()
        plt.plot(adj_time,newRange,'o')
        plt.plot(xx3, func3(xx3, *popt),
            label='fit: initial velocity=%5.3f, drag coefficient=%5.3f' % tuple(popt))
    '''

    #else:
    popt, pcov = curve_fit(func4, x2, linAcc, bounds=([-5,0], [5,2]))
    plt.figure()
    plt.plot(x2,linAcc,'o', label='vSum')
    plt.plot(xx3, func4(xx3, *popt),
        label='fit: vi=%5.3f, Cd=%5.3f' % tuple(popt))
    plt.plot(x2, xLinAcc, 'o', label='xLinAcc')
    plt.plot(x2, yLinAcc, 'o', label='yLinAcc')
    plt.plot(x2, zLinAcc, 'o', label='zLinAcc')
    plt.legend()
#    if datafile[ii] == 'rocket_launch.csv':
#        plt.plot(x2,newRange,'o')
#    else:
#        plt.plot(x2,d2,'o', label = 'experimental data')

#    plt.plot(xx3, func3(xx3, *popt),
#            label='fit: initial velocity=%5.3f, drag coefficient=%5.3f' % tuple(popt))

    plt.title("{} (velocity bounds [-5,5]) free fall".format(title[ii]))
    plt.xlabel("Time (s)")
    plt.ylabel("Acceleration")
    plt.legend()
    model_data = func4(x2, *popt)
    slope, intercept, r_value, p_value, std_err = stats.linregress(model_data, d2)
    print("r-squared:",r_value**2)
    plt.savefig(figname[ii], bbox_inches='tight')

plt.show()
