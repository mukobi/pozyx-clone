import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import scipy.optimize as opt
from scipy.optimize import curve_fit
from math import pi
#################################################### parameters ##########################################
ti = 11.039127 # when did the rocket take off?
tf = 14.669509 #when did the rocket hit the ground?
t = 14.669509-11.039127 # how long wasa object in the air?

s = 2052.0-368.0 # FOR 1D VERTICLE MOTION ONLY how much did rocket shift in meters (final position - initial position)

n = 3.636 # to start newRange at zer

##################### parameters for drag force ##########################################################
diameter = 0.008107319666 # diameter of object
radius = 1/2 * diameter
A = pi*radius**2 # cross sectional area in meters
v = 16 # initial velocity
#v = 17.740803207
#vsq = v**2 # maximum velocity during free fall
rho = 1.225 # density of air at sea level at 20 degrees C
m = 0.227 # mass of the object in kg
g = 9.81
Fg = -m*g

#dragForce = C1*((rho*v**2)/2)*A
#adrag = (Fg-dragForce)/m # acceleration calculated from dragForce
#print('dragForce = {}'.format(dragForce))
#print('adrag = {}'.format(adrag))
##########################################################################################################
##########################################################################################################
df=pd.read_csv('rocket_4096_oct24_3.csv', delimiter=',', usecols = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28])

df.columns = ['index', 'time', 'difference', 'hz', 'avgHz', 'pressure', 'acceleration-x', 'acceleration-y', 'acceleration-z', 'magnetic-x', 'magnetic-y', 'magnetic-z', 'angularVelocity-x', 'angularVelocity-y', 'angularVelocity-z', 'heading', 'roll', 'pitch', 'quaternion-x', 'quaternion-y', 'quaternion-z', 'quaternion-w', 'linearAcceleration-x', 'linearAcceleration-y', 'linearAcceleration-z', 'gravity-x', 'gravity-y', 'gravity-z', 'range']

#df2 = df.ix[166:216].dropna() #index pertaining to rocket's motion

df2 = df.ix[166:216].dropna()
df3 = df.ix[168:216].dropna() # for newRange calculations
df4 = df.ix[169:214].dropna()

############################################# entire data set ###########################################
x=df['time'].values
d=df['range'].values
p=df['pressure'].values
mx=df['magnetic-x'].values
my=df['magnetic-y'].values
mz=df['magnetic-z'].values
heading=df['heading'].values
pitch=df['pitch'].values
roll=df['roll'].values
gx=df['gravity-x'].values
gy=df['gravity-y'].values
gz=df['gravity-z'].values
##########################################################################################################

######################################### data pertaining to rocket's motion #############################
xa=df2['time'].values
x2 = xa - ti
d2=df2['range'].values
p2=df2['pressure'].values
ax2=df2['linearAcceleration-x'].values * 0.01
ay2=df2['linearAcceleration-y'].values * 0.01
az2=df2['linearAcceleration-z'].values * 0.01

Ax2=df2['acceleration-x'].values * 0.01
Ay2=df2['acceleration-y'].values * 0.01
Az2=df2['acceleration-z'].values * 0.01

mx2=df2['magnetic-x'].values
my2=df2['magnetic-y'].values
mz2=df2['magnetic-z'].values
heading2=df2['heading'].values
pitch2=df2['pitch'].values
roll2=df2['roll'].values
gx2=df2['gravity-x'].values * 0.01
gy2=df2['gravity-y'].values * 0.01
gz2=df2['gravity-z'].values * 0.01
qx2=df2['quaternion-x'].values
qy2=df2['quaternion-y'].values
qz2=df2['quaternion-z'].values
qw2=df2['quaternion-w'].values
##########################################################################################################
x3=df3['time'].values
d3=df3['range'].values
p3=df3['pressure'].values
mx3=df3['magnetic-x'].values
my3=df3['magnetic-y'].values
mz3=df3['magnetic-z'].values
heading3=df3['heading'].values
pitch3=df3['pitch'].values
roll=df3['roll'].values
gx3=df3['gravity-x'].values
gy3=df3['gravity-y'].values
gz3=df3['gravity-z'].values

ax4=df4['linearAcceleration-x'].values
ay4=df4['linearAcceleration-y'].values
x44=df4['time'].values

