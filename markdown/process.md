# Process

## Table of Contents
1. [Introduction]()
2. [Data Conversion]()
3. [Data Cleaning]()
    1. [Duplicates]()
    2. [Names and Nulls]()
    3. [Categorical Columns]()
    4. [Numerical Columns]()
    5. [Imputation]()
    6. [Target Variable]()
    7. [Metadata Feature Engineering]()
        1. [Reflux Indicated]()
        2. [Voice Handicap Index (VHI) Z-Score]()
        3. [VHI Impact]()
4. [Feature Engineering]()
    1. [Short Term Features]()
    2. [Spectrograms]()
5. [Build Database]()
6. [Data Analysis & Visualisation]()
    1. [Analysis]()
    2. [Visualisation]()
7. [Machine Learning Models]()
    1. [Deep Learning for Metadata]()
    2. [Convolutional Neural Network for Spectrograms]()
    3. [Recurrent Neural Network for Short Term Features]()
8. [Streamlit App]


## Introduction
The intent is to build a modularised workflow to minimise repetition and optimise the ML model workflow (build, train, test, optimise).

1. Convert the `wfdb` to `wav` format for use with python libraries to extract features.

2. Extract features and store in a dataframe.

3. Data cleaning for storage in SQL database.

4. Build machine learning models:
    - CNN for visual features (spectrogram)
    - RNN for features with temporal component (MFCCs)



