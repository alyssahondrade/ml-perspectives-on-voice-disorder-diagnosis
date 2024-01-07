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
    
    # Add vhi_impact, based on research paper, encode as integers
    zscore = metadata_dict['vhi_zscore']
    if zscore < 0:
        # Within normal limits
        metadata_dict['vhi_impact'] = 0
    elif zscore < 1:
        # No significant impact
        metadata_dict['vhi_impact'] = 1
    elif zscore < 2:
        # Mild significant impact
        metadata_dict['vhi_impact'] = 2
    elif zscore < 3:
        # Moderate significant impact
        metadata_dict['vhi_impact'] = 3
    else:
        # Sever significant impact
        metadata_dict['vhi_impact'] = 4
    
    # Calculate alcohol_pd
    if metadata_dict['alcohol_units'] == 'Per week':
        metadata_dict['alcohol_pd'] = round(metadata_dict['alc_pw'] / 7, 2)
    else:
        metadata_dict['alcohol_pd'] = metadata_dict['alc_pd']
    pprint(metadata_dict)