x6 = df2['time'].ix[169:216].values # time frame for velocity plot and models
####################################### for calculating new range #########################################
dt = t # rocket's time in the air

new_v=s/dt # for discounting horizontal motion
new_x=new_v*dt # for discounting horizontal motion

newd = np.sqrt(d2**2-new_x**2) # total range discounting horizontal motion
newRange = newd[~np.isnan(newd)]

df3['newRange'] = newRange
velocity = (np.ediff1d(newRange) / np.ediff1d(x3) ) * 0.001 # velocity from new range
################################# plot the raw data within motion parameters #############################

def func(x,a,b,c):
    return a*(x**2) + b*x + c
pfit, success = opt.curve_fit(func,x2,d2)
xx = np.linspace(0,3.63038170e+00,100)
print('raw range coeffs: {}'.format(pfit))
plt.figure()
plt.subplot(1,1,1)
plt.tick_params()
plt.title('Raw Range')
plt.xlabel('Time (s)')
plt.ylabel('Distance (m)')
plt.plot(x2, d2, 'o')
plt.plot(xx,func(xx,*pfit),'--', alpha=.8)
gravity = 'a = {} m/s$^2$'.format(np.around(4592.73*2*0.001, 2))
print(gravity)
plt.figtext(0.45,0.20, gravity, style='italic')
plt.tight_layout()


############################################### plot euler angles #########################################
#import pdb; pdb.set_trace()
plt.figure()
plt.subplot(1,1,1)
plt.title('Euler Angles')
plt.tick_params()
plt.plot(x2, heading2, '-o', label='yaw')
plt.plot(x2, pitch2, '-o', label='roll')
plt.plot(x2, roll2,'-o', label='pitch')
plt.xlabel('Time (s)')
plt.ylabel('Angle ($^\circ$)')
plt.legend()
plt.tight_layout()
###########################################################################################################

################################################## plot gravity ###########################################
plt.figure()
plt.subplot(1,1,1)
plt.title('Gravity')
plt.xlabel('Time (s)')
plt.ylabel('Gravity (m/s$^2$)')
plt.plot(x2, gx2, '-o', label='x')
plt.plot(x2, gy2, '-o', label='y')
plt.plot(x2, gz2,'-o', label='z')
plt.legend()
plt.tight_layout()
#######################################################################################################3###

################################################ plot  linear acceleration ################################
plt.figure()
plt.subplot(1,1,1)
plt.title('Linear Acceleration')
plt.tick_params()
plt.xlabel('Time (s)')
plt.ylabel('Linear Acceleration (m/s$^2$)')
plt.plot(x2, ax2, '-o',label='x')
plt.plot(x2, ay2, '-o',label='y')

plt.plot(x2, az2,'-o', label='z')
plt.legend()
plt.tight_layout()

############################################################################################################

############################################## plot mapped changes in acceleration ########################
df4=df.ix[169:214].copy()

x7_mod = df['time'].ix[169:214].values
df4['x7_mod'] = x7_mod


newRange_mod = df['range'].ix[169:214].values*0.001


adj_newRange_mod = newRange_mod  - n
df4['adj_newRange_mod'] = adj_newRange_mod

#adj_newRange_mod = newRange_mod

adj_x7_mod = x7_mod - ti
df4['adj_x7_mod']= adj_x7_mod

z = np.polyfit(adj_x7_mod, adj_newRange_mod, 2)
rDFabove10m = df4[df4['adj_newRange_mod'] > 6]
rDFabove12m = df4[df4['adj_newRange_mod'] > 10]
#rDFabove10m = df4['adj_newRange_mod'] > 10000
#rDFabove12m = df4['adj_newRange_mod'] > 12000

#import pdb; pdb.set_trace()
rocketZ10m = np.polyfit(rDFabove10m['time'],rDFabove10m['adj_newRange_mod'],2)
rocketZ12m = np.polyfit(rDFabove12m['time'],rDFabove12m['adj_newRange_mod'],2)

glist = list( map(lambda x0: x0*2, [z[0], rocketZ10m[0], rocketZ12m[0]]) )
for g in glist:
    print( 'g = {:g}'.format(g) )


x4 = rDFabove10m.adj_x7_mod.values
d4 = rDFabove10m.adj_newRange_mod.values
x5 = rDFabove12m.adj_x7_mod.values
d5 = rDFabove12m.adj_newRange_mod.values

