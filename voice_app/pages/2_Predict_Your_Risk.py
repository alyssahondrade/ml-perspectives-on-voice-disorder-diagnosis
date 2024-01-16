# Import dependencies
import streamlit as st
import pandas as pd
import numpy as np
import os
import json
import joblib
import pickle

import matplotlib.pyplot as plt
from utils.visualisation import display_waveform, display_spectrogram
from utils.interaction import metadata_questionnaire
from utils.preprocessing import meta_preprocessing
from utils.interaction import build_sidebar


def page_configuration():
    st.set_page_config(
        page_title = "Voice Disorder Diagnosis"
    )
    
    st.title("Voice Disorder Diagnosis")
    st.header("Machine Learning Model - Questionnaire")


@st.cache_resource # Only load the model once
def load_model(model_path):
    
    # Load the pickle file
    with open(model_path, 'rb') as file:
        model = pickle.load(file)
    
    return model


def make_keras_predictions(data, model_meta, model_path, scaler_path):
    # Preprocess the user responses
    st.header('Questionnaire')
    user_responses = metadata_questionnaire()
    processed_sample = meta_preprocessing(user_responses, data, model_meta)
    
    # Load the scaler
    X_scaler = joblib.load(scaler_path)
    scaled_sample = X_scaler.transform(processed_sample)
    
    # Load the model
    with st.spinner("Loading model..."):
        model = load_model(model_path)
        
    # Make predictions using the loaded model
    prediction = model.predict(scaled_sample)
    
    if st.button(label="Submit", use_container_width = True):
        st.divider()
        left_col, mid_col, right_col = st.columns(3)
        with mid_col:
            st.metric(
                label = "Probability of Voice Disorder",
                value = f'{round(prediction[0][0] * 100, 1)}%',
                label_visibility = "visible"
            )
    else:
        st.divider()
        left_col, mid_col, right_col = st.columns(3)
        with mid_col:
            st.metric(
                label = "Probability of Voice Disorder",
                value = '0%',
                label_visibility = "visible"
            )


def main():
    # Get the absolute path to the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Define the directories
    root_dir = os.path.dirname(os.path.dirname(script_dir))
    voice_app_dir = os.path.dirname(script_dir)

    # Specify the path to default_data
    data_path = os.path.join(voice_app_dir, 'assets', 'default_data.json')
    with open(data_path, 'r') as file:
        data = json.load(file)
    
    # Specify the path to model_meta
    meta_path = os.path.join(voice_app_dir, 'assets', 'model_meta.json')
    with open(meta_path, 'r') as file:
        model_meta = json.load(file)

    # Specify the path to the trained model
    model_name = "pickled_run_41_0.824.h5" # Trained model using 82% DNN Model
    model_path = os.path.join(root_dir, 'models', model_name)

    # Specify the path to the scaler
    scaler_path = os.path.join(voice_app_dir, 'assets', 'scaler.joblib')
    
    # Build the page
    page_configuration()
    build_sidebar()
    st.divider()
    make_keras_predictions(data, model_meta, model_path, scaler_path)


if __name__ == '__main__':
    main()