import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df=pd.read_csv('/Users/CoraJune/Documents/HomeData/rocket/rocket_4096_oct24_3.csv', delimiter=',', usecols=[1, 5, 9, 10, 11, 15, 16, 17, 25, 26, 27, 28])

df.columns = ['time', 'pressure', 'magx', 'magy', 'magz', 'heading', 'roll', 'pitch', 'gravx', 'gravy', 'gravz', 'dist']

df2 = df.ix[170:213]

x=df['time']
d=df['dist']
p=df['pressure']
mx=df['magx']
my=df['magy']
mz=df['magz']
h=df['heading']
pi=df['pitch']
r=df['roll']
gx=df['gravx']
gy=df['gravy']
gz=df['gravz']

x2=df2['time']
d2=df2['dist']
p2=df2['pressure']
mx2=df2['magx']
my2=df2['magy']
mz2=df2['magz']
h2=df2['heading']
pi2=df2['pitch']
r2=df2['roll']
gx2=df2['gravx']
gy2=df2['gravy']
gz2=df2['gravz']

plt.subplot(1,1,1)
plt.tick_params(labelsize=6)
plt.plot(x2, d2, 'o')
z = np.polyfit(x2, d2, 2)
p = np.poly1d(z)
plt.plot(x,p(x),"--")

print(df2.dist.dtype)

equation = "y = %.6f x^2 + %.6f x + %.6f"%(z[0],z[1],z[2])

print(equation)

gravity = z[0]*2

print(gravity)

#plt.figtext(.502,.1, equation,  style='italic', size=10)

plt.show()
