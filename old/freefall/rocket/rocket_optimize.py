import pandas as pd
import matplotlib as mpl
#mpl.use('Qt5Agg')
import matplotlib.pyplot as plt
import numpy as np
import scipy.optimize as opt
from math import isclose
from scipy.optimize import curve_fit
from scipy import stats

#print('plt backend:', plt.get_backend())
#exit(0)

df=pd.read_csv('rocket1.csv', delimiter=',', usecols = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28])


df.columns = ['index', 'time', 'difference', 'hz', 'avgHz', 'pressure', 'acceleration-x', 'acceleration-y', 'acceleration-z', 'magnetic-x', 'magnetic-y', 'magnetic-z', 'angularVelocity-x', 'angularVelocity-y', 'angularVelocity-z', 'heading', 'roll', 'pitch', 'quaternion-x', 'quaternion-y', 'quaternion-z', 'quaternion-w', 'linearAcceleration-x', 'linearAcceleration-y', 'linearAcceleration-z', 'gravity-x', 'gravity-y', 'gravity-z', 'range']

#df2 = df.ix[166:216].dropna() #index pertaining to rocket's motion

df2 = df.ix[437:469].dropna()
df3 = df.ix[168:216].dropna() # for newRange calculations
x = df2['time'].values
x2 = x - x[0]

d = df2['range'].values*(-0.001)
d2 = d - d[0]

t0_new = x2[0]
xdata = np.array([x2,x2])

x3Raw = df3['time'].values
x3 = x3Raw - x3Raw[0]

from math import pi
diameter = 0.07083 # cross sectional area
radius = 1/2 * diameter
A = pi*radius**2 # cross sectional area in meters
rho = 1.225 # density of air at sea level at 20 degrees C
m = 0.225 # mass of the object in kg
g = -10.5
Fg = m*g

#import pdb; pdb.set_trace()
dtGlobal = 0.0000001
dtGlobal = 0.001
#dtGlobal = 0.00001
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
        x = x + vel * dt + (1/2) * (a) * dt**2
        vel = vel + a * dt

        if vel < 0:
            dragForce = -(drag*((rho*(vel)**2)/2)*A)
        else:
            dragForce = drag*((rho*vel**2)/2)*A
        a = (Fg-dragForce)/m

        #xDict[t_curr] = x
        t_next = tlist[i]
        #print('t_curr:', t_curr, 'x:', x, 't_next:', t_next, 'i:',i) # debugging
        if isclose(t_curr, t_next,abs_tol=dt) :
            xlist.append(x)
            i+=1        # go to next target time in list

    return np.array(xlist)


''' let's see what we get from one pair of initial v and drag coeff'''
#xVals = func3(x2, 20, 0.5, 1000)
#print(xVals)
#plt.plot(x2, xVals, 'bo')
#plt.show()
#exit(0)

#popt, pcov = curve_fit(func3, x2, d2, bounds=([13,0], [25,1]))
popt, pcov = curve_fit(func3, x2, d2, bounds=([0,0], [0.0001,1]))
print(popt)
plt.figure()
x_filt = d2[d2 >= 0]
plt.plot(x2,d2,'o', label = 'experimental data')
plt.plot(xx3, func3(xx3, *popt),
         label='fit: initial velocity=%5.3f, drag coefficient=%5.3f' % tuple(popt))
plt.title("Model with Optimized Velocity and Drag Coefficient")
plt.legend()
model_data = func3(x2, *popt)
slope, intercept, r_value, p_value, std_err = stats.linregress(model_data, d2)
print("r-squared:",r_value**2)
plt.savefig("fitting_rocket.pdf", bbox_inches='tight')

plt.show()
