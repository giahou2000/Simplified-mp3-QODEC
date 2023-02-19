# def summary(a: int, b: int) -> int:
#     print("Hello!")
#     return a+b

# print(summary(3, 5))

import numpy as np
import math
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy import fft
from frame import *
from mp3 import *
import winsound
from codec0 import *

h_coeffs = np.load('h.npy', allow_pickle=True).tolist()
# print(type(h_coeffs))
h_coeffs = h_coeffs['h'].reshape(-1,)
# print(h_coeffs[4])
# print(h_coeffs)
# print(len(h_coeffs))
# print(type(h_coeffs))

samplerate, data = wavfile.read('./myfile.wav')

fs = 44100
h = h_coeffs # the standard h coefficients
M = 32 # number of filters
H = make_mp3_analysisfb(h, M) # subband filtering analysis coefficients computation
G = make_mp3_synthesisfb(h, M) # subband filtering synthesis coefficients computation

M = 32
N = 36
samples = M*N
iterations = (data.size)/samples
# print(iterations)

xhat, Ytot = codec0(data, h, M, N)

Ytot_1 = coder0(data, h, M, N)
xhat_1 = decoder0(Ytot_1, h, M, N)