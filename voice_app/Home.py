# Import dependencies
import streamlit as st
import pandas as pd
import numpy as np
import os
import json
import joblib

import matplotlib.pyplot as plt
from utils.visualisation import display_waveform, display_spectrogram
from utils.interaction import metadata_questionnaire
from utils.interaction import build_sidebar
from utils.preprocessing import meta_preprocessing


def page_configuration():
    st.set_page_config(
        page_title = "Voice Disorder Diagnosis",
        page_icon = ":home:"
    )
    
    st.title("Voice Disorder Diagnosis")
    st.header("Machine Learning Models")


def audio_select():
    # Define the path to the directory
    # audio_path = "assets/sample_audio/"
    # audio_path = os.path.abspath("assets/sample_audio/")
    # audio_files = os.listdir(audio_path)
    
    # Get the absolute path to the current script (Home.py)
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Specify the path to the "assets/sample_audio" folder
    audio_path = os.path.join(script_dir, 'assets', 'sample_audio')

    # List the files in the "sample_audio" folder
    audio_files = os.listdir(audio_path)
    
    # Dynamically update names in the file
    audio_mapping = dict()
    for idx, filename in enumerate(audio_files):
        audio_name = f"Audio {idx + 1}"
        audio_mapping[audio_name] = filename

    # Create the buttons for the audio files
    selected_radiobutton = st.radio(
        "Select a sample audio file",
        list(audio_mapping.keys()),
        horizontal = True
    )
    
    # Get the file selected
    selected_audio = os.path.join(
        audio_path,
        audio_mapping[selected_radiobutton]
    )
    
    # Button to play the audio
    st.audio(
        selected_audio,
        format = "audio/wav",
        start_time = 0
    )
    
    # Plot the selected waveform
    st.subheader("Waveform")
    fig_wave = plt.figure()
    display_waveform(selected_audio)
    st.pyplot(fig_wave)

    # Plot the selected spectrogram
    st.subheader("Spectrogram")
    fig_spec = plt.figure()
    display_spectrogram(selected_audio)
    st.pyplot(fig_spec)

    
def build_uploader():
    user_voice = st.file_uploader(
        label = "Upload your voice sample",
        type = "wav",
        accept_multiple_files = False,
        label_visibility = "visible"
    )
    

def main():
    page_configuration()
    build_sidebar()
    st.divider()
    build_uploader()
    audio_select()
    st.divider()


if __name__ == '__main__':
    main()