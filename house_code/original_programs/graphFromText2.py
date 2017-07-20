import pandas as pd
import matplotlib.pyplot as plt



#df=pd.read_csv('/Users/CoraJune/Documents/GitHub/Pozyx/Data/Motor_Turntable/rps_motor_turntable_1.txt', delimiter=' ',  usecols=['Time','RPS','Rotations'])
df=pd.read_csv('/Users/CoraJune/Documents/GitHub/Pozyx/Data/Motor_Turntable/motorturntable4.txt', delimiter=' ',  usecols=['Time','Linear-Acceleration-X','Acceleration-X','Linear-Acceleration-Y','Acceleration-Y','Linear-Acceleration-Z','Acceleration-Z','Magnetic-X','Magnetic-Y','Magnetic-Z','Heading'])


x=df['Time']
y1=df['Magnetic-X']
y2=df['Magnetic-Y']
plt.subplot(3,1,1)
plt.plot(x,y1)
plt.plot(x,y2)
plt.xlabel('Time')
plt.legend( loc=2, prop={'size': 4})


x=df['Time']
y3=df['Linear-Acceleration-Y']
y4=df['Acceleration-Y']
plt.subplot(3,1,2)
plt.plot(x,y3)
plt.plot(x,y4)
plt.xlabel('Time')
plt.legend( loc=2, prop={'size': 4})



x=df['Time']
y5=df['Linear-Acceleration-Z']
y6=df['Acceleration-Z']
plt.subplot(3,1,3)
plt.plot(x,y5)
plt.plot(x,y6)
plt.xlabel('Time')
plt.legend( loc=2, prop={'size': 4})


plt.show()
#print(df)

ax = df.plot.scatter(x='Time', y='Linear-Acceleration-X', s=1,  title='Linear-Acceleration-X')
ax.set_xlabel("Time")
ax.set_ylabel("Acceleration-X")
ax.plot()
plt.show()

df=pd.read_csv('/Users/CoraJune/Documents/GitHub/Pozyx/Data/pressure_test_srtc_2.txt', delimiter=' ',  usecols=['Time','Pressure'])

print(df.columns)
ax1 = df.plot.line(x='Time', y='Pressure', linewidth=1,  title='Pressure')
ax1.set_xlabel("Time")
ax1.set_ylabel("Pressure")
ax1.plot()
plt.show()

df=pd.read_csv('/Users/CoraJune/Documents/GitHub/Pozyx/Data/acceleration_test_still.txt', delimiter=' ',  usecols=['Time','Linear-Acceleration-Z'])


ax2 = df.plot.line(x='Time', y='Linear-Acceleration-Z', s=1,  title='Linear-Acceleration-Z')
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


