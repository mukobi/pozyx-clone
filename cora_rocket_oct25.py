import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import scipy.optimize as opt
from scipy.optimize import curve_fit

plt.rcParams['text.usetex']=True
params = {'legend.fontsize': 8}
plt.rcParams.update(params)

df=pd.read_csv('rocket_4096_oct24_3.csv', delimiter=',', usecols=[1, 5, 9, 10, 11, 15, 16, 17, 25, 26, 27, 28])

df.columns = ['time', 'pressure', 'magx', 'magy', 'magz', 'Heading', 'Roll', 'Pitch', 'Gravity-X', 'Gravity-Y', 'Gravity-Z', 'Distance']

df2 = df.ix[166:216].dropna() #index pertaining to rocket's motion 

############################################# entire data set ###########################################
x=df['time']
d=df['Distance']
p=df['pressure']
mx=df['magx']
my=df['magy']
mz=df['magz']
h=df['Heading']
pi=df['Pitch']
r=df['Roll']
gx=df['Gravity-X']
gy=df['Gravity-Y']
gz=df['Gravity-Z']
##########################################################################################################

######################################### data pertaining to rocket's motion #############################
x2=df2['time']
d2=df2['Distance']
p2=df2['pressure']
mx2=df2['magx']
my2=df2['magy']
mz2=df2['magz']
h2=df2['Heading']
pi2=df2['Pitch']
r2=df2['Roll']
gx2=df2['Gravity-X']
gy2=df2['Gravity-Y']
gz2=df2['Gravity-Z']
###########################################################################################################

####################################### for calculating new range #########################################
dt = 14.669509-11.039127 # rocket's time in the air

new_v=(2052.0-368.0)/dt # for discounting horizontal motion
new_x=new_v*dt # for discounting horizontal motion

df2['newRange']=np.sqrt(df2['Distance']**2-new_x**2) # total range discounting horixontal motion

df3 = df2.ix[168:216].dropna() # new parameters for discounting horizontal motion

x3 = df3['time'] # time for distance discounting horizontal motion

newRange = df2['newRange'].dropna() # new name for data that discounts horizontal motion
###########################################################################################################

############################# for calculating velocity from new range #####################################
df2['velocity'] = (newRange - newRange.shift(1)) / (df2['time'] - df2['time'].shift(1))*0.001 # velocity from new range
velocity = df2['velocity'].dropna() # new name for velocity from horizontal range

x6 = df2['time'].ix[169:216]
##########################################################################################################

##################### parameters for drag force ##########################################################
A = 0.008107319666 # cross sectional area
C1 = 0.4 # drag coefficient
v = 17.740803207
vsq = v**2 # maximum velocity during free fall
rho = 1.225 # density of air at sea level at 20 degrees C
m = 0.227
g=9.81
Fg = -m*g

dragForce = C1*((rho*v)/2)*A
adrag = (Fg-dragForce)/m
print('dragForce = {}'.format(dragForce))
print('adrag = {}'.format(adrag))
##########################################################################################################

################################# plot the raw data within motion parameters #############################
def func(x,a,b,c):
    return a*(x**2) + b*x + c
pfit, success = opt.curve_fit(func,x2,d2)
xx2 = np.linspace(11.039127,14.669509,100)
print('raw range coeffs: {}'.format(pfit))
plt.subplot(1,1,1)
plt.tick_params(labelsize=6)
plt.title('Raw Range')
plt.xlabel('Time')
plt.ylabel('Distance')
plt.plot(x2, d2, 'o')
plt.plot(xx2,func(xx2,*pfit),'--')
#z = np.polyfit(x2, d2, 2)
#p = np.poly1d(z)
#plt.plot(x2,p(x2),"--")
#plt.legend(loc=2, prop={'size': 10})
#equation = "y = %.6f x^2 + %.6f x + %.6f"%(z[0],z[1],z[2])
#print('raw range: {}'.format(equation))
gravity = 'g = {}'.format(4592.73931405*2*0.001)
print(gravity)
#plt.figtext(.25,.2, equation,  style='italic', size=8)
plt.figtext(0.45,0.15, gravity, style='italic',size=8)
plt.savefig('figures/rawrange.pdf')
##########################################################################################################

