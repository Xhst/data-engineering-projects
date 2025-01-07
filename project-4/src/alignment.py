import json
import re
import os
import paths
import torch
from pathlib import Path
from collections import defaultdict
from hdbscan import HDBSCAN

from embedder import Embedder


def need_alignment(to_check: str) -> bool:
    # Regex to match only special characters or the letters 'e', 'B', 'M'
    pattern = r'^[^a-zA-Z]*[ebm]*[^a-zA-Z]*$'
    return not bool(re.match(pattern, to_check.lower()))


def extract_claim_pieces(directory_path: str) -> tuple[list[tuple[str, str]], list[tuple[str, str]], list[tuple[str, str]]]:
    """
    Extracts claims pieces from all JSON files in a directory and stores them in a lists of tuples.

    Args:
        directory_path (str): Path to the directory containing JSON files.

    Returns:
        dict[str, list[Claim]]: Dictionary where the key is the file name and the value is a list of Claim objects.
    """
    spec_names = []
    spec_values = []
    metrics = []
    directory = Path(directory_path)

    if not directory.is_dir():
        raise ValueError(f"The provided path '{directory_path}' is not a directory.")

    # Iterate over all JSON files in the directory
    for file_path in directory.glob("*.json"):
        file_name = file_path.name  # Extract file name
        paper_id_table_id = file_name.rstrip("_claims.json")

        try:
            with open(file_path, 'r') as file:
                data = json.load(file)

            for entry in data:
                for claim_id, content in entry.items():
                    # Extract specifications
                    if "specifications" in content:
                        for spec_id, spec in content["specifications"].items():
                            full_id = f"{paper_id_table_id}_{claim_id}_{spec_id}"
                            spec_names.append((full_id, spec["name"]))

                            if need_alignment(spec["value"]):
                                spec_values.append((full_id, spec["value"]))

                    # Extract measure and outcome
                    metric_id = f"{paper_id_table_id}_{claim_id}"
                    metric = content.get("Measure", "")
                    metrics.append((metric_id, metric))

        except Exception as e:
            print(f"Error processing file {file_name}: {e}")

    return (spec_names, spec_values, metrics)


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


def create_alignment(directory_path):
    (spec_names, spec_values, metrics) = extract_claim_pieces(directory_path)

    # embed sets elements
    embedder = Embedder()

    def create_embeddings(tuple_list):
        embeddings = {}
        for _, value in tuple_list:
            if value not in embeddings:
                embeddeding = embedder.get_sentence_embedding(value)
                embeddings[value] = embeddeding
        return embeddings

    name2emb = create_embeddings(spec_names)
    value2emb = create_embeddings(spec_values)
    metric2emb = create_embeddings(metrics)

    # clustering
    embeddings = torch.tensor([value for value in name2emb.values()])
    clusterer = HDBSCAN(metric='euclidean', min_cluster_size=2, min_samples=2)
    cluster_labels = clusterer.fit_predict(embeddings.numpy())

    save_clusters(name2emb, cluster_labels, 'clusters', f'clusters_name_hdbscan.json')

    # alignment


    # save json


if __name__ == "__main__":

    if not os.path.exists(paths.ALIGNMENT):
        os.makedirs(paths.ALIGNMENT)
        print(f"\n\033[32mCreated directory: {paths.ALIGNMENT}\033[0m\n")
        
    create_alignment(paths.CLAIMS)