import json
import sys
import os
import re

### --------- ###
prv_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(prv_folder)
import paths
from ansi_colors import *
### --------- ###

# Pairs can be (str1, str2) in GT and (str2, str1) in json file... need normalization
def normalize_pair(pair):
    return tuple(sorted(pair))

def evaluate(gt_file_path, json_file_path):
    with open(gt_file_path, 'r', encoding='utf-8') as gt_file:
        gt_lines = gt_file.readlines()

    with open(json_file_path, 'r', encoding='utf-8') as json_file:
        json_data = json.load(json_file)


    gt_pairs = set()

    # To take only the predicted pairs of the same vocabulary as the GT 
    gt_name_set = set()

    # GT pairs set
    for line in gt_lines:
        line = line.strip()
        if not line:
            continue

        pair = tuple(re.findall(r'"([^"]*)"', line))

        str1, str2 = pair
        gt_name_set.add(str1)
        gt_name_set.add(str2)

        gt_pairs.add((pair)) 


    predicted_pairs = set()

    # Predicted pairs set (filtered on GT vocabulary)
    for entry in json_data:
        pair = (entry['entry1'], entry['entry2'])

        str1, str2 = pair
        if str1 in gt_name_set and str2 in gt_name_set:
            predicted_pairs.add(pair)

    # Normalization
    gt_pairs_normalized = {normalize_pair(pair) for pair in gt_pairs}
    predicted_pairs_normalized = {normalize_pair(pair) for pair in predicted_pairs}

    correct_pairs = correct_pairs = gt_pairs_normalized.intersection(predicted_pairs_normalized)


    precision = len(correct_pairs) / len(predicted_pairs_normalized) if predicted_pairs_normalized else 0
    recall = len(correct_pairs) / len(gt_pairs_normalized) if gt_pairs_normalized else 0
    f1 = 2 * ((precision * recall) / (precision + recall)) if (precision + recall) > 0 else 0

    print(f"\n{CYAN}Pairwise matching EVALUATION for {json_file_path.rsplit('/', 1)[-1]}{RESET}")
    print(f"- {GREEN}Precision: {RESET}{precision:.2f}")
    print(f"- {GREEN}Recall: {RESET}{recall:.2f}")
    print(f"- {GREEN}F1: {RESET}{f1:.2f}\n")
    




if __name__ == "__main__":

    gt_file_path = f"{paths.GROUND_TRUTH}/gt.txt"
    json_file_path = f"{paths.PAIRWISE_MATCHING.RESULTS_JAROWINKLER.value}/lsh_bigram.json"

    evaluate(gt_file_path, json_file_path)

