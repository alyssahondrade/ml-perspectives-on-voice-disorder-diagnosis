# Import dependencies
import streamlit as st
import pandas as pd
import numpy as np
import os
import json
import joblib
import tensorflow as tf
import matplotlib.pyplot as plt

from utils.interaction import metadata_questionnaire
from utils.interaction import build_sidebar
from utils.preprocessing import meta_preprocessing
from utils.preprocessing import spec_preprocessing, st_preprocessing
from utils.visualisation import display_waveform, display_spectrogram


def build_header():
    # Page Configuration
    st.set_page_config(
        page_title = "Explore Voice"
    )
    
    # Title
    st.title("Explore Voice")
    
    # Information
    st.write(
        """
        This voice disorder diagnostic tool uses a Convolutional Neural\
        Network which achieved a peak accuracy of 78%. The dataset used\
        to train the model are the spectrograms derived from the audio signals.
        """
    )
    st.divider()
    
    # Instructions
    st.subheader("Instructions")
    st.write(
        """
        Select or upload a voice sample. The following criteria must be met\
        to match the data the model was trained with:\n
        - Neutral /a/ vocalisation of 5 seconds length\n
        - WAV file format\n
        
        
        Use the "Run" button to submit a sample. After which you can explore\
        the waveform and spectrogram, and choose to play the audio file.
        """
    )
    st.divider()
    
    # Section header
    st.header('Choose a Sample')

def audio_select():
    # Get the absolute path to the current script (Home.py)
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Define the directories
    root_dir = os.path.dirname(os.path.dirname(script_dir))
    voice_app_dir = os.path.dirname(script_dir)
    
    # Specify the path to the "assets/sample_audio" folder
    audio_path = os.path.join(voice_app_dir, 'assets', 'sample_audio')

    # List the files in the "sample_audio" folder
    audio_files = os.listdir(audio_path)
    
    # Dynamically update names in the file
    audio_mapping = dict()
    counter = 0
    for filename in audio_files:
        if filename.endswith(".wav"):
            counter += 1
            audio_name = f"Audio {counter}"
            audio_mapping[audio_name] = filename

    return [audio_mapping, audio_path]


def audio_interface(selected_audio):
    
    # Pass the selected audio to the preprocessing functions
    reshaped_array = spec_preprocessing(selected_audio)
    
    # Button to play the audio
    st.audio(
        data = selected_audio,
        format = "audio/wav",
        start_time = 0
    )
    
    return reshaped_array


def user_selection():
    # Get the audio files to choose from
    audio_mapping, audio_path = audio_select()
    
    # Add the upload option as a key to audio_mapping
    audio_mapping['Upload Sample'] = ""
    
    left_col, right_col = st.columns(2)
    with left_col:
        # User selection buttons
        selected_radiobutton = st.radio(
            label = "Select/Upload a Sample",
            options = list(audio_mapping.keys())
        )

        # Get the file selected
        if selected_radiobutton != 'Upload Sample':
            selected_audio = os.path.join(
                audio_path,
                audio_mapping[selected_radiobutton]
            )
        
    with right_col:
        # Check if upload option selected
        if selected_radiobutton == 'Upload Sample':

            # Enable the file uploader
            uploaded_file = st.file_uploader(
                label = "Upload your voice sample",
                type = "wav",
                accept_multiple_files = False,
                disabled = False
            )

            # Confirm file upload
            if uploaded_file is not None:
                
                # Temp folder path
                script_dir = os.path.dirname(os.path.abspath(__file__))
                root_dir = os.path.dirname(os.path.dirname(script_dir))
                voice_app_dir = os.path.dirname(script_dir)
                temp_sample_path = os.path.join(voice_app_dir, 'temp', 'sample.wav')

                # Read the file to the temp folder
                with open(temp_sample_path, "wb") as temp_file:
                    temp_file.write(uploaded_file.read())

        else:
            # Disable the file uploader
            st.file_uploader(
                label = "Upload your voice sample",
                type = "wav",
                accept_multiple_files = False,
                disabled = True
            )
    
    # Run button
    run_button = st.button(
        label = "Run",
        use_container_width = True
    )
    
    st.divider()
    
    if run_button:
        if selected_radiobutton != 'Upload Sample':
            reshaped = audio_interface(selected_audio)
            st.success(f"Running: {selected_audio.split('/')[-1]}")
            return [reshaped, selected_audio]
        else:
            if uploaded_file is not None:
                reshaped = audio_interface(temp_sample_path)
                st.success(f"Running: {uploaded_file.name}")
                return [reshaped, temp_sample_path]
            else:
                st.warning("Please upload a file or choose a sample.")


def make_cnn_predictions(reshaped_data, scaler_path, model_path):
    # Define the pixel dimension for scaling
    height_px = reshaped_data[0]
    width_px = reshaped_data[1]
    
    # Load the scaler
    X_scaler = joblib.load(scaler_path)
    scaled_sample = X_scaler.transform(reshaped_data[2])
    
    # Reshape the sample
    scaled_reshaped = scaled_sample.reshape((1, height_px, width_px, 3))
    
    # Load the model
    model = tf.keras.models.load_model(model_path)
    
    # Make predictions
    prediction = model.predict(scaled_reshaped)

    return prediction[0][0]


def delete_temp_contents(temp_folder_path):
    # Check if the folder is not empty
    if any(os.scandir(temp_folder_path)):
        for file_name in os.listdir(temp_folder_path):
            file_path = os.path.join(temp_folder_path, file_name)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    os.rmdir(file_path)
            except Exception as e:
                print(f"Error deleting {file_path}: {e}")
    else:
        print(f"The folder {temp_folder_path} is already empty.")

def main():
    # Get the absolute path to the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Define the directories
    root_dir = os.path.dirname(os.path.dirname(script_dir))
    voice_app_dir = os.path.dirname(script_dir)

    # Specify the path to the trained model
    model_name = "best_cnn_0.784.h5" # Trained model using 82% DNN Model
    model_path = os.path.join(root_dir, 'models', model_name)

    # Specify the path to the scaler
    scaler_path = os.path.join(voice_app_dir, 'assets', 'cnn_scaler.joblib')
    
    # Build the page
    build_header()
    build_sidebar()
    
    try:
        # Get the user selection
        reshaped_data, audio_path = user_selection()
        
        # Make a prediction
        prediction = make_cnn_predictions(reshaped_data, scaler_path, model_path)
        
        # Display the prediction
        st.divider()
        left_col, mid_col, right_col = st.columns(3)
        with mid_col:
            st.metric(
                label = "Probability of Voice Disorder",
                value = f'{round(prediction * 100, 1)}%'
            )
            
        # Plot the visuals
        st.divider()
        first_col, second_col = st.columns(2)
        with first_col:
            # Plot the selected spectrogram
            st.subheader("Spectrogram")
            fig_spec = plt.figure()
            display_spectrogram(audio_path)
            st.pyplot(fig_spec)

        with second_col:
            # Plot the selected waveform
            st.subheader("Waveform")
            fig_wave = plt.figure()
            display_waveform(audio_path)
            st.pyplot(fig_wave)

    except:
        st.warning("Please upload a file or choose a sample.")
    
    # Empty the contents of the temp folder
    temp_folder_path = os.path.join(voice_app_dir, 'temp')
    delete_temp_contents(temp_folder_path)
    

if __name__ == '__main__':
    main()