import pandas as pd
import recordlinkage
import json
import re
import os

directory = '../blocking/results/'

for filename in os.listdir(directory):
    if filename.endswith('.json'): 
        filepath = os.path.join(directory, filename)
        print(f"Processing file: {filepath}")
        
        with open(filepath, 'r') as f:
            blocks = json.load(f)

        blocking_method = filename.split('_blocking.')[0]

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
        compare.string('entry_cleaned', 'entry_cleaned', method='jarowinkler', threshold=0.85)
        comparison_results = compare.compute(pairs, df)

        matches = comparison_results[comparison_results.sum(axis=1) > 0]

        matched_pairs = []
        matched_pairs = []
        for index1, index2 in matches.index:
            matched_pairs.append({
                "entry1": str(df.loc[index1, "entry"]),
                "entry2": str(df.loc[index2, "entry"]),
                "block_id": int(df.loc[index1, "block_id"])  
            })

        os.makedirs('results/jarowinkler', exist_ok=True)

        with open(f'results/jarowinkler/{blocking_method}.json', 'w') as f:
            json.dump(matched_pairs, f, indent=4)