################################## plot gravity and euler angles #########################################
plt.figure()
plt.subplot(2,1,1)
plt.title('Euler Angles')
plt.tick_params(labelsize=6)
plt.plot(x2, h2)
plt.plot(x2, pi2)
plt.plot(x2, r2)
plt.xlabel('Time')
plt.ylabel('Angle ($^\circ$)')
plt.legend(loc=3, prop={'size': 6})
plt.tight_layout()
plt.subplot(2,1,2)
plt.title('Gravity')
plt.tick_params(labelsize=6)
plt.plot(x2, gx2)
plt.plot(x2, gy2)
plt.plot(x2, gz2)
plt.xlabel('Time')
plt.ylabel('Gravity')
plt.legend(loc=3, prop={'size': 6})
plt.tight_layout()
plt.savefig('figures/euler_gravity.pdf')
##########################################################################################################

################################# plot range discounting horizontal motion ##############################
def func1(x,a,b,c):
    return a*(x**2) + b*x + c
pfit1, success1 = opt.curve_fit(func1,x3,newRange)
xx3 = np.linspace(11.171177,14.669509,100)

print('pfit1 coeffs: {}'.format(pfit1))
plt.figure()
plt.subplot(1,1,1)
plt.tick_params(labelsize=6)
plt.title('New Range')
plt.plot(x3, newRange,'o')
plt.plot(xx3,func1(xx3,*pfit1),'--')
plt.xlabel('Time')
plt.ylabel('Distance')
z = np.polyfit(x3, newRange, 2)
#p = np.poly1d(z)
#plt.plot(x3,p(x3),"--")
#plt.legend(loc=2, prop={'size': 10})
#equation2 = "y = %.6f x^2 + %.6f x + %.6f"%(z[0],z[1],z[2])
#print('new range: {}'.format(equation2))
newGravity = 'g = {}'.format(4709.66938958*2*0.001)
#print('new g = {}'.format(newGravity))
#plt.figtext(.25,.2, equation2,  style='italic', size=8)
plt.figtext(0.45,0.15, newGravity, style='italic',size=8)
plt.savefig('figures/newrange.pdf')
##########################################################################################################
print(velocity)
################################ calculate and plot g for different heights ###############################
rDFabove10m = df[df['Distance'] > 10000]
rDFabove12m = df[df['Distance'] > 12000]
rocketZ10m = np.polyfit(rDFabove10m['time'],rDFabove10m['Distance'],2)
rocketZ12m = np.polyfit(rDFabove12m['time'],rDFabove12m['Distance'],2)

glist = list( map(lambda x0: x0*2, [z[0], rocketZ10m[0], rocketZ12m[0]]) ) 
for g in glist:
    print( 'g = {:g}'.format(g) )

x4 = rDFabove10m.time
d4 = rDFabove10m.Distance
x5 = rDFabove12m.time
d5 = rDFabove12m.Distance

plt.figure()
plt.subplot(1,1,1)
plt.tick_params(labelsize=6)
plt.title('Mapped Changes in Gravity Due to Drag')
plt.xlabel('Time')
plt.ylabel('Distance')
plt.plot(x2,d2,'o')
plt.plot(x4,d4,'o')
plt.plot(x5,d5,'o')
plt.savefig('figures/gmap.pdf')
###########################################################################################################

################################## plot velocity from new range ###########################################
plt.figure()
plt.subplot(1,1,1)
plt.tick_params(labelsize=6)
plt.title('Velocity')
plt.xlabel('Time (s)')
plt.ylabel('Velocity (mm/s)')
plt.plot(x6,velocity,'o')
z = np.polyfit(x6, velocity, 1)
p = np.poly1d(z)
plt.plot(x6,p(x6),"--")
vequation = "y = %.6f x + %.6f"%(z[0],z[1])
plt.figtext(.15,.25,vequation, style='italic', size=8)
print('new velocity: {}'.format(vequation))
print('new velocity g = {}'.format(z[0]))
plt.legend(loc=1, prop={'size': 10})
plt.savefig('figures/velocity.pdf')
###########################################################################################################
"""
df2['v2'] = (velocity*0.001)**2

v2 = df2['v2'] 

df2['drag2'] = C*((rho*v2)/2)*A 

drag2 = df2['drag2'].dropna()

df2['acceleration'] = (Fg-drag2)/m

acceleration = df2['acceleration'].dropna()

plt.figure()
plt.subplot(1,1,1)
plt.tick_params(labelsize=6)
plt.title('(Fg-D/m)')
plt.xlabel('Time (s)')
plt.ylabel('(Fg-D)/m')
plt.plot(x6,acceleration,'o')
plt.legend(loc=1, prop={'size': 10})
plt.savefig('figures/new_a.pdf')
"""
############################################## CREATE THE MODELS ##############################################
df2['x7'] = df2['time'].ix[169:216] 
x7=df2['x7'].dropna()

N=38 # number of elements in x7
C1 = 0.4 # drag coefficient 1
C2 = 0.7 # drag coefficient 2
C3=1.0 # drag coefficient 3

