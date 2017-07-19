import pandas as pd
import matplotlib.pyplot as plt
from pandas import Series

headers=['Time', 'Linear-Acceleration-X']

df=pd.read_csv('/Users/CoraJune/Documents/GitHub/Pozyx/Data/testing_files_1.txt', delimiter=' ',  usecols=['Time','Linear-Acceleration-X','Acceleration-X','Linear-Acceleration-Y','Acceleration-Y','Linear-Acceleration-Z','Acceleration-Z'])

x=df['Time']
y1=df['Linear-Acceleration-X']
y2=df['Acceleration-X']
plt.plot(x,y1)
plt.plot(x,y2)
plt.show()

x=df['Time']
y3=df['Linear-Acceleration-Y']
y4=df['Acceleration-Y']
plt.plot(x,y3)
plt.plot(x,y4)
plt.show()

x=df['Time']
y5=df['Linear-Acceleration-Z']
y6=df['Acceleration-Z']
plt.plot(x,y5)
plt.plot(x,y6)
plt.show()

print(df)

ax = df.plot.scatter(x='Time', y='Linear-Acceleration-X', s=1,  title='Linear-Acceleration-X')
ax.set_xlabel("Time")
ax.set_ylabel("Acceleration-X")
ax.plot()
plt.show()

df=pd.read_csv('/Users/CoraJune/Documents/GitHub/Pozyx/Data/acceleration_test_still.txt', delimiter=' ',  usecols=['Time','Linear-Acceleration-Y'])


ax1 = df.plot.scatter(x='Time', y='Linear-Acceleration-Y', s=1,  title='Linear-Acceleration-Y')
ax.set_xlabel("Time")
ax.set_ylabel("Acceleration-Y")
ax.plot()
plt.show()

df=pd.read_csv('/Users/CoraJune/Documents/GitHub/Pozyx/Data/acceleration_test_still.txt', delimiter=' ',  usecols=['Time','Linear-Acceleration-Z'])


ax2 = df.plot.scatter(x='Time', y='Linear-Acceleration-Z', s=1,  title='Linear-Acceleration-Z')
ax2.set_xlabel("Time")
ax2.set_ylabel("Acceleration-Z")
ax2.plot()
plt.show()

df.plot()



#df1=df.diff(1,0)['Angular Velocity']
#ax1=df1.plot.line(x=2, y='Angular Velocity', linewidth=1, title='Angular Acceleration')

#ax1.set_xlabel("Time")
#ax1.set_ylabel("Angular Acceleration")
#ax1.plot()
#plt.show()


