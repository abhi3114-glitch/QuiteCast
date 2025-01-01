import streamlit as st
import numpy as np
import src.audio as audio_mod
import src.dsp as dsp_mod
import soundfile as sf
import io
import json

st.set_page_config(page_title="QuietCast", layout="wide")

st.title("QuietCast 🎧")
st.markdown("### Personalized Noise Filter Generator")
st.markdown("record room noise -> analyze -> generate EQ -> silence the world")

if 'noise_data' not in st.session_state:
    st.session_state.noise_data = None
if 'fs' not in st.session_state:
    st.session_state.fs = 44100
if 'eq_profile' not in st.session_state:
    st.session_state.eq_profile = None

# --- SIDEBAR ---
with st.sidebar:
    st.header("Settings")
    duration = st.slider("Recording Duration (s)", 3, 15, 5)
    fs = st.selectbox("Sample Rate", [44100, 48000], index=0)
    st.session_state.fs = fs

# --- SECTION 1: RECORD ---
st.divider()
st.subheader("1. Setup Noise Profile")

col1, col2 = st.columns([1, 2])
with col1:
    if st.button("🎙️ Record Room Noise"):
        with st.spinner(f"Recording for {duration} seconds... Please stay quiet."):
            # We need to run this potentially in a way that doesn't freeze UI, 
            # but Streamlit runs script top-to-bottom. 
            # sounddevice.rec is non-blocking but we used sd.wait().
            # This will block the UI, which is fine for 5-10s.
            try:
                data = audio_mod.record_audio(duration, fs=fs)
                st.session_state.noise_data = data
                st.success("Recording complete!")
            except Exception as e:
                st.error(f"Error recording: {e}")

# Helper to cache expensive DSP operations
@st.cache_data
def cached_analyze(data, fs):
    return dsp_mod.analyze_noise_profile(data, fs)

@st.cache_data
def cached_generate_eq(xf, mag, fs):
    return dsp_mod.generate_eq_profile(xf, mag, fs=fs)

@st.cache_data
def cached_apply_eq(audio_i, fs_i, eq_i):
    # wrapper to allow hashing if needed, but numpy arrays work
    return dsp_mod.apply_eq(audio_i, fs_i, eq_i)

with col2:
    if st.session_state.noise_data is not None:
        st.audio(st.session_state.noise_data, sample_rate=fs)
        
        # Analyze
        xf, mag = cached_analyze(st.session_state.noise_data, fs)
        
        # Plot Spectrum - Downsampled for performance
        # 10s of audio @ 44k = 440k samples. Spectrum is 220k bins.
        # Streamlit frontend chokes on that. Decimate to ~1000-2000 points.
        decimation_factor = max(1, len(xf) // 2000)
        
        # We only care about up to 20kHz usually, which is index len(xf).
        # Just standard slicing.
        st.line_chart(dict(zip(xf[:len(xf)//2:decimation_factor], mag[:len(mag)//2:decimation_factor])))
        
        # Generate EQ
        if st.button("Generate QuietCast EQ"):
            eq = cached_generate_eq(xf, mag, fs=fs)
            st.session_state.eq_profile = eq
            st.success(f"Generated {len(eq)} filter bands!")

# --- SECTION 2: EQ AND EXPORT ---
if st.session_state.eq_profile:
    st.divider()
    st.subheader("2. Your Noise Profile")
    
    # Display EQ bands
    eq_data = st.session_state.eq_profile
    st.json(eq_data, expanded=False)
    
    st.download_button(
        label="Download Preset JSON",
        data=json.dumps(eq_data, indent=2),
        file_name="quietcast_preset.json",
        mime="application/json"
    )

# --- SECTION 3: PREVIEW ---
    st.divider()
    st.subheader("3. Preview Cancellation")
    
    uploaded_file = st.file_uploader("Upload a music track / audio sample to test", type=["wav", "mp3"])
    
    if uploaded_file:
        # Load audio
        # sf.read accepts file-like objects? Yes usually.
        try:
             # soundfile might need a workaround for bytesIO depending on version, 
             # usually works.
            preview_data, preview_fs = sf.read(uploaded_file)
            
            # If stereo, mix to mono for simple processing or process channels separately.
            # Our dsp.py apply_eq expects 1D likely.
            if len(preview_data.shape) > 1:
                st.warning("Stereo detected. Processing first channel only for preview.")
                preview_data_mono = preview_data[:, 0]
            else:
                preview_data_mono = preview_data

            if st.button("Apply QuietCast Filter"):
                filtered = cached_apply_eq(preview_data_mono, preview_fs, st.session_state.eq_profile) # use cache
                
                c1, c2 = st.columns(2)
                with c1:
                    st.caption("Original")
                    st.audio(uploaded_file)
                with c2:
                    st.caption("Filtered (Noise Reduced)")
                    # We need to write to bytes to play
                    out_io = io.BytesIO()
                    sf.write(out_io, filtered, preview_fs, format='WAV')
                    st.audio(out_io.getvalue(), format="audio/wav")
                    
        except Exception as e:
            st.error(f"Error processing file: {e}")
