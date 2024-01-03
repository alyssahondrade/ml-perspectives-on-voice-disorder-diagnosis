# Import dependencies
import streamlit as st
import numpy as np
import librosa
import librosa.display
import matplotlib.pyplot as plt


def display_waveform(filepath_audio):
    """
    Purpose:
    - Display audio file's waveform.

    Input: filepath_audio
    Output: Displays plot
    """

    # Load the audio file using librosa
    y, sr = librosa.load(
        filepath_audio,
        sr = None # preserve sampling rate
    )

    # Plot the waveform
    librosa.display.waveshow(y, sr=sr)

    # Add the labels
    plt.title('Waveform')
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')


def display_spectrogram(filepath_audio):
    """
    Purpose:
    - Display audio file's spectrogram.

    Input: filepath_audio
    Output: Displays plot
    """
    
    # Load the audio file using librosa
    y, sr = librosa.load(
        filepath_audio,
        sr = None # preserve sampling rate
    )

    # Plot the spectrogram
    D = librosa.amplitude_to_db(
        np.abs(librosa.stft(y)),
        ref = np.max
    )

    # Plot the spectrogram
    librosa.display.specshow(
        D,
        sr = sr,
        x_axis = 'time',
        y_axis = 'log' # can also choose: linear
    )
    
    # Add labels
    plt.title('Spectrogram')
    plt.colorbar(format='%+2.0f dB')


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
            final_score = raw_score * 106 / 40
        else:
            final_score = raw_score

        # Display the final score
        st.subheader(f"{type.upper()} Score: {int(final_score)}")
        
    
    return final_score