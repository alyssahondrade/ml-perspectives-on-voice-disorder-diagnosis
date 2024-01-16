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

import soundfile as sf


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

#     # Create the buttons for the audio files
#     selected_radiobutton = st.radio(
#         label = "Select a sample audio file",
#         options = list(audio_mapping.keys()),
#         horizontal = True
#     )
    
#     # Get the file selected
#     selected_audio = os.path.join(
#         audio_path,
#         audio_mapping[selected_radiobutton]
#     )
    
    # return selected_audio

def audio_interface(selected_audio):
    
    # Button to play the audio
    st.audio(
        data = selected_audio,
        format = "audio/wav",
        start_time = 0
    )
    
    # Pass the selected audio to the preprocessing functions
    reshaped_array = spec_preprocessing(selected_audio)


    
# def build_uploader():
#     user_voice = st.file_uploader(
#         label = "Upload your voice sample",
#         type = "wav",
#         accept_multiple_files = False,
#         label_visibility = "visible"
#     )
    
#     return user_voice
    
    
def main():
    build_sidebar()
    
    left_col, right_col = st.columns(2)
    with left_col:
        # User to upload a file
        uploaded_file = st.file_uploader(
            label = "Upload your voice sample",
            type = "wav",
            accept_multiple_files = False,
            label_visibility = "visible",
            disabled = False
        )

        # Confirm file upload
        if uploaded_file is not None:
            # Confirm the file the user uploaded
            st.success(f"File: {uploaded_file.name}")
            
            # Temp folder path
            script_dir = os.path.dirname(os.path.abspath(__file__))
            root_dir = os.path.dirname(os.path.dirname(script_dir))
            voice_app_dir = os.path.dirname(script_dir)
            temp_sample_path = os.path.join(voice_app_dir, 'temp', 'sample.wav')
            
            with open(temp_sample_path, "wb") as temp_file:
                temp_file.write(uploaded_file.read())

        else:
            st.warning("Please upload a file.")
            
        # Get the user to submit the file
        # submit_sample = st.button(label="Submit")
            
    with right_col:
        # Get the audio files to choose from
        audio_mapping, audio_path = audio_select()
        
        # User to select a sample
        selected_radiobutton = st.radio(
            label = "Select a sample audio file",
            options = list(audio_mapping.keys()),
            horizontal = False,
            disabled = False
        )

        # Get the file selected
        selected_audio = os.path.join(
            audio_path,
            audio_mapping[selected_radiobutton]
        )
        
    st.divider()
    run_button = st.button(
        label = "Run",
        use_container_width = True
    )
    
    if run_button:
        # Run the interface
        if uploaded_file is not None:
        # if submit_sample:
            audio_interface(temp_sample_path)
            st.success(f"Running: {uploaded_file.name}")
        else:
            audio_interface(selected_audio)
            st.success(f"Running: {selected_audio.split('/')[-1]}")
    
#     # Initialize selected_audio with a default value
#     selected_audio = None
    
#     left_button, right_button = st.columns(2)
#     with left_button:
#         left_btn = st.button(
#             label = "Upload a sample",
#             use_container_width = True
#         )
        
#         if left_btn:
            # selected_audio = st.file_uploader(
            #     label = "Upload your voice sample",
            #     type = "wav",
            #     accept_multiple_files = False,
            #     label_visibility = "visible",
            #     disabled = False
            # )
            
#         # else:
#         #     # Disable the uploader
#         #     st.file_uploader(
#         #         label = "Upload your voice sample",
#         #         disabled = True
#         #     )

#     with right_button:
#         right_btn = st.button(
#             label = "Choose a sample",
#             use_container_width = True
#         )
        
#         audio_mapping, audio_path = audio_select()
        
#         if right_btn:
#             # Create the buttons for the audio files
#             selected_radiobutton = st.radio(
#                 label = "Select a sample audio file",
#                 options = list(audio_mapping.keys()),
#                 horizontal = True,
#                 disabled = False
#             )

#             # Get the file selected
#             selected_audio = os.path.join(
#                 audio_path,
#                 audio_mapping[selected_radiobutton]
#             )
#         # else:
#         #     # Disable the buttons
#         #     st.radio(
#         #         label = "Select a sample audio file",
#         #         options = list(audio_mapping.keys()),
#         #         horizontal = True,
#         #         disabled = True
#         #     )
    
#     # Run the interface
#     audio_interface(selected_audio)



if __name__ == '__main__':
    main()