import json
import requests

models = ["allenai/scibert_scivocab_uncased", "bert-base-uncased", "distilbert-base-uncased"]
functions = ["tab_embedding", "tab_cap_embedding", "tab_cap_ref_embedding", "weighted_embedding"]
queries = [
    "NDCG on movielens dataset",
    "Recommender systems Recall on dataset goodbook",
    "Recommender systems MRR",
    "Deep Learning dataset Apple Flower",
    "Deep Learning GPT-3 precision and f1"
    "Deep Learning GPT-3 precision and f-measure"
]

results_json = {}

results_json["lucene"] = {}
for i, query in enumerate(queries, start=1):
    response = requests.get(f"http://localhost:3000/api/search/tables?query={query}&modelName=lucene&methodName=lucene&useHybrid=false&useGroundTruth=true")
    query_key = f"q{i}"
    results_json["lucene"][query_key] = {}

    pos = 1
    for table in response.json()['tables']:
        results_json["lucene"][query_key][str(pos)] = table.get('paperId') + "#" + table.get('tableId')
        pos += 1

for model in models:
    results_json[model] = {}
    for function in functions:
        results_json[model][function] = {}

        for i, query in enumerate(queries, start=1):
            response = requests.get(f"http://localhost:3000/api/search/tables?query={query}&modelName={model}&methodName={function}&useHybrid=false&useGroundTruth=true")
            query_key = f"q{i}"
            results_json[model][function][query_key] = {}

            pos = 1
            for table in response.json()['tables']:
                results_json[model][function][query_key][str(pos)] = table.get('paperId') + "#" + table.get('tableId')
                pos += 1

            print(f"Results for query {query_key} with model {model} and function {function} done.")

output_file = "./results.json"
with open(output_file, "w") as f:
    json.dump(results_json, f, indent=4)

print(f"Results saved to {output_file}")