import scipy.signal
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

plt.rcParams['text.usetex']=True
params = {'legend.fontsize': 8}
plt.rcParams.update(params)

df=pd.read_csv('/Users/CoraJune/Documents/GitHub/cjs_stuff/smoothing_tests/savgol_filter/overlook_park_elmer_1.csv', delimiter=',', usecols=[1,5])

#df2=pd.read_csv('/Users/CoraJune/Google Drive/Pozyx/Data/lab_applications/lab_redos/atwood_machine/ema_updated/alpha=0.5/newest_ema_6_0.5.csv', delimiter=',', usecols=['Time', '0x6030 Range'])

#df3=pd.read_csv('/Users/CoraJune/Google Drive/Pozyx/Data/lab_applications/lab_redos/atwood_machine/ema_updated/alpha=0.5/newest_ema_5_0.5.csv', delimiter=',', usecols=['Time', '0x6030 Range'])

df = df.apply(pd.Series.interpolate)

df.columns = ['Time', 'Range']

x = df['Time']
y = df['Range']

#x2 = df2['Time2']
#y2 = df2['Range2']

#x3 = df3['Time']
#y3 = df3['Range']

# Position parameters
w = 69
p = 6

#velocity parameters

w2 =69 
p2 = 6

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
#plt.plot(yhat, color='C1', linestyle = '--')
plt.title('raw position data')

plt.subplot(2,2,3)
plt.plot(x, yhat, color='C0')
plt.title('smoothed position data')

plt.subplot(2,2,2)
plt.plot(x, velocity, color = 'C0')
plt.plot(x, yhat2, linestyle = '--', color = 'C1')
plt.title('velocity from smoothed position')

plt.subplot(2,2,4)
#plt.plot(velocity)
plt.plot(x, yhat2)
plt.title('smoothed velocity')
plt.suptitle('savitzky-golay filter', fontweight = 'bold')
plt.tight_layout(rect=[0, 0.03, 1, 0.95])


#df.to_csv('savgol_elmer22.csv')

plt.show()



