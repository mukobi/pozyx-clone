import numpy as np
class models:

    def Position():
        N = 100 # allows you to create each model out of 100 points

        model_times = np.linspace(x2[0], x2[-1], 100)   # create array of 100 times within experimental timeframe for the modeled positions
        x_mod = np.zeros(shape=(N))   # create empty array with space for 100 elements
        v_mod = np.zeros(shape=(N))
        a_mod = np.zeros(shape=(N))
        dragForce = np.zeros(shape=(N))
        dt = ( x2[-1]-x2[0] ) / N

        plt.figure()
        plt.plot(x2,d2, 'C7', marker = 'o', linestyle="None")
        c_vect = np.array([0,0.651,1])
        #for c in range(3) :
        x_mod[0] = 0    # initial position of zero
        v_mod[0] = 0    # initial velocity of zero
        dragForce[0] = blueBall.xSectionArea * 0.5 * c_vect[c] * rho * v_mod[0]**2   # initial drag force
        a_mod[0] = ( Fg-dragForce[0] ) / blueBall.mass  # initial acceleration based on initial drag force
        n=0

        for n in range(0,N-1):
            x_mod[n+1] = x_mod[n]  + v_mod[n] * dt  + (1/2) * (a_mod[n]) * dt**2 # simply y=x + v*t + (1/2)*a*t^2
            v_mod[n+1] = v_mod[n] + a_mod[n] * dt # updated velocity is v + a*t

            if v_mod[n] < 0 :
                dragForce[n+1] = -( c_vect[c]*( (rho*v_mod[n]**2) /2 ) * blueBall.xSectionArea ) # if/else may not be necessary

            else:
                dragForce[n+1] = c_vect[c]*( (rho*v_mod[n]**2) /2 ) * blueBall.xSectionArea

            a_mod[n+1] = ( Fg-dragForce[n+1] ) /blueBall.mass  # update acceleration with updated drag force
        #    print(a_mod)
            n = n+1

#import pdb; pdb.set_trace()
