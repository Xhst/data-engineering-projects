import pymilvus as pm
import time
from indexer import create_index
from embedder import Embedder

if __name__ == "__main__":
    models = ["bert-base-uncased", "distilbert-base-uncased", "allenai/scibert_scivocab_uncased", 
              "all-mpnet-base-v2", "sentence-transformers/sentence-t5-large"]
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
            create_index(embedder, function_name=function, is_ground_truth_index=True)
            elapsed_time = time.time() - start_time
            print(f"Indexing done in {elapsed_time:.2f} seconds.")