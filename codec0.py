"""
3.1.4: Subband filtering
Implementation of codec0, coder0 and decoder0 functions.
We import frame, mp3 and nothing python files that are given by the task.
"""

import numpy as np
from frame import *
from mp3 import *
from nothing import *

def codec0(wavin, h, M, N):
    """
    wavin:      wav file to be coded and decoded
    h:          standard impulse response
    M:          number of filters
    N:          number of samples

    The function returns two matrices:
    - Ytot: has a size of [iterations*N, M]
    - xhat: vector
    """
    H = make_mp3_analysisfb(h, M)
    G = make_mp3_synthesisfb(h, M)
    L = len(h)

    # 3.1.4.a: Reading samples and calculating the iterations
    samples = M*N # 32X36
    iterations = int((wavin.size)/samples)
    print(f"iterations: {iterations}")

    # buffer size given by the task: q = (N-1)*M + L
    # Creating Ytot and xhat matrices
    Ytot = np.empty([0, M])
    xhat = []

    padding = L - M
    for i in range(iterations):
        # We have to perform a padding action for the last iteration 
        if (i == iterations - 1):
            x_buffer = wavin[(i * samples) : (((i+1) * samples))]
            x_buffer = np.pad(x_buffer, (0, padding), 'constant')
        else: 
            x_buffer = wavin[(i * samples) : (((i+1) * samples + padding))]
        
        # 3.1.4.b: Computation of the frame Y
        Y = frame_sub_analysis(x_buffer, H, N)

        # 3.1.4.c: Process via donothing function
        Yc = donothing(Y)
        
        # 3.1.4.d: Collect the coded frames into Ytot matrix
        Ytot = np.append(Ytot, Yc, axis=0)

        # 3.1.4.e: For each frame we perform the inverse idonothing function
        Yh = idonothing(Yc)

        # 3.1.4.f: Production of xhat vector using the frame_sub_synthesis function
        xhat = np.append(xhat, frame_sub_synthesis(Yh, G))
    
    return xhat, Ytot

    # 3.1.5: Coder0 Implementation. Function that implements the steps 3.1.4.a - 3.1.4.d
def coder0(wavin, h, M, N):

    """
    wavin:      wav file to be coded
    h:          standard impulse response
    M:          number of filters
    N:          number of samples

    The function returns the Ytot matrix
    """
    H = make_mp3_analysisfb(h, M)
    L = len(h)

    # 4.a: Reading samples and calculating the iterations
    samples = M*N # 32X36
    iterations = int((wavin.size)/samples)

    # buffer size q = (N-1)*M + L
    Ytot = np.empty((0, M))
    
    padding = L - M
    for i in range(iterations):
        if (i == iterations - 1):
            x_buffer = wavin[(i * samples) : (((i+1) * samples))]
            x_buffer = np.pad(x_buffer, (0, padding), 'constant')
        else: 
            x_buffer = wavin[(i * samples) : (((i+1) * samples + L - M))]
        
        Y = frame_sub_analysis(x_buffer, H, N)
        Yc = donothing(Y)
        Ytot = np.append(Ytot, Yc, axis=0)

    return Ytot

# 3.1.6: Decoder Implementation. Function that implement steps 3.1.4.e and 3.1.4.f
def decoder0(Ytot, h, M, N):
    """
    Ytot:       the coder result
    h:          standard impulse response
    M:          number of filters
    N:          number of samples

    The function returns the decoded vector xhat
    """
    G = make_mp3_synthesisfb(h, M)

    iterations = int(len(Ytot) / N)
    print(f"iterations: {iterations}")
    
    xhat = np.array(0)
    for i in range(iterations):
        """
        Yc calculation through Ytot
        """
        Yh = idonothing(Ytot[i*N:(i*N + N), :])
        xhat = np.append(xhat, frame_sub_synthesis(Yh, G))
 
    return xhat
    
    