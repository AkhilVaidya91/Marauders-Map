import numpy as numpy
import pandas as pd
import numpy as np
import tensorflow_hub as hub
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler


def embed(input):
    module_url = "https://tfhub.dev/google/universal-sentence-encoder/4"
    model = hub.load(module_url)
    return model(input)

def generate_use_embeddings(data):
    embeddings = embed(data)
    embeddings = np.array(embeddings).tolist()
    return embeddings

def autogenerate_labels(df):
    map_data = df['Map Data'].to_numpy()

    embeddings_list = generate_use_embeddings(map_data)
    np_embeddings = np.array(embeddings_list)
    df_embeddings = pd.DataFrame(np_embeddings)
    scaler = StandardScaler()
    scaled_embeddings = scaler.fit_transform(np_embeddings)

    n_clusters = 4
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    kmeans.fit(scaled_embeddings)

    y_kmeans = kmeans.labels_

    df['label'] = y_kmeans + 1
    return df, df_embeddings