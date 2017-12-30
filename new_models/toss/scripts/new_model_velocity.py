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
datafile = ['red_toss2.csv', 'yellow_toss2.csv', 'blue_toss2.csv', 'orange_toss.csv', 'rocket_launch.csv']
ball = [redBall, yellowBall, blueBall, orangeBall, rocket]
title = ['red ball', 'yellow ball', 'blue ball', 'orange ball', 'rocket']
figname = ['redBall', 'yellowBall', 'blueBall', 'orangeBall', 'rocket']
rows = [slice(417,454,1), slice(359,396,1), slice(172,209,1), slice(2319,2347,1), slice(166,216,1)]
vi = [7.440, 6.824, 6.642, 7.545, 17.788]

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

    da=df2['range'].values*0.001
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
        model_times = np.linspace(adj_time[0], adj_time[-1], 100)
    else:
        model_times = np.linspace(x2[0], x2[-1], 100)   # create array of 100 times within experimental timeframe for the modeled positions

    x_mod = np.zeros(shape=(N))   # create empty array with space for 100 elements
    v_mod = np.zeros(shape=(N))
    a_mod = np.zeros(shape=(N))
    dragForce = np.zeros(shape=(N))
    dt = ( x2[-1]-x2[0] ) / N
    print(datafile)
    plt.figure()
    
    #if datafile[ii] == 'rocket_launch.csv':
     #   plt.ylim(ymin=-1)
      #  plt.ylim(ymax=17.5)
       # plt.plot(adj_x7_mod,adj_newRange_mod,'o')
    #else:
     #   plt.plot(x2, d2, 'o')
#    c_vect=np.array([0])
    c_vect = np.array([0,0.034,0.08])
#    c_vect = np.array([0,0.2,0.4,0.6,0.8,1])
    for c in range(3) :
        x_mod[0] = 0    # initial position of zero
        v_mod[0] = vi[ii]    # initial velocity of zero
        dragForce[0] = ball[ii].xSectionArea * 0.5 * c_vect[c] * rho * v_mod[0]**2   # initial drag force
        a_mod[0] = ( Fg-dragForce[0] ) / ball[ii].mass  # initial acceleration based on initial drag force
        n=0
        print(c_vect[c])
        for n in range(0,N-1):
            x_mod[n+1] = x_mod[n]  + v_mod[n] * dt  + (1/2) * (a_mod[n]) * dt**2 # simply y=x + v*t + (1/2)*a*t^2
            v_mod[n+1] = v_mod[n] + a_mod[n] * dt # updated velocity is v + a*t

            if v_mod[n] < 0 :
                dragForce[n+1] = -( c_vect[c]*( (rho*v_mod[n]**2) /2 ) * ball[ii].xSectionArea ) # if/else may not be necessary

            else:
                dragForce[n+1] = c_vect[c]*( (rho*v_mod[n]**2) /2 ) * ball[ii].xSectionArea

            a_mod[n+1] = ( Fg-dragForce[n+1] ) /ball[ii].mass  # update acceleration with updated drag force
        #    print(a_mod)
            n = n+1
#        import pdb; pdb.set_trace()

            #plot the model results
        plt.plot(model_times, v_mod, label='$C_d={}$'.format(c_vect[c]))
    plt.xlabel("Time (s)")
    plt.ylabel("Velocity (m/$s$)")
    plt.title("Velocity (V$_i$={})".format(vi[ii]))
    plt.legend()
    plt.savefig(figname[ii], bbox_inches='tight')

#import pdb; pdb.set_trace()
print(x_mod)

plt.show()
        #plt.savefig("modelP_orange_freefall.pdf", bbox_inches='tight')
