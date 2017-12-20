import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import scipy.optimize as opt
from scipy.optimize import curve_fit
from math import pi
#################################################### parameters ##########################################
ti = 11.039127 # when did the rocket take off?
tf = 14.669509 #when did the rocket hit the ground?
t = 14.669509-11.039127 # how long wasa object in the air?

s = 2052.0-368.0 # FOR 1D VERTICLE MOTION ONLY how much did rocket shift in meters (final position - initial position)

n = 3.636 # to start newRange at zer

##################### parameters for drag force ##########################################################
diameter = 0.0508 # diameter of object
radius = 1/2 * diameter
A = pi*radius**2 # cross sectional area in meters
v = 16 # initial velocity
#v = 17.740803207
#vsq = v**2 # maximum velocity during free fall
rho = 1.225 # density of air at sea level at 20 degrees C
m = 0.227 # mass of the object in kg
g = 9.81
Fg = -m*g
##########################################################################################################
##########################################################################################################
df=pd.read_csv('rocket_4096_oct24_3.csv', delimiter=',', usecols = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28])

df.columns = ['index', 'time', 'difference', 'hz', 'avgHz', 'pressure', 'acceleration-x', 'acceleration-y', 'acceleration-z', 'magnetic-x', 'magnetic-y', 'magnetic-z', 'angularVelocity-x', 'angularVelocity-y', 'angularVelocity-z', 'heading', 'roll', 'pitch', 'quaternion-x', 'quaternion-y', 'quaternion-z', 'quaternion-w', 'linearAcceleration-x', 'linearAcceleration-y', 'linearAcceleration-z', 'gravity-x', 'gravity-y', 'gravity-z', 'range']

#df2 = df.ix[166:216].dropna() #index pertaining to rocket's motion

df2 = df.ix[166:216].dropna()
df3 = df.ix[168:216].dropna() # for newRange calculations
df4 = df.ix[169:214].dropna()


############################################# entire data set ###########################################
x=df['time'].values
d=df['range'].values
p=df['pressure'].values
mx=df['magnetic-x'].values
my=df['magnetic-y'].values
mz=df['magnetic-z'].values
heading=df['heading'].values
pitch=df['pitch'].values
roll=df['roll'].values
gx=df['gravity-x'].values
gy=df['gravity-y'].values
gz=df['gravity-z'].values
##########################################################################################################

######################################### data pertaining to rocket's motion #############################
xa=df2['time'].values
x2 = xa - ti
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
##########################################################################################################
x3=df3['time'].values
d3=df3['range'].values
p3=df3['pressure'].values
mx3=df3['magnetic-x'].values
my3=df3['magnetic-y'].values
mz3=df3['magnetic-z'].values
heading3=df3['heading'].values
pitch3=df3['pitch'].values
roll=df3['roll'].values
gx3=df3['gravity-x'].values
gy3=df3['gravity-y'].values
gz3=df3['gravity-z'].values


x6 = df2['time'].ix[169:216].values # time frame for velocity plot and models
####################################### for calculating new range #########################################
dt = t # rocket's time in the air

new_v=s/dt # for discounting horizontal motion
new_x=new_v*dt # for discounting horizontal motion

newd = np.sqrt(d2**2-new_x**2) # total range discounting horizontal motion
newRange = newd[~np.isnan(newd)]

df3['newRange'] = newRange
velocity = (np.ediff1d(newRange) / np.ediff1d(x3) ) * 0.001 # velocity from new range

x7_mod = df['time'].ix[169:214].values
x7_vel_mod = df['time'].ix[170:214].values

newRange_mod = df['range'].ix[169:214].values*0.001

adj_newRange_mod = newRange_mod  - 3.636

#adj_newRange_mod = newRange_mod

adj_x7_mod = x7_mod - 11.23917484

adj_x7_vel_mod = x7_vel_mod - 11.17117691

xx7 = np.linspace(2.83447221e-09,3.29492307e+00,100)

vel = (np.ediff1d(adj_newRange_mod) / np.ediff1d(adj_x7_mod))

#import pdb; pdb.set_trace()
#import pdb; pdb.set_trace()
N = 100




x_mod=np.zeros(shape=(N))
v_mod=np.zeros(shape=(N))
a_mod=np.zeros(shape=(N))
dragForce=np.zeros(shape=(N))

c_vect = [0,0.1,0.2,0.3,0.4]    # drag coefficients to try
plt.figure()
plt.plot(adj_x7_mod,adj_newRange_mod,'o', label='$experimental\ data$') # plot experimental data

for c_vect in range(len(c_vect)) :
    x_mod[0] = 0    # initial position
    v_mod[0] = v    # initial velocity
    dragForce[0] = c_vect*((rho*v_mod[0]**2)/2)*A   # initial drag forcw
    a_mod[0] = (Fg-dragForce[0])/m  # initial acceleration
    n=0

    for n in range(0,N-1):
        x_mod[n+1] = x_mod[n] + v_mod[n] * 3.29492307e+00/100+ (1/2) * (a_mod[n]) * (3.29492307e+00/100)**2 # y = x + vt + (1/2) at^2 for new position
        v_mod[n+1] = v_mod[n] + a_mod[n] * 3.29492307e+00/100   # y = v + at for new velocity

        if v_mod[n] < 0 :   # when velocity is negative, drag force is negative
            dragForce[n+1] = -(c_vect*((rho*(v_mod[n])**2)/2)*A)

        else: # when velocity is positive, drag force is positive
            dragForce[n+1] = c_vect*((rho*v_mod[n]**2)/2)*A

        a_mod[n+1] = (Fg-dragForce[n+1])/m
        n = n+1
    x_filt = x_mod[x_mod >= 0]

    plt.plot(xx7,x_mod)
plt.show()