x_mod=np.zeros(shape=(N))
v_mod=np.zeros(shape=(N))
a_mod=np.zeros(shape=(N))
dragForce=np.zeros(shape=(N))

x_mod[0] = 0
v_mod[0] = 18
dragForce[0] = C1*((rho*v_mod[0]**2)/2)*A
a_mod[0] = (Fg-dragForce[0])/m
n=0

print('loop')
while x_mod[n] >= 0:
    #x_mod[n+1] = x_mod[n] + v_mod[n] * 0.2459540905 + (1/2) * (a_mod[n]) * 0.2459540905**2 
    #v_mod[n+1] = v_mod[n] + a_mod[n] * 0.2459540905
    x_mod[n+1] = x_mod[n] + v_mod[n] * 0.092+ (1/2) * (a_mod[n]) * 0.092**2 
    v_mod[n+1] = v_mod[n] + a_mod[n] * 0.092

    if v_mod[n] < 0 :
        dragForce[n+1] = -(C1*((rho*(v_mod[n])**2)/2)*A)
        #dragForce[n+1]=0
    else:
        dragForce[n+1] = C1*((rho*v_mod[n]**2)/2)*A
        #dragForce[n+1]=0
    a_mod[n+1] = (Fg-dragForce[n+1])/m
    n = n+1


x_mod2=np.zeros(shape=(N))
v_mod2=np.zeros(shape=(N))
a_mod2=np.zeros(shape=(N))
dragForce2=np.zeros(shape=(N))

x_mod2[0] = 0 
v_mod2[0] = 18
dragForce2[0] = C1*((rho*v_mod2[0]**2)/2)*A
a_mod2[0] = (Fg-dragForce[0])/m
n2=0

dragForce2[0] = C2*((rho*v_mod2[0]**2)/2)*A
while x_mod2[n2] >= 0:
    #x_mod[n+1] = x_mod[n] + v_mod[n] * 0.2459540905 + (1/2) * (a_mod[n]) * 0.2459540905**2 
    #v_mod[n+1] = v_mod[n] + a_mod[n] * 0.2459540905
    x_mod2[n2+1] = x_mod2[n2] + v_mod2[n2] * 0.0892+ (1/2) * (a_mod2[n2]) * 0.0892**2 
    v_mod2[n2+1] = v_mod2[n2] + a_mod2[n2] * 0.0892

    if v_mod2[n2] < 0 :
        dragForce2[n2+1] = -(C2*((rho*(v_mod2[n2])**2)/2)*A)
        #dragForce[n+1]=0
    else:
        dragForce2[n2+1] = C2*((rho*v_mod2[n2]**2)/2)*A
        #dragForce[n+1]=0
    a_mod2[n2+1] = (Fg-dragForce2[n2+1])/m
    n2 = n2+1



x_mod3=np.zeros(shape=(N))
v_mod3=np.zeros(shape=(N))
a_mod3=np.zeros(shape=(N))
dragForce3=np.zeros(shape=(N))

x_mod3[0] = 0
v_mod3[0] = 18
dragForce3[0] = C3*((rho*v_mod3[0]**2)/2)*A
a_mod3[0] = (Fg-dragForce[0])/m
n3=0

dragForce3[0] = C3*((rho*v_mod3[0]**2)/2)*A
while x_mod3[n3] >= 0:
    #x_mod[n+1] = x_mod[n] + v_mod[n] * 0.2459540905 + (1/2) * (a_mod[n]) * 0.2459540905**2 
    #v_mod[n+1] = v_mod[n] + a_mod[n] * 0.2459540905
    x_mod3[n3+1] = x_mod3[n3] + v_mod3[n3] * 0.0828+ (1/2) * (a_mod3[n3]) * 0.0828**2 
    v_mod3[n3+1] = v_mod3[n3] + a_mod3[n3] * 0.0828

    if v_mod3[n3] < 0 :
        dragForce2[n3+1] = -(C3*((rho*(v_mod3[n3])**2)/2)*A)
        #dragForce[n+1]=0
    else:
        dragForce3[n3+1] = C3*((rho*v_mod3[n3]**2)/2)*A
        #dragForce[n+1]=0
    a_mod3[n3+1] = (Fg-dragForce3[n3+1])/m
    n3 = n3+1

plt.figure()
plt.subplot(1,1,1)
#plt.plot(x7.ix[169:216],x_mod, 'o')
plt.plot(x_mod)
plt.plot(x_mod2)
plt.plot(x_mod3)
#plt.plot(x_mod3,'o')
plt.legend()
#plt.subplot(2,1,2)
#plt.plot(v_mod,'o')

plt.show()

