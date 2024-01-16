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
        page_title = "Voice Disorder Diagnosis",
        page_icon = ":home:"
    )
    
    st.title("Voice Disorder Diagnosis")
    st.header("Machine Learning Models")



    

def main():
    page_configuration()
    build_sidebar()
    st.divider()


if __name__ == '__main__':
    main()