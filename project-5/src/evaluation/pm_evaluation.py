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

def evaluate(gt_file_path, predict_file_path):
    with open(gt_file_path, 'r', encoding='utf-8') as gt_file:
        gt_lines = gt_file.readlines()

    with open(predict_file_path, 'r', encoding='utf-8') as predict_file:    
        predicted_pairs = predict_file.readlines()

    # To take only the predicted pairs of the same vocabulary as the GT 
    gt_pairs = extract_gt_pairs(gt_lines)

    # Predicted pairs set (filtered on GT vocabulary)
    true_positive = set()
    for line in predicted_pairs:
        item1, item2, label = line.split(' || ')
        pair = item1, item2           
        
        if pair in gt_pairs:
            if int(label) == 0: 
                print("False negative: " + str(pair))
            else:
                true_positive.add(pair)

    
    # PRECISION VIENE 1 PERCHE NON ABBIAMO FALSI POSITIVIIIIII :((((((((
    precision = len(true_positive) / len(predicted_pairs) if predicted_pairs else 0
    recall = len(true_positive) / len(gt_pairs) if gt_pairs else 0
    f1 = 2 * ((precision * recall) / (precision + recall)) if (precision + recall) > 0 else 0

    print(f"\n{CYAN}Pairwise matching EVALUATION for {predict_file_path.rsplit('/', 1)[-1]}{RESET}")
    print(f"- {GREEN}Precision: {RESET}{precision:.2f}")
    print(f"- {GREEN}Recall: {RESET}{recall:.2f}")
    print(f"- {GREEN}F1: {RESET}{f1:.2f}\n")


def get_pairs_for_pairwise_matching(blockin_path: str, gt_file_path: str):
    pairs_to_evaluate = set()
    
    with open(gt_file_path, 'r', encoding='utf-8') as gt_file:
        gt_lines = gt_file.readlines()

    with open(blockin_path, 'r', encoding='utf-8') as blocking_file:
        blocks = json.load(blocking_file)

    gt_pairs = extract_gt_pairs(gt_lines)

    for block in blocks:
        if len(block) == 1:
            continue
        for item1, item2 in gt_pairs:
            if item1 in block and item2 in block:
                pairs_to_evaluate.add(item1, item2)
    
    return pairs_to_evaluate
        
         
def extract_gt_pairs(gt_lines: list[str]):
    gt_pairs = set()
    
    # GT pairs set
    for line in gt_lines:
        line = line.strip()
        if not line:
            continue

        pair = tuple(line.split(' || '))
        
        gt_pairs.add(pair)
    
    return gt_pairs
