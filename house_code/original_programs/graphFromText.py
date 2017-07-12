import pandas as pd
import matplotlib.pyplot as plt


headers = ['X','Y']


df=pd.read_csv('/Users/CoraJune/Documents/GitHub/Pozyx/house code/tutorials altered/FrisbeeFast1.txt', header=None, delimiter=' ', usecols=[2,16])


ax = df.plot.scatter(x=2, y=16, marker='.',  title='Angular Velocity')
ax.set_xlabel("Time")
ax.set_ylabel("Angular Velocity")


print(df)
plt.show()


df1=pd.read_csv('/Users/CoraJune/Desktop/HomeData/151g.txt', header=None, delimiter=' ', usecols=[2,16])
ax1=df1.plot.scatter(x=2, y=16, marker='.', title='Angular Velocity 2')

plt.show()

