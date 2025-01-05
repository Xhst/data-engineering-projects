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
        # Extract claims as sets of tuples ((spec1, value1), ... , (measure, outcome))
        gt_claims = {tuple(claim.specs) + ((claim.measure, claim.outcome),) for claim in gt_dict[file_name]}
        pred_claims = {tuple(claim.specs) + ((claim.measure, claim.outcome),) for claim in pred_dict[file_name]}

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


def evaluate_claims_parts(gt_dict: dict[str, list[Claim]], pred_dict: dict[str, list[Claim]]) -> tuple[float, float, int]:
    """
    Evaluates precision and recall for specifications using pre-extracted Claim objects.

    Args:
        gt_dict (dict[str, list[Claim]]): Ground truth claims.
        pred_dict (dict[str, list[Claim]]): Predicted claims.

    Returns:
        tuple[float, float, int]: Precision, recall, and the number of files evaluated.
    """
    print(f"- {RED}CLAIMS PARTS evaluation started:{RESET}")

    common_files = set(gt_dict.keys()).intersection(set(pred_dict.keys()))
    true_positives = 0
    false_positives = 0
    false_negatives = 0
    file_number = len(common_files)

    for file_name in common_files:
        # Extract claims parts as sets of tuples ((claim1_spec1, claim1_value1), ... , (measure1, outcome1), (claim2_spec1, claim2_value1), ... , (measure2, outcome2))
        gt_specs = {
            (name, value) for claim in gt_dict[file_name] for name, value in (claim.specs + [(claim.measure, claim.outcome)])
        }
        pred_specs = {
            (name, value) for claim in pred_dict[file_name] for name, value in (claim.specs + [(claim.measure, claim.outcome)])
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