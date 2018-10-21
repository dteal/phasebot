#/usr/bin/python3
"""
Generates tones with arbitrary frequencies and modulation.
"""

import sounddevice as sd
import math
import scipy.signal as sp
import numpy as np
import matplotlib.pyplot as plt

# sounddevice docs: https://python-sounddevice.readthedocs.io/en/0.3.12/usage.html#recording
# scipy.signal docs: https://docs.scipy.org/doc/scipy/reference/signal.html

fs = 44100 # sampling rate (Hz)
sd.default.samplerate = fs
sd.default.channels = 2
duration = 1 # (s)

frequencies = [400, 500, 600, 700] # Hz
modulation = [1, 0.5, 0.25, 0.125] # %

timepoints = np.linspace(0, duration, duration*fs, dtype='float64')
signal = np.zeros(timepoints.size)
for index, freq in enumerate(frequencies):
    oscillator = np.sin(timepoints*freq*2*np.pi)
    for i in range(len(oscillator)):
        if (i*1.0/len(oscillator))/modulation[index]<1:
            oscillator[i]=0

    plt.plot(oscillator); plt.show()

while True:
    sd.play(signal)
    sd.wait()
