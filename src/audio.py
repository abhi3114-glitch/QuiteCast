import sounddevice as sd
import numpy as np
import soundfile as sf

def record_audio(duration, fs=44100, channels=1):
    """
    Record audio for a specific duration.
    Returns: numpy array of the recording.
    """
    print(f"Recording for {duration} seconds...")
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=channels)
    sd.wait()  # Wait until recording is finished
    print("Recording finished")
    return recording.flatten()

def save_audio(data, fs, filename):
    sf.write(filename, data, fs)

def load_audio(filename):
    data, fs = sf.read(filename)
    return data, fs
