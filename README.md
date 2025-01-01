# QuietCast

**Personalized Noise Filter Based on Room Audio Sample**

QuietCast records a few seconds of your ambient room noise (e.g., fan, hum, AC) and generates a custom EQ curve to suppress those specific frequencies from your audio.

## Features

- **Noise Profiling**: Records 5-10 seconds of room noise using your microphone.
- **Spectrum Analysis**: Visualizes the frequency spectrum of your environment to identify noise peaks.
- **Auto-EQ**: Automatically detects dominant noise frequencies and generates a suppression filter.
- **Preview Mode**: Upload an audio file or song to hear the difference with the filter applied.
- **Export**: Download the generated EQ preset as a JSON file.

## Setup and Run

1.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

2.  **Run the App**:
    *For Python 3.11 (Recommended):*
    ```bash
    py -3.11 -m streamlit run app.py
    ```
    *Standard Launch:*
    ```bash
    streamlit run app.py
    ```

## Usage

1.  **Record**: Click "Record Room Noise" and remain quiet for the duration of the recording.
2.  **Analyze**: The application will display the frequency spectrum. Look for peaks which indicate noise.
3.  **Generate**: Click "Generate QuietCast EQ". The app will calculate the optimal filter bands.
4.  **Preview**: Upload a music track (WAV/MP3) to hear the noise reduction effect.
5.  **Export**: Download the JSON preset for use in other EQ software or for your records.

## Privacy Note

All processing is done **locally** on your machine. Audio is processed in memory and never uploaded to the cloud.

> [!WARNING]
> **Environment Note:** This project relies on `numpy` and `scipy`.
> If you are using **Python 3.14 (Pre-release)**, you may experience crashes or import errors.
> It is highly recommended to use a stable Python version (e.g., **3.10**, **3.11**, or **3.12**).
