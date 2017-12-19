import scipy.signal
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

plt.rcParams['text.usetex']=True
params = {'legend.fontsize': 8}
plt.rcParams.update(params)

df=pd.read_csv('12_13_17_1D_1.csv', delimiter=',', usecols=[1,28])

df = df.apply(pd.Series.interpolate)

df.columns = ['Time', 'Range']

x = df['Time']
y = df['Range']

# Position parameters
w = 13
p = 3

# Velocity parameters

w2 =13 
p2 = 3

#yhat = scipy.signal.savgol_filter(y3, 9, 1) # Default: window size 51, polynomial order 3. 

yhat = scipy.signal.savgol_filter(y, w, p) # Looks good for elmer.

#yhat = scipy.signal.savgol_filter(y, 9, 1) # Default: window size 51, polynomial order 3.

df['yhat'] = yhat

df['velocity'] = ((df['yhat'] - df['yhat'].shift(1)) / (df['Time'] - df['Time'].shift(1)))

velocity = df['velocity']

yhat2 = scipy.signal.savgol_filter(velocity, w2, p2)
df['yhat2'] = yhat2

plt.figure(figsize=(10,6))
plt.subplot(2,2,1)
plt.plot(x, y, color = 'C0')
plt.ylabel("Distance")
plt.xlabel("Time")
#plt.plot(yhat, color='C1', linestyle = '--')
plt.title('Raw Position Data')

plt.subplot(2,2,3)
plt.plot(x, yhat, color='C0')
plt.title('Smoothed Position Data')
plt.ylabel("Distance")
plt.xlabel("Time")

plt.subplot(2,2,2)
plt.plot(x, velocity, color = 'C0')
plt.plot(x, yhat2, linestyle = '--', color = 'C1')
plt.legend()
plt.title('Velocity from Smoothed Position')
plt.ylabel("Distance")
plt.xlabel("Time")


plt.subplot(2,2,4)
#plt.plot(velocity)
plt.plot(x, yhat2)
plt.title('Smoothed Velocity')
plt.ylabel("Distance")
plt.xlabel("Time")
plt.suptitle('savitzky-golay filter', fontweight = 'bold')
plt.tight_layout(rect=[0, 0.03, 1, 0.95])

#df.to_csv('savgol_elmer22.csv')

plt.show()



