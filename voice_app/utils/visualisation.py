# Import dependencies
import streamlit as st
import numpy as np
import librosa
import librosa.display
import matplotlib.pyplot as plt
import os
from PIL import Image as pil_Image

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

    
def load_audio(filepath_audio):
    """
    Purpose: Create a load audio code block to adhere to DRY principles.
    
    Input: filepath_audio
    Output: y, sr, D
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
    
    return [y, sr, D]

def display_spectrogram(filepath_audio):
    """
    Purpose:
    - Display audio file's spectrogram.

    Input: filepath_audio
    Output: Displays plot
    """
    
    # Load the audio file
    y, sr, D = load_audio(filepath_audio)

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

def export_spectrogram(filepath_audio):
    """
    Purpose:
    - Export a clean version of the spectrogram.
    
    Input: filepath_audio
    Output: Creates a png in the temp folder
    """
    
    # Load the audio file
    y, sr, D = load_audio(filepath_audio)
    
    # Plot the clean spectrogram
    fig, ax = plt.subplots()
    librosa.display.specshow(
        D,
        sr = sr,
        x_axis = 'time',
        y_axis = 'linear'
    )

    # Remove labels and border
    plt.tight_layout()
    plt.title('')
    plt.axis('off')
    
    # Specify the path to default_data
    script_dir = os.path.dirname(os.path.abspath(__file__))
    voice_app_dir = os.path.dirname(script_dir)
    orig_spec = os.path.join(
        voice_app_dir, 'temp', 'original_spectrogram.png')
    
    # Export image
    plt.savefig(orig_spec, bbox_inches='tight', pad_inches=0)
    plt.close()
    
    # Define resize parameters
    new_width = 293
    new_height = 216
    
    # Resize the image
    img = pil_Image.open(orig_spec)
    
    # Resize
    resized = img.resize((new_width, new_height))

    # Create a new figure
    plt.figure(figsize = (new_width / 100, new_height/100))
    
    # Remove labels and border
    plt.tight_layout()
    plt.title('')
    plt.axis('off')
    
    # Plot the resized image
    plt.imshow(resized)

    # Updated path
    resized_spec = os.path.join(
        voice_app_dir, 'temp', 'resized_spectrogram.png')
    
    # Export updated image
    plt.savefig(resized_spec, bbox_inches='tight', pad_inches=0)