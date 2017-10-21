# -*- coding: utf-8 -*-
"""
Matt Fleetwood
10 - 20 - 2017
Portland, OR

Modified Pozyx file to cite the read data using pd.read_csv from a local file pathway.
SciPy's Wiener filter function is also used to test how effective it might be for this example.

The following is taken from SciPy's API for the Wiener filter

docs.scipy.org/doc/scipy-0.14.0/reference/generated/scipy.signal.wiener.html 

Parameters:	

            im : ndarray
                 An N-dimensional array.
            
            mysize : int or arraylike, optional
                     A scalar or an N-length list giving the size of the Wiener filter window in each dimension. Elements of mysize should be odd. If mysize is a scalar, then this scalar is used as the size in each dimension.
            
            noise : float, optional
                    The noise-power to use. If None, then noise is estimated as the average of the local variance of the input.

Returns:	
            out : ndarray
                  Wiener filtered result with the same shape as im.
"""

import pandas as pd

#error_bad_lines=False, 
#C:\Users\Etcyl\Desktop\pozyx\Data
df=pd.read_csv('C:\Users\Etcyl\Desktop\pozyx\Data\walking_varying_speed_multi_test_ch2.csv', delimiter=' ',  usecols=[5, 9], names=['0x6103 Range','manual velocity'])

orig_range = []

orig_range = df['0x6103 Range']
man_vel = df['manual velocity']