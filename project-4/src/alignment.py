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
                            spec_names.append((full_id, spec["name"], spec["value"]))

                            if need_alignment(spec["value"]):
                                spec_values.append((full_id, spec["value"]))

                    # Extract measure and outcome
                    metric_id = f"{paper_id_table_id}_{claim_id}"
                    metric = content.get("Measure", "")
                    outcome = content.get("Outcome", "")
                    metrics.append((metric_id, metric, outcome))

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

    directory = Path(directory_path)

    with open('./clusters/names_ready_to_align.json', 'r') as name_file, open('./clusters/metrics_ready_to_align.json', 'r') as metric_file, open('./clusters/values_ready_to_align.json', 'r') as value_file:
        names_to_align = json.load(name_file)
        metrics_to_align = json.load(metric_file)
        values_to_align = json.load(value_file)

    names_alignment: dict[str, list[str]] = defaultdict(list)
    metrics_alignment: dict[str, list[str]] = defaultdict(list)
    values_alignment: dict[str, list[str]] = defaultdict(list)

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
                            name_val = f'{spec["name"]}: {spec["value"]}'
                            found = False
                            for name_to_align in names_to_align:
                                for value in names_to_align[name_to_align]:
                                    if value == name_val:
                                        names_alignment[name_to_align].append(full_id)
                                        found = True
                                        break
                                if found:
                                    break
                            if not found:
                                names_alignment[spec['name']].append(full_id)

                            found = False
                            for value_to_align in values_to_align:
                                for value in values_to_align[value_to_align]:
                                    if value == spec["value"]:
                                        names_alignment[value_to_align].append(full_id)
                                        found = True
                                        break
                                if found:
                                    break
                            if not found:
                                values_alignment[spec['value']].append(full_id)
                        
                    metric_id = f"{paper_id_table_id}_{claim_id}"
                    metric = content.get("Measure", "")
                    outcome = content.get("Outcome", "")

                    metric_outcome = f"{metric}: {outcome}"
                    found = False
                    for metric_to_align in metrics_to_align:
                        for value in metrics_to_align[metric_to_align]:
                            if value == metric_outcome:
                                metrics_alignment[metric_to_align].append(metric_id)
                                found = True
                                break
                        if found:
                            break
                    if not found:
                        metrics_alignment[metric].append(metric_id)

        except Exception as e:
            print(f"Error processing file {file_name}: {e}")

    alignment = {
        "aligned_names": names_alignment,
        "aligned_values": values_alignment,
        "aligned_metrics": metrics_alignment
    }

    with open('../alignment/TEAM_FOREST_ALIGNMENT.json', 'w') as alignment_file:
        json.dump(alignment, alignment_file, indent=4)


def create_clusters(directory_path):
    (spec_names, spec_values, metrics) = extract_claim_pieces(directory_path)

    # embed sets elements
    embedder = Embedder()

    def create_embeddings(tuple_list):
        embeddings = {}
        for id, name, value in tuple_list:
            name_value = name + ": " + value 
            if name_value not in embeddings:
                embeddeding = embedder.get_sentence_embedding(name_value)
                embeddings[name_value] = embeddeding
        return embeddings

    name2emb = create_embeddings(spec_names)
    #value2emb = create_embeddings(spec_values)
    metric2emb = create_embeddings(metrics)

    # clustering
    embeddings = torch.tensor([value for value in metric2emb.values()])
    clusterer = HDBSCAN(metric='euclidean', min_cluster_size=2, min_samples=2)
    cluster_labels = clusterer.fit_predict(embeddings.numpy())

    save_clusters(metric2emb, cluster_labels, 'clusters', f'clusters_metric_hdbscan.json')


if __name__ == "__main__":

    if not os.path.exists(paths.ALIGNMENT):
        os.makedirs(paths.ALIGNMENT)
        print(f"\n\033[32mCreated directory: {paths.ALIGNMENT}\033[0m\n")

    # these clusters help to do it manually later
    #create_clusters(paths.CLAIMS)  
    
    # this creates the actual alignment based on files inside the clusters folder
    create_alignment(paths.CLAIMS)