# Import dependencies
import streamlit as st
import pandas as pd
import numpy as np
import os
import json

import matplotlib.pyplot as plt
from utils.visualisation import display_waveform, display_spectrogram

def page_configuration():
    st.set_page_config(
        page_title = "Voice Disorder Diagnosis",
        page_icon = ":home:"
    )
    
    st.title("Voice Disorder Diagnosis")
    st.header("Machine Learning Models")


def audio_select():
    # Define the path to the directory
    audio_path = "assets/sample_audio/"
    audio_files = os.listdir(audio_path)
    
    # Dynamically update names in the file
    audio_mapping = dict()
    for idx, filename in enumerate(audio_files):
        audio_name = f"Audio {idx + 1}"
        audio_mapping[audio_name] = filename

    # Create the buttons for the audio files
    selected_radiobutton = st.radio(
        "Select a sample audio file",
        list(audio_mapping.keys()),
        horizontal = True
    )
    
    # Get the file selected
    selected_audio = os.path.join(
        audio_path,
        audio_mapping[selected_radiobutton]
    )
    
    # Button to play the audio
    st.audio(
        selected_audio,
        format = "audio/wav",
        start_time = 0
    )
    
    # Plot the selected waveform
    st.subheader("Waveform")
    fig_wave = plt.figure()
    display_waveform(selected_audio)
    st.pyplot(fig_wave)

    # Plot the selected spectrogram
    st.subheader("Spectrogram")
    fig_spec = plt.figure()
    display_spectrogram(selected_audio)
    st.pyplot(fig_spec)


def main():
    page_configuration()
    st.divider()
    audio_select()
    
    # Read JSON file
    data_path = 'assets/default_data.json'
    with open(data_path, 'r') as file:
        data = json.load(file)
    
    st.divider()
    st.header('Questionnaire')

    demographic, sa_scores = st.columns(2)
    with demographic:
        st.subheader("Demographic Information")

        # Age input
        user_age = st.number_input(
            label = f"Age ({data['min_age']}-{data['max_age']})",
            min_value = data['min_age'],
            max_value = data['max_age'],
            value = "min"
        )
        
        # Gender input
        user_gender = st.radio(
            label = "Gender",
            options = data['gender_options'],
            horizontal = True
        )
        
    with sa_scores:
        st.subheader("Self-Assessment Scores")
        
        # VHI Score
        user_vhi = st.number_input(
            label = f"VHI Score ({data['min_vhi_score']}-{data['max_vhi_score']})",
            min_value = data['min_vhi_score'],
            max_value = data['max_vhi_score'],
            value = data['avg_vhi_score']
        )
        
        # RSI Score
        user_rsi = st.number_input(
            label = f"RSI Score ({data['min_rsi_score']}-{data['max_rsi_score']})",
            min_value = data['min_rsi_score'],
            max_value = data['max_rsi_score'],
            value = data['avg_rsi_score']
        )

    # Lifestyle questions
    st.subheader("Lifestyle")
    
    # Smoker
    initial_smoker, followup_smoker = st.columns(2)
    with initial_smoker:
        # Options: no, casual, yes
        user_smoker_opt = st.radio(
            label = "Do you smoke?",
            options = data['smoker_options'],
            index = int(len(data['smoker_options'])/2)
        )            
    with followup_smoker:
        # Number of cigarettes per day
        if user_smoker_opt in ["Casual", "Yes"]:
            user_smoker_count = st.number_input(
                label = "How many cigarettes per day?",
                value = data['avg_cig_pd']
            )
        else:
            # Disable selection if: no
            st.number_input(
                label = "How many cigarettes per day?",
                value = data['min_cig_pd'],
                disabled = True
            )

    # Alcohol Consumption
    initial_alcohol, followup_alcohol = st.columns(2)
    with initial_alcohol:
        # Options: nondrinker, casual, habitual
        user_alc_opt = st.radio(
            label = "Alcohol consumption",
            options = data['alcohol_options'],
            index = int(len(data['alcohol_options'])/2)
        )
    with followup_alcohol:
        if user_alc_opt in ["Casual", "Habitual"]:
            # User to select units: per day v. per week
            alc_units = st.selectbox(
                label = "Units: per day or per week",
                options = ['Per day', 'Per week']
            )

            # Trigger based on selected option
            if alc_units == "Per day":
                alc_pd = st.number_input(
                    label = "How many glasses per day?",
                    value = data['avg_alc_pd']
                )
            else:
                alc_pw = st.number_input(
                    label = "How many glasses per week?",
                    value = data['avg_alc_pw']
                )
        else:
            # Disable selection if: nondrinker
            st.selectbox(
                label = "Units: per day or per week",
                options = ['Per day', 'Per week'],
                disabled = True
            )
            alc_pd = st.number_input(
                label = "How many glasses per day?",
                value = data['avg_alc_pd'],
                disabled = True
            )

    # Water consumption
    user_water = st.slider(
        label = "How many litres of water do you drink per day?",
        min_value = data['min_water'],
        max_value = data['max_water'],
        value = 0.5 * data['max_water'],
        step = 0.25
    )
    
    # Habits
    habit_bool = dict()
    habit_pd = dict()
    
    for habit in sorted(data['habit_cols']):
        # Clean up the name
        clean_name = habit.replace("_", " ").capitalize()
        
        # If not 'tomatoes' create columns
        if habit != 'tomatoes':
            selection_col, pd_col = st.columns(2)
            with selection_col:
                # Create a toggle
                response_bool = st.radio(
                    label = clean_name,
                    options = data['habit_options'],
                    index = int(len(data['habit_options'])/2)
                )

                # Save the response to the dictionary
                habit_bool[clean_name] = response_bool

            with pd_col:
                if response_bool != "Never":
                    # Integer habits
                    if habit in ['chocolate', 'soft_cheese']:
                        response_pd = st.slider(
                            label = f"How many {habit} per day?",
                            min_value = 0,
                            max_value = data[f'max_{habit}'],
                            value = data[f'avg_{habit}'],
                            step = 10
                        )
                    elif habit == 'coffee':
                        response_pd = st.slider(
                            label = f"How many {habit} per day?",
                            min_value = 0,
                            max_value = data[f'max_{habit}'],
                            value = data[f'avg_{habit}'],
                            step = 1
                        )
                    # Float habits
                    else:
                        response_pd = st.slider(
                            label = f"How many {habit} per day?",
                            min_value = 0.0,
                            max_value = data[f'max_{habit}'],
                            value = data[f'avg_{habit}'],
                            step = 0.5
                        )
                    
                    # Save the response to the dictionary
                    habit_pd[clean_name] = response_pd
                    
                else:
                    # Disable selection if: never
                    # Integer habits
                    if habit in ['chocolate', 'coffee', 'soft_cheese']:
                        st.slider(
                            label = f"How many {habit} per day?",
                            min_value = 0,
                            max_value = data[f'max_{habit}'],
                            value = data[f'avg_{habit}'],
                            disabled = True
                        )
                    # Float habits
                    else:
                        st.slider(
                            label = f"How many {habit} per day?",
                            min_value = 0.0,
                            max_value = data[f'max_{habit}'],
                            value = data[f'avg_{habit}'],
                            disabled = True
                        )
        else:
            # If 'tomatoes' column, create a toggle
                response_bool = st.radio(
                    label = clean_name,
                    options = data['habit_options'],
                    index = int(len(data['habit_options'])/2),
                    horizontal = True
                )

                # Save the response to the dictionary
                habit_bool[clean_name] = response_bool
            
    
    print(habit_bool, habit_pd)

    

if __name__ == '__main__':
    main()