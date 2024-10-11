# High Fidelity Functional Map Generation for Industrial-Commercial-Residential Areas and Cluster Identification using Map Text Data Classification

## Project Overview

This project aims to develop an automated system for generating high-fidelity functional maps of regions, classifying areas into industrial, commercial, and residential zones. It also identifies clusters within these classifications to optimize routes for Unmanned Aerial Vehicles (UAVs) conducting Air Quality Index (AQI) monitoring.

The system addresses the limitations of static AQI monitoring stations by leveraging machine learning, geospatial data, and UAV technology to create an efficient method for high-precision air quality monitoring across diverse urban and rural landscapes.

## Project Structure

- `data/`: Contains raw and processed data files
- `models/`: Stores trained classification models
- `src/`: Flask backend, Streamlit frontend code
- `utils/`: Utility scripts for data loading and processing/classification rules
- `notebooks/`: Jupyter notebooks for data preprocessing and classification
- `documentation/`: Additional project documentation

## Features

1. High-fidelity geospatial map generation
2. Region classification into residential, commercial, industrial, and other types
3. Data-driven route optimization for UAV-based AQI monitoring
4. Real-time AQI data collection across diverse regions


## Data Processing

Data preprocessing steps are documented in the Jupyter notebooks located in the `notebooks/` directory. These include:

- Data collection from Maps API
- Text data cleaning and normalization
- Feature extraction, vectorization and clustering
- Data labeling and augmentation

## Models

Machine learning models used for text classification, including:

- USE (Universal Sentence Encoder)
- BERT (Bidirectional Encoder Representations from Transformers)
- XGBoost
- LSTM (Long Short-Term Memory networks)
- Llama 3.2
