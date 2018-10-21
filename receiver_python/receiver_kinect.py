#!/usr/bin/python3
"""
Records a tone using the Kinect 360.
"""

import sounddevice as sd
import scipy.signal as sp
import scipy.fftpack as sf
import numpy as np
import matplotlib.pyplot as plt
#import pygame
import queue
import freenectaudio as fa

# sounddevice docs: https://python-sounddevice.readthedocs.io/en/0.3.12/usage.html#recording
# scipy.signal docs: https://docs.scipy.org/doc/scipy/reference/signal.html

# design for 8 kHz
fs = 16000 # sampling rate (Hz)
freq = 440 # frequency of interest (Hz)
duration = .05 # block time (s)


def design_bandpass(low, high, fs, order):
    nyq = fs * 0.5
    return sp.butter(order, [low/nyq, high/nyq], btype='bandpass')
def apply_bandpass(signal):
    b, a = design_bandpass(390, 410, fs, order=3)
    print(b,a)
    return scipy.signal.lfilter(b, a, signal, axis=0)

class Recorder:
    def __init__(self):
        self.data = np.zeros((int(fs*duration), 4))
        self.phase14 = np.zeros((10,))

    def callback(self, mic1, mic2, mic3, mic4, buffered_frames_remaining):
        np.roll(self.data, 1, axis=0)
        self.data[0,0] = mic1
        self.data[0,1] = mic2
        self.data[0,2] = mic3
        self.data[0,3] = mic4
        if buffered_frames_remaining == 0:
            self.process() # take time off to process data

    def process(self):
        n = self.data.shape[0]
        window = np.reshape(sp.windows.hamming(n), (n,1))
        signal = self.data * window
        amplitudes = np.abs(np.real(sf.fft(signal, axis=0)[0:n//2]))
        phases = np.imag(sf.fft(signal, axis=0)[0:n//2])
        freqs = np.linspace(0, fs/2, n//2)
        index = int(440*n/fs)
        self.phase14 = np.roll(self.phase14, 1)
        self.phase14[0] = phases[index, 0] - phases[index, 3]
        print(np.average(self.phase14))

#pygame.init()
#screen = pygame.display.set_mode((500,500))
r = Recorder()
fa.init_audio(r.callback)
"""
done = False
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    phase = np.average(r.phase)
    if phase < -20:
        phase = -20
    if phase > 20:
        phase = 20
    screen.fill((0,0,0))
    pygame.draw.rect(screen, ((phase+20)*255/40, 0, 255 - (phase+20)*255/40), pygame.Rect(int((phase+20)*10), 0, 100, 500))
    pygame.display.flip()
"""
