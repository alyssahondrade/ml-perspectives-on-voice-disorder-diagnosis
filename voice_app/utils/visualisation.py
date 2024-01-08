# Import dependencies
import streamlit as st
import numpy as np
import librosa
import librosa.display
import matplotlib.pyplot as plt

def display_waveform(filepath_audio):
    """
    Purpose:
    - Display audio file's waveform.

    Input: filepath_audio
    Output: Displays plot
    """

    # Load the audio file using librosa
    y, sr = librosa.load(
        filepath_audio,
        sr = None # preserve sampling rate
    )

    # Plot the waveform
    librosa.display.waveshow(y, sr=sr)

    # Add the labels
    plt.title('Waveform')
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')


def display_spectrogram(filepath_audio):
    """
    Purpose:
    - Display audio file's spectrogram.

    Input: filepath_audio
    Output: Displays plot
    """
    
    # Load the audio file using librosa
    y, sr = librosa.load(
        filepath_audio,
        sr = None # preserve sampling rate
    )

    # Plot the spectrogram
    D = librosa.amplitude_to_db(
        np.abs(librosa.stft(y)),
        ref = np.max
    )

    # Plot the spectrogram
    librosa.display.specshow(
        D,
        sr = sr,
        x_axis = 'time',
        y_axis = 'linear' # can also choose: linear
    )
    
    # Add labels
    plt.title('Spectrogram')
    plt.colorbar(format='%+2.0f dB')