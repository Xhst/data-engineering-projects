import pymilvus as pm
import json
import paths
import os
from index_schema import schema
from embedder import Embedder

embedder = Embedder()

def convert_json_to_entities(data, paper_id):
    entities = []
    for table_id, table_data in data.items():
        entities.append({
            "id": f"{paper_id}#{table_id}",
            "paper_id": paper_id,
            "table_id": table_id,
            "vector": embedder.get_sentence_embedding(
                table_data["table"] 
                + table_data["caption"] 
                + " ".join(table_data["references"])
            )
        })
    return entities


if __name__ == "__main__":
    try:
        pm.connections.connect("default", host="localhost", port="19530")
        print("Connection successful!")
    except pm.exceptions.MilvusException as e:
        print(f"Failed to connect to Milvus: {e}")
        exit()

    collection_name = "table_collection"

    if pm.has_collection(collection_name):
        pm.Collection(collection_name).drop()

    collection = pm.Collection(name=collection_name, schema=schema)

    for filename in os.listdir(paths.GROUND_TRUTH + "/sample"):
        if filename.endswith(".json"):
            print(f"Indexing {filename}")
            with open(os.path.join(paths.GROUND_TRUTH + "/sample", filename), "r", encoding="utf-8") as file:
                paper_id = filename.replace(".json", "")
                data = json.load(file)
                collection.insert(convert_json_to_entities(data, paper_id))
        
