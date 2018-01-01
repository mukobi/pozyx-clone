import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import scipy.optimize as opt
from scipy.optimize import curve_fit
from math import isclose
#####################################################################

df=pd.read_csv('12_27_17_walking13.csv', delimiter=',', usecols = [0,1,28, 29])

df.columns = ['index', 'time', 'posx', 'posy']


df2 = df.ix[::].dropna() #index range pertaining to data of interest

posx=df['posx'].values
posy=df['posy'].values

pxa=df2['posx'].values*0.001
xi = pxa[0] # when was the ball released?
x_final = pxa[-1] - xi # sets land time assuming drop time is zero
px = pxa - xi + 1 # sets release time to zero

pya=df2['posy'].values*0.001
di = pya[0] # when was the ball released?
d_final = pya[-1] - di # sets land position assuming throw position is zero
py = pya - di # sets release time to zero

plt.figure()
plt.plot(px,py,'o')
plt.title("X vs. Y", fontsize = 20)
plt.xlabel("X (m)", fontsize = 15)
plt.ylabel("Y (m)", fontsize = 15)
plt.tick_params(labelsize = 'large')
plt.savefig("walking.pdf")
#import pdb; pdb.set_trace()
"""
########################## plot raw data ###########################
def func(x,a,b,c):
    return a*(x**2) + b*x + c
pfit, success = opt.curve_fit(func,x2,d2)
xx = np.linspace(0, x_final ,1000)
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
plt.plot(x2[1:], velocity, 'o')
plt.plot(xx,func(xx,*pfit),'--', alpha=.8)
plt.title("Velocity")
plt.xlabel("Time(s)")
plt.ylabel("Velocity (m/s)")
plt.tight_layout()
"""
plt.show()


