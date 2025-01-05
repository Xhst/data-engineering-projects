import json
from ansi_colors import *
from pathlib import Path
from dataclasses import dataclass


@dataclass
class Claim():
    specs: list[tuple[str,str]]
    measure: str
    outcome: str


def extract_claims_from_directory(directory_path: str) -> dict[str, list[Claim]]:
    """
    Extracts claims from all JSON files in a directory and stores them in a dictionary.

    Args:
        directory_path (str): Path to the directory containing JSON files.

    Returns:
        dict[str, list[Claim]]: Dictionary where the key is the file name and the value is a list of Claim objects.
    """
    claims_dict = {}
    directory = Path(directory_path)

    if not directory.is_dir():
        raise ValueError(f"The provided path '{directory_path}' is not a directory.")

    # Iterate over all JSON files in the directory
    for file_path in directory.glob("*.json"):
        file_name = file_path.name  # Extract file name

        try:
            with open(file_path, 'r') as file:
                data = json.load(file)

            claims = []

            for entry in data:
                for _, content in entry.items():
                    # Extract specifications
                    specs = []
                    if "specifications" in content:
                        for spec_id, spec in content["specifications"].items():
                            specs.append((spec["name"], spec["value"]))

                    # Extract measure and outcome
                    measure = content.get("Measure", "")
                    outcome = content.get("Outcome", "")

                    # Create a Claim object
                    claim = Claim(specs=specs, measure=measure, outcome=outcome)
                    claims.append(claim)

            # Add to dictionary with file_name as the key
            claims_dict[file_name] = claims

        except Exception as e:
            print(f"Error processing file {file_name}: {e}")

    return claims_dict


def evaluate_claims(gt_dict: dict[str, list[Claim]], pred_dict: dict[str, list[Claim]]) -> tuple[float, float, int]:
    """
    Evaluates precision and recall for claims using pre-extracted Claim objects.

    Args:
        gt_dict (dict[str, list[Claim]]): Ground truth claims.
        pred_dict (dict[str, list[Claim]]): Predicted claims.

    Returns:
        tuple[float, float, int]: Precision, recall, and the number of files evaluated.
    """
    print(f"- {RED}CLAIMS evaluation started:{RESET}")

    common_files = set(gt_dict.keys()).intersection(set(pred_dict.keys()))
    true_positives = 0
    false_positives = 0
    false_negatives = 0
    file_number = len(common_files)

    for file_name in common_files:
        gt_claims = {tuple(claim.specs) + (claim.measure, claim.outcome) for claim in gt_dict[file_name]}
        pred_claims = {tuple(claim.specs) + (claim.measure, claim.outcome) for claim in pred_dict[file_name]}

        # True Positives: Claims present in both ground truth and predictions
        true_positives += len(gt_claims & pred_claims)

        # False Positives: Claims present in predictions but not in ground truth
        false_positives += len(pred_claims - gt_claims)

        # False Negatives: Claims present in ground truth but not in predictions
        false_negatives += len(gt_claims - pred_claims)

    # Precision: TP / (TP + FP)
    precision = true_positives / (true_positives + false_positives) if (true_positives + false_positives) > 0 else 0

    # Recall: TP / (TP + FN)
    recall = true_positives / (true_positives + false_negatives) if (true_positives + false_negatives) > 0 else 0

    return precision, recall, file_number


def evaluate_specs(gt_dict: dict[str, list[Claim]], pred_dict: dict[str, list[Claim]]) -> tuple[float, float, int]:
    """
    Evaluates precision and recall for specifications using pre-extracted Claim objects.

    Args:
        gt_dict (dict[str, list[Claim]]): Ground truth claims.
        pred_dict (dict[str, list[Claim]]): Predicted claims.

    Returns:
        tuple[float, float, int]: Precision, recall, and the number of files evaluated.
    """
    print(f"- {RED}SPECS evaluation started:{RESET}")

    common_files = set(gt_dict.keys()).intersection(set(pred_dict.keys()))
    true_positives = 0
    false_positives = 0
    false_negatives = 0
    file_number = len(common_files)

    for file_name in common_files:
        # Extract specifications as sets of tuples
        gt_specs = {
            (name, value) for claim in gt_dict[file_name] for name, value in claim.specs
        }
        pred_specs = {
            (name, value) for claim in pred_dict[file_name] for name, value in claim.specs
        }

        # True Positives: Specifications present in both ground truth and predictions
        true_positives += len(gt_specs & pred_specs)

        # False Positives: Specifications present in predictions but not in ground truth
        false_positives += len(pred_specs - gt_specs)

        # False Negatives: Specifications present in ground truth but not in predictions
        false_negatives += len(gt_specs - pred_specs)

    # Precision: TP / (TP + FP)
    precision = true_positives / (true_positives + false_positives) if (true_positives + false_positives) > 0 else 0

    # Recall: TP / (TP + FN)
    recall = true_positives / (true_positives + false_negatives) if (true_positives + false_negatives) > 0 else 0

    return precision, recall, file_number

