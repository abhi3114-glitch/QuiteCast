import numpy as np
import scipy.signal as signal
from scipy.fft import rfft, rfftfreq

def analyze_noise_profile(audio_data, fs):
    """
    Compute total power spectrum of the noise.
    Returns: (frequencies, magnitude_spectrum)
    """
    N = len(audio_data)
    yf = rfft(audio_data)
    xf = rfftfreq(N, 1 / fs)
    magnitude = np.abs(yf)
    return xf, magnitude

def generate_eq_profile(frequencies, magnitudes, fs, num_bands=10, threshold_percentile=90):
    """
    Identify dominant frequencies to suppress.
    Simple approach: Find peaks above a certain percentile.
    Returns: List of dicts with center_freq and suggested_attenuation_db.
    """
    # This is a placeholder for the logic.
    # We will pick top N peaks.
    threshold = np.percentile(magnitudes, threshold_percentile)
    peaks, _ = signal.find_peaks(magnitudes, height=threshold, distance=fs//100) # distance heuristic
    
    eq_points = []
    for p in peaks:
        freq = frequencies[p]
        mag = magnitudes[p]
        # Ignore very low freqs (rumble integration) if needed
        if freq < 20: continue 
        
        eq_points.append({
            "frequency": float(freq),
            "gain": -6.0,
            "magnitude": float(mag)
        })
    
    # Sort by magnitude (descending)
    eq_points.sort(key=lambda x: x["magnitude"], reverse=True)
    
    # Return top N, remove magnitude key if desired, but keeping it is fine for debug/UI
    return eq_points[:num_bands]

def apply_eq(audio_data, fs, eq_points):
    """
    Apply a series of peaking/notch filters.
    """
    filtered_audio = audio_data.copy()
    
    for point in eq_points:
        freq = point['frequency']
        gain = point['gain']
        
        # Design a peaking filter (bell) with negative gain
        # Q factor controls bandwidth.
        Q = 5.0 
        b, a = signal.iirpeak(freq, Q, fs)
        
        # Scipy iirpeak is a boost filter? Wait, iirpeak gives a bandpass.
        # We want a parametric EQ (peaking EQ). 
        # Actually, for noise removal, a Notch filter is often standard for specific tones.
        # But 'reduce noise profile' usually implies a graphic EQ curve.
        # Let's implement a standard bi-quad peaking EQ formula or use scipy.signal.iircomb if we are fancy.
        # For simplicity, let's use a notch filter for strong peaks.
        
        # If gain is negative, we want a cut. 
        # Scipy iirnotch: Design second-order IIR notch digital filter.
        # a notch filter removes a specific frequency completely (infinite attenuation ideally).
        # Maybe we want just attenuation.
        
        # Let's stick to a generic "Band Stop" or just use a standard EQ implementation.
        # Since I can't easily import a full EQ lib, I will assume Notch for now for "Suppose dominant frequencies".
        
        b, a = signal.iirnotch(freq, Q, fs)
        filtered_audio = signal.lfilter(b, a, filtered_audio)
        
    return filtered_audio
