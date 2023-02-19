import numpy as np
from frame import *
from mp3 import *
from nothing import *
# xhat, Ytot = codec0(wavin, h, M, N)

def codec0(wavin, h, M, N):
    """
    wavin:      wav file
    h:          standard impulse response
    M:          number of filters
    N:          number of samples
    """
    H = make_mp3_analysisfb(h, M)
    G = make_mp3_synthesisfb(h, M)
    L = len(h)
    # H: 512 x 32

    # 4.a: Reading samples
    samples = M*N # 32X36
    iterations = (wavin.size)/samples
    print(f"iterations: {iterations}")

    # buffer size
    q = (N-1)*M + L
    Ytot = []
    xhat = []
    
    padding = L - M
    count = 0
    for i in range(int(iterations)):
        if (i == iterations - 1):
            x_buffer = wavin[(i * samples) : (((i+1) * samples))]
            x_buffer = np.pad(x_buffer, (0, padding), 'constant')
            # print("If check")
        else: 
            # print("Check")
            x_buffer = wavin[(i * samples) : (((i+1) * samples + L - M))]
        
        # print(f"Size of x_buffer: {np.shape(x_buffer)}")
        Y = frame_sub_analysis(x_buffer, H, N)
        Yc = donothing(Y)
        Ytot = np.append(Ytot, Yc)
        Yh = idonothing(Yc)
        xhat = np.append(xhat, frame_sub_synthesis(Yh, G))
    print(np.shape(Ytot))
    return xhat, Ytot

    # Coder0 Implementation
def coder0(wavin, h, M, N):

    """
    wavin:      wav file
    h:          standard impulse response
    M:          number of filters
    N:          number of samples
    """
    H = make_mp3_analysisfb(h, M)
    G = make_mp3_synthesisfb(h, M)
    L = len(h)
    # H: 512 x 32

    # 4.a: Reading samples
    samples = M*N # 32X36
    iterations = (wavin.size)/samples
    print(f"iterations: {iterations}")

    # buffer size
    # q = (N-1)*M + L
    Ytot = []
    
    padding = L - M
    for i in range(int(iterations)):
        if (i == iterations - 1):
            x_buffer = wavin[(i * samples) : (((i+1) * samples))]
            x_buffer = np.pad(x_buffer, (0, padding), 'constant')
            # print("If check")
        else: 
            # print("Check")
            x_buffer = wavin[(i * samples) : (((i+1) * samples + L - M))]
        
        # print(f"Size of x_buffer: {np.shape(x_buffer)}")
        Y = frame_sub_analysis(x_buffer, H, N)
        Yc = donothing(Y)
        Ytot = np.append(Ytot, Yc)

    print("Coder sucks!")
    return Ytot


def decoder0(Ytot, h, M, N):
    """
    Ytot:       the coder result
    h:          standard impulse response
    M:          number of filters
    N:          number of samples
    """
    G = make_mp3_synthesisfb(h, M)

    # 4.a: Reading samples
    samples = M*N # 32X36
    iterations = np.size(Ytot)/samples
    print(f"iterations: {iterations}")
    
    xhat = []
    for i in range(int(iterations)):
        Yh = idonothing(Ytot[i*samples : i*samples + samples])
        xhat = np.append(xhat, frame_sub_synthesis(Yh, G))

    print("Decoder sucks as well!")  
    return xhat

# Testing
# xhat, Ytot = codec0(np.array([0, 5, 3, 5, 3, 4]), np.array([1, 2, 3]), 32, 36)
# print(xhat)
# print("==============================")
# print(Ytot)
    
    