import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import numpy as np
import src.dsp as dsp

def test_eq_generation():
    fs = 44100
    duration = 1.0
    t = np.linspace(0, duration, int(fs * duration), endpoint=False)
    
    # 3 sine waves + noise
    # 1000 Hz, 5000 Hz, 12000 Hz
    sig = 0.5 * np.sin(2 * np.pi * 1000 * t) + \
          0.3 * np.sin(2 * np.pi * 5000 * t) + \
          0.2 * np.sin(2 * np.pi * 12000 * t) + \
          0.05 * np.random.normal(size=len(t))
          
    xf, mag = dsp.analyze_noise_profile(sig, fs)
    
    # We expect peaks at 1k, 5k, 12k
    eq = dsp.generate_eq_profile(xf, mag, fs=fs, num_bands=5)
    
    print(f"Found {len(eq)} peaks")
    found_freqs = sorted([p['frequency'] for p in eq])
    print(f"Found Frequencies: {found_freqs}")
    
    # Check if we found close to 1000, 5000, 12000
    expected = [1000, 5000, 12000]
    hits = 0
    missing = []
    for e in expected:
        # Check if any found freq is within 50Hz
        if any(abs(f - e) < 50 for f in found_freqs):
            hits += 1
        else:
            missing.append(e)
            
    if hits == 3:
        print("SUCCESS: Frequency identification works.")
    else:
        print(f"FAILURE: Did not find {missing}. Found: {found_freqs}")
        sys.exit(1)

if __name__ == "__main__":
    test_eq_generation()
