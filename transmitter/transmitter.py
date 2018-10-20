#!/usr/bin/python3
"""
Generates a tone.
"""

import sounddevice as sd
import scipy.signal as sp
import numpy as np
import matplotlib.pyplot as plt

# sounddevice docs: https://python-sounddevice.readthedocs.io/en/0.3.12/usage.html#recording
# scipy.signal docs: https://docs.scipy.org/doc/scipy/reference/signal.html

fs = 44100 # sampling rate (Hz)
sd.default.samplerate = fs
sd.default.channels = 2
duration = 10 # (s)
frequency = 400 # (Hz)
amplitude = 1 # half of peak-to-peak amplitude (wave varies from -1 to 1, so amplitude min is 0, max is 1)

timepoints = np.linspace(0, duration, duration*fs, dtype='float64')
wavepoints = amplitude*np.sin(timepoints*frequency*2*np.pi)
sd.play(wavepoints)
sd.wait()
