#!/usr/bin/python3
"""
Records a tone.
"""

import sounddevice as sd
import scipy.signal as sp
import scipy.fftpack
import numpy as np
import matplotlib.pyplot as plt

# sounddevice docs: https://python-sounddevice.readthedocs.io/en/0.3.12/usage.html#recording
# scipy.signal docs: https://docs.scipy.org/doc/scipy/reference/signal.html

# design for 8 kHz
fs = 48000 # sampling rate (Hz)
freq = 15030 # frequency of interest (Hz)
count = 0
duration = .01

def design_bandpass(low, high, fs, order):
    """
    Returns parameters (numerator, denominator) for a bandpass filter
    with the given low and high frequency cutoffs, sampling frequency,
    and order.
    """
    nyq = fs * 0.5
    return sp.butter(order, [low/nyq, high/nyq], btype='bandpass')

def apply_bandpass(signal):
    b, a = design_bandpass(19900, 20100, fs, order=3)
    print(b,a)
    return scipy.signal.lfilter(b, a, signal, axis=0)

class Recorder:
    def __init__(self):
        self.count = 0

    def callback(self, indata, frames, time, status):
        print('==========')
        if self.count == 0:
            print(indata.shape)
            print(self.count)
            print(frames)
            print(time)
            print(status)
            plt.plot(indata); plt.title('data')
            plt.plot(apply_bandpass(indata)); plt.title('data'); plt.show()
            plt.plot(np.abs(scipy.fftpack.fft(indata, axis=0)[0:int(len(indata)/2)])); plt.title('fft')
            plt.plot(np.abs(scipy.fftpack.fft(apply_bandpass(indata), axis=0)[0:int(len(indata)/2)])); plt.title('fft'); plt.show()
        self.count += 1

r = Recorder()
with sd.InputStream(channels=1, callback=r.callback, blocksize=int(duration*fs)):
    pass
    #while True:
        #pass

