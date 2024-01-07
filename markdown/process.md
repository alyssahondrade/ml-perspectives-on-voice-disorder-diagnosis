# Process

## Table of Contents
1. [Introduction]()
2. [Data Conversion]()
3. [Data Cleaning]()
    1. [Duplicates]()
    2. [Names and Nulls]()
    3. [Categorical Columns]()
    4. [Numerical Columns]()


    1. [Metadata]()
        1. [Skew Function]()
        2. [Encoding]()
    2. [Spectrograms]()


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


### Imputation
1. Return the non-null values for each unique value in the column.

2. Extract the indices of unique values with nulls.

3. Plot a histogram of this data and calculate the __skew score__ using `scipy` library's `skew()`.
    - Close to `0` means relatively symmetric, use: `mean`.
    - Close to `-1` means skewed to the left (negatively skewed), use: `median`.
    - Close to `1` means skewed to the right (positively skewed), use: `median`.

4. Calculate this for each unique value in the column and update missing values accordingly.


### Metadata
1. Simplify the column names: lowercase and underscores
2. Convert `NU` values to `NaN`
3. Clean categorical columns
4. Clean numerical columns

#### Skew Function
Due to the dataset size, needed to minimise dropping rows, used imputation instead. Skew function used to determine whether to use `mean` or `median` to impute missing values.


### Spectrograms