## Data Conversion
[Link to the notebook](https://github.com/alyssahondrade/Project4/blob/main/notebooks/01_convert_raw_data.ipynb)

Convert the `wfdb` to `wav` format.
1. Define constants necessary to convert:
    - `SIGNED_32BIT = 2 ** 31 - 1`. A signed 32-bit is required, 32-bit in this case [Source](https://physionet.org/content/voiced/1.0.0/).
    - `SAMPLE_WIDTH = 4`. Since 32-bit, 8 bits per byte.

2. Import the raw data to confirm the information text file is available with the corresponding audio file.

3. Use the [`wfdb`](https://wfdb.io) library the read the `wfdb` record, extracting both the signal and its sampling frequency.

4. Normalise and scale to the 32-bit range.

5. Use the [`pydub`](http://pydub.com) library to create an `AudioSegment` object, for export as a `wav` file.



## Data Cleaning
[Link to the notebook](https://github.com/alyssahondrade/Project4/blob/main/notebooks/02_metadata_cleaning.ipynb)


### Duplicates
Checked the ID distribution using `value_counts()`, with `voice005` and `voice055` identified to have duplicates.

1. All duplicate rows displayed for inspection, using: `duplicated(keep=False)`.

2. On initial inspection, only `Reflux Symptom Index (RSI) Score` were different.

3. Created a loop to compare duplicates column-wise using a mask, to confirm only the RSI Score is different.

Due to the dataset size, initial response was to calculate the average RSI Score and retain the duplicates. However, it was noted the error originated from the information text files itself, that the audio files are not duplicates. As a result, the following IDs are to be removed from all future code:

    `[voice005, voice006, voice054, voice055]`


### Names and Nulls
1. Convert all column names to lower case.

2. Simplify names, for example: `in a day` to `pd` (per day).

3. Replace all spaces with an underscore.

4. Convert `NU` values to `NaN`.


### Categorical Columns
1. No cleaning required for the `gender` column.

2. `occupation_status` column:
    - Used `value_counts(dropna=False)` to identify null values.
    - Replaced null values with `Unknown`.
    - Note: binning required for this column if used as a feature.

3. `smoker` column:
    - Replaced `No` with `no` for consistency.
    - Simplified `casual smoker` to `casual`.
    - Encoding plan for this column:
        - `0` for `no`
        - `1` for `casual`
        - `2` for `yes`

4. `alcohol_consumption` column:
    - Simplified response to single words: `casual`, `nondrinker`, `habitual`.
    - Encoding plan for this column:
        - `0` for `nondrinker`
        - `1` for `casual`
        - `2` for `habitual`

5. Dropped `eating_habits` column as it was empty, used as a header in the information text file.
    - Identify the eating habits columns: `carbonated_beverages`, `tomatoes`, `coffee`, `chocolate`, `soft_cheese`, `citrus_fruits`
    - Identify the unique values in these columns: `almost always`, `never`, `sometimes`, `almost never`, `always`
    - Encoding plan for this column:
        - `0` for `never`
        - `1` for `almost_never`
        - `2` for `sometimes`
        - `3` for `almost_always`
        - `4` for `always`


### Numerical Columns
1. Convert integer columns to `int` type: `age`, `vhi_score`, `rsi_score`.

2. `cigarettes_pd` column:
    - Null values for `yes` in the `smoker` column, hence a valid response is required for `cigarettes_pd` column.
    - Defined a method for [imputation](https://github.com/alyssahondrade/Project4/blob/main/markdown/process.md#imputation) to determine whether the missing data should be imputed with a __mean__ or __median__.
    - Convert the imputation method to a function to minimise repetition. Refer to the `imputation()` function in [functions.ipynb](https://github.com/alyssahondrade/Project4/blob/main/notebooks/functions.ipynb).

3. `alcohol_pd` column:
    - Define a function to handle the `per week` values, as well as the `/` and use of commas instead of decimal points. Refer to the `split_values()` and `clean_pd()` functions in [functions.ipynb](https://github.com/alyssahondrade/Project4/blob/main/notebooks/functions.ipynb).
    - Use the `apply()` method with the created function.
    - Impute missing values, as with the previous column.
    - Convert the column type to a `float` with 2 decimal points to capture the detail from the `per week` responses.

4. `water_litres_pd` column:
    - No null values.
    - Convert the commas to decimal points.
    - Convert the column type to a `float` with 2 decimal points, as per the original format.

5. `carbonated_pd` column:
    - Alter the function used to clean `alcohol_pd` to handle the following: `for week`, `-`, `for mounth`.
    - Impute missing values where applicable.
    - `always` failed with imputation as no valid values exist. Explore methods for imputation:
        - Check the `mean` and `median` for each unique value.
        - Check the summary statistics for its closest neighbour: `almost always`.
        - Use the maximum value for `almost always` as the value for all `always`.
    
6. `coffee_pd` column:
    - Impute missing values.
    - Convert the column type to an `int` as this is the original format and the imputed values are reasonably close to integer values.

7. `chocolate_grams_pd` column:
    - Create a function to handle the `gr` and `g`.
    - Alter the function used to clean `alcohol_pd` to handle the result after using the previous function.
    - Impute missing values.
    - As with `coffee_pd`, cast to integers.

8. `soft_cheese_pd` column:
    - Alter the function used to clean `alcohol_pd` to handle: `gr/ month`, `gr.`, and combinations of `/` with `gr`,
    - As with `coffee_pd`, cast to integers.

9. `citrus_fruits_pd` column:
    - Write a function to convert the gram-value to the number of fruits. Refer to the `fruit_gram()` function in [functions.ipynb](https://github.com/alyssahondrade/Project4/blob/main/notebooks/functions.ipynb).
    - Apply the function used to clean `alcohol_pd`.
    - Impute missing values.
    - Convert the column type to a `float` with 2 decimal points, as with `alcohol_pd`.


### Imputation
1. Return the non-null values for each unique value in the column.

2. Extract the indices of unique values with nulls.

3. Plot a histogram of this data and calculate the __skew score__ using `scipy` library's `skew()`.
    - Close to `0` means relatively symmetric, use: `mean`.
    - Close to `-1` means skewed to the left (negatively skewed), use: `median`.
    - Close to `1` means skewed to the right (positively skewed), use: `median`.

4. Calculate this for each unique value in the column and update missing values accordingly.


### Target Variable
1. Isolate the `diagnosis` column.

2. Use regex to separate the primary diagnosis (`base`) and the `subtype`.

3. Fill the null values in the `subtype` with `no subtype`.

4. Rename `base` back to `diagnosis`.


### Metadata Feature Engineering

#### Reflux Indicated
Created `reflux_indicated` column, based on domain knowledge ([Source](https://melbentgroup.com.au/wp-content/uploads/2015/10/MEG-Reflux-Severity-Index-RSI.pdf)):

> Normative data suggests that a RSI of greater than or equal to 13 is clinically significant. Therefore, a RSI > 13 may be indicative of significant reflux disease.


#### Voice Handicap Index (VHI Impact) Z-Score
Created `vhi_zscore` column, based on the paper ([Source](https://therapistsforarmenia.org/wp-content/uploads/2021/03/Voice-Handicap-Index-VHI.pdf)):

- `Normal mean = 8.75`
- `Standard deviation = 14.97`

Interpretation:
- Negative values are WNL (within normal limits), means no perception of handicap.
- Positive values indicate that voice impairment has a negative impact on aspects of daily life.

|![zscore_interpretation](https://github.com/alyssahondrade/Project4/blob/main/images/zscore_interpretation.png)|
|:---:|
|Z-Score Interpretation Table|


#### VHI Impact
Created `vhi_impact` column, based on the z-score interpretation table above.


## Feature Engineering
[Link to the notebook](https://github.com/alyssahondrade/Project4/blob/main/notebooks/03_feature_engineering.ipynb)

### Short Term Features
1. Define the frame size and step (in ms), with a 50% overlap ([Source 1](https://github.com/tyiannak/pyAudioAnalysis/wiki/3.-Feature-Extraction#single-file-feature-extraction---storing-to-file)), ([Source 2](https://www.tandfonline.com/doi/full/10.1080/24751839.2018.1501542))
    - Set `window_length = 0.050`.
    - Set `hop_size = 0.025`.

2. Use the [`pyAudioAnalysis`](https://github.com/tyiannak/pyAudioAnalysis) library to extract the short term features ([Source](https://github.com/tyiannak/pyAudioAnalysis/wiki/3.-Feature-Extraction#single-file-feature-extraction---storing-to-file)). The features available are:

| Feature ID | Feature Name | Description |
|:---:|:---:|---|
|1|Zero Crossing Rate|The rate of sign-changes of the signal during the duration of a particular frame.|
|2|Energy|The sum of squares of the signal values, normalized by the respective frame length.|
|3|Entropy of Energy|The entropy of sub-frames' normalized energies. It can be interpreted as a measure of abrupt changes.|
|4|Spectral Centroid|The center of gravity of the spectrum.|
|5|Spectral Spread|The second central moment of the spectrum.|
|6|Spectral Entropy|Entropy of the normalized spectral energies for a set of sub-frames.|
|7|Spectral Flux|The squared difference between the normalized magnitudes of the spectra of the two successive frames.|
|8|Spectral Rolloff|The frequency below which 90% of the magnitude distribution of the spectrum is concentrated.|
|9-21|MFCCs|Mel Frequency Cepstral Coefficients form a cepstral representation where the frequency bands are not linear but distributed according to the mel-scale.|
|22-33|Chroma Vector|A 12-element representation of the spectral energy where the bins represent the 12 equal-tempered pitch classes of western-type music (semitone spacing).|
|34|Chroma Deviation|The standard deviation of the 12 chroma coefficients.|

3. Parse each feature per voice sample to an array, convert this to a dataframe: `st_features_df`.

4. Loop through each column in `st_features_df` (i.e. feature) and create a dataframe for each, parsing each array to its own value.
    - Pad the arrays with zeroes using: `fillna(0)`.
    - Each feature component becomes its own column, to allow the SQLITE database to handle the data.


### Spectrograms
1. Use the `librosa` library to create the spectrogram for each voice sample.
    - Remove labels and the border using: `plt.tight_layout()` and `plt.axis('off')`.
    - Ensure there is no border using: `pad_inches=0` with `plt.savefig()`.
    - Use `plt.close()` to prevent each image plotting, to improve code runtime.

2. Resize the image to reduce the number of feature inputs for the machine learning model later.
    - Refer to the `resize_option()` function in [functions.ipynb](https://github.com/alyssahondrade/Project4/blob/main/notebooks/functions.ipynb).

3. Parse each image to separate RGBA channel lists, for export as a CSV.
    - Refer to the `spect_to_csv()` function in [functions.ipynb](https://github.com/alyssahondrade/Project4/blob/main/notebooks/functions.ipynb).
    


## Build Database
[Link to the notebook](https://github.com/alyssahondrade/Project4/blob/main/notebooks/04_build_database.ipynb)

1. Create the SQLITE engine using: `create_engine()`.

2. Extract all the files in the [`clean_data`](https://github.com/alyssahondrade/Project4/tree/main/resources/clean_data) subdirectory, reading each CSV to its own dataframe.

3. Write each dataframe to the database using: `to_sql()`.

4. Confirm all the tables were uploaded using: `inspect()`.



## Data Analysis & Visualisation
[Link to the notebook](https://github.com/alyssahondrade/Project4/blob/main/notebooks/05_data_analysis_visualisation.ipynb)

### Analysis
This section calculates the default values used in the Streamlit app.

1. Initialise a dictionary to hold all the values.

2. Calculate relevant values used for each metadata feature.

3. Export the dictionary to a JSON file

### Visualisation
This section uses visualisations to explore the data extracted from the information files.

|![age_distribution](https://github.com/alyssahondrade/Project4/blob/main/images/viz_demographics.png)|
|:---:|
|Age Distribution|

|![diagnosis_distribution](https://github.com/alyssahondrade/Project4/blob/main/images/viz_diagnosis_distribution.png)|
|:---:|
|Diagnosis Distribution|

|![subtype_distribution](https://github.com/alyssahondrade/Project4/blob/main/images/viz_subtype_distribution.png)|
|:---:|
|Subtype Distribution|

|![subtype_heatmap](https://github.com/alyssahondrade/Project4/blob/main/images/viz_subtype_heatmap.png)|
|:---:|
|Diagnosis vs Subtype|

