import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


plt.rcParams['text.usetex']=True
params = {'legend.fontsize': 8}
plt.rcParams.update(params)

df=pd.read_csv('12_13_17_1D_1.csv', delimiter=',', usecols=[1,28])

df.columns = ['Time', 'Range']

df = df.apply(pd.Series.interpolate)

x = df['Time']
y = df['Range']

n =15  #small n = less smoothed

#fwd = pd.Series.ewm(df,span=n, adjust=True).mean()
#bwd = pd.Series.ewm(df[::-1],span=n, adjust=True).mean()
#filtered = np.stack(( fwd, bwd[::-1] ))
#filtered = np.mean(filtered, axis=0)
fwd = df['Range'].ewm(span=n, adjust=True).mean()
bwd = df['Range'][::-1].ewm(span=n, adjust=True).mean()
newDF = pd.DataFrame()
newDF['fwd'] = fwd
newDF['bwd'] = bwd
meanDF = newDF.mean(axis=1)


# do more bere
plt.subplot(3,1,1)
plt.plot(x,y)
plt.xlabel('Time')
plt.ylabel('Range')
plt.title('Raw Position Data')
plt.subplot(3,1,2)
plt.title('Smoothed and Raw Data')
plt.plot(x,y, color = 'orange')
plt.plot(x,meanDF, color='green')
plt.plot(x,fwd, color='red')
plt.plot(x[::-1],bwd, color='blue')
plt.legend()
plt.xlabel('Time')
plt.ylabel('Distance')
plt.tight_layout()

#calculate and plot velocity from smoothed data
velocity_meanDF = ((meanDF - meanDF.shift(1)) / (df['Time'] - df['Time'].shift(1)))

plt.subplot(3,1,3)
plt.title('Velocity from Smoothed Position Data')
plt.plot(x,velocity_meanDF)
plt.xlabel('Time')
plt.ylabel('Velocity')

""" this is code for plotting velocity from raw position data that may or may not be working currently
df['Velocity'] = ((df['Range'] - df['Range'].shift(1)) / (df['Time'] - df['Time'].shift(1)))
y2 = df['Velocity']
m = 10
fwd2 = pd.Series.ewm(df.Velocity,span=m, adjust=True).mean()
bwd2 = pd.Series.ewm(df.Velocity[::-1],span=m, adjust=True).mean()
filtered2 = np.stack(( fwd2, bwd2[::-1] ))
filtered2 = np.mean(filtered2, axis=0)
plt.subplot(2,1,2)
plt.title('velocity smoothed and raw data')
plt.plot(y2, color = 'orange')
plt.plot(filtered2, color='green')
plt.plot(fwd2, color='red')
plt.plot(bwd2, color='blue')
plt.xlabel('time')
plt.ylabel('velocity')
plt.tight_layout()
#smoothed_velocity = ((df.filtered - df.filtered.shift(1)) /  df['Time'] - df['Time'].shift(1))
#print(smoothed_velocity)
#plt.subplot (2,2,3)
#plt.title ('smoothed velocity')
#plt.plot (smoothed_velocity, color = 'orange')
"""
plt.tight_layout()
plt.show()
