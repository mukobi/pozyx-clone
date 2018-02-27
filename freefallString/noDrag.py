import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import scipy.optimize as opt
from scipy.optimize import curve_fit

df=pd.read_csv('freefallString.csv', delimiter=',', usecols = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28])

df.columns = ['index', 'time', 'difference','hz','aveHz','pressure','xAcc','yAcc','zAcc','xMag','yMag','zMag','xAngVel','yAngVel','zAngVel','yaw','roll','pitch','xQuat','yQuat','zQuat','wQuat','xLinAcc','yLinAcc','zLinAcc','xGrav','yGrav','zGrav','range']

df2 = df.ix[154:162] #index range pertaining to data of interest

distance = df2.range.values
time = df2.time.values

xLinAcc = df2.xLinAcc.values
yLinAcc = df2.yLinAcc.values
zLinAcc = df2.zLinAcc.values
quadSum = np.sqrt(xLinAcc**2 + yLinAcc**2 + zLinAcc**2)
df2['quadSum'] = quadSum

ax = df2.plot('time', 'xLinAcc', title = 'linAcc', style='-o', legend = True)
df2.plot(x = 'time', y = 'yLinAcc', ax = ax, color = 'C1', style='-o', legend = True)
df2.plot('time', 'zLinAcc', ax = ax, color = 'C2', style='-o', legend = True)
df2.plot('time','quadSum', ax = ax, color = 'C7', style = '-o', legend = True)
ax.set_ylabel('acceleration')
fig = ax.get_figure()
#fig.savefig('acceleration.pdf')







def func(x,a,b,c):
    return a*(x**2) + b*x + c
pfit, success = opt.curve_fit(func,time,distance)
xx = np.linspace(time[0],time[-1],100)
print('raw range coeffs: {}'.format(pfit))
plt.figure()
plt.subplot(1,1,1)
plt.tick_params()
plt.title('Raw Range')
plt.xlabel('Time (s)')
plt.ylabel('Distance (m)')
plt.plot(time, distance, 'o')
plt.plot(xx,func(xx,*pfit),'--', alpha=.8)
gravity = 'a = {} m/s$^2$'.format(np.around(pfit[0]*-2*0.001, 2))
print(gravity)
plt.figtext(0.485,0.20, gravity, style='italic')
plt.tight_layout()

plt.show()
