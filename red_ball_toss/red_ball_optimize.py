import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import scipy.optimize as opt
from scipy.optimize import curve_fit
from scipy import stats
from math import isclose
#####################################################################

# enter your parameters here. this contains information about the ball that was dropped.
from math import pi
circumference = 31.3 #in cm
diameter = circumference / pi
radius = .5 * diameter * 0.01
A = pi*radius**2        # cross sectional area in meters
rho = 1.225             # density of air at sea level at 20 degrees C
m = 33*0.001                # mass of the object in kg
g=9.8
Fg = -m*g

df=pd.read_csv('r_ball_toss6.csv', delimiter=',', usecols = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28])

df.columns = ['index', 'time', 'difference', 'hz', 'avgHz', 'pressure', 'acceleration-x', 'acceleration-y', 'acceleration-z', 'magnetic-x', 'magnetic-y', 'magnetic-z', 'angularVelocity-x', 'angularVelocity-y', 'angularVelocity-z', 'heading', 'roll', 'pitch', 'quaternion-x', 'quaternion-y', 'quaternion-z', 'quaternion-w', 'linearAcceleration-x', 'linearAcceleration-y', 'linearAcceleration-z', 'gravity-x', 'gravity-y', 'gravity-z', 'range']


df2 = df.ix[35:64].dropna() #index range pertaining to data of interest

# entire data set
x=df['time'].values
d=df['range'].values*0.001

#data pertaining to object's motion
xa=df2['time'].values
xi = xa[0]  # when was the ball released?
x_final = xa[-1] - xi # sets land time assuming drop time is zero
x2 = xa - xi # sets release time to zero
d2=df2['range'].values*0.001

dtGlobal = 0.001
unitConv = 1000

t0_new = x2[0]
xdata = np.array([x2,x2])


def func3(t, vel, drag) :
    dt = dtGlobal
    x = 0
    t_curr = t0_new
    xlist = [x]
    a=g


    if not hasattr(t, '__len__') :
        tlist = [0,t]   # make a list out of a single target t value
    else :
        tlist = t
    i = 1 # list index, initialized to 1 since i=0 is initial time, which we already have

    while not isclose(t_curr, tlist[-1], abs_tol=dt) :
        t_curr += dt
        x = x + vel * dt + (1/2) * (a) * dt**2
        vel = vel + a * dt

        if vel < 0:
            dragForce = -(drag*((rho*(vel)**2)/2)*A)
        else:
            dragForce = drag*((rho*vel**2)/2)*A
        a = (Fg-dragForce)/m
        t_next = tlist[i]
        if isclose(t_curr, t_next, abs_tol=dt) :
            xlist.append(x)
            i+=1
    return np.array(xlist)
# find the optimal values of velocity and drag coefficient
popt, pcov = curve_fit(func3, x2, d2, bounds=([0,0], [10,10]))
print(popt)

# calculate and print r-squared
model_data = func3(x2, *popt)
slope, intercept, r_value, p_value, std_err = stats.linregress(model_data, d2)
print("r-squared:",r_value**2)

# plot the optimal model
plt.title("Optimized Velocity and Drag Coefficient")
plt.plot(x2,d2,'o', label="experimental data")
plt.plot(x2, func3(x2, *popt),
         label='fit: v_start=%5.3f, c_vect=%5.3f' % tuple(popt))
plt.legend()

plt.show()