plt.figure()
plt.subplot(1,1,1)
plt.tick_params()
plt.title('Mapped Changes in Acceleration')
plt.xlabel('Time (s)')
plt.ylabel('Distance (m)')
plt.plot(adj_x7_mod,adj_newRange_mod,'o',label= '$d>0m$')
plt.plot(x4,d4,'o', label = '$d>6m$')
plt.plot(x5,d5,'o', label = '$d>10m$')
plt.legend()
zero = '$d>0m:$ a = {} m/s$^2$'.format(np.around(9419.34*0.001, 2))
ten = '$d>6m$: a = {} m/s$^2$'.format(np.around(9.73394, 2))
twelve = '$d>10m$: a = {} m/s$^2$'.format(np.around(9.77461, 2))
plt.figtext(0.32,0.35, zero, style='italic')
plt.figtext(0.32,0.25, ten, style='italic')
plt.figtext(0.32,0.15, twelve, style='italic')
plt.tight_layout()
###############################################################################################################

############################################# plot newRange ###################################################
def func1(x,a,b,c):
    return a*(x**2) + b*x + c
pfit1, success1 = opt.curve_fit(func1,x3,newRange)
xx3 = np.linspace(11.171177,14.669509,38)

print('pfit1 coeffs: {}'.format(pfit1))
plt.figure()
plt.subplot(1,1,1)
plt.tick_params()
plt.title('New Range')
plt.plot(x3, newRange,'o')
plt.plot(xx3,func1(xx3,*pfit1),'--', alpha=.8)
plt.xlabel('Time')
plt.ylabel('Distance')
z = np.polyfit(x3, newRange, 2)
newGravity = 'g = {}'.format(4709.66938958*2*0.001)
plt.figtext(0.45,0.15, newGravity, style='italic')
plt.tight_layout()
###############################################################################################################

################################################## plot pressure ##############################################
def func4(x,a,b,c):
    return a*(x**2) + b*x + c
pfit4, success4 = opt.curve_fit(func4,x2,p2)
xx3 = np.linspace(0,3.63038170e+00,100)

plt.figure()
plt.subplot(1,1,1)
plt.tick_params()
plt.title('Pressure')
plt.xlabel('Time (s)')
plt.ylabel('Pressure (Pa)')
plt.plot(x2, p2, 'o')
plt.plot(xx3,func(xx3,*pfit4),'--', alpha=.8)
plt.tight_layout()
###############################################################################################################

############################################## print newRange velocity ########################################
plt.figure()
plt.subplot(1,1,1)
plt.tick_params()
plt.title('Velocity')
plt.xlabel('Time (s)')
plt.ylabel('Velocity (mm/s)')
plt.plot(x6,velocity,'o')

def func3(x,a,b):
    return a*x + b
popt3, success3 = opt.curve_fit(func3,x6,velocity)

z = np.polyfit(x6, velocity, 1)
p = np.poly1d(z)

vequation = "y = %.6f x + %.6f"%(z[0],z[1])
plt.figtext(.15,.25,vequation, style='italic')
print('new velocity: {}'.format(vequation))
print('new velocity g = {}'.format(z[0]))

plt.plot(x6,func3(x6,*popt3),'--', label='{}'.format(vequation), alpha=0.8)
plt.legend()
plt.tight_layout()
#################################################################################################################
x7_mod = df['time'].ix[169:214].values
x7_vel_mod = df['time'].ix[170:214].values

newRange_mod = df['range'].ix[169:214].values*0.001

adj_newRange_mod = newRange_mod  - 3.636

#adj_newRange_mod = newRange_mod

adj_x7_mod = x7_mod - 11.23917484

adj_x7_vel_mod = x7_vel_mod - 11.17117691

xx7 = np.linspace(2.83447221e-09,3.29492307e+00,100)

vel = (np.ediff1d(adj_newRange_mod) / np.ediff1d(adj_x7_mod))

#import pdb; pdb.set_trace()
#import pdb; pdb.set_trace()
N = 100
####################################################### try C1 ##############################################
x_mod=np.zeros(shape=(N))
v_mod=np.zeros(shape=(N))
a_mod=np.zeros(shape=(N))
dragForce=np.zeros(shape=(N))

