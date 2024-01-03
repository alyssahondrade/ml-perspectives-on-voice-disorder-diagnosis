# Import dependencies
import streamlit as st
import pandas as pd
import numpy
import os

import matplotlib.pyplot as plt
from utils.visualisation import display_waveform

st.set_page_config(
    page_title = "Voice Disorder Diagnosis",
    page_icon = ":home:"
)

st.title("Perspectives on Voice Disorder Diagnosis")
st.header("Machine Learning Models")

# Test image
image_path = "assets/images/icons8-home-50.png"
st.image(image_path, caption = "My home icon", use_column_width=True)

### Sample audio files ###

# Define the path to the directory
audio_path = "assets/sample_audio/"
audio_files = os.listdir(audio_path)

# Dynamically update names in the file
audio_mapping = {
    f"Audio {i+1}": filename for i, filename in enumerate(audio_files)
}

# Create the buttons for the audio files
selected_radiobutton = st.radio(
    "Select a sample audio file",
    list(audio_mapping.keys())
)

# Get the file selected
selected_audio = os.path.join(
    audio_path,
    audio_mapping[selected_radiobutton]
)

# Button to play the audio
st.audio(selected_audio, format="audio/wav", start_time=0)

# Plot the selected waveform
fig, ax = plt.subplots()
display_waveform(selected_audio)
st.pyplot(fig)