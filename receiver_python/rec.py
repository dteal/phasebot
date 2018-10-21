#!/usr/bin/python3
"""
Records a tone.
"""

import sounddevice as sd
import scipy.signal as sp
import scipy.fftpack as sf
import numpy as np
import matplotlib.pyplot as plt

# sounddevice docs: https://python-sounddevice.readthedocs.io/en/0.3.12/usage.html#recording
# scipy.signal docs: https://docs.scipy.org/doc/scipy/reference/signal.html

# design for 8 kHz
fs = 40000 # sampling rate (Hz)
freq = 400 # frequency of interest (Hz)
duration = .1 # block time (s)

def design_bandpass(low, high, fs, order):
    nyq = fs * 0.5
    return sp.butter(order, [low/nyq, high/nyq], btype='bandpass')
def apply_bandpass(signal):
    b, a = design_bandpass(390, 410, fs, order=3)
    print(b,a)
    return scipy.signal.lfilter(b, a, signal, axis=0)

class Recorder:
    def __init__(self):
        self.count = 0

    def callback(self, data, frames, time, status):
        n = data.shape[0]
        window = np.reshape(sp.windows.hamming(n), (n,1))
        signal = data[:] * window
        amplitudes = np.abs(np.real(sf.fft(signal, axis=0)[0:n//2]))
        phases = np.imag(sf.fft(signal, axis=0)[0:n//2])
        freqs = np.linspace(0, fs/2, n//2)
        index = int(400*n/fs)
        print(phases[index, 0] - phases[index, 1])

r = Recorder()
stream = sd.InputStream(channels=2, samplerate=fs, callback=r.callback, blocksize=int(duration*fs))
with stream:
    while True:
        pass

