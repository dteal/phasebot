#!/usr/bin/python3
"""
Records a tone.
"""

import sounddevice as sd
import scipy.signal as sp
import scipy.fftpack as sf
import numpy as np
import matplotlib.pyplot as plt
import pygame
import queue

# sounddevice docs: https://python-sounddevice.readthedocs.io/en/0.3.12/usage.html#recording
# scipy.signal docs: https://docs.scipy.org/doc/scipy/reference/signal.html

# design for 8 kHz
fs = 48000 # sampling rate (Hz)
freq = 17950 # frequency of interest (Hz)
duration = .001 # block time (s)

class Recorder:
    def __init__(self):
        self.phase = np.zeros((10,))

    def callback(self, data, frames, time, status):
        n = data.shape[0]
        window = np.reshape(sp.windows.hamming(n), (n,1))
        signal = data[:] * window
        amplitudes = np.abs(np.real(sf.fft(signal, axis=0)[0:n//2]))
        phases = np.imag(sf.fft(signal, axis=0)[0:n//2])
        freqs = np.linspace(0, fs/2, n//2)
        index = int(17950*n/fs)-1
        self.phase = np.roll(self.phase, 1)
        self.phase[0] = phases[index, 0] - phases[index, 1]
        print(amplitudes[index,0])

pygame.init()
screen = pygame.display.set_mode((500,500))
r = Recorder()
stream = sd.InputStream(channels=2, samplerate=fs, callback=r.callback, blocksize=int(duration*fs))
with stream:
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
