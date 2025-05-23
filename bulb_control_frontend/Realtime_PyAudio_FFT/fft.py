"""Applies the Fast Fourier Transformation (FFT) to audio data from initialised audio source"""

import numpy as np


def getFFT(data, log_scale=False):
    """Returns the FFT of the given data"""
    data = data * np.hamming(len(data))
    try:
        FFT = np.abs(np.fft.rfft(data)[1:])
    except:
        FFT = np.fft.fft(data)
        left, right = np.split(np.abs(FFT), 2)
        FFT = np.add(left, right[::-1])

    if log_scale:
        try:
            FFT = np.multiply(20, np.log10(FFT))
        except Exception as e:
            print("Log(FFT) failed: %s" % str(e))

    return FFT
