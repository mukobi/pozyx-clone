import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import scipy.optimize as opt
from scipy.optimize import curve_fit

df=pd.read_csv('rocket_4096_oct24_3.csv', delimiter=',', usecols = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28])

df.columns = ['index', 'time', 'difference', 'hz', 'avgHz', 'pressure', 'acceleration-x', 'acceleration-y', 'acceleration-z', 'magnetic-x', 'magnetic-y', 'magnetic-z', 'angularVelocity-x', 'angularVelocity-y', 'angularVelocity-z', 'heading', 'roll', 'pitch', 'quaternion-x', 'quaternion-y', 'quaternion-z', 'quaternion-w', 'linearAcceleration-x', 'linearAcceleration-y', 'linearAcceleration-z', 'gravity-x', 'gravity-y', 'gravity-z', 'range']

#df2 = df.ix[166:216].dropna() #index pertaining to rocket's motion

df2 = df.ix[166:216].dropna()
ti = 11.039127 # when did the rocket take off?
xa=df2['time'].values
x2 = xa - ti
xdata = np.array([x2,x2])
d2=df2['range'].values
p2=df2['pressure'].values
ax2=df2['linearAcceleration-x'].values * 0.01
ay2=df2['linearAcceleration-y'].values * 0.01
az2=df2['linearAcceleration-z'].values * 0.01

Ax2=df2['acceleration-x'].values * 0.01
Ay2=df2['acceleration-y'].values * 0.01
Az2=df2['acceleration-z'].values * 0.01

mx2=df2['magnetic-x'].values
my2=df2['magnetic-y'].values
mz2=df2['magnetic-z'].values
heading2=df2['heading'].values
pitch2=df2['pitch'].values
roll2=df2['roll'].values
gx2=df2['gravity-x'].values * 0.01
gy2=df2['gravity-y'].values * 0.01
gz2=df2['gravity-z'].values * 0.01
qx2=df2['quaternion-x'].values
qy2=df2['quaternion-y'].values
qz2=df2['quaternion-z'].values
qw2=df2['quaternion-w'].values

A = 0.008107319666 # cross sectional area


rho = 1.225 # density of air at sea level at 20 degrees C
m = 0.227 # mass of the object in kg
g=9.81
Fg = -m*g

"""
x=np.zeros(shape=(N))
x[n+1]=np.zeros(shape=(N))
a=np.zeros(shape=(N))
dragForce=np.zeros(shape=(N))
"""

#dragForce[0] = c_vect[0]*((rho*v[0]**2)/2)*A
#n=0

def func(t, vel, drag):
    dt = 0.0000001
  #  testint = t/dt
  #  import pdb; pdb.set_trace()
    #print("t is:", t)
    N=int(t/dt)
    x=0
    rho = 1.225 # density of air at sea level at 20 degrees C
    m = 0.227 # mass of the object in kg
    g=9.81
    Fg = -m*g
    a=g
    A=0.008107319666
    #for vv in vel:
        #for c in c_vect:
    for n in range(N):
        x = x + vel * dt + (1/2) * (a) * dt**2
        vel = vel + a * dt

        if vel < 0:
            dragForce = -(drag*((rho*(vel)**2)/2)*A)

        else:
            dragForce = drag*((rho*vel**2)/2)*A
        a = (Fg-dragForce)/m
    return x

def func2(tlist,vel,drag):
    xlist = list()
    for t in tlist:
        x = func(t,vel,drag)
        xlist.append(x)
    return xlist

#N2=5
#for n in range(0,N2-1):
#    print(func(n,16,0.3))
popt, pcov = curve_fit(func2, x2, d2, bounds=([13,0], [25,1]))
plt.plot(x2, func(x2, *popt), 'g--',
         label='fit: v_start=%5.3f, c_vect=%5.3f' % tuple(popt))
plt.show()




