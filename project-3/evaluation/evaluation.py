import json
import requests

models = [
    "bert-base-uncased", 
    "distilbert-base-uncased", 
    "allenai/scibert_scivocab_uncased", 
    "all-mpnet-base-v2", 
    "sentence-transformers/sentence-t5-large", 
    "sentence-transformers/all-MiniLM-L6-v2", 
    "deepset/sentence_bert"
]
functions = ["tab_embedding", "tab_cap_embedding", "tab_cap_ref_embedding", "weighted_embedding"]
queries = [
    "NDCG movielens",
    "Recommender Recall Goodbook",
    "Recommender MRR",
    "Deep Learning Apple Flower",
    "Deep Learning GPT-3 precision f1",
    "Deep Learning GPT-3 precision f-measure"
]

metrics_arguments_querys_list = [
    ('Recommender systems', " movielens NDCG"),
    ('Recommender systems', "Recall Goodbook"),
    ('Recommender systems', "MRR"),
    ('Deep Learning', "Apple Flower"),
    ('Deep Learning', "GPT-3 precision f1"),
    ('Deep Learning', "GPT-3 precision f-measure")
]

ground_truth_paper_ids: list[str] = ["2008.03797", "2102.08921", "2301.04366v1", "2404.17723", "2405.02156v1", "2405.17060v1",
            "2406.02638v2", "2407.03440", "2407.09157v1", "2407.13531v1", "2408.04641v1", "2408.09646v1",
            "2409.10272", "2409.10309v2", "2409.17165v1", "2409.17400"]

def evaluate(hybrid: bool = False): 
    results_json = {}

    results_json["lucene"] = {}
    results_json["lucene"]["bm25"] = {}
    for i, (queryArgument, queryTable) in enumerate(metrics_arguments_querys_list, start=1):
        response = requests.get(f"http://localhost:3000/api/search/tables?queryArgument={queryArgument}&queryTable={queryTable}&modelName=lucene&methodName=lucene&useHybrid={hybrid}&useGroundTruth=true")
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

            for i, (queryArgument, queryTable) in enumerate(metrics_arguments_querys_list, start=1):
                response = requests.get(f"http://localhost:3000/api/search/tables?queryArgument={queryArgument}&queryTable={queryTable}&modelName={model}&methodName={function}&useHybrid={hybrid}&useGroundTruth=true&numberOfResults=15")
                query_key = f"q{i}"
                results_json[model][function][query_key] = {}

                pos = 1
                for table in response.json()['tables']:
                    results_json[model][function][query_key][str(pos)] = table.get('paperId') + "#" + table.get('tableId')
                    pos += 1

                print(f"Results for query {query_key} with model {model} and function {function} done.")

    output_file = "./results_hybrid.json" if hybrid else "./results.json"

    with open(output_file, "w") as f:
        json.dump(results_json, f, indent=4)

    print(f"Results saved to {output_file}")


evaluate(hybrid=True)
evaluate(hybrid=False)