c_vect = [0,0.1,0.2,0.3,0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]    # drag coefficients to try
plt.figure()
plt.plot(adj_x7_mod,adj_newRange_mod,'o', label='$experimental\ data$') # plot experimental data

for c_vect in range(len(c_vect)) :
    x_mod[0] = 0    # initial position
    v_mod[0] = v    # initial velocity
    dragForce[0] = c_vect*((rho*v_mod[0]**2)/2)*A   # initial drag forcw
    a_mod[0] = (Fg-dragForce[0])/m  # initial acceleration
    n=0

    for n in range(0,N-1):
        x_mod[n+1] = x_mod[n] + v_mod[n] * 3.29492307e+00/100+ (1/2) * (a_mod[n]) * (3.29492307e+00/100)**2 # y = x + vt + (1/2) at^2 for new position
        v_mod[n+1] = v_mod[n] + a_mod[n] * 3.29492307e+00/100   # y = v + at for new velocity

        if v_mod[n] < 0 :   # when velocity is negative, drag force is negative
            dragForce[n+1] = -(c_vect*((rho*(v_mod[n])**2)/2)*A)

        else: # when velocity is positive, drag force is positive
            dragForce[n+1] = c_vect*((rho*v_mod[n]**2)/2)*A

        a_mod[n+1] = (Fg-dragForce[n+1])/m
        n = n+1
    x_filt = x_mod[x_mod >= 0]

    plt.plot(xx7,x_mod)
