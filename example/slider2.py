from matplotlib.widgets import Slider  # import the Slider widget

import numpy as np
import matplotlib.pyplot as plt
from math import pi
from physProps import *
from functions import models



g = -9.81
Fg = g * blueBall.mass
rho = 1.225

df=pd.read_csv('blue_drop.csv', delimiter=',', usecols = [0,1,28])

df.columns = ['index', 'time', 'range']


df2 = df.ix[415:456].dropna() #index range pertaining to data of interest

xa=df2['time'].values
xi = xa[0] # when was the ball released?
x_final = xa[-1] - xi # sets land time assuming drop time is zero
x2 = xa - xi # sets release time to zero

da=df2['range'].values*-0.001
di = da[0] # when was the ball released?
d_final = da[-1] - di # sets land time assuming drop time is zero
d2 = da - di # sets release time to zero

################################### create the models ################################
c_min = 0    # the minimial value of the paramater a
c_max = 1   # the maximal value of the paramater a
c_init = 0   # the value of the parameter a to be used initially, when the graph is created

x = x2

fig = plt.figure(figsize=(8,3))

# first we create the general layount of the figure
# with two axes objects: one for the plot of the function
# and the other for the slider
sin_ax = plt.axes([0.1, 0.2, 0.8, 0.65])
slider_ax = plt.axes([0.1, 0.05, 0.8, 0.05])


# in plot_ax we plot the function with the initial value of the parameter a
plt.axes(sin_ax) # select sin_ax
#    plt.title()

import pdb;pdb.set_trace()
model_plot, = plt.plot(x2, models.Position, 'r')

# here we create the slider
c_slider = Slider(slider_ax,      # the axes object containing the slider
                  'Cd',            # the name of the slider parameter
                  c_min,          # minimal value of the parameter
                  c_max,          # maximal value of the parameter
                  valinit=c_init  # initial value of the parameter
                )

# Next we define a function that will be executed each time the value
# indicated by the slider changes. The variable of this function will
# be assigned the value of the slider.

def update(c):
    model_plot.set_ydata(models.Position.x_mod) # set new y-coordinates of the plotted points
    fig.canvas.draw_idle()          # redraw the plot

# the final step is to specify that the slider needs to
# execute the above function when its value changes
c_slider.on_changed(update)

plt.show()
