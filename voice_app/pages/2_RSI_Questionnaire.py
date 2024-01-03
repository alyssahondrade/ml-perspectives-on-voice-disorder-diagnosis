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
        'Question 3': '',
        'Question 4': '',
        'Question 5': '',
        'Question 6': '',
        'Question 7': '',
        'Question 8': '',
        'Question 9': '',
        'Question 10': ''
    }

    
    options = [
        'No problem',
        'Very mild problem',
        'Moderate or slight problem',
        'Moderate problem',
        'Severe problem',
        'Problem as bad as it can be'
    ]
    user_responses = create_questionnaire('rsi', questions, options)

if __name__ == '__main__':
    main()