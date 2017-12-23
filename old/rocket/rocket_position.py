import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import scipy.optimize as opt
from scipy.optimize import curve_fit
from math import pi
################## parameters ###########################
ti = 11.039127 # when did the rocket take off?
tf = 14.669509 #when did the rocket hit the ground?
t = 14.669509-11.039127 # how long wasa object in the air?

s = 2052.0-368.0 # FOR 1D VERTICLE MOTION ONLY how much did rocket shift in meters (final position - initial position)

n = 3.636 # to start newRange at zer

############ parameters for drag force ################
diameter = 0.008107319666 # diameter of object
radius = 1/2 * diameter
A = pi*radius**2 # cross sectional area in meters
v = 16 # initial velocity
#v = 17.740803207
#vsq = v**2 # maximum velocity during free fall
rho = 1.225 # density of air at sea level at 20 degrees C
m = 0.227 # mass of the object in kg
g = 9.81
Fg = -m*g

########################################################
df=pd.read_csv('rocket_4096_oct24_3.csv', delimiter=',', usecols = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28])

df.columns = ['index', 'time', 'difference', 'hz', 'avgHz', 'pressure', 'acceleration-x', 'acceleration-y', 'acceleration-z', 'magnetic-x', 'magnetic-y', 'magnetic-z', 'angularVelocity-x', 'angularVelocity-y', 'angularVelocity-z', 'heading', 'roll', 'pitch', 'quaternion-x', 'quaternion-y', 'quaternion-z', 'quaternion-w', 'linearAcceleration-x', 'linearAcceleration-y', 'linearAcceleration-z', 'gravity-x', 'gravity-y', 'gravity-z', 'range']

df2 = df.ix[167:216].dropna()
df3 = df.ix[168:216].dropna() # for newRange calculations
df4 = df.ix[169:214].dropna()

x=df['time'].values
d=df['range'].values

xa=df2['time'].values
x2 = xa - ti
d2=df2['range'].values

x3=df3['time'].values
d3=df3['range'].values

############################## for calculating new range #############################
dt = t # rocket's time in the air

new_v=s/dt # for discounting horizontal motion
new_x=new_v*dt # for discounting horizontal motion

newd = np.sqrt(d2**2-new_x**2) # total range discounting horizontal motion
newRange = newd[~np.isnan(newd)]

#df3['newRange'] = newRange
velocity = (np.ediff1d(newRange) / np.ediff1d(x3) ) * 0.001 # velocity from new range
###################### plot the raw data within motion parameters ####################

def func(x,a,b,c):
    return a*(x**2) + b*x + c
pfit, success = opt.curve_fit(func,x2,d2)
xx = np.linspace(x2[0],x2[-1],100)
print('raw range coeffs: {}'.format(pfit))
plt.figure()
plt.subplot(1,1,1)
plt.tick_params()
plt.title('Raw Range')
plt.xlabel('Time (s)')
plt.ylabel('Distance (m)')
plt.plot(x2, d2, 'o')
plt.plot(xx,func(xx,*pfit),'--', alpha=.8)
gravity = 'a = {} m/s$^2$'.format(np.around(pfit[0]*-2*0.001, 2))
print(gravity)
plt.figtext(0.485,0.20, gravity, style='italic')
plt.tight_layout()
plt.savefig("rawRange_rocket.pdf", bbox_inches='tight')
####################### plot newRange ##########################
def func1(x,a,b,c):
    return a*(x**2) + b*x + c
pfit1, success1 = opt.curve_fit(func1,x3,newRange)
xx3 = np.linspace(11.171177,14.669509,38)

print('pfit1 coeffs: {}'.format(pfit1))
plt.figure()
plt.subplot(1,1,1)
plt.tick_params()
plt.title('New Range')
plt.plot(x3, newRange,'o')
plt.plot(xx3,func1(xx3,*pfit1),'--', alpha=.8)
plt.xlabel('Time')
plt.ylabel('Distance')
z = np.polyfit(x3, newRange, 2)
newGravity = 'a = {} m/s^2'.format(pfit1[0]*-2*0.001)
plt.figtext(0.35,0.15, newGravity, style='italic')
plt.tight_layout()
plt.savefig("newRange_rocket.pdf", bbox_inches='tight')
########################### plot velocity ###########################

velocity = (np.ediff1d(newRange) / np.ediff1d(x3) )
def func(x,a,b):
    return a*x + b
pfit, success = opt.curve_fit(func, x3[1:], velocity)
xx = np.linspace(x3[0], x3[-1] ,100)
print('velocity coeffs: {}'.format(pfit))
plt.figure()
plt.plot(x3[1:], velocity)
plt.plot(xx,func(xx,*pfit),'--', alpha=.8)
plt.title("Velocity")
plt.xlabel("Time(s)")
plt.ylabel("Velocity (m/s)")
plt.tight_layout()
plt.savefig("velocity_rocket.pdf", bbox_inches='tight')

plt.show()
