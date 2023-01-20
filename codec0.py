import numpy as np
# xhat, Ytot = codec0(wavin, h, M, N)

def codec0(wavin, h, M, N):
    """
    wavin:      wav file
    h:          standard impulse response
    M:          number of filters
    N:          number of samples
    """
    samples = M*N
    iterations = (wavin.size)/samples
    for i in range(iterations):






    x_buffer = [0 for i in range((N-1)*M + len(h))]

    print(x_buffer)
    print(np.shape(x_buffer))

# Testing
codec0(0, [1, 2, 3], 32, 36)
    
    