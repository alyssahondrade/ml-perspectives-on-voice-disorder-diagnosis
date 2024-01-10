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
    # Trained model using 82% DNN Model
    # model_path = "../models/dl/run_41_0.824.h5"
    # model = tf.keras.models.load_model(model_path)
    
    # Pickle
    # model_path = "../models/pickled_run_41_0.824.h5"
    with open(model_path, 'rb') as file:
        model = pickle.load(file)
    
    # UNCOMMENT BELOW, for 88% Stack Model
    # model_path = "../models/stack/run_18_0.882.h5"
    # model = joblib.load(model_path)
    return model


def make_keras_predictions(data, model_meta, model_path):
    # Preprocess the user responses
    st.header('Questionnaire')
    user_responses = metadata_questionnaire()
    processed_sample = meta_preprocessing(user_responses, data, model_meta)
    
    # Load the scaler
    X_scaler = joblib.load('assets/scaler.joblib')
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

def make_joblib_predictions():
    # Preprocess the user responses
    st.header('Questionnaire')
    user_responses = metadata_questionnaire()
    processed_sample = meta_preprocessing(user_responses)
    
    # Load the scaler
    X_scaler = joblib.load('assets/scaler.joblib')
    scaled_sample = X_scaler.transform(processed_sample)
    
    # Load the model
    with st.spinner("Loading model..."):
        model = load_model()
        
    # Make predictions using the loaded model
    prediction = model.predict(scaled_sample)
    print(prediction)
    
    # Return value
    if prediction == 1:
        result = "Pathological"
    else:
        result = "Healthy"
    
    if st.button(label="Submit", use_container_width = True):
        st.divider()
        left_col, mid_col, right_col = st.columns(3)
        with mid_col:
            st.metric(
                label = "Healthy or Pathological?",
                value = result,
                label_visibility = "visible"
            )
    else:
        st.divider()
        left_col, mid_col, right_col = st.columns(3)
        with mid_col:
            st.metric(
                label = "Healthy or Pathological?",
                value = '?',
                label_visibility = "visible"
            )

def main():
    # Get the absolute path to the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Navigate up one level to the "voice_app" directory
    voice_app_dir = os.path.dirname(script_dir)

    # Specify the path to default_data in the "assets" folder
    data_path = os.path.join(voice_app_dir, 'assets', 'default_data.json')
    with open(data_path, 'r') as file:
        data = json.load(file)
    
    # Specify the path to model_meta in the "assets" folder
    meta_path = os.path.join(voice_app_dir, 'assets', 'model_meta.json')
    with open(meta_path, 'r') as file:
        model_meta = json.load(file)

    # Specify the path to the trained model
    model_name = "pickled_run_41_0.824.h5"
    root_dir = os.path.dirname(os.path.dirname(script_dir))
    model_path = os.path.join(root_dir, 'models', model_name)
    # model_path = "../models/

    page_configuration()
    build_sidebar()
    st.divider()
    make_keras_predictions(data, model_meta, model_path)
    
    
    # UNCOMMENT BELOW, if Stack was used instead of keras
    # make_joblib_predictions()



if __name__ == '__main__':
    main()