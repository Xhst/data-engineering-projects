import sys
import os
import json
import time
import torch
from sklearn.cluster import DBSCAN, KMeans, AgglomerativeClustering
from hdbscan import HDBSCAN
import umap.umap_ as umap

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from file_reader import read_file
from llm import query_groq
from embedder import Embedder

SOURCES_FOLDER = '../../sources'

def load_sources_dataframes(sources_folder: str) -> dict:
    """
    Load the data from the sources folder into a dictionary of DataFrames
    
    Args:
        sources_folder (str): The path to the folder containing the source files
    
    Returns:
        dict: A dictionary containing the data from the source files as DataFrames
    """
    
    # read all folders in the sources folder
    sources_data = {}

    for folder in os.listdir(sources_folder):
        folder_path = os.path.join(sources_folder, folder)
        if os.path.isdir(folder_path):
            sources_data[folder] = {}
            for file in os.listdir(folder_path):
                file_path = os.path.join(folder_path, file)
                if os.path.isfile(file_path):
                    sources_data[folder][file] = read_file(file_path)
    
    return sources_data


def get_field_description(field: str, values: list[str] = []) -> str:
    """
    Get the descriptions of a field from the GROQ API
    
    Args:
        field (str): The field to get the description for
    
    Returns:
        str: The description of the field
    """
    system_prompt = '''
    You will receive a name of a field, with some values associated, of a dataset and you have to provide a description for that field.
    The dataset is about Companies.
    In your response you must only include a brief description of the field, maximum 20 words.
    '''

    content = f'''
    Please provide a description for the field: {field}

    Example of values for the field:
    {values}
    '''
    return query_groq(messages=[
        {
            "role": "system",
            "content": system_prompt
        },
        {
            "role": "user",
            "content": content
        }
    ], temperature=0.2)


def get_fields_descriptions(sources_data: dict) -> dict:
    """
    Get the descriptions of the fields in the sources data
    
    Args:
        sources_data (dict): The data from the sources
    
    Returns:
        dict: A dictionary containing the descriptions of the fields in the sources data
    """
    fields_descriptions = {}
    
    for source, data in sources_data.items():
        fields_descriptions[source] = {}

        for file, df in data.items():
            fields_descriptions[source][file] = {}

            if df is None:
                print(f'Dataframe missing for {file}')
                continue

            for col_name in df.columns:
                field_name = col_name
                field_values = df[col_name].head(5).tolist()

                try:
                    fields_descriptions[source][file][field_name] = get_field_description(field_name, field_values)
                except Exception:
                    print(f'Error getting description for field {field_name}')
                    fields_descriptions[source][file][field_name] = ''

                # sleep to avoid rate limiting
                time.sleep(1)
    
    return fields_descriptions


def create_fields_descriptions_embeddings(fields_descriptions: dict) -> dict:
    """
    Create embeddings for the fields descriptions
    
    Args:
        fields_descriptions (dict): The descriptions of the fields
    
    Returns:
        dict: A dictionary containing the embeddings of the fields descriptions
    """
    fields_descriptions_embeddings = {}

    embedder = Embedder()
    
    for source, data in fields_descriptions.items():
        fields_descriptions_embeddings[source] = {}

        for file, fields in data.items():
            fields_descriptions_embeddings[source][file] = {}

            for field, description in fields.items():
                fields_descriptions_embeddings[source][file][field] = embedder.get_sentence_embedding(description).tolist()
    
    return fields_descriptions_embeddings


def cluster_embeddings(embeddings, algorithm, **kwargs):
    """
    Perform clustering on the embeddings using the specified algorithm.
    """
    if algorithm == 'hdbscan':
        clusterer = HDBSCAN(metric='euclidean', **kwargs)
        cluster_labels = clusterer.fit_predict(embeddings.numpy())
    elif algorithm == 'kmeans':
        clusterer = KMeans(**kwargs)
        cluster_labels = clusterer.fit_predict(embeddings.numpy())
    elif algorithm == 'dbscan':
        clusterer = DBSCAN(metric='euclidean', **kwargs)
        cluster_labels = clusterer.fit_predict(embeddings.numpy())
    elif algorithm == 'agglomerative':
        clusterer = AgglomerativeClustering(metric='euclidean', **kwargs)
        cluster_labels = clusterer.fit_predict(embeddings.numpy())
    else:
        raise ValueError(f"Invalid clustering algorithm: {algorithm}")
    return cluster_labels


def flatten_dict(d, parent_key='', sep='__'):
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)


def save_clusters(item2embedding, cluster_labels, output_dir, output_file):
    """
    Save the clustering results to a JSON file.
    """
    print("Saving clusters to JSON...")
    clusters = {}
    for i, label in enumerate(cluster_labels):
        filename = list(item2embedding.keys())[i]
        if label not in clusters:
            clusters[label] = []
        clusters[label].append(filename)

    # Convert cluster labels to int (if necessary) for JSON serialization
    clusters = {int(k): v for k, v in clusters.items()}

    with open(output_dir + "/" + output_file, 'w') as f:
        json.dump(clusters, f, indent=4)

    print(f"Clusters saved successfully to " + output_dir + "/" + output_file)


if __name__ == '__main__':
    sources_data = load_sources_dataframes(SOURCES_FOLDER)
    
    # Uncomment to get fields descriptions (may change the results due to the temperature parameter)
    #fields_descriptions = get_fields_descriptions(sources_data)

    # Save fields descriptions
    #with open('./descriptions/fields_descriptions.json', 'w') as f:
    #    json.dump(fields_descriptions, f, indent=4)

    fields_descriptions = json.load(open('./descriptions/fields_descriptions.json'))

    fields_descriptions_embeddings = create_fields_descriptions_embeddings(fields_descriptions)

    # Save embeddings
    #with open('./descriptions/fields_descriptions_embeddings.json', 'w') as f:
    #    json.dump(fields_descriptions_embeddings, f, indent=4)

    # Load embeddings from file
    #fields_descriptions_embeddings = json.load(open('./descriptions/fields_descriptions_embeddings.json'))

    fields_descriptions_embeddings = flatten_dict(fields_descriptions_embeddings)

    # HDBSCAN
    embeddings = torch.tensor([value for value in fields_descriptions_embeddings.values()])
    cluster_labels = cluster_embeddings(embeddings, 'hdbscan', min_cluster_size=3, min_samples=2)
    save_clusters(fields_descriptions_embeddings, cluster_labels, 'clusters', f'clusters_hdbscan.json')

    # UMAP + HDBSCAN
    reducer = umap.UMAP(metric='cosine', output_metric='euclidean', n_neighbors=8)
    umap_embeddings = torch.tensor(reducer.fit_transform(embeddings))
    cluster_labels = cluster_embeddings(umap_embeddings, 'hdbscan', min_cluster_size=3, min_samples=2)
    save_clusters(fields_descriptions_embeddings, cluster_labels, 'clusters', f'clusters_hdbscan_umap.json')


    


