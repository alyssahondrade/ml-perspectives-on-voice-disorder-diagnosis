# Import dependencies
import streamlit as st
import json
from pprint import pprint

# Read JSON file
data_path = 'assets/default_data.json'
with open(data_path, 'r') as file:
    data = json.load(file)
    
def calculate_score(options, responses):
    """
    Purposes:
    - Map options to a numerical score for calculations

    Input: Responses in a dictionary format
    Output: Mapped scores
    """
    
    # Get the responses as a list
    word_response = list(responses.values())

    # Convert to numerical value
    num_response = [options.index(word) for word in word_response]

    return sum(num_response)


def create_questionnaire(type, questions, options):
    """
    Purpose:
    - Build questionnaire

    Input:
    - Questions in a dictionary format
    - Options, as it would appear in the form

    Output: Sum of all scores
    """

    # Initialise a dictionary to hold responses
    responses = dict()

    # Initialise default final_score for later update
    final_score = 0

    # Add divider for formatting
    st.divider()

    # Loop through each key in the questions dictionary
    for idx, (key, value) in enumerate(questions.items()):

        # Headers
        st.header(f"Question {idx+1}")
        st.subheader(value)

        # Radiobutton
        if type == 'vhi':
            
            # Horizontal buttons for VHI
            response = st.radio(
                label = f"Question {idx+1}: {value}",
                options = options,
                horizontal = True,
                label_visibility = "hidden"
            )
        else:

            # Vertical buttons for RSI
            response = st.radio(
                label = f"Question {idx+1}: {value}",
                options = options,
                label_visibility = "hidden"
            )

        # Add divider for formatting
        st.divider()

        # Populate the response dictionary
        responses[key] = response

    # Submit button
    if st.button(label = "Submit", use_container_width = True):
        
        # Calculate the raw score
        raw_score = calculate_score(options, responses)
        
        # Scale the score
        if type == 'vhi':
            # Scaling factor
            scale_factor = data['max_vhi_score'] / data['max_vhi10_score']
            final_score = raw_score * scale_factor
        else:
            final_score = raw_score

        # Display the final score
        st.subheader(f"{type.upper()} Score: {int(final_score)}")
        
    
    return final_score


def meta_demographic(metadata_dict):
    """
    Purpose: Builds the demographic section of metadata questionnaire
    """
    
    # Initialise two columns
    demographic, sa_scores = st.columns(2)
    
    # First column
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
        
        # Save the responses to the dictionary
        metadata_dict['age'] = user_age
        metadata_dict['gender'] = user_gender
        
    # Second column
    with sa_scores:
        st.subheader("Self-Assessment Scores")
        
        # Labels
        vhi = f"VHI Score ({data['min_vhi_score']}-{data['max_vhi_score']})"
        rsi = f"RSI Score ({data['min_rsi_score']}-{data['max_rsi_score']})"
        
        # VHI Score        
        user_vhi = st.number_input(
            label = vhi,
            min_value = data['min_vhi_score'],
            max_value = data['max_vhi_score'],
            value = data['avg_vhi_score']
        )
        
        # RSI Score
        user_rsi = st.number_input(
            label = rsi,
            min_value = data['min_rsi_score'],
            max_value = data['max_rsi_score'],
            value = data['avg_rsi_score']
        )
        
        # Save the responses to the dictionary
        metadata_dict['vhi_score'] = user_vhi
        metadata_dict['rsi_score'] = user_rsi


def metadata_smoker(metadata_dict):
    """
    Purpose: Builds the smoker section of metadata questionnaire
    """
    
    # Initialise two columns
    initial_smoker, followup_smoker = st.columns(2)
    
    # First column
    with initial_smoker:
        # Options: no, casual, yes
        user_smoker_opt = st.radio(
            label = "Do you smoke?",
            options = data['smoker_options'],
            index = int(len(data['smoker_options'])/2)
        )
    
    # Second column
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
    
    # Save the responses to the dictionary
    metadata_dict['smoker'] = user_smoker_opt
    metadata_dict['cigarettes_pd'] = user_smoker_count


def metadata_alcohol(metadata_dict):
    """
    Purpose: Builds the alcohol section of metadata questionnaire
    """
    
    # Initialise two columns
    initial_alcohol, followup_alcohol = st.columns(2)
    
    # First column
    with initial_alcohol:
        # Options: nondrinker, casual, habitual
        user_alc_opt = st.radio(
            label = "Alcohol consumption",
            options = data['alcohol_options'],
            index = int(len(data['alcohol_options'])/2)
        )
        
    # Second column
    with followup_alcohol:
        
        # Trigger options if selected
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
                # Save the response
                metadata_dict['alc_pd'] = alc_pd
            else:
                alc_pw = st.number_input(
                    label = "How many glasses per week?",
                    value = data['avg_alc_pw']
                )
                # Save the response
                metadata_dict['alc_pw'] = alc_pw
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

    # Save the responses to the dictionary
    metadata_dict['alcohol_consumption'] = user_alc_opt
    metadata_dict['alcohol_units'] = alc_units


def metadata_water(metadata_dict):
    """
    Purpose: Builds the water section of metadata questionnaire
    """
    
    # Create the slider
    user_water = st.slider(
        label = "How many litres of water do you drink per day?",
        min_value = data['min_water'],
        max_value = data['max_water'],
        value = 0.5 * data['max_water'],
        step = 0.25
    )
    
    # Save the response to the dictionary
    metadata_dict['water_litres_pd'] = user_water

    
def metadata_habits(habit_bool, habit_pd):
    """
    Purpose: Builds the eating habits section of metadata questionnaire
    """
    
    # Loop through each habit
    for habit in sorted(data['habit_cols']):
        
        # Clean up the name
        clean_name = habit.replace("_", " ").capitalize()
        
        # If not 'tomatoes' create columns
        if habit != 'tomatoes':
            
            # Initialise two columns
            selection_col, pd_col = st.columns(2)
            
            # First column
            with selection_col:
                
                # Create a set of radio buttons
                response_bool = st.radio(
                    label = clean_name,
                    options = data['habit_options'],
                    index = int(len(data['habit_options'])/2)
                )

                # Save the response to the dictionary
                habit_bool[clean_name] = response_bool

            # Second column
            with pd_col:
                
                # Trigger based on selected option
                if response_bool != "Never":
                    
                    # Integer (large values) habits
                    if habit in ['chocolate', 'soft_cheese']:
                        response_pd = st.slider(
                            label = f"How many {habit} per day?",
                            min_value = 0,
                            max_value = data[f'max_{habit}'],
                            value = data[f'avg_{habit}'],
                            step = 10
                        )
                    
                    # Integer (small values) habits
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
                
                # Disable selection if: never
                else:

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
            # If 'tomatoes' column, create a horizontal selection
            response_bool = st.radio(
                label = clean_name,
                options = data['habit_options'],
                index = int(len(data['habit_options'])/2),
                horizontal = True
            )

            # Save the response to the dictionary
            habit_bool[clean_name] = response_bool

    
def metadata_questionnaire():
    # Initialise dictionary to hold results
    metadata_dict = dict()
    
    meta_demographic(metadata_dict)
    
    # Lifestyle questions
    st.subheader("Lifestyle")
    metadata_smoker(metadata_dict)
    metadata_alcohol(metadata_dict)
    metadata_water(metadata_dict)
    
    # Habits
    st.subheader("Eating Habits")
    habit_bool = dict()
    habit_pd = dict()
    metadata_habits(habit_bool, habit_pd)
    
    
    pprint(metadata_dict)
    pprint(habit_bool)
    pprint(habit_pd)