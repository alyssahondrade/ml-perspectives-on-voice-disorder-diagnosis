# Import dependencies
import streamlit as st
from utils.visualisation import create_questionnaire


def main():
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
    user_responses = create_questionnaire('rsi', questions, options)

if __name__ == '__main__':
    main()