# Import dependencies
import streamlit as st
import pandas as pd
import numpy as np
import os
import json
import joblib

from utils.interaction import metadata_questionnaire
from utils.interaction import build_sidebar
from utils.preprocessing import meta_preprocessing
from utils.preprocessing import spec_preprocessing, st_preprocessing


def page_configuration():
    st.set_page_config(
        page_title = "Explore Voice"
    )
    
    st.title("Explore Voice")
    # st.header("Machine Learning Model - Questionnaire")

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
    for idx, filename in enumerate(audio_files):
        audio_name = f"Audio {idx + 1}"
        audio_mapping[audio_name] = filename

    return [audio_mapping, audio_path]


def audio_interface(selected_audio):
    
    # Button to play the audio
    st.audio(
        data = selected_audio,
        format = "audio/wav",
        start_time = 0
    )
    
    # Pass the selected audio to the preprocessing functions
    reshaped_array = spec_preprocessing(selected_audio)


def user_selection():
    # Get the audio files to choose from
    audio_mapping, audio_path = audio_select()
    
    # Add the upload option as a key to audio_mapping
    audio_mapping['Upload Sample'] = ""
    print(audio_mapping)
    
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
            audio_interface(selected_audio)
            st.success(f"Running: {selected_audio.split('/')[-1]}")
        else:
            if uploaded_file is not None:
                audio_interface(temp_sample_path)
                st.success(f"Running: {uploaded_file.name}")
            else:
                st.warning("Please upload a file or choose a sample.")


def main():
    page_configuration()
    build_sidebar()
    user_selection()
    

if __name__ == '__main__':
    main()