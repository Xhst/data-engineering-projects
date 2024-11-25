import pymilvus as pm
import json
import paths
import os
import time
from table_embedding import get_function_from_name
from index_schema import schema
from embedder import Embedder


def convert_json_to_entities(data, paper_id, embedder: Embedder, function):
    entities = []
    for table_id, table_data in data.items():
        entities.append({
            "id": f"{paper_id}#{table_id}",
            "paper_id": paper_id,
            "table_id": table_id,
            "vector": function(embedder, table_data),
        })
    return entities
    

def create_index(embedder: Embedder, function_name: str, is_ground_truth_index: bool = False):
    function = get_function_from_name(function_name)

    collection_name = get_collection_name(embedder, function_name, is_ground_truth_index)

    if pm.has_collection(collection_name):
        pm.Collection(collection_name).drop()

    collection = pm.Collection(name=collection_name, schema=schema)

    folder = paths.GROUND_TRUTH + "/sample" if is_ground_truth_index else paths.TABLE_FOLDER

    for filename in os.listdir(folder):
        if filename.endswith(".json"):
            with open(os.path.join(folder, filename), "r", encoding="utf-8") as file:
                paper_id = filename.replace(".json", "")
                try:
                    data = json.load(file)
                    collection.insert(convert_json_to_entities(data, paper_id, embedder, function))
                except Exception as e:
                    continue
    
    # IVF_FLAT -> Inverted File with Flat Index
    index_params = {"index_type": "IVF_FLAT", "metric_type": "COSINE", "params": {"nlist": 200}}

    collection.create_index(field_name="vector", index_params=index_params)


def get_collection_name(embedder: Embedder, function_name: str, use_ground_truth: bool) -> str:
    collection_name_prefix = ""
    if use_ground_truth:
        collection_name_prefix += "gt_"

    return (collection_name_prefix + embedder.model_name + "_" + function_name).replace("/", "_").replace("-", "_")


if __name__ == "__main__":
    models = ["bert-base-uncased", "distilbert-base-uncased", "allenai/scibert_scivocab_uncased"]
    functions = ["tab_embedding", "tab_cap_embedding", "tab_cap_ref_embedding", "weighted_embedding"]

    try:
        pm.connections.connect("default", host="localhost", port="19530")
        print("Connection successful!")
    except pm.exceptions.MilvusException as e:
        print(f"Failed to connect to Milvus: {e}")
        exit()

    for model in models:
        for function in functions:
            print(f"Creating index with model {model} and function {function}...")
            start_time = time.time()
            embedder = Embedder(model_name=model)
            create_index(embedder, function_name=function)
            elapsed_time = time.time() - start_time
            print(f"Indexing done in {elapsed_time:.2f} seconds.")
        
