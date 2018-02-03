import tkinter as tk
import sys
import os
from tkinter import *
import pandas as pd
import matplotlib as mpl
mpl.use('TkAgg')
import matplotlib.pyplot as plt
import numpy as np
import scipy.optimize as opt
from math import isclose
from scipy.optimize import curve_fit
from scipy import stats
from tkinter.filedialog import askopenfilename
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure

##################################################################################3####

root = tk.Tk()
root.title('Modeling Application')

def modelPosition():
    g = float(g_input.get())
    mass = float(mass_input.get())
    Fg = g * mass
    rho = 1.225
    xSectionArea = float(xSectionArea_input.get())
    firstRow = float(firstRow_input.get())
    lastRow = float(lastRow_input.get())
    rows = slice(firstRow, lastRow, 1)
    vi = 18
    rows = slice(firstRow, lastRow, 1)

    df=pd.read_csv(infile, delimiter=',', usecols = [0,1,28])
    df.columns = ['index', 'time', 'range']

    df2 = df.ix[rows].dropna() #index range pertaining to data of interest

    xa=df2['time'].values
    xi = xa[0] # when was the ball released?
    x_final = xa[-1] - xi # sets land time assuming drop time is zero
    x2 = xa - xi # sets release time to zero

    da=df2['range'].values*-1
    di = da[0] # when was the ball released?
    d_final = da[-1] - di # sets land time assuming drop time is zero
    d2 = da - di # sets release time to zero

    C1 = float(C1_input.get())
    C2 = float(C2_input.get())
    C3 = float(C3_input.get())

    N = 100 # allows you to create each model out of 100 points
    model_times = np.linspace(x2[0], x2[-1], 100)   # create array of 100 times within experimental timeframe for the modeled positions

    x_mod = np.zeros(shape=(N))   # create empty array with space for 100 elements
    v_mod = np.zeros(shape=(N))
    a_mod = np.zeros(shape=(N))
    dragForce = np.zeros(shape=(N))
    dt = ( x2[-1]-x2[0] ) / N

    plt.figure()

    plt.plot(x2, d2, 'C3', marker = 'o', linestyle="None")
    c_vect = np.array([C1, C2, C3])
#    c_vect = np.array([0,0.2,0.4])
    for c in range(3) :
        x_mod[0] = 0    # initial position of zero
        v_mod[0] = vi    # initial velocity of zero
        dragForce[0] = xSectionArea * 0.5 * c_vect[c] * rho * v_mod[0]**2   # initial drag force
        a_mod[0] = ( Fg-dragForce[0] ) / mass  # initial acceleration based on initial drag force
        n=0
        print(c_vect[c])
        for n in range(0,N-1):
            x_mod[n+1] = x_mod[n]  + v_mod[n] * dt  + (1/2) * (a_mod[n]) * dt**2 # simply y=x + v*t + (1/2)*a*t^2
            v_mod[n+1] = v_mod[n] + a_mod[n] * dt # updated velocity is v + a*t

            if v_mod[n] < 0 :
                dragForce[n+1] = -( c_vect[c]*( (rho*v_mod[n]**2) /2 ) * xSectionArea ) # if/else may not be necessary

            else:
                dragForce[n+1] = c_vect[c]*( (rho*v_mod[n]**2) /2 ) * xSectionArea

            a_mod[n+1] = ( Fg-dragForce[n+1] ) / mass  # update acceleration with updated drag force
        #    print(a_mod)
            n = n+1
#        import pdb; pdb.set_trace()

            #plot the model results

        plt.plot(model_times, x_mod, label='$C_d={}$'.format(c_vect[c]))
    plt.xlabel("Time (s)", fontsize=15)
    plt.ylabel("Position (m/s)", fontsize=15)
    plt.title("Position (Initial Velocity: {} m/s)".format(vi), fontsize=20)
    plt.tick_params(labelsize='large')
    plt.legend()

    plt.show()



def browse():
    global infile #used so that only infile information is fetched instead of executing it directly.
    infile = askopenfilename()





browseButton = tk.Button(root, text = "Browse", command=browse) #used to create a button
browseButton.grid(row = 1, column = 1) #used to pack it in. Without it, the button won't appear


g_input = tk.Entry(root)

mass_input = tk.Entry(root)

xSectionArea_input = tk.Entry(root)

firstRow_input = tk.Entry(root)

lastRow_input = tk.Entry(root)

Label(root, text="Gravity (Earth=-9.81)").grid(row = 2, column = 0)
g_input.grid(row = 2, column = 1)

Label(root, text="Mass").grid(row = 3, column = 0)
mass_input.grid(row = 3, column = 1)


Label(root, text="Cross Sectional Area").grid(row = 4, column = 0)
xSectionArea_input.grid(row = 4, column = 1)


Label(root, text="First Data Line").grid(row = 5, column = 0)
firstRow_input.grid(row = 5, column = 1)


Label(root, text="Last Data Line").grid(row = 6, column = 0)
lastRow_input.grid(row = 6, column = 1)

C1_input = tk.Entry(root, width=5)
Label(root, text="C1").grid(row = 8, column = 0)
C1_input.grid(row = 8, column = 1)

C2_input = tk.Entry(root, width=5)
Label(root, text="C2").grid(row = 9, column = 0)
C2_input.grid(row = 9, column = 1)

C3_input = tk.Entry(root, width=5)
Label(root, text="C3").grid(row = 10, column = 0)
C3_input.grid(row = 10, column = 1)

positionButton = tk.Button(root, text="model position", command=modelPosition)

positionButton.grid(row = 11, column = 1)


root.mainloop()
