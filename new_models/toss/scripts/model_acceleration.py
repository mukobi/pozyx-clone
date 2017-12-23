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


datafile = ['red_toss.csv', 'yellow_toss.csv', 'blue_toss.csv', 'orange_toss.csv']
ball = [redBall, yellowBall, blueBall, orangeBall]
title = ['red ball', 'yellow ball', 'blue ball', 'orange ball']
figname = ['redBall.pdf', 'yellowBall.pdf', 'blueBall.pdf', 'orangeBall.pdf']
rows = [slice(38,63,1), slice(42,72,1), slice(2237,2265,1), slice(2319,2347,1)]

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

    da=df2['range'].values*-0.001
    di = da[0] # when was the ball released?
    d_final = da[-1] - di # sets land time assuming drop time is zero
    d2 = da - di # sets release time to zero

    ################################### create the models ################################
    N = 100 # allows you to create each model out of 100 points

    model_times = np.linspace(x2[0], x2[-1], 100)   # create array of 100 times within experimental timeframe for the modeled positions
    x_mod = np.zeros(shape=(N))   # create empty array with space for 100 elements
    v_mod = np.zeros(shape=(N))
    a_mod = np.zeros(shape=(N))
    dragForce = np.zeros(shape=(N))
    dt = ( x2[-1]-x2[0] ) / N
    print(datafile)
    plt.figure()
    #plt.plot(x2,d2,'o')
#    c_vect=np.array([0])
    c_vect = np.array([0,0.2,0.4,0.6,0.8,1])
    for c in range(6) :
        x_mod[0] = 0    # initial position of zero
        v_mod[0] = 0    # initial velocity of zero
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
        plt.plot(model_times, a_mod, label='$C_d={}$'.format(c_vect[c]))
    plt.xlabel("Time (s)")
    plt.ylabel("Acceleration (m/$s^2$)")
    plt.title(title[ii])
    plt.legend()
    plt.savefig(figname[ii], bbox_inches='tight')

#import pdb; pdb.set_trace()


plt.show()
        #plt.savefig("modelP_orange_freefall.pdf", bbox_inches='tight')
