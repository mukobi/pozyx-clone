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

root = tk.Tk()



def fit(g, mass, xSectionArea, firstRow, lastRow, infile, someNumber):
    g = float(g_input.get())
#    tk.messagebox.showinfo("Gravity = ", g)



    mass = float(mass_input.get())
#    tkMessageBox.showinfo("Mass (kg) = ", mass)


    Fg = g * mass
    rho = 1.225

    xSectionArea = float(xSectionArea_input.get())
#    tkMessageBox.showinfo("cross section area = ", root)



    firstRow = float(firstRow_input.get())
#    tkMessageBox.showinfo("first row:", root)



    lastRow = float(lastRow_input.get())
#    tkMessageBox.showinfo("last row:", root)
    rows = slice(firstRow, lastRow, 1)

    upperC = float(uc_input.get())
    lowerC = float(lc_input.get())
    upperV = float(uv_input.get())
    lowerV = float(lv_input.get())

    df=pd.read_csv(infile, delimiter=',', usecols = [0,1,28])

    df.columns = ['index', 'time', 'range']


    df2 = df.ix[rows].dropna() #index range pertaining to data of interest

    xa=df2['time'].values
    xi = xa[0] # when was the ball released?
    x_final = xa[-1] - xi # sets land time assuming drop time is zero
    x2 = xa - xi # sets release time to zero

    da=df2['range'].values*someNumber.get()
    di = da[0] # when was the ball released?
    d_final = da[-1] - di # sets land time assuming drop time is zero
    d2 = da - di # sets release time to zero

    t0_new = x2[0]
    xdata = np.array([x2,x2])


    dtGlobal = 0.0000001
    dtGlobal = 0.001

    unitConv = 1000 # convert model units from meters to mm

    xx3 = np.linspace(x2[0],x2[-1],100)

    def func3(t, vel, drag):
        dt = dtGlobal
        vel = vel
        x=0                 # initial position
        t_curr = t0_new     # inital time
        xlist = [x]
        a=g

    # fix for scalar input
        if not hasattr(t, '__len__') :
            tlist = [0,t]       # make a list out of a single target t value
        else :
            tlist = t

        i = 1           # list index, initialized to 1 since i=0 is initial time, which we already have
        while not isclose(t_curr, tlist[-1], abs_tol=dt) :
            t_curr += dt
            x = x + vel * dt + (1/2) * a * dt**2
            vel = vel + a * dt

            if vel < 0:
                dragForce = -(drag*((rho*(vel)**2)/2)*xSectionArea)
            else:
                dragForce = drag*((rho*vel**2)/2)*xSectionArea
            a = (Fg-dragForce)/mass


            t_next = tlist[i]

            if isclose(t_curr, t_next,abs_tol=dt) :
                xlist.append(x)
                i+=1        # go to next target time in list

        return np.array(xlist)*unitConv


    popt, pcov = curve_fit(func3, x2, d2, bounds=([lowerV,lowerC], [upperV,upperC]))
    plt.figure()
    x_filt = d2[d2 >= 0]
    plt.plot(x2,d2,'o', label = 'experimental data')
    plt.plot(xx3, func3(xx3, *popt),
        label='fit: initial velocity=%5.3f, drag coefficient=%5.3f' % tuple(popt))
    plt.legend()
    print('here')
    plt.show()


def browse():
    global infile #used so that only infile information is fetched instead of executing it directly.
    infile = askopenfilename()

#label = tk.Label(root, text = "This program optimizes initial velocity and drag coefficient") #writes a text on the box
#label.grid(row = 0, column = 1) #used to pack the file in it. Without this, no text will appear

browseButton = tk.Button(root, text = "Browse", command=browse) #used to create a button
browseButton.grid(row = 1, column = 1) #used to pack it in. Without it, the button won't appear


g_input = tk.Entry(root)

mass_input = tk.Entry(root)

xSectionArea_input = tk.Entry(root)

firstRow_input = tk.Entry(root)

lastRow_input = tk.Entry(root)

uc_input = tk.Entry(root, width=5)

lc_input = tk.Entry(root, width=5)

lv_input = tk.Entry(root, width=5)

uv_input = tk.Entry(root, width=5)

fitButton = tk.Button(root, text="fit data", command=fit)

#options = tk.Frame(root)

Label(root, text="Velocity Bounds:").grid(row = 5, column = 4)
lv_input.grid(row = 5, column = 5)
uv_input.grid(row = 5, column = 6)

Label(root, text="Drag Coeff. Bounds:").grid(row = 6, column = 4)
lc_input.grid(row = 6, column = 5)
uc_input.grid(row = 6, column = 6)


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

fitButton.grid(row = 7, column = 1)

root.mainloop()
