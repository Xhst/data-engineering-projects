import json
import requests

models = ["allenai/scibert_scivocab_uncased", "bert-base-uncased", "distilbert-base-uncased"]
functions = ["tab_embedding", "tab_cap_embedding", "tab_cap_ref_embedding", "weighted_embedding"]
queries = [
    "NDCG on movielens dataset",
    "Recommender systems Recall on dataset goodbook",
    "Recommender systems MRR",
    "Deep Learning dataset Apple Flower",
    "Deep Learning GPT-3 precision and f1",
    "Deep Learning GPT-3 precision and f-measure"
]

ground_truth_paper_ids: list[str] = ["2008.03797", "2102.08921", "2301.04366v1", "2404.17723", "2405.02156v1", "2405.17060v1",
            "2406.02638v2", "2407.03440", "2407.09157v1", "2407.13531v1", "2408.04641v1", "2408.09646v1",
            "2409.10272", "2409.10309v2", "2409.17165v1", "2409.17400"]

results_json = {}

results_json["lucene"] = {}
results_json["lucene"]["bm25"] = {}
for i, query in enumerate(queries, start=1):
    response = requests.get(f"http://localhost:3000/api/search/tables?query={query}&modelName=lucene&methodName=lucene&useHybrid=false&useGroundTruth=true")
    query_key = f"q{i}"
    results_json["lucene"]["bm25"][query_key] = {}

    pos = 1
    for table in response.json()['tables']:
        # we only check on gt papers because we don't have gt_index on lucene for now
        if (table.get('paperId') not in ground_truth_paper_ids): continue
        
        results_json["lucene"]["bm25"][query_key][str(pos)] = table.get('paperId') + "#" + table.get('tableId')
        pos += 1
        
        # we only want the first 15
        if pos >= 16: break

for model in models:
    results_json[model] = {}
    for function in functions:
        results_json[model][function] = {}

        for i, query in enumerate(queries, start=1):
            response = requests.get(f"http://localhost:3000/api/search/tables?query={query}&modelName={model}&methodName={function}&useHybrid=false&useGroundTruth=true&numberOfResults=15")
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