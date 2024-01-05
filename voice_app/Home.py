# Import dependencies
import streamlit as st
import pandas as pd
import numpy as np
import os
import json

import matplotlib.pyplot as plt
from utils.visualisation import display_waveform, display_spectrogram

def page_configuration():
    st.set_page_config(
        page_title = "Voice Disorder Diagnosis",
        page_icon = ":home:"
    )
    
    st.title("Voice Disorder Diagnosis")
    st.header("Machine Learning Models")


def audio_select():
    # Define the path to the directory
    audio_path = "assets/sample_audio/"
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


def main():
    page_configuration()
    st.divider()
    audio_select()
    
    # Read JSON file
    data_path = 'assets/default_data.json'
    with open(data_path, 'r') as file:
        data = json.load(file)
    
    st.header('Questionnaire')
    
    
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Age")

    with col2:
        
        # Age input
        user_age = st.number_input(
            label = "Age",
            min_value = data['min_age'],
            max_value = data['max_age'],
            value = "min"
        )
        
        # Gender input
        user_gender = st.radio(
            label = "Gender",
            options = data['gender_options'],
            horizontal = True
        )
        
        # VHI Score
        # user_vhi = st.number_input(
            # label = "VHI Score",


if __name__ == '__main__':
    main()