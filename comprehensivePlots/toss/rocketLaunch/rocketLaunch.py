import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import scipy.optimize as opt
from scipy.optimize import curve_fit
from math import pi
from physProps import *
params = {'mathtext.default': 'regular'}
plt.rcParams.update(params)
#####################################################################
# old: datafile = ['red_drop.csv', 'yellow_drop.csv', 'blue_drop.csv', 'orange_drop.csv', 'rocket_drop.csv']
g = -9.81
Fg = g * blueBall.mass
rho = 1.225

df=pd.read_csv('rocket_launch.csv', delimiter=',', usecols = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28])

df.columns = ['index', 'time', 'difference','hz','aveHz','pressure','xAcc','yAcc','zAcc','xMag','yMag','zMag','xAngVel','yAngVel','zAngVel','yaw','roll','pitch','xQuat','yQuat','zQuat','wQuat','xLinAcc','yLinAcc','zLinAcc','xGrav','yGrav','zGrav','range']


df2 = df.ix[167:216].dropna() #index range pertaining to data of interest

xa=df2['time'].values
xi = xa[0] # when was the ball released?
x_final = xa[-1] - xi # sets land time assuming drop time is zero
x2 = xa - xi # sets release time to zero

da=df2['range'].values
di = da[0] # when was the ball released?
d_final = da[-1] - di # sets land time assuming drop time is zero
d2 = da - di # sets release time to zero

xAcc = df2.xAcc.values
yAcc = df2.zAcc.values
zAcc = df2.zAcc.values
acc = np.sqrt(xAcc**2 + yAcc**2 + zAcc**2)
df2['acc'] = acc

xGrav = df2.xGrav.values
yGrav = df2.yGrav.values
zGrav = df2.zGrav.values
grav = np.sqrt(xGrav**2 + yGrav**2 + zGrav**2)
df2['grav'] = grav

xLinAcc = df2.xLinAcc.values
yLinAcc = df2.yLinAcc.values
zLinAcc = df2.zLinAcc.values
linAcc = np.sqrt(xLinAcc**2 + yLinAcc**2 + zLinAcc**2)
df2['linAcc'] = linAcc

df3 = df.ix[168:216].dropna() # for newRange calculations
x3=df3['time'].values
raw_d3=df3['range'].values*0.001
d3 = raw_d3 - raw_d3[0]

dt = x3[-1] - x3[0]   # rocket's time in the air
s = d3[-1] - d3[0]    # final distance from anchor - initial distance from anchor
new_v = s / dt          # for discounting horizontal motion
new_x = new_v * dt      # for discounting horizontal motion

newd = np.sqrt(d2**2 - new_x**2) # total range discounting horizontal motion
plain_newRange = newd[~np.isnan(newd)]
newRange = plain_newRange - plain_newRange[0]
#import pdb; pdb.set_trace()
#        new_time = df['time'].ix[169:214].values
new_time = df2['time'].ix[167:216].values
#        newRange_mod = df['range'].ix[169:214].values*0.001

#        adj_newRange_mod = newRange_mod  - newRange_mod[0]

adj_time = new_time - new_time[0]


#import pdb; pdb.set_trace()
axPressure = df2.plot.scatter('time', 'pressure',title = 'pressure vs time')
fig = axPressure.get_figure()
fig.savefig('pressure.pdf')

#import pdb; pdb.set_trace()
axRange = plt.scatter(adj_time, newRange, title = 'range vs time')
fig = axRange.get_figure()
fig.savefig('range.pdf')

ax = df2.plot('time', 'xAcc', title = 'acceleration vs time', style='-o', legend = True)
df2.plot(x = 'time', y = 'yAcc', ax = ax, color = 'C1', style='-o', legend = True)
df2.plot('time', 'zAcc', ax = ax, color = 'C2', style='-o', legend = True)
df2.plot('time','acc', ax = ax, color = 'C7', style = '-o', legend = True)
ax.set_ylabel('acceleration')
fig = ax.get_figure()
fig.savefig('acceleration.pdf')

ax2 = df2.plot('time', 'xMag', title = 'mag field vs time', style='-o', legend = True)
df2.plot('time', 'yMag', ax = ax2, color = 'C1', style='-o', legend = True)
df2.plot('time', 'zMag', ax = ax2, color = 'C2', style='-o', legend = True)
ax2.set_ylabel('magnetic field')
fig = ax2.get_figure()
fig.savefig('magField.pdf')

ax3 = df2.plot('time', 'xAngVel', title = 'angular velocity vs time', style='-o', legend = True)
df2.plot('time', 'yAngVel', ax = ax3, color = 'C1', style='-o', legend = True)
df2.plot('time', 'zAngVel', ax = ax3, color = 'C2', style='-o', legend = True)
ax3.set_ylabel('angular velocity')
fig = ax3.get_figure()
fig.savefig('angVel.pdf')

ax4 = df2.plot('time', 'yaw', title = 'euler angles vs time', style='-o', legend = True)
df2.plot('time', 'roll', ax = ax4, color = 'C1', style='-o', legend = True)
df2.plot('time', 'pitch', ax = ax4, color = 'C2', style='-o', legend = True)
ax4.set_ylabel('euler angles')
fig = ax4.get_figure()
fig.savefig('eulerAngles.pdf')

ax5 = df2.plot('time', 'xQuat', title = 'quaternions vs time', style='-o', legend = True)
df2.plot('time', 'yQuat', ax = ax5, color = 'C1', style='-o', legend = True)
df2.plot('time', 'zQuat', ax = ax5, color = 'C2', style='-o', legend = True)
df2.plot('time', 'wQuat', ax = ax5, color = 'C3', style='-o', legend = True)
ax5.set_ylabel('quaternions')
fig = ax5.get_figure()
fig.savefig('quaternions.pdf')

ax6 = df2.plot('time', 'xLinAcc', title = 'linear acceleration vs time', style='-o', legend = True)
df2.plot('time', 'yLinAcc', ax = ax6, color = 'C1', style='-o', legend = True)
df2.plot('time', 'zLinAcc', ax = ax6, color = 'C2', style='-o', legend = True)
df2.plot('time','linAcc', ax = ax6, color = 'C7', style = '-o', legend = True)
ax6.set_ylabel('linear acceleration')
fig = ax6.get_figure()
fig.savefig('linAcc.pdf')

ax7 = df2.plot('time', 'xGrav', title = 'gravity vs time', style='-o', legend = True)
df2.plot('time', 'yGrav', ax = ax7, color = 'C1', style='-o', legend = True)
df2.plot('time', 'zGrav', ax = ax7, color = 'C2', style='-o', legend = True)
df2.plot('time','grav', ax = ax7, color = 'C7', style = '-o', legend = True)
ax7.set_ylabel('gravity')
fig = ax7.get_figure()
fig.savefig('gravity.pdf')

plt.show()
