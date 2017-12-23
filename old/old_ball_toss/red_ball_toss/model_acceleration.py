import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import scipy.optimize as opt
from scipy.optimize import curve_fit
from math import isclose
#####################################################################

# enter your parameters here. this contains information about the ball that was dropped.

from math import pi
circumference = 31.3 #in cm
diameter = circumference / pi
radius = .5 * diameter * 0.01
A = pi*radius**2        # cross sectional area in meters
print(A)
rho = 1.225             # density of air at sea level at 20 degrees C
m = 33*0.001                # mass of the object in kg
g = - 9.8
Fg = m*g
vi = 8

df=pd.read_csv('r_ball_toss6.csv', delimiter=',', usecols = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28])

df.columns = ['index', 'time', 'difference', 'hz', 'avgHz', 'pressure', 'acceleration-x', 'acceleration-y', 'acceleration-z', 'magnetic-x', 'magnetic-y', 'magnetic-z', 'angularVelocity-x', 'angularVelocity-y', 'angularVelocity-z', 'heading', 'roll', 'pitch', 'quaternion-x', 'quaternion-y', 'quaternion-z', 'quaternion-w', 'linearAcceleration-x', 'linearAcceleration-y', 'linearAcceleration-z', 'gravity-x', 'gravity-y', 'gravity-z', 'range']


df2 = df.ix[35:64].dropna() #index range pertaining to data of interest

############################################ entire data set ###########################################
x=df['time'].values
d=df['range'].values*0.001

########################### data pertaining to rocket's motion #######################
xa=df2['time'].values
xi = xa[0] # when was the ball released?
x_final = xa[-1] - xi # sets land time assuming drop time is zero
x2 = xa - xi # sets release time to zero
d2=df2['range'].values*0.001

################################### create the models ################################
N = 100 # allows you to create each model out of 100 points

model_times = np.linspace(x2[0], x2[-1], 100)   # create array of 100 times within experimental timeframe for the modeled positions
x_mod=np.zeros(shape=(N))   # create empty array with space for 100 elements
v_mod=np.zeros(shape=(N))
a_mod=np.zeros(shape=(N))
dragForce=np.zeros(shape=(N))

plt.figure()

c_vect = [0,0.1,0.2,0.3,0.4]
for c in range(5) :
    x_mod[0] = 0    # initial position of zero
    v_mod[0] = vi
    dragForce[0] = c_vect[c]*((rho*v_mod[0]**2)/2)*A   # initial drag force
    a_mod[0] = (Fg-dragForce[0])/m  # initial acceleration based on initial drag force
    n=0

    for n in range(0,N-1):
        x_mod[n+1] = x_mod[n]  + v_mod[n] * (x2[-1]-x2[0])/100 + (1/2) * (a_mod[n]) * (x2[-1]-x2[0])/100**2 # simply y=x + v*t + (1/2)*a*t^2
        v_mod[n+1] = v_mod[n] + a_mod[n] * (x2[-1]-x2[0])/100 # updated velocity is v + a*t

        if v_mod[n] < 0 :
            dragForce[n+1] = -(c_vect[c]*((rho*(v_mod[n])**2)/2)*A)

        else:
            dragForce[n+1] = c_vect[c]*((rho*v_mod[n]**2)/2)*A

        a_mod[n+1] = (Fg-dragForce[n+1])/m  # update acceleration with updated drag force
        n = n+1

    #plot the model results
    plt.plot(model_times, a_mod)
plt.xlabel("Time (s)")
plt.ylabel("Acceleration (m/s^2)")
plt.title("Modeled Acceleration Graphs")
plt.legend()
plt.savefig("modelA_red.pdf", bbox_inches='tight')
plt.show()
