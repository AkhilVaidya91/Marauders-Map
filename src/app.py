######################################## IMPORTING REQUIRED LIBRARIES ####################################
import os
import sys
import pandas as pd
import streamlit as st
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
data_folder = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')
from utilities import get_data, input_filter, clean_data, autogenerate_labels

def data_sourcing(left_lat, left_lon, dist, loc_name):
    lat, lon = input_filter(lat = left_lat, lon=left_lon)
    df = get_data(lat, lon, dist)
    df.to_csv(f'{data_folder}/LOCATION_{loc_name}_DATA.csv', index=False)
    return df

def data_clean_for_training(df):
    df = clean_data(df)
    df.to_csv(f'{data_folder}/MMR_DATA_CLEAN.csv', index=False)
    return df

st.title("Map Data Analysis - ETL Pipeline")

left_lat = st.number_input("Enter the left latitude", value=18.889833)
left_lon = st.number_input("Enter the left longitude", value=72.779844)
print(left_lat, left_lon)
loc_name = st.text_input("Enter the location name", value="Mumbai")
dist = st.number_input("Enter the distance", value=35)

if st.button("Run ETL Pipeline"):
    df = data_sourcing(left_lat, left_lon, dist, loc_name)
    if df:
        st.write("Data loaded successfully !!")

    df = clean_data(df)
    labelled_df, embeddings_df = autogenerate_labels(df)

    labelled_df.to_csv(f'{data_folder}/DATA_{loc_name}_CLEAN_LABELLED.csv', index=False)
    embeddings_df.to_csv(f'{data_folder}/DATA_{loc_name}_CLEAN_EMBEDDINGS.csv', index=False)

    st.write("ETL Pipeline executed successfully !!")