import json
import paths


def parse_claim(claim_string, claim_index):
    claim_string = claim_string.strip("|")
    
    if claim_string.strip().endswith("|}"):

        specs_part = claim_string
        measure = "-"
        outcome = "-"
    else:
        # La stringa contiene metric e value
        specs_part, measure, outcome = claim_string.rsplit(", ", 2)
    
    
    specs_part = specs_part.strip("|{|").strip("|}")
    
    specs = []
    for spec in specs_part.split(", |"):
        name, value = spec.split(", ", 1)
        value = value.rstrip("|")
        specs.append({"name": name, "value": value})

    return {
        str(claim_index): {
            "specifications": {
                str(i): spec
                for i, spec in enumerate(specs)
            },
            "Measure": measure,
            "Outcome": outcome
        }
    }

'''    
    return {
        "Claim": str(claim_index),
        "Specifications": specs,
        "Measure": measure,
        "Outcome": outcome
    }
'''

def build(input_data, paperId, tableId, output_dir):

    claims_strings = [claim for claim in input_data.split("\n") if claim.strip()]
    claims = [parse_claim(claim, idx) for idx, claim in enumerate(claims_strings)]

    output_file = output_dir + "/" + paperId + "_" + tableId + "_claims.json"
    with open(output_file, "w") as f:
        json.dump(claims, f, indent=4)

    print(f"\033[32mFile JSON saved as {output_file}\033[0m")
    
if __name__ == "__main__":
    # helper sugo, dw about it
    with open(paths.LLM_RESPONSE + "/2206.10526_S3.T1_llmResponse.txt", "r") as file:
        content = file.read()
        
        build(content, "2206.10526", "1", paths.GROUND_TRUTH.CLAIMS.value)  # ===> mi rifiuto di farla...