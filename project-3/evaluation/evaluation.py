import sys
import os
import json
from collections import defaultdict

# Add the desired path to sys.path
sys.path.append('../table-searcher')

# Now you can import the module
from paths import TABLE_FOLDER, GROUND_TRUTH, RESULTS


def evaluate_system(path_to_system: str) -> tuple[float, float]:
    mrr, ndcg = [0, 0]
    
    search_results: list[dict[int, dict[str,str,float]]] = [defaultdict(dict)]
    
    for file_name in os.listdir(path_to_system):
        # Build the full file path
        file_path = os.path.join(path_to_system, file_name)
        
        # Check if it's a JSON file
        if os.path.isfile(file_path) and file_name.endswith(".json"):
            # Open and load the JSON file
            with open(file_path, 'r') as json_file:
                try:
                    query_data: dict[int, dict[str,str,float]] = json.load(json_file)
                    search_results.append(query_data)
                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON in file {file_name}: {e}")

        # Print the list of JSON data
        print(search_results)
    
    
    return mrr, ndcg