# Import dependencies
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