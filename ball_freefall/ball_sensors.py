import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import scipy.optimize as opt
from scipy.optimize import curve_fit
from math import isclose
#####################################################################

df=pd.read_csv('ball_drop.csv', delimiter=',', usecols = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28])

df.columns = ['index', 'time', 'difference', 'hz', 'avgHz', 'pressure', 'acceleration-x', 'acceleration-y', 'acceleration-z', 'magnetic-x', 'magnetic-y', 'magnetic-z', 'angularVelocity-x', 'angularVelocity-y', 'angularVelocity-z', 'heading', 'roll', 'pitch', 'quaternion-x', 'quaternion-y', 'quaternion-z', 'quaternion-w', 'linearAcceleration-x', 'linearAcceleration-y', 'linearAcceleration-z', 'gravity-x', 'gravity-y', 'gravity-z', 'range']


df2 = df.ix[2484:2540].dropna() #index range pertaining to data of interest

############################################# entire data set ###########################################
x=df['time'].values
d=df['range'].values*0.001
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

xa=df2['time'].values
xi = xa[0] # when was the ball released?
x_final = xa[-1] - xi # sets land time assuming drop time is zero
x2 = xa - xi # sets release time to zero
d2=df2['range'].values*0.001
p2=df2['pressure'].values
lax2=df2['linearAcceleration-x'].values * 0.01
lay2=df2['linearAcceleration-y'].values * 0.01
laz2=df2['linearAcceleration-z'].values * 0.01

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
####################### plot euler angles ###########################
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
####################################################################

############################ plot gravity ##########################
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
####################################################################

#################### plot linear acceleration ######################
plt.figure()
plt.subplot(1,1,1)
plt.title('Linear Acceleration')
plt.tick_params()
plt.xlabel('Time (s)')
plt.ylabel('Linear Acceleration (m/s$^2$)')
plt.plot(x2, lax2, '-o',label='x')
plt.plot(x2, lay2, '-o',label='y')
plt.plot(x2, laz2,'-o', label='z')
plt.legend()
plt.tight_layout()
####################################################################
plt.show()
