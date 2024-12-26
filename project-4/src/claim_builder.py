import json
import paths


def parse_claim(claim_string, claim_index):
    claim_string = claim_string.strip("|")
    
    specs_part, measure, outcome = claim_string.rsplit(", ", 2)
    
    specs_part = specs_part.strip("|{|").strip("|}")
    
    specs = []
    for spec in specs_part.split(", |"):
        name, value = spec.split(", ")
        value = value.rstrip("|")
        specs.append({"name": name, "value": value})
    
    return {
        "Claim": str(claim_index),
        "Specifications": specs,
        "Measure": measure,
        "Outcome": outcome
    }

def build(input_data, paperId, tableId):

    claims_strings = [claim for claim in input_data.split("\n") if claim.strip()]
    claims = [parse_claim(claim, idx) for idx, claim in enumerate(claims_strings)]

    output_file = paths.CLAIMS + "/" + paperId + "_" + tableId + "claims.json"
    with open(output_file, "w") as f:
        json.dump(claims, f, indent=4)

    print(f"\033[32mFile JSON saved as {output_file}\033[0m")