from distutils.core import setup, Extension
setup(name='freenectaudio', version='1.0',  \
      ext_modules=[Extension('freenectaudio', ['freenectaudio.c'], libraries=['freenect'])])