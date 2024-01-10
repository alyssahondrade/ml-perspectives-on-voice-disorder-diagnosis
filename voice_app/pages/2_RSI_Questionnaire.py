# Import dependencies
import streamlit as st
import os
import json
from utils.interaction import create_questionnaire
from utils.interaction import build_sidebar

def build_header():
    # Title
    st.title("Reflux Severity Index Questionnaire")
    
    # Instructions
    st.subheader("Instructions")
    st.write(
        """
        These are statements many people have used to describe their voices\
        and the effects of their voices on their lives.

        In the last 1 month, how did the following problems affect you?
        
        Please select the response that reflects the severity of the problem\
        for you, for each statement.
        """
    )
    
    # Reference
    ref_text = "Source: Melbourne ENT Group - Reflux Severity Index (RSI)"
    ref_link = "https://melbentgroup.com.au/wp-content/uploads/2015/10/MEG-Reflux-Severity-Index-RSI.pdf"
    st.markdown(f"[{ref_text}]({ref_link})")


def build_questions(data):
    # Questions derived from Melbourne ENT Group RSI Questionnaire
    questions = {
        'Question 1': 'Hoarseness or a problem with your voice',
        'Question 2': 'Clearing your throat',
        'Question 3': 'Excess throat or mucous post-nasal drip',
        'Question 4': 'Difficulty swallowing food, liquids, or pills',
        'Question 5': 'Coughing after you ate or after lying down',
        'Question 6': 'Breathing difficulties or choking episodes',
        'Question 7': 'Troublesome or annoying cough',
        'Question 8': 'Sensations of something sticking in your throat',
        'Question 9': 'Heartburn, chest pain, or indigestion'
    }

    # Define the options
    options = [
        'No problem',
        'Very mild problem',
        'Moderate or slight problem',
        'Moderate problem',
        'Severe problem',
        'Problem as bad as it can be'
    ]

    # Use function to create questionnaire
    user_responses = create_questionnaire('rsi', questions, options, data)


def main():
    # Read JSON file
    # data_path = '/voice_app/assets/default_data.json'
    # data_path = os.path.abspath('/voice_app/assets/default_data.json')

        
        
    # Get the absolute path to the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Navigate up one level to the "voice_app" directory
    voice_app_dir = os.path.dirname(script_dir)

    # Specify the path to the data file in the "assets" folder
    data_path = os.path.join(voice_app_dir, 'assets', 'default_data.json')
    with open(data_path, 'r') as file:
        data = json.load(file)

    build_header()
    build_questions(data)
    build_sidebar()


if __name__ == '__main__':
    main()