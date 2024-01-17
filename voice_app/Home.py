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


def build_header():
    # Page configuration
    st.set_page_config(
        page_title = "Voice Disorder Diagnosis"
    )
    
    st.title("Machine Learning Perspectives on Voice Disorder Diagnosis")
    
    # Information
    st.write(
        """
        Welcome to the voice disorder diagnostic tool!\n
        
        This app was developed by building machine learning models which\
        look at three perspectives of voice:\n
        - Visual, using spectrograms.
        - Temporal, using short term features of the audio signal.
        - External factors, such as demographic and lifestyle habits.
        
        Please use the navigation sidebar to explore the app.
        """
    )
    st.divider()

def main():
    build_header()
    build_sidebar()


if __name__ == '__main__':
    main()