# Multimedia systems course | ECE AUTH | Winter semester 2022
# Simplified mp3 CODEC
# Giachoudis Christos
# Kostopoulos Andreas Marios

"""
Make the necessary imports
"""
import numpy as np
import math
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy import fft
from frame import *
from mp3 import *
import winsound
from codec0 import *
import wave

"""
Load h coefficients
"""
h_coeffs = np.load('h.npy', allow_pickle=True).tolist()
# print(type(h_coeffs)) # just checking
h_coeffs = h_coeffs['h'].reshape(-1,)
# print(h_coeffs[4]) # just checking
print("The prototype h coeffecients are:")
print(h_coeffs)
print("with size:")
print(len(h_coeffs))
# print(type(h_coeffs)) # just checking

"""
Import the sound wav file
"""
samplerate, data = wavfile.read('./myfile.wav')
print(f"WAV file imported successfully!!! This file has been created with a sample rate of {samplerate} Hz.")

"""
3.1.1: Compute H and G
"""
fs = 44100
h = h_coeffs # the standard h coefficients
M = 32 # number of filters
H = make_mp3_analysisfb(h, M) # subband filtering analysis coefficients computation
G = make_mp3_synthesisfb(h, M) # subband filtering synthesis coefficients computation

"""
3.1.2: Vizualize H and G in Hz
"""
# Preparing the figure
plt.figure(figsize=(10,5))
Hs = np.transpose(H)

# Fourier Transform
fft_h = []
for i in range(M):
    fft_h.append(fft.rfft(Hs[i]))
fft_h_db = 10*np.log10((np.abs(fft_h))**2)

# Fixing the frequency domain
n = 2 * fft_h_db[0].size - 1
timestep = 1/fs

freq = fft.rfftfreq(n, timestep)

# Plotting
for i in range(M):
    plt.plot(freq, fft_h_db[i])

plt.show()

"""
3.1.3: Vizualize H and G in barks
"""
# Typical Conversion 
bark = 13*np.arctan(0.00076*freq) + 3.5*np.arctan((freq/7500)**2)

# Traunmuller conversion (same thing, just another way to make the conversion to barks)
# bark = ((26.81*freq) / (1960+freq)) - 0.53
# Wang, Sekey & Gersho (not working properly)
# bark = 6 * np.arccosh(freq/600)

# Plotting

# Preparing the figure
plt.figure(figsize=(10,5))
for i in range(M):
    plt.plot((bark), fft_h_db[i])

plt.show()

"""
3.1.4: Call codec0
"""
N = 36
samples = M*N
iterations = (data.size)/samples
print(f"{iterations} iterations where done for the calculations")
xhat, Ytot = codec0(data, h, M, N)

"""
3.1.5: Call coder0
"""
Ytot_1 = coder0(data, h, M, N)

"""
3.1.6: Call decoder0
"""
xhat_1 = decoder0(Ytot_1, h, M, N)

"""
3.1.7a: Compare the 2 signals(sound files)
"""
# Original file test
winsound.PlaySound('myfile.wav', winsound.SND_FILENAME)

# Test file after applying the codec
out = wave.open("sound.wav", "wb")
out.setnchannels(1)
out.setsampwidth(2) # number of bytes
out.setframerate(samplerate)
out.writeframesraw(xhat)
# winsound.PlaySound('sound.wav', winsound.SND_FILENAME)

"""
3.1.7b: Compute the SNR of error: x - xhat
"""
shift = 480
shifted_xhat = np.copy(xhat[:-shift])
shifted_data = np.copy(data[shift:])
print(data.size)
print(xhat.size)
print(xhat_1.size)
diff = data - xhat
# Preparing the figure
plt.figure(figsize=(10,5))
plt.plot(diff)
plt.show()