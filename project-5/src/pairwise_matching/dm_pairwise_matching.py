import pandas as pd
import itertools
import json
import re
import sys
import os
import deepmatcher as dm

### --------- ###
prv_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(prv_folder)
import paths
from ansi_colors import *
### --------- ###


def pairs_csv_builder(directory):
    
    '''
    This function processes each JSON file within the specified blocking_directory. 
    For each JSON file, it reads the content, and for every block, it generates all possible 
    pairs of entries from the same block. These pairs are then saved with their corresponding block ID into a CSV file.
    '''

    for filename in os.listdir(directory):
        if filename.endswith('.json'):
            filepath = os.path.join(directory, filename)
            print(f"\n{CYAN}Processing file:{RESET} {filepath}")
            
            with open(filepath, 'r') as f:
                blocks = json.load(f)

            blocking_method = filename.split('_blocking.')[0]

            data = []
            for block_id, block in enumerate(blocks):
                for entry in block:
                    data.append({"block_id": block_id, "entry": entry})

            df = pd.DataFrame(data)
            df['entry'] = df['entry'].apply(lambda x: re.sub(r'\[.*?\]', '', x).strip())

            pairs = []

            # Itera sui gruppi con lo stesso block_id
            for block_id, group in df.groupby('block_id'):  
                # Genera tutte le combinazioni di coppie all'interno dello stesso blocco
                combinations = itertools.combinations(group['entry'], 2)
                for left, right in combinations:
                    pairs.append({
                        'id': f"{block_id}_{hash(left)}_{hash(right)}",
                        'left_': left,
                        'right_': right
                    })

            pairs_df = pd.DataFrame(pairs)

            output_dir = paths.PAIRWISE_MATCHING.RESULTS_DM_UNLABELED.value
            os.makedirs(output_dir, exist_ok=True)

            output_file = os.path.join(output_dir, f"{blocking_method}_pairs.csv")

            pairs_df.to_csv(output_file, index=False)

            print(f"{GREEN}Generated CSV file:{RESET} {output_file}")


def predict_pairs(directory):
    for filename in os.listdir(directory):
        if filename.endswith('.csv'):
            filepath = os.path.join(directory, filename)
            print(f"\n{CYAN}Processing file:{RESET} {filepath}")
            
            df = pd.read_csv(filepath)

            model = dm.MatchingModel()
            model.load_state(paths.MODELS.DEEP_MATCHER.value)

            processed_data = dm.data.process_unlabeled(path = filepath,
                                                       trained_model=model)
            
            model.eval()
            predictions = model.run_prediction(processed_data,output_attributes=True)

            os.makedirs(paths.PAIRWISE_MATCHING.RESULTS_DM_PREDICTED.value, exist_ok=True)
            predictions.to_csv(f"{paths.PAIRWISE_MATCHING.RESULTS_DM_PREDICTED.value}/{filename.removesuffix('.csv')}_predicted.csv", index=False)



if __name__ == "__main__":
    
    directory = paths.BLOCKING.RESULTS.value
    pairs_csv_builder(directory)
    
    #directory = paths.PAIRWISE_MATCHING.RESULTS_DM_UNLABELED.value
    #predict_pairs(directory)