plt.show()
#import pdb; pdb.set_trace()
###############################################################################################################
"""
######################################################## try C2  ##############################################
x_mod2=np.zeros(shape=(N))
v_mod2=np.zeros(shape=(N))
a_mod2=np.zeros(shape=(N))
dragForce2=np.zeros(shape=(N))

x_mod2[0] = 0
v_mod2[0] = v
dragForce2[0] = C2*((rho*v_mod2[0]**2)/2)*A
a_mod2[0] = (Fg-dragForce2[0])/m
n2=0

dragForce2[0] = C2*((rho*v_mod2[0]**2)/2)*A
for n2 in range(0,N-1):
    x_mod2[n2+1] = x_mod2[n2] + v_mod2[n2] * (3.29492307e+00/100)+ (1/2) * (a_mod2[n2]) * (3.29492307e+00/100)**2
    v_mod2[n2+1] = v_mod2[n2] + a_mod2[n2] * (3.29492307e+00/100)

    if v_mod2[n2] < 0 :
        dragForce2[n2+1] = -(C2*((rho*(v_mod2[n2])**2)/2)*A)
        #dragForce[n+1]=0
    else:
        dragForce2[n2+1] = C2*((rho*v_mod2[n2]**2)/2)*A

    a_mod2[n2+1] = (Fg-dragForce2[n2+1])/m
    n2 = n2+1
x_filt2 = x_mod2[x_mod2 >= 0]
##############################################################################################################
####################################################### try C3  ##############################################
x_mod3=np.zeros(shape=(N))
v_mod3=np.zeros(shape=(N))
a_mod3=np.zeros(shape=(N))
dragForce3=np.zeros(shape=(N))

x_mod3[0] = 0
v_mod3[0] = v
dragForce3[0] = C3*((rho*v_mod3[0]**2)/2)*A
a_mod3[0] = (Fg-dragForce3[0])/m
n3=0


for n3 in range(0,N-1):
    x_mod3[n3+1] = x_mod3[n3] + v_mod3[n3] * 3.29492307e+00/100+ (1/2) * (a_mod3[n3]) * (3.29492307e+00/100)**2
    v_mod3[n3+1] = v_mod3[n3] + a_mod3[n3] * 3.29492307e+00/100

    if v_mod3[n3] < 0 :
        dragForce3[n3+1] = -(C3*((rho*(v_mod3[n3])**2)/2)*A)
        #dragForce[n+1]=0
    else:
        dragForce3[n3+1] = C3*((rho*v_mod3[n3]**2)/2)*A
        #dragForce[n+1]=0
    a_mod3[n3+1] = (Fg-dragForce3[n3+1])/m
    n3 = n3+1
x_filt3 = x_mod3[x_mod3 >= 0]
#############################################################################################################

###################################################### try C4  ##############################################
x_mod4=np.zeros(shape=(N))
v_mod4=np.zeros(shape=(N))
a_mod4=np.zeros(shape=(N))
dragForce4=np.zeros(shape=(N))

x_mod4[0] = 0
v_mod4[0] = v
dragForce4[0] = C4*((rho*v_mod4[0]**2)/2)*A
a_mod4[0] = (Fg-dragForce4[0])/m
n4=0

print('loop')
for n4 in range (0,N-1):
    x_mod4[n4+1] = x_mod4[n4] + v_mod4[n4] * 3.29492307e+00/100+ (1/2) * (a_mod4[n4]) * (3.29492307e+00/100)**2
    v_mod4[n4+1] = v_mod4[n4] + a_mod4[n4] * 3.29492307e+00/100

    if v_mod4[n4] < 0 :
        dragForce4[n4+1] = -(C4*((rho*(v_mod4[n4])**2)/2)*A)
        #dragForce[n+1]=0
    else:
        dragForce4[n4+1] = C4*((rho*v_mod4[n4]**2)/2)*A
        #dragForce[n+1]=0
    a_mod4[n4+1] = (Fg-dragForce4[n4+1])/m
    n4 = n4+1


##############################################################################################################
###################################################### try C5 ################################################

x_mod5=np.zeros(shape=(N))
v_mod5=np.zeros(shape=(N))
a_mod5=np.zeros(shape=(N))
dragForce5=np.zeros(shape=(N))

x_mod5[0] = 0
v_mod5[0] = v
dragForce5[0] = C5*((rho*v_mod5[0]**2)/2)*A
a_mod5[0] = (Fg-dragForce5[0])/m
n5=0
print('loop')
for n5 in range(0, N-1):
    x_mod5[n5+1] = x_mod5[n5] + v_mod5[n5] *3.29492307e+00/100+ (1/2) * (a_mod5[n5]) * 3.29492307e+00/100**2
    v_mod5[n5+1] = v_mod5[n5] + a_mod5[n5] * 3.29492307e+00/100

    if v_mod5[n5] < 0 :
        dragForce5[n5+1] = -(C5*((rho*(v_mod5[n5])**2)/2)*A)
        #dragForce[n+1]=0
    else:
        dragForce5[n5+1] = C5*((rho*v_mod5[n5]**2)/2)*A
        #dragForce[n+1]=0
    a_mod5[n5+1] = (Fg-dragForce5[n5+1])/m
    n5 = n5+1
##############################################################################################################
##################################################### try C6 #################################################
x_mod6=np.zeros(shape=(N))
v_mod6=np.zeros(shape=(N))
a_mod6=np.zeros(shape=(N))
dragForce6=np.zeros(shape=(N))

x_mod6[0] = 0
v_mod6[0] = v
dragForce6[0] = C6*((rho*v_mod6[0]**2)/2)*A
a_mod6[0] = (Fg-dragForce6[0])/m
n6=0

for n6 in range(0,N-1):
    x_mod6[n6+1] = x_mod6[n6] + v_mod6[n6] * 3.29492307e+00/100+ (1/2) * (a_mod6[n6]) * (3.29492307e+00/100)**2
    v_mod6[n6+1] = v_mod6[n6] + a_mod6[n6] * 3.29492307e+00/100

    if v_mod6[n6] < 0 :
        dragForce6[n6+1] = -(C6*((rho*(v_mod6[n6])**2)/2)*A)
        #dragForce[n+1]=0
    else:
        dragForce6[n6+1] = C6*((rho*v_mod6[n6]**2)/2)*A
        #dragForce[n+1]=0
    a_mod6[n6+1] = (Fg-dragForce6[n6+1])/m
    n6 = n6+1

x3_halfgraph = x3 -11.03912687
plt.figure()
plt.subplot(1,1,1)
plt.plot(x3_halfgraph,newRange)
plt.axvline(x=1.92786718)

##############################################################################################################

##################################### plot position model ###################################################
plt.figure()
plt.plot(xx7,x_mod, label='$C=0$')
plt.plot(xx7,x_mod2, label='$C=0.1$')
plt.plot(xx7,x_mod3, label='$C=0.2$')
plt.plot(xx7,x_mod4, label='$C=0.3$')
plt.plot(xx7,x_mod5, label='$C=0.4$')
plt.plot(xx7,x_mod6, label='$C=0.5$')
plt.plot(adj_x7_mod,adj_newRange_mod,'o', label='$experimental\ data$')
plt.ylim([0,13.5])
plt.legend()
plt.xlabel('Time (s)')
plt.ylabel('Position (m)')
plt.title('Modeled Position and Experimental Data')
plt.tick_params()
plt.tight_layout()
#############################################################################################################

########################################### plot velocity model #############################################
plt.figure()
plt.title('Modeled Velocity')
plt.subplot(1,1,1)
plt.xlabel('Time (s)')
plt.ylabel('Velocity (m/2)')
plt.plot(xx7,v_mod, label='$C=0$')
plt.plot(xx7,v_mod2, label='$C=0.1$')
plt.plot(xx7,v_mod3, label='$C=0.2$')
plt.plot(xx7,v_mod4, label='$C=0.3$')
plt.plot(xx7,v_mod5, label='$C=0.4$')
plt.plot(xx7,v_mod6, label='$C=0.5$')
#plt.plot(adj_x7_vel_mod, vel,'o', label='experimental data')
plt.legend()
plt.tick_params()
plt.tight_layout()
#############################################################################################################

############################# plot velocity model and where velocity should cross zero ######################
plt.figure()
plt.title('Modeled Velocity (where it should cross zero)')
plt.subplot()
plt.xlabel('Time (s)')
plt.ylabel('Velocity (m/2)')
plt.plot(xx7,v_mod, label='$C=0$')
plt.plot(xx7,v_mod2, label='$C=0.2$')
plt.plot(xx7,v_mod3, label='$C=0.3$')
plt.plot(xx7,v_mod4, label='$C=0.4$')
plt.plot(xx7,v_mod5, label='$C=0.15$')
plt.plot(xx7,v_mod6, label='$C=0.1$')
#plt.plot(adj_x7_vel_mod, vel,'o', label='experimental data',lw=5)
plt.axvline(x=1.628823090000001, color='k', linestyle='--')
plt.axhline(y=0, color='k', linestyle='--')
plt.tick_params()
plt.tight_layout()
###############################################################################################################

######################################## plot acceleration model ##############################################
plt.figure()
plt.title('Modeled Acceleration')
plt.subplot(1,1,1)
plt.xlabel('Time (s)')
plt.ylabel('Acceleration (m/s$^2$)')
plt.plot(xx7,a_mod, label='$C=0$')
plt.plot(xx7,a_mod2, label='$C=0.1$')
plt.plot(xx7,a_mod3, label='$C=0.2$')
plt.plot(xx7,a_mod4, label='$C=0.3$')
plt.plot(xx7,a_mod5, label='$C=0.4$')
plt.plot(xx7,a_mod6, label='$C=0.5$')
plt.legend()
plt.tick_params()
plt.tight_layout()
################################################################################################################
plt.show()
##################################### rotation matrix for axis correction ######################################
"""
"""
N2 = 38 # number of data points in array

# these just create a new space for each new value to be held
R=np.zeros(shape=(N2),dtype=object)
EA=np.zeros(shape=(N2),dtype=object)
Eg=np.zeros(shape=(N2),dtype=object)
newa=np.zeros(shape=(N2),dtype=object)
newax=np.zeros(shape=(N2))
neway=np.zeros(shape=(N2))
newaz=np.zeros(shape=(N2))
newg=np.zeros(shape=(N2),dtype=object)
newgx=np.zeros(shape=(N2))
newgy=np.zeros(shape=(N2))
newgz=np.zeros(shape=(N2))

# use quaternion rotation matrix
for n in range(N2):

    R[n] = np.array([[1-2*qy2[n]**2-2*qz2[n]**2, 2*qx2[n]*qy2[n]+2*qw2[n]*qz2[n], 2*qx2[n]*qz2[n]-2*qw2[n]*qy2[n]],[2*qx2[n]*qy2[n]-2*qw2[n]*qz2[n], 1-2*qx2[n]**2-2*qz2[n]**2, 2*qy2[n]*qz2[n]+2*qw2[n]*qx2[n]],[2*qx2[n]*qz2[n]+2*qw2[n]*qy2[n], 2*qy2[n]*qz2[n]-2*qw2[n]*qx2[n], 1-2*qx2[n]**2-2*qy2[n]**2]])

    qx2[n] = qx2[n+1] # goes onto the next element in the array
    qy2[n] = qy2[n+1]
    qz2[n] = qz2[n+1]
    qw2[n] = qw2[n+1]
    n = n+1

# create E (array of acceleration matrices)
for n in range(N2):

    EA[n] = np.array([[Ax2[n]],[Ay2[n]],[Az2[n]]]) # create the acceleration matrix
    Ax2[n]=Ax2[n+1] # go through each element in the acceleration data
    Ay2[n]=Ay2[n+1]
    Az2[n]=Az2[n+1]

    Eg[n] = np.array([[gx2[n]],[gy2[n]],[gz2[n]]]) # create the acceleration matrix
    gx2[n]=gx2[n+1] # go through each element in the acceleration data
    gy2[n]=gy2[n+1]
    gz2[n]=gz2[n+1]


    n = n+1


# multiply E and R 
for n in range(N2):
    newa[n] = np.matmul(R[n],EA[n])
    newg[n] = np.matmul(R[n],Eg[n])

    n=n+1

# this just pulls values for ax, ay, az out of each matrix and into their own array
for n in range(N2):
    newax[n] = newa[n][0]
    neway[n] = newa[n][1]
    newaz[n] = newa[n][2]
    newgx[n] = newg[n][0]
    newgy[n] = newg[n][1]
    newgz[n] = newg[n][2]

import pdb; pdb.set_trace()

# plot the rotation corrected data
plt.figure(figsize=(8,6))
plt.subplot(3,2,1)
plt.title('new ax')
plt.plot(x6-11.17117691,newax)
plt.subplot(3,2,3)
plt.title('new ay')
plt.plot(x6-11.17117691,neway)
plt.subplot(3,2,5)
plt.title('new az')
plt.plot(x6-11.17117691,newaz)
plt.subplot(3,2,2)
plt.plot(x2,Ax2)
plt.title('original ax')
plt.subplot(3,2,4)
plt.plot(x2,Ay2)
plt.title('original ay')
plt.subplot(3,2,6)
plt.plot(x2,Az2)
plt.title('original az')
plt.tight_layout()


plt.figure(figsize=(7,6))
plt.subplot(3,1,1)
plt.title('new gx')
plt.plot(x6-11.17117691,newgx)
plt.subplot(3,1,2)
plt.title('new gy')
plt.plot(x6-11.17117691,newgy)
plt.subplot(3,1,3)
plt.title('new gz')
plt.plot(x6-11.17117691,newgz)
plt.tight_layout()


#import pdb; pdb.set_trace()

plt.figure()
plt.title('Modeled Acceleration')
plt.subplot(1,1,1)
plt.xlabel('Time (s)')
plt.ylabel('Acceleration (m/s$^2$)')
plt.plot(xx7,a_mod, label='$C=0$')
plt.plot(xx7,a_mod2, label='$C=0.1$')
plt.plot(xx7,a_mod3, label='$C=0.2$')
plt.plot(xx7,a_mod4, label='$C=0.3$')
plt.plot(xx7,a_mod5, label='$C=0.4$')
plt.plot(xx7,a_mod6, label='$C=0.5$')
plt.plot(x6-11.17117691, neway)
plt.legend()
plt.tick_params()
plt.tight_layout()

plt.show()


"""


"""
x=np.zeros(shape=(N))
v=np.zeros(shape=(N))
a=np.zeros(shape=(N))
dragForce=np.zeros(shape=(N))

v_start=np.arange(13,21,1)
C=np.arange(0,1,0.1)

x[0] = 0

for n in v_start:
    v[0] = v_start[n]

dragForce[0] = C1*((rho*v[0]**2)/2)*A
a[0] = (Fg-dragForce[0])/m
n=0

def func(t, v_start, C):

        for n in range(0,N-1):
            x[n+1] = x[n] + v[n] * 3.29492307e+00/100+ (1/2) * (a[n]) * (3.29492307e+00/100)**2
            v[n+1] = v[n] + a[n] * 3.29492307e+00/100

            if v[n] < 0 :
                dragForce[n+1] = -(C1*((rho*(v[n])**2)/2)*A)

            else:
                dragForce[n+1] = C1*((rho*v[n]**2)/2)*A

            a[n+1] = (Fg-dragForce[n+1])/m
            n = n+1
"""
