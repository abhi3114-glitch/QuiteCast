try:
    import numpy as np
    print("Numpy imported")
    a = np.array([1, 2, 3])
    print(f"Array: {a}")
    import scipy
    print("Scipy imported")
    from scipy.fft import rfft
    print("rfft imported")
except Exception as e:
    print(f"Error: {e}")
