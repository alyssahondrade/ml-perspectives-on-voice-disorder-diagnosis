### Import dependencies ###
import streamlit as st
import json
from pprint import pprint
import pandas as pd

### Read JSON files ###

# Data used to populate the default values in the questionnaire
data_path = 'assets/default_data.json'
with open(data_path, 'r') as file:
    data = json.load(file)

# Feature names to match the ML model
feature_path = 'assets/model_meta.json'
with open(feature_path, 'r') as file:
    model_meta = json.load(file)
    

### FUNCTIONS ###
def meta_preprocessing(metadata_dict):
    """
    PURPOSE: Convert user responses to preprocessed equivalent.
    
    Input: user responses as a dictionary
    Output: preprocessed responses as a dictionary
    """
    
    # Create a copy of the dictionary as the output
    output_dict = dict(metadata_dict)
    
    # Calculate reflux_indicated
    rsi_score = output_dict['rsi_score']
    if rsi_score >= 13:
        output_dict['reflux_indicated'] = 1
    else:
        output_dict['reflux_indicated'] = 0

    # Calculate vhi_zscore, based on research paper
    normal_mean = 8.75
    stddev = 14.97
    equation = (output_dict['vhi_score'] - normal_mean) / stddev
    output_dict['vhi_zscore'] = round(equation, 2)
    
    # Add vhi_impact, based on research paper, encode as integers
    zscore = output_dict['vhi_zscore']
    if zscore < 0:
        # Within normal limits
        output_dict['vhi_impact'] = 0
    elif zscore < 1:
        # No significant impact
        output_dict['vhi_impact'] = 1
    elif zscore < 2:
        # Mild significant impact
        output_dict['vhi_impact'] = 2
    elif zscore < 3:
        # Moderate significant impact
        output_dict['vhi_impact'] = 3
    else:
        # Sever significant impact
        output_dict['vhi_impact'] = 4
    
    # Calculate alcohol_pd
    if output_dict['alcohol_units'] == 'Per week':
        output_dict['alcohol_pd'] = round(output_dict['alc_pw'] / 7, 2)
    elif output_dict['alcohol_units'] == 'Per day':
        output_dict['alcohol_pd'] = output_dict['alc_pd']
    else:
        output_dict['alcohol_pd'] = 0
        
    # Encode the smoker column
    smoker_opt = output_dict['smoker'].lower()
    output_dict['smoker'] = model_meta['smoker_map'][smoker_opt]
    
    # Encode the alcohol column
    alc_opt = output_dict['alcohol_consumption'].lower()
    output_dict['alcohol_consumption'] = model_meta['alcohol_map'][alc_opt]

    # Convert the nested dictionary to correct keys   
    for habit in data['habit_cols']:
        # Encode the word responses
        word_option = output_dict['habit_bool'][habit].lower()
        output_dict[habit] = model_meta['habit_map'][word_option]
        
        # Convert the values
        if habit == 'carbonated_beverages':
            simple_name = habit.split("_")[0]
            output_dict[f'{simple_name}_pd'] = output_dict['habit_pd'][habit]
            
        elif habit == 'chocolate':
            output_dict[f'{habit}_grams_pd'] = output_dict['habit_pd'][habit]
            
        elif habit == 'tomatoes':
            continue
        else:
            output_dict[f'{habit}_pd'] = output_dict['habit_pd'][habit]

    # Encode the gender column
    if output_dict['gender'] == 'F':
        output_dict['gender_f'] = 1
        output_dict['gender_m'] = 0
    else:
        output_dict['gender_f'] = 0
        output_dict['gender_m'] = 1
    
    # Convert string values to lowercase
    for key, value in output_dict.items():
        if isinstance(value, str):
            output_dict[key] = value.lower()
            
    # Encode the occupation status column
    for name in model_meta['feature_names']:
        
        # Check the columns with 'occupation_status_'
        if name.startswith('occupation_status_'):
            
            # Find the occupation
            occ = name.split("_")[2]
            
            # Encode the values
            if output_dict['occupation_status'] == occ:
                output_dict[name] = 1
            else:
                output_dict[name] = 0
            
    # Drop unnecessary keys
    delete_keys = [
        'alc_pd', 'alc_pw', 'alcohol_units',
        'habit_bool', 'habit_pd',
        'gender', 'occupation_status'
    ]

    # Delete the key that exists
    for key in delete_keys:
        if key in output_dict:
            del output_dict[key]
    
    # Convert to a pandas dataframe
    output_df = pd.DataFrame(output_dict, index=[0])
    
    # Rearrange columns, must be in the same order as during fit
    output_df = output_df[model_meta['feature_names']]
    
    pprint(output_dict)
    return output_df