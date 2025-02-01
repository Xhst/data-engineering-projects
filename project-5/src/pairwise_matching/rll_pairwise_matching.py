import pandas as pd
import recordlinkage
import json
import re
import os
import sys

### --------- ###
prv_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(prv_folder)
import paths
### --------- ###

def pairwise_matching(blocking_path: str, threshold: float):
    if blocking_path.endswith('.json'): 
        filepath = os.path.join(paths.BLOCKING.RESULTS.value, blocking_path)
        print(f"Processing file: {filepath}")
        
        with open(filepath, 'r') as f:
            blocks = json.load(f)

        blocking_method = blocking_path.split('_blocking.')[0]

        data = []
        for block_id, block in enumerate(blocks):
            for entry in block:
                data.append({"block_id": block_id, "entry": entry})

        df = pd.DataFrame(data)

        df['entry_cleaned'] = df['entry'].apply(lambda x: re.sub(r'\[.*?\]', '', x).strip())

        indexer = recordlinkage.Index()
        indexer.block('block_id')
        pairs = indexer.index(df)

        compare = recordlinkage.Compare()
        compare.string('entry_cleaned', 'entry_cleaned', method='jarowinkler', threshold=threshold)
        comparison_results = compare.compute(pairs, df)

        os.makedirs('results/jarowinkler', exist_ok=True)
        
        with open('results/jarowinkler/' + blocking_method + '_t' + str(threshold) + '.txt', 'w', encoding="utf8") as f:
            for (index1, index2), score in comparison_results.iterrows():
                label = int(score.sum() > 0)  # 1 if matched, 0 otherwise
                f.write(f"{df.loc[index1, 'entry']} || {df.loc[index2, 'entry']} || {label}\n")