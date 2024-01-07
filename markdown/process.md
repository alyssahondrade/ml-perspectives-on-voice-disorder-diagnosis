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
    7. [Feature Engineering]()
        1. [Reflux Indicated]()
        2. [Voice Handicap Index (VHI) Z-Score]()
        3. [VHI Impact]()


## Introduction
The intent is to build a modularised workflow to minimise repetition and optimise the ML model workflow (build, train, test, optimise).
1. Convert the `wfdb` to `wav` format for use with python libraries to extract features.
2. Extract features and store in a dataframe.
3. Data cleaning for storage in SQL database.
4. Build machine learning models:
    - CNN for visual features (spectrogram)
    - RNN for features with temporal component (MFCCs)

## Data Conversion
[Link to the notebook]()

Convert the `wfdb` to `wav` format.
1. Define constants necessary to convert:
    - `SIGNED_32BIT = 2 ** 31 - 1`. A signed 32-bit is required, 32-bit in this case [Source](https://physionet.org/content/voiced/1.0.0/).
    - `SAMPLE_WIDTH = 4`. Since 32-bit, 8 bits per byte.
2. Import the raw data to confirm the information text file is available with the corresponding audio file.
3. Use the `wfdb` library the read the `wfdb` record, extracting both the signal and its sampling frequency.
4. Normalise and scale to the 32-bit range.
5. Use the `pydub` library to create an `AudioSegment` object, for export as a `wav` file.

## Data Cleaning
[Link to the notebook]()

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
    - Defined a method for [imputation]() to determine whether the missing data should be imputed with a __mean__ or __median__.
    - Convert the imputation method to a function to minimise repetition.

3. `alcohol_pd` column:
    - Define a function to handle the `per week` values, as well as the `/` and use of commas instead of decimal points.
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
    - Write a function to convert the gram-value to the number of fruits.
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


### Feature Engineering

#### Reflux Indicated
Created `reflux_indicated` column, based on domain knowledge ([Source](https://melbentgroup.com.au/wp-content/uploads/2015/10/MEG-Reflux-Severity-Index-RSI.pdf)):

> Normative data suggests that a RSI of greater than or equal to 13 is clinically significant.

> Therefore, a RSI > 13 may be indicative of significant reflux disease.


#### Voice Handicap Index (VHI Impact) Z-Score
Created `vhi_zscore` column, based on the paper ([Source](https://therapistsforarmenia.org/wp-content/uploads/2021/03/Voice-Handicap-Index-VHI.pdf)):

- `Normal mean = 8.75`
- `Standard deviation = 14.97`

Interpretation:

> - Negative values are WNL (within normal limits), means no perception of handicap.

> - Positive values indicate that voice impairment has a negative impact on aspects of daily life.

|![zscore_interpretation](https://github.com/alyssahondrade/Project4/blob/main/images/zscore_interpretation.png)|
|:---:|
|Z-Score Interpretation Table|

