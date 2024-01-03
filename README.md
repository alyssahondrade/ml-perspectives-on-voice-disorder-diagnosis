# Project4
Data Analytics Bootcamp Project 4

Github repository at: [https://github.com/alyssahondrade/Project4.git](https://github.com/alyssahondrade/Project4.git)


## Table of Contents
1. [Introduction](https://github.com/alyssahondrade/Project4#introduction)
    1. [Background](https://github.com/alyssahondrade/Project4#background)
    2. [Scope](https://github.com/alyssahondrade/Project4#scope)
    3. [Repository Structure](https://github.com/alyssahondrade/Project4#repository-structure)
    4. [Dataset](https://github.com/alyssahondrade/Project4#dataset)
2. [Technology](https://github.com/alyssahondrade/Project4#technology)
3. [Process](https://github.com/alyssahondrade/Project4#process)
4. [References](https://github.com/alyssahondrade/Project4#references)


## Introduction

### Background
The goal of this project is to explore different perspectives, using domain-knowledge, of voice disorder diagnosis using multiple machine learning models.


### Scope
The project will tackle the __binary classification problem of predicting a voice disorder diagnosis__.

Perspectives
1. Time-domain features
    - Extracted from original waveforms.
    - Examples include signal mean, variance, standard deviation, RMS, zero crossing rate, entropy, and energy.
2. Frequency-domain features
    - Derived from converting the waveforms to spectrum plots.
    - The focus will be on harmonics (which come from vocal folds) and formants (which correspond to resonance in the vocal tract) only.
3. Time-frequency domain features
    - Mel-frequency cepstral coefficients (MFCCs) only, which capture the overall spectral content of the signal.

4. Visual features
    - Using the signal's spectrogram, created by taking short-time Fourier Transforms (STFTs) of the signal to visualise the frequency content of time-varying signals.


### Repository Structure
- `markdown` directory contains all markdown files which support the README and project.
- `models` directory contains all pre-trained models.
- `notebooks` directory contains all Jupyter notebooks.

The `resources` directory contains the following subdirectories:
- `audio_files` contains the samples in `wav` format.
- `clean_data` contains the cleaned data in `csv` format.
- `spectrograms_linear` contains the images in `png` format.
- `voiced_dataset` is the raw dataset.

### Dataset
The VOICED database includes clinically-verified 208 voice samples, from 150 pathological and 58 healthy voices.

The dataset can be downloaded from: [https://physionet.org/content/voiced/1.0.0/](https://physionet.org/content/voiced/1.0.0/)

The original publication is available at: [https://www.sciencedirect.com/science/article/abs/pii/S0045790617338739](https://www.sciencedirect.com/science/article/abs/pii/S0045790617338739)


## Technology
1. Python Pandas - for data cleaning and preprocessing.
2. Python Matplotlib - for visualising waveforms and spectrograms.
3. SQL database - to store engineered features.


## Process
Available at: [https://github.com/alyssahondrade/Project4/blob/main/markdown/process.md](https://github.com/alyssahondrade/Project4/blob/main/markdown/process.md)


## References
Available at: [https://github.com/alyssahondrade/Project4/blob/main/markdown/references.md](https://github.com/alyssahondrade/Project4/blob/main/markdown/references.md)