# Project4
Data Analytics Bootcamp Project 4

Github repository at: [https://github.com/alyssahondrade/Project4.git](https://github.com/alyssahondrade/Project4.git)


## Table of Contents
1. [Introduction]()
    1. [Background]()
    2. [Scope]()
    3. [Repository Structure]()
    4. [Dataset]()
2. [Technology]()
3. [Process]()
4. [References]()


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

The original publication is available at: [https://www.sciencedirect.com/science/article/abs/pii/S0045790617338739?via%3Dihub](https://www.sciencedirect.com/science/article/abs/pii/S0045790617338739?via%3Dihub)


## Technology
1. Python Pandas - for data cleaning and preprocessing.
2. Python Matplotlibn - for visualising waveforms and spectrograms.
3. SQL database - to store engineered features.


## Process
Available at: []()


## References
Available at: []()