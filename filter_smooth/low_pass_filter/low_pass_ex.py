import numpy as np
from scipy.signal import butter, lfilter, freqz
from scipy import signal
import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv('12_13_17_1D_1.csv', delimiter=',', usecols=['Time', '0x6829 Range'])
df2 = df.apply(pd.Series.interpolate)

#df2 = pd.read_csv('2_error_test_tripods_1334mm.csv', delimiter=',', usecols=['Time', '0x6030_Range'])

#df3 = pd.read_csv('3_error_test_tripods_1334mm.csv', delimiter=',', usecols=['Time', '0x6030_Range'])

df2.columns = ['Time','Range']
#df2.columns = ['Time','Range']
#df3.columns = ['Time','Range']

x = df2['Time']
position = df2['Range']
bwdpos = df2['Range'][::-1]
mean = df2.Range.mean()

#x2 = df2['Time']
#position2 = df2['Range']
#mean2 = df2.Range.mean()

#x3 = df3['Time']
#position3 = df3['Range']
#mean3 = df3.Range.mean()

def butter_lowpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return b, a

def butter_lowpass_filter(position, cutoff, fs, order=5):
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = signal.filtfilt(b, a, position)
    return y


# Filter requirements.
order = 3
fs = 60       # sample rate, Hz
cutoff = 2.5  # desired cutoff frequency of the filter, Hz

# Get the filter coefficients so we can check its frequency response.
b, a = butter_lowpass(cutoff, fs, order)

# Plot the frequency response.
w, h = freqz(b, a, worN=8000)
plt.subplot(2, 1, 1)
plt.plot(0.5*fs*w/np.pi, np.abs(h), 'b')
plt.plot(cutoff, 0.5*np.sqrt(2), 'ko')
plt.axvline(cutoff, color='k')
plt.xlim(0, 0.5*fs)
plt.title("Lowpass Filter Frequency Response")
plt.xlabel('Frequency [Hz]')
plt.grid()


# Filter the data, and plot both the original and filtered signals.
y = butter_lowpass_filter(position, cutoff, fs, order)

plt.subplot(2,1,2)
plt.plot(x, position, 'b-', label='data')
plt.plot(x, y, 'g-', linewidth=2, label='filtered data')
plt.xlabel('Time [sec]')
plt.grid()
plt.legend()

plt.subplots_adjust(hspace=0.35)
plt.show()
