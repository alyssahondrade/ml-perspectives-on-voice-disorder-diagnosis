### Import dependencies ###
import streamlit as st
import json
from pprint import pprint

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
    elif metadata_dict['alcohol_units'] == 'Per day':
        metadata_dict['alcohol_pd'] = metadata_dict['alc_pd']
    
    # Create a copy of the dictionary as the output
    output_dict = dict(metadata_dict)
    
    # Convert the nested dictionary to correct keys   
    for habit in data['habit_cols']:
        # Convert the word responses
        word_option = output_dict['habit_bool'][habit]
        
        # if habit == 'smoker':
            # print(model_meta['smoker_map'])
        # output_dict[habit] = 
        
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
        # 'habit_bool', 'habit_pd',
        'gender', 'occupation_status'
    ]

    # Delete the key that exists
    for key in delete_keys:
        if key in output_dict:
            del output_dict[key]

    pprint(output_dict)
    return output_dict


