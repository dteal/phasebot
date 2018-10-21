#!/usr/bin/python3
"""
Records a tone using the Kinect 360.
"""

import sounddevice as sd
import scipy.signal as sp
import scipy.fftpack as sf
import numpy as np
import matplotlib.pyplot as plt
import wave
#import pygame
import queue
import freenectaudio as fa
#import scipy.io.wavfile as sw
import sys

# sounddevice docs: https://python-sounddevice.readthedocs.io/en/0.3.12/usage.html#recording
# scipy.signal docs: https://docs.scipy.org/doc/scipy/reference/signal.html

# design for 8 kHz
fs = 16000 # sampling rate (Hz)
freq = 880 # frequency of interest (Hz)
duration = .05 # block time (s)


def design_bandpass(low, high, fs, order):
    nyq = fs * 0.5
    return sp.butter(order, [high/nyq], btype='highpass')
def apply_bandpass(signal):
    b, a = design_bandpass(0.0, 10.0, 50.0, order=3)
    return sp.lfilter(b, a, signal, axis=0)

class Recorder:
    def __init__(self):
        #self.data = np.zeros((int(fs*duration), 4))
        self.data = np.zeros((256, 4))
        self.phase1 = np.zeros((100, ))[:]
        self.phase2 = np.zeros((100, ))[:]
        self.phase3 = np.zeros((100, ))[:]
        self.phase4 = np.zeros((100, ))[:]

        self.phase14 = np.zeros((5, ))[:]
        self.phase13 = np.zeros((5, ))[:]
        self.phase12 = np.zeros((5, ))[:]
        self.phase24 = np.zeros((5, ))[:]
        self.phase23 = np.zeros((5, ))[:]
        self.phase34 = np.zeros((5, ))[:]

    def callback(self, mic1, mic2, mic3, mic4, buffered_frames_remaining):
        self.data[0,0] = mic1*1.0
        self.data[0,1] = mic2*1.0 # microphones 2,3,4 have ~7,8,9 sample delay
        self.data[0,2] = mic3*1.0 # compared to microphone 1
        self.data[0,3] = mic4*1.0
        self.data = np.roll(self.data, -1, axis=0)
        #if not self.data[0,0] == 0:
        #    sw.write('test.wav', fs, self.data[:,0])
        #    sys.exit(0)
        if buffered_frames_remaining == 0:
            self.process() # take time off to process data

    def process(self):
        n = self.data.shape[0]
        #sw.write(outfile, fs, self.data[:,0])
        #window = np.reshape(sp.windows.hamming(n), (n,1))
        signal = self.data# * window
        #print('{}\t{}\t{}'.format(np.average(signal[:,0]), np.max(signal[:,0]), np.min(signal[:,0])))
        #plt.plot(apply_bandpass(signal[:,0])); plt.show()
        #amplitudes = np.abs(np.real(sf.fft(signal, axis=0)[0:n//2]))
        phases = np.imag(sf.fft(signal, axis=0)[0:n//2])
        index = int(880*n/fs)
        #print('{0: >#016.4f}'.format(amplitudes[index, 3]/1e6))
        #print('{0: >#016.4f}'.format(phases[index, 0]/1e6))

        self.phase1 = np.roll(self.phase1, 1)
        self.phase2 = np.roll(self.phase1, 2)
        self.phase3 = np.roll(self.phase1, 3)
        self.phase4 = np.roll(self.phase1, 4)
        self.phase1[0] = phases[index,0]
        self.phase1[1] = phases[index,1]
        self.phase1[2] = phases[index,2]
        self.phase1[3] = phases[index,3]

        self.phase14 = apply_bandpass(self.phase1)[-1] - apply_bandpass(self.phase4)[-1]
        print('{0: >#016.4f}'.format(self.phase14/1e6))

        #print('{: >#016.4f}{: >#016.4f}{: >#016.4f}{: >#016.4f}{: >#016.4f}{: >#016.4f}'.format(np.average(self.phase14)/1e6, np.average(self.phase13)/1e6, np.average(self.phase12)/1e6, np.average(self.phase24)/1e6, np.average(self.phase23)/1e6, np.average(self.phase34)/1e6))
        self.data = np.zeros((256, 4))

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
