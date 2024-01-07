# Import dependencies
import streamlit as st
from pprint import pprint

def meta_preprocessing(metadata_dict):
    
    # Calculate reflux_indicated
    rsi_score = metadata_dict['rsi_score']
    if rsi_score >= 13:
        metadata_dict['reflux_indicated'] = 1
    else:
        metadata_dict['reflux_indicated'] = 0

    # Calculate vhi_zscore, based on research paper
    normal_mean = 8.75
    stddev = 14.97
    equation = (metadata_dict['vhi_score'] - normal_mean) / stddev
    metadata_dict['vhi_zscore'] = round(equation, 2)
    
    pprint(metadata_dict)