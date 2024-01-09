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
from utils.interaction import build_sidebar

def page_configuration():
    st.set_page_config(
        page_title = "Voice Disorder Diagnosis"
    )
    
    st.title("Voice Disorder Diagnosis")
    st.header("Machine Learning Model - Questionnaire")


@st.cache_resource # Only load the model once
def load_model():
    # model_path = "../models/dl/run_21_0.824.h5"
    # model_path = "../models/dl/run_39_0.824.h5"
    model_path = "../models/dl/run_41_0.824.h5"
    # model_path = "../models/stack/run_18_0.882.h5"
    model = tf.keras.models.load_model(model_path)
    # model = joblib.load(model_path)
    return model


def make_keras_predictions():
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
    page_configuration()
    build_sidebar()
    st.divider()
    make_keras_predictions()
    # make_joblib_predictions()



if __name__ == '__main__':
    main()