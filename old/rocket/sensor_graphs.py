import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import scipy.optimize as opt
from scipy.optimize import curve_fit
from math import pi

##################### parameters for drag force ######################################
diameter = 0.008107319666       # diameter of object
radius = 1/2 * diameter
A = pi*radius**2                # cross sectional area in meters
v = 16                          # initial velocity to test
rho = 1.225                     # density of air at sea level at 20 degrees C
m = 0.227                       # mass of the object in kg
g = 9.81
Fg = -m*g

######################################################################################
df=pd.read_csv('rocket_4096_oct24_3.csv', delimiter=',', usecols = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28])

df.columns = ['index', 'time', 'difference', 'hz', 'avgHz', 'pressure', 'acceleration-x', 'acceleration-y', 'acceleration-z', 'magnetic-x', 'magnetic-y', 'magnetic-z', 'angularVelocity-x', 'angularVelocity-y', 'angularVelocity-z', 'heading', 'roll', 'pitch', 'quaternion-x', 'quaternion-y', 'quaternion-z', 'quaternion-w', 'linearAcceleration-x', 'linearAcceleration-y', 'linearAcceleration-z', 'gravity-x', 'gravity-y', 'gravity-z', 'range']

df2 = df.ix[166:216].dropna()
df3 = df.ix[168:216].dropna() # for newRange calculations
df4 = df.ix[169:214].dropna()

# entire data set
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

# data pertaining to object's motion
xa=df2['time'].values

t = xa[-1]-xa[0]   # how long wasa object in the air?

x2 = xa-t
n = xa[0]   # to start newRange at zero


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
ax4=df4['linearAcceleration-x'].values
ay4=df4['linearAcceleration-y'].values

############################# plot euler angles ############################
plt.figure()
plt.subplot(1,1,1)
plt.title('Euler Angles')
plt.tick_params()
plt.plot(x2, heading2, '-o', label='yaw')
plt.plot(x2, pitch2, '-o', label='roll')
plt.plot(x2, roll2,'-o', label='pitch')
plt.xlabel('Time (s)')
plt.ylabel('Angle ($^\circ$)')
plt.legend()
plt.tight_layout()


############################ plot gravity ##################################
plt.figure()
plt.subplot(1,1,1)
plt.title('Gravity')
plt.xlabel('Time (s)')
plt.ylabel('Gravity (m/s$^2$)')
plt.plot(x2, gx2, '-o', label='x')
plt.plot(x2, gy2, '-o', label='y')
plt.plot(x2, gz2,'-o', label='z')
plt.legend()
plt.tight_layout()


####################### plot  linear acceleration #########################
plt.figure()
plt.subplot(1,1,1)
plt.title('Linear Acceleration')
plt.tick_params()
plt.xlabel('Time (s)')
plt.ylabel('Linear Acceleration (m/s$^2$)')
plt.plot(x2, ax2, '-o',label='x')
plt.plot(x2, ay2, '-o',label='y')
plt.plot(x2, az2,'-o', label='z')
plt.legend()
plt.tight_layout()

######################### plot acceleration ###############################
plt.figure()
plt.subplot(1,1,1)
plt.title('Acceleration')
plt.tick_params()
plt.xlabel('Time (s)')
plt.ylabel('Acceleration (m/s$^2$)')
plt.plot(x2, Ax2, '-o',label='x')
plt.plot(x2, Ay2, '-o',label='y')
plt.plot(x2, Az2,'-o', label='z')
plt.legend()
plt.tight_layout()
plt.show()
