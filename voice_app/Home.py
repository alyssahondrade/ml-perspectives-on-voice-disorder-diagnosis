# Import dependencies
import streamlit as st
import pandas as pd
import numpy as np
import os
import json
import tensorflow as tf
import joblib

import matplotlib.pyplot as plt
from utils.visualisation import display_waveform, display_spectrogram
from utils.interaction import metadata_questionnaire
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


@st.cache_resource # Only load the model once
def load_model():
    # model_path = "../models/dl/run_21_0.824.h5"
    model_path = "../models/dl/run_39_0.824.h5"
    model = tf.keras.models.load_model(model_path)
    return model



def main():
    page_configuration()
    st.divider()
    user_voice = st.file_uploader(
        label = "Upload your voice sample",
        type = "wav",
        accept_multiple_files = False,
        label_visibility = "visible"
    )
    audio_select()
    
    st.divider()
    st.header('Questionnaire')
    user_responses = metadata_questionnaire()
    
    # Preprocess the user responses
    processed_sample = meta_preprocessing(user_responses)
    # print(processed_sample)
    
    # Load the scaler
    X_scaler = joblib.load('assets/scaler.joblib')
    
    # Use the scaler
    scaled_sample = X_scaler.transform(processed_sample)
    print(scaled_sample)

    with st.spinner("Loading model..."):
        model = load_model()
        
    # Make predictions using the loaded model
    prediction = model.predict(scaled_sample)

    # Display the prediction
    print("Model Prediction:", prediction)

if __name__ == '__main__':
    main()