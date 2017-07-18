import pandas as pd
import matplotlib.pyplot as plt



df=pd.read_csv('/Users/CoraJune/Documents/GitHub/Pozyx/Data/FrisbeeTestAltered.txt', header=None, delimiter=' ', usecols=[2,16], names=['Time','Angular Velocity'])


ax = df.plot.line(x='Time', y='Angular Velocity', linewidth=1,  title='Angular Velocity')
ax.set_xlabel("Time")
ax.set_ylabel("Angular Velocity")
ax.plot()
plt.show()

df1=df.diff(1,0)['Angular Velocity']
ax1=df1.plot.line(x=2, y='Angular Velocity', linewidth=1, title='Angular Acceleration')

ax1.set_xlabel("Time")
ax1.set_ylabel("Angular Acceleration")
ax1.plot()
plt.show()