# for evaluation method 2
def calculate_metrics_with_threshold(
    gt_dict: dict[str, list[Claim]],
    pred_dict: dict[str, list[Claim]],
    threshold: float
) -> dict[str, float]:
    """
    Calculates claims and specifications metrics simultaneously.
    A claim is a true positive if the precision of its specifications is >= threshold.

    Args:
        gt_dict (dict[str, list[Claim]]): Ground truth claims.
        pred_dict (dict[str, list[Claim]]): Predicted claims.
        threshold (float): Precision threshold (0 to 1) for specifications.

    Returns:
        dict[str, float]: A dictionary containing precision, recall, and F1 for both claims and specifications.
    """
    spec_true_positives = 0
    spec_false_positives = 0
    spec_false_negatives = 0

    claim_true_positives = 0
    claim_false_positives = 0
    claim_false_negatives = 0

    # Process common files
    common_files = set(gt_dict.keys()).intersection(set(pred_dict.keys()))
    
    for file_name in common_files:
        gt_claims = gt_dict[file_name]
        pred_claims = pred_dict[file_name]

        gt_claims_matched = set()  # Track matched ground truth claims
        pred_claims_matched = set()  # Track matched predicted claims

        for pred_index, pred_claim in enumerate(pred_claims):
            pred_specs = set(pred_claim.specs)

            best_match_index = -1
            best_spec_precision = 0

            for gt_index, gt_claim in enumerate(gt_claims):
                if gt_index in gt_claims_matched:
                    continue

                gt_specs = set(gt_claim.specs)

                # Calculate TP, FP
                spec_tp = len(pred_specs & gt_specs)
                spec_fp = len(pred_specs - gt_specs)

                # Calculate precision for specifications
                spec_precision = spec_tp / (spec_tp + spec_fp) if (spec_tp + spec_fp) > 0 else 0

                # Track the best match
                if spec_precision > best_spec_precision:
                    best_spec_precision = spec_precision
                    best_match_index = gt_index

            # Check if this claim is a true positive based on the threshold
            if best_spec_precision >= threshold:
                claim_true_positives += 1
                gt_claims_matched.add(best_match_index)
                pred_claims_matched.add(pred_index)

                # Update specification metrics for true positive claims
                gt_specs = set(gt_claims[best_match_index].specs)
                spec_true_positives += len(pred_specs & gt_specs)
                spec_false_positives += len(pred_specs - gt_specs)
                spec_false_negatives += len(gt_specs - pred_specs)
            else:
                claim_false_positives += 1

        # Remaining unmatched ground truth claims are false negatives
        claim_false_negatives += len(gt_claims) - len(gt_claims_matched)

        # Remaining unmatched predicted claims are false positives
        claim_false_positives += len(pred_claims) - len(pred_claims_matched)

    # Calculate specifications metrics
    spec_precision = spec_true_positives / (spec_true_positives + spec_false_positives) if (spec_true_positives + spec_false_positives) > 0 else 0
    spec_recall = spec_true_positives / (spec_true_positives + spec_false_negatives) if (spec_true_positives + spec_false_negatives) > 0 else 0
    spec_f1 = (
        2 * spec_precision * spec_recall / (spec_precision + spec_recall)
        if (spec_precision + spec_recall) > 0
        else 0
    )

    # Calculate claims metrics
    claim_precision = claim_true_positives / (claim_true_positives + claim_false_positives) if (claim_true_positives + claim_false_positives) > 0 else 0
    claim_recall = claim_true_positives / (claim_true_positives + claim_false_negatives) if (claim_true_positives + claim_false_negatives) > 0 else 0
    claim_f1 = (
        2 * claim_precision * claim_recall / (claim_precision + claim_recall)
        if (claim_precision + claim_recall) > 0
        else 0
    )

    return {
        "spec_precision": spec_precision,
        "spec_recall": spec_recall,
        "spec_f1": spec_f1,
        "claim_precision": claim_precision,
        "claim_recall": claim_recall,
        "claim_f1": claim_f1,
    }