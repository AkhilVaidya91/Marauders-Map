######################################## IMPORTING REQUIRED LIBRARIES ####################################
import os
import sys
import pandas as pd
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
data_folder = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')
from utilities import get_data, input_filter, clean_data, autogenerate_labels


################################################## INPUTS ################################################

left_lat = 18.889833
left_lon = 72.779844
dist = 35

def data_sourcing():
    lat, lon = input_filter(lat = left_lat, lon=left_lon)
    df = get_data(lat, lon, dist)
    df.to_csv(f'{data_folder}/MMR_DATA.csv', index=False)
    return df

def data_clean_for_training(df):
    df = clean_data(df)
    df.to_csv(f'{data_folder}/MMR_DATA_CLEAN.csv', index=False)
    return df


if __name__ == '__main__':

    # df = data_sourcing() ## testing the data sourcing endpoint
    # if df:
    #     print("Data loaded successfully !!")

    # clean_df = data_clean_for_training(df)

    df = pd.read_csv(f'{data_folder}/MMR_DATA.csv')
    df = clean_data(df)
    labelled_df, embeddings_df = autogenerate_labels(df)

    labelled_df.to_csv(f'{data_folder}/MMR_DATA_CLEAN_LABELLED.csv', index=False)
    embeddings_df.to_csv(f'{data_folder}/MMR_CLEAN_EMBEDDINGS.csv', index=False)