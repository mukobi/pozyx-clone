''' Present an interactive function explorer with slider widgets.
Scrub the sliders to change the properties of the ``sin`` curve, or
type into the title text box to update the title of the plot.
Use the ``bokeh serve`` command to run the example by executing:
    bokeh serve sliders.py
at your command prompt. Then navigate to the URL
    http://localhost:5006/sliders
in your browser.
'''
import numpy as np

from bokeh.io import curdoc
from bokeh.layouts import row, widgetbox
from bokeh.models import ColumnDataSource
from bokeh.models.widgets import Slider, TextInput
from bokeh.plotting import figure
from physProps import *
# Set up data

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


N = 100 # allows you to create each model out of 100 points

model_times = np.linspace(x2[0], x2[-1], 100)   # create array of 100 times within experimental timeframe for the modeled positions
x_mod = np.zeros(shape=(N))   # create empty array with space for 100 elements
v_mod = np.zeros(shape=(N))
a_mod = np.zeros(shape=(N))
dragForce = np.zeros(shape=(N))
dt = ( x2[-1]-x2[0] ) / N

#plt.figure()
#plt.plot(x2,d2, 'C7', marker = 'o', linestyle="None")
c_vect = np.array([0,0.651,1])
#for c in range(3) :
x_mod[0] = 0    # initial position of zero
v_mod[0] = 0    # initial velocity of zero

drag_coeff = 0
dragForce[0] = blueBall.xSectionArea * 0.5 * drag_coeff * rho * v_mod[0]**2   # initial drag force
a_mod[0] = ( Fg-dragForce[0] ) / blueBall.mass  # initial acceleration based on initial drag force

n=0
for n in range(0,N-1):
    x_mod[n+1] = x_mod[n]  + v_mod[n] * dt  + (1/2) * (a_mod[n]) * dt**2 # simply y=x + v*t + (1/2)*a*t^2
    v_mod[n+1] = v_mod[n] + a_mod[n] * dt # updated velocity is v + a*t

    if v_mod[n] < 0 :
        dragForce[n+1] = -( drag_coeff*( (rho*v_mod[n]**2) /2 ) * blueBall.xSectionArea ) # if/else may not be necessary

    else:
        dragForce[n+1] = drag_coeff*( (rho*v_mod[n]**2) /2 ) * blueBall.xSectionArea

    a_mod[n+1] = ( Fg-dragForce[n+1] ) /blueBall.mass  # update acceleration with updated drag force
#    print(a_mod)
    n = n+1






x = model_times
y = x_mod
source = ColumnDataSource(data=dict(x=model_times, y=x_mod))


# Set up plot
plot = figure(plot_height=400, plot_width=400, title="my sine wave",
              tools="crosshair,pan,reset,save,wheel_zoom")

plot.line('x', 'y', source=source, line_width=3, line_alpha=0.6)


# Set up widgets
#text = TextInput(title="title", value='my sine wave')
drag_coeff = Slider(title="Drag Coefficient", value=0.0, start=0, end=1, step=0.01)
#amplitude = Slider(title="amplitude", value=1.0, start=-5.0, end=5.0, step=0.1)
#phase = Slider(title="phase", value=0.0, start=0.0, end=2*np.pi)
#freq = Slider(title="frequency", value=1.0, start=0.1, end=5.1, step=0.1)


# Set up callbacks
#def update_title(attrname, old, new):
 #   plot.title.text = text.value

#text.on_change('value', update_title)

def update_data(attrname, old, new):

    # Get the current slider values
    c = drag_coeff.value
#    b = offset.value
#    w = phase.value
#    k = freq.value

    # Generate the new curve
    x = model_times
    y = x_mod

    source.data = dict(x=x, y=y)

for c in [drag_coeff]:
    c.on_change('value', update_data)


# Set up layouts and add to document
inputs = widgetbox(drag_coeff)

curdoc().add_root(row(inputs, plot, width=800))
curdoc().title = "Sliders"

