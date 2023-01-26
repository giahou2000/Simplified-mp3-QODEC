import numpy as np
from frame import *
from mp3 import *
# xhat, Ytot = codec0(wavin, h, M, N)

def codec0(wavin, h, M, N):
    """
    wavin:      wav file
    h:          standard impulse response
    M:          number of filters
    N:          number of samples
    """
    H = make_mp3_analysisfb(h, M)

    samples = M*N
    iterations = (wavin.size)/samples
    q = 10 # something else
    for i in range(iterations):
        x_buffer = wavin[(i * samples) : (i * samples + samples - 1)]
        Y = frame_sub_analysis(x_buffer, H, q)

    print(x_buffer)
    print(np.shape(x_buffer))

# Testing
codec0(0, [1, 2, 3], 32, 36)
    
    