import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy
import scipy.fftpack
import scipy.signal as signal

plt.rcParams['text.usetex']=True
params = {'legend.fontsize': 8}
plt.rcParams.update(params)

df = pd.read_csv('error_test_tripods_1334mm.csv', delimiter=',', usecols=['Time', '0x6030_Range'])

df2 = pd.read_csv('2_error_test_tripods_1334mm.csv', delimiter=',', usecols=['Time', '0x6030_Range'])

df3 = pd.read_csv('3_error_test_tripods_1334mm.csv', delimiter=',', usecols=['Time', '0x6030_Range'])


df.columns = ['Time','Range']
df2.columns = ['Time','Range']
df3.columns = ['Time','Range']

x = df['Time']
y = df['Range']
mean = df.Range.mean()

x2 = df2['Time']
y2 = df2['Range']
mean2 = df2.Range.mean()

x3 = df3['Time']
y3 = df3['Range']
mean3 = df3.Range.mean()

plt.figure(figsize=(10,6))
plt.subplot(3,1,1)
plt.plot(x,y)
plt.xlabel('Time')
plt.ylabel('Range')

plt.subplot(3,1,2)
plt.plot(x2,y2)
plt.xlabel('Time')
plt.ylabel('Range')

plt.subplot(3,1,3)
plt.plot(x3,y3)
plt.xlabel('Time')
plt.ylabel('Range')
plt.suptitle('Raw Rata', fontweight = 'bold')
plt.tight_layout(rect=[0, 0.03, 1, 0.95])

newRange = df['Range'] - mean
newRange2 = df2['Range'] - mean2
newRange3 = df3['Range'] - mean3

fft = abs(scipy.fft(newRange))
freqs = scipy.fftpack.fftfreq(fft.size, df['Time'][1]-df['Time'][0])

fft2 = abs(scipy.fft(newRange2))
freqs2 = scipy.fftpack.fftfreq(fft2.size, df2['Time'][1]-df2['Time'][0])

fft3 = abs(scipy.fft(newRange3))
freqs3 = scipy.fftpack.fftfreq(fft3.size, df3['Time'][1]-df3['Time'][0])

plt.figure(figsize=(10,6))
plt.subplot(311)
plt.plot(freqs,fft)
plt.xlabel('Frequency')
plt.ylabel('Power')

plt.subplot(312)
plt.subplot(3,1,2)
plt.plot(freqs2,fft2)
plt.xlabel('Frequency')
plt.ylabel('Power')

plt.subplot(313)
plt.subplot(3,1,3)
plt.plot(freqs3,fft3)
plt.xlabel('Frequency')
plt.ylabel('Power')

plt.suptitle('Discrete Fourier Transform', fontweight = 'bold')
plt.tight_layout(rect=[0, 0.03, 1, 0.95])

# First, design the Buterworth filter

N  = 1   # Filter order
Wn = 0.01 # Cutoff frequency
B, A = signal.butter(N, Wn, output='ba')
 
# Second, apply the filter
fftf = signal.filtfilt(B,A, fft)
fftf2 = signal.filtfilt(B,A, fft2)
fftf3 = signal.filtfilt(B,A, fft3)

#return high-pass qmf filter from low pass
hi1 = scipy.signal.qmf(fftf)
hi2 = scipy.signal.qmf(fftf2)
hi3 = scipy.signal.qmf(fftf3)

# Make plots
plt.figure(figsize=(10,6))
plt.subplot(321)
plt.plot(freqs,fft, 'C0')
plt.plot(freqs,hi1, 'C1',linewidth=2)
plt.ylabel("Power")
plt.xlabel("Frequency")
plt.legend(['Original','Filtered'], loc = 1)

plt.subplot(322)
plt.plot(freqs,fft-hi1, 'C0')
plt.ylabel("Power")
plt.xlabel("Frequency")
plt.legend(['Residuals'], loc = 1)

plt.subplot(323)
plt.plot(freqs2,fft2, 'C0')
plt.plot(freqs2,hi2, 'C1',linewidth=2)
plt.ylabel("Power")
plt.xlabel("Frequency")
plt.legend(['Original','Filtered'], loc = 1)

plt.subplot(324)
plt.plot(freqs2,fft2-hi2, 'C0')
plt.ylabel("Power")
plt.xlabel("Frequency")
plt.legend(['Residuals'], loc = 1)
plt.tight_layout()

plt.subplot(325)
plt.plot(freqs3,fft3, 'C0')
plt.plot(freqs3,hi3, 'C1',linewidth=2)
plt.ylabel("Power")
plt.xlabel("Frequency")
plt.legend(['Original','Filtered'], loc = 1)

plt.subplot(326)
plt.plot(freqs3,fft3-hi3, 'C0')
plt.ylabel("Power")
plt.xlabel("Frequency")
plt.legend(['Residuals'], loc = 1)

plt.suptitle('Raw DFT, Filtered DFT, and Residuals', fontweight = 'bold')
plt.tight_layout(rect=[0, 0.03, 1, 0.95])

# First, design the Buterworth filter
N2  = 1    # Filter order
Wn2 = 0.01 # Cutoff frequency
B, A = signal.butter(N, Wn, output='ba')

# Second, apply the filter
filtered_range = signal.filtfilt(B,A, df['Range'])
filtered_range2 = signal.filtfilt(B,A, df2['Range'])
filtered_range3 = signal.filtfilt(B,A, df3['Range'])

#return high-pass qmf filter from low pass
range_hi1 = scipy.signal.qmf(filtered_range)
range_hi2 = scipy.signal.qmf(filtered_range2)
range_hi3 = scipy.signal.qmf(filtered_range3)

# Make plots

plt.figure(figsize=(10,6))
plt.subplot(311)
plt.plot(x,y, 'C0')
plt.plot(x,range_hi1, 'C1',linewidth=2)
plt.ylabel("Range")
plt.xlabel("Time")
plt.legend(['Original','Filtered'], loc = 1)

plt.subplot(312)
plt.plot(x2,y2, 'C0')
plt.plot(x2,range_hi2, 'C1',linewidth=2)
plt.ylabel("Range")
plt.xlabel("Time")
plt.legend(['Original','filtered'], loc = 1)

plt.subplot(313)
plt.plot(x3,y3, 'C0')
plt.plot(x3,range_hi3, 'C1',linewidth=2)
plt.ylabel("Range")
plt.xlabel("Time")
plt.legend(['Original','filtered'], loc = 1)
plt.suptitle('Filtered Position Data', fontweight = 'bold')
plt.tight_layout(rect=[0, 0.03, 1, 0.95])

plt.show()
