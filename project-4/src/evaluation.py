import os
import json

import paths

# Precision on claims
def evaluate_claims(gt_path: str, claim_path: str) -> tuple[float, float, int]:
    print(gt_path)

    gt_files = set(os.listdir(gt_path))
    claim_files = set(os.listdir(claim_path))
    
    # Files intersection
    common_files = gt_files.intersection(claim_files)
    correct_claims = 0
    
    file_number = 0

    claims_len = 0
    gt_claims_len = 0
    
    for file_name in common_files:

        if file_name == "1812.05040_4_claims.json":
            continue

        file_number += 1

        print(f"\n\033[34mProcessing file: {file_name} ...")

        gt_file = os.path.join(gt_path, file_name)
        claim_file = os.path.join(claim_path, file_name)
        
        with open(gt_file, 'r') as gt, open(claim_file, 'r') as claim:
            gt_data = json.load(gt)
            claim_data = json.load(claim)
        
        local_correct_claims = 0

        claims_len += len(claim_data)
        gt_claims_len += len(gt_data)

        gt_dict = {list(item.keys())[0]: item[list(item.keys())[0]] for item in gt_data}
        claim_dict = {list(item.keys())[0]: item[list(item.keys())[0]] for item in claim_data}
        
        # Confrontare le chiavi numeriche
        for key in range(len(claim_data)):

            if str(key) in gt_dict and gt_dict[str(key)] == claim_dict[str(key)]:
                correct_claims += 1
                local_correct_claims += 1

        # Local precision
        print(f"\033[36mFile completed with:\nP = \033[0m{local_correct_claims / len(claim_data) if len(claim_data) > 0 else 0}")

        # Local recall
        print(f"\033[36mR = \033[0m{local_correct_claims / len(gt_data) if len(gt_data) > 0 else 0}")
    
    # Precision
    precision = correct_claims / claims_len if claims_len > 0 else 0

    # Recall
    recall = correct_claims / gt_claims_len if gt_claims_len > 0 else 0
    
    return (precision, recall, file_number)


if __name__ == "__main__":

    precision, recall, file_number = evaluate_claims(paths.GROUND_TRUTH.CLAIMS.value, paths.CLAIMS)
    f1 = 2 * ((precision * recall) / (precision + recall))

    print(f"\033[32\nmDone! \033[0m{file_number}\033[32m files were analyzed\033[0m")
    print(f"\033[32mPrecision = \033[0m {precision:.2f}")
    print(f"\033[32mRecall = \033[0m {recall:.2f}")
    print(f"\033[32mF1 = \033[0m {f1:.2f}\n")
