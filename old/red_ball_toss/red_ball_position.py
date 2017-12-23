import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import scipy.optimize as opt
from scipy.optimize import curve_fit
from math import isclose
#####################################################################

df=pd.read_csv('r_ball_toss6.csv', delimiter=',', usecols = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28])

df.columns = ['index', 'time', 'difference', 'hz', 'avgHz', 'pressure', 'acceleration-x', 'acceleration-y', 'acceleration-z', 'magnetic-x', 'magnetic-y', 'magnetic-z', 'angularVelocity-x', 'angularVelocity-y', 'angularVelocity-z', 'heading', 'roll', 'pitch', 'quaternion-x', 'quaternion-y', 'quaternion-z', 'quaternion-w', 'linearAcceleration-x', 'linearAcceleration-y', 'linearAcceleration-z', 'gravity-x', 'gravity-y', 'gravity-z', 'range']


df2 = df.ix[35:64].dropna() #index range pertaining to data of interest


x=df['time'].values
d=df['range'].values*0.001
xa=df2['time'].values
xi = xa[0] # when was the ball released?
x_final = xa[-1] - xi # sets land time assuming drop time is zero
x2 = xa - xi # sets release time to zero
d2=df2['range'].values*0.001

########################## plot raw data ###########################
def func(x,a,b,c):
    return a*(x**2) + b*x + c
pfit, success = opt.curve_fit(func,x2,d2)
xx = np.linspace(0, x_final ,100)
print('raw range coeffs: {}'.format(pfit))
plt.figure()
plt.subplot(1,1,1)
plt.tick_params()
plt.title('Raw Range')
plt.xlabel('Time (s)')
plt.ylabel('Distance (m)')
plt.plot(x2, d2, 'o')
plt.plot(xx,func(xx,*pfit),'--', alpha=.8)
gravity = 'a = {} m/s$^2$'.format(np.around(pfit[0]*-2, 2))
print(gravity)
plt.figtext(0.45,0.20, gravity, style='italic')
plt.tight_layout()

########################### plot velocity ###########################
velocity = (np.ediff1d(d2) / np.ediff1d(x2) )
def func(x,a,b):
    return a*x + b
pfit, success = opt.curve_fit(func, x2[1:], velocity)
xx = np.linspace(0, x_final ,100)
print('velocity coeffs: {}'.format(pfit))
plt.figure()
plt.plot(x2[1:], velocity)
plt.plot(xx,func(xx,*pfit),'--', alpha=.8)
plt.title("Velocity")
plt.xlabel("Time(s)")
plt.ylabel("Velocity (m/s)")
plt.tight_layout()

plt.show()
