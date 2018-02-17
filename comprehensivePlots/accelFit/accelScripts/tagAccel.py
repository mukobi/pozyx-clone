import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import colors as mcolors
import numpy as np
import scipy.optimize as opt
from scipy.optimize import curve_fit
from math import pi
params = {'mathtext.default': 'regular'}
plt.rcParams.update(params)
#####################################################################

df=pd.read_csv('tag_freefall.csv', delimiter=',', usecols = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28])

df.columns = ['index', 'time', 'difference','hz','aveHz','pressure','xAcc','yAcc','zAcc','xMag','yMag','zMag','xAngVel','yAngVel','zAngVel','yaw','roll','pitch','xQuat','yQuat','zQuat','wQuat','xLinAcc','yLinAcc','zLinAcc','xGrav','yGrav','zGrav','range']

df2 = df.iloc[80:95] #index range pertaining to data of interest
#416:454
xAcc = df2.xAcc.values
yAcc = df2.yAcc.values
zAcc = df2.zAcc.values
acc = np.sqrt(xAcc**2 + yAcc**2 + zAcc**2)
df2['acc'] = acc

xLinAcc = df2.xLinAcc.values
yLinAcc = df2.yLinAcc.values
zLinAcc = df2.zLinAcc.values
linAcc = np.sqrt(xLinAcc**2 + yLinAcc**2 + zLinAcc**2)
df2['linAcc'] = linAcc

ax = df2.plot('time', 'xAcc', title = 'acceleration vs time trial 1', style='-o', legend = True)
df2.plot(x = 'time', y = 'yAcc', ax = ax, color = 'C1', style='-o', legend = True)
df2.plot('time', 'zAcc', ax = ax, color = 'C2', style='-o', legend = True)
df2.plot('time','acc', ax = ax, color = 'C7', style = '-o', legend = True)
ax.set_ylabel('acceleration')
fig = ax.get_figure()
fig.savefig('acceleration.pdf')

ax6 = df2.plot('time', 'xLinAcc', title = 'linear acceleration vs time trial 1', style='-o', legend = True)
df2.plot('time', 'yLinAcc', ax = ax6, color = 'C1', style='-o', legend = True)
df2.plot('time', 'zLinAcc', ax = ax6, color = 'C2', style='-o', legend = True)
df2.plot('time','linAcc', ax = ax6, color = 'C7', style = '-o', legend = True)
ax6.set_ylabel('linear acceleration')
fig = ax6.get_figure()
fig.savefig('linAcc.pdf')






df3=pd.read_csv('tag_freefall2.csv', delimiter=',', usecols = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28])

df.columns = ['index', 'time', 'difference','hz','aveHz','pressure','xAcc','yAcc','zAcc','xMag','yMag','zMag','xAngVel','yAngVel','zAngVel','yaw','roll','pitch','xQuat','yQuat','zQuat','wQuat','xLinAcc','yLinAcc','zLinAcc','xGrav','yGrav','zGrav','range']

df4 = df.iloc[80:95] #index range pertaining to data of interest
#416:454
xAcc = df2.xAcc.values
yAcc = df2.yAcc.values
zAcc = df2.zAcc.values
acc = np.sqrt(xAcc**2 + yAcc**2 + zAcc**2)
df2['acc'] = acc

xLinAcc = df2.xLinAcc.values
yLinAcc = df2.yLinAcc.values
zLinAcc = df2.zLinAcc.values
linAcc = np.sqrt(xLinAcc**2 + yLinAcc**2 + zLinAcc**2)
df2['linAcc'] = linAcc

ax = df2.plot('time', 'xAcc', title = 'acceleration vs time trial 2', style='-o', legend = True)
df2.plot(x = 'time', y = 'yAcc', ax = ax, color = 'C1', style='-o', legend = True)
df2.plot('time', 'zAcc', ax = ax, color = 'C2', style='-o', legend = True)
df2.plot('time','acc', ax = ax, color = 'C7', style = '-o', legend = True)
ax.set_ylabel('acceleration')
fig = ax.get_figure()
fig.savefig('acceleration.pdf')

ax6 = df2.plot('time', 'xLinAcc', title = 'linear acceleration vs time trial 2', style='-o', legend = True)
df2.plot('time', 'yLinAcc', ax = ax6, color = 'C1', style='-o', legend = True)
df2.plot('time', 'zLinAcc', ax = ax6, color = 'C2', style='-o', legend = True)
df2.plot('time','linAcc', ax = ax6, color = 'C7', style = '-o', legend = True)
ax6.set_ylabel('linear acceleration')
fig = ax6.get_figure()
fig.savefig('linAcc.pdf')

plt.show()
