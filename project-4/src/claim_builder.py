import json

import paths

# Funzione per analizzare una singola stringa
def parse_claim(claim_string, claim_index):
    # Rimuove il delimitatore iniziale e finale
    claim_string = claim_string.strip("|")
    
    # Divide specifiche e metrica
    specs_part, measure, outcome = claim_string.rsplit(", ", 2)
    
    # Elimina i delimitatori di specifiche
    specs_part = specs_part.strip("|{|").strip("|}")
    
    # Dividi le specifiche in coppie nome-valore
    specs = []
    for spec in specs_part.split(", |"):
        name, value = spec.split(", ")
        value = value.rstrip("|")
        specs.append({"name": name, "value": value})
    
    # Restituisce il dizionario per il claim corrente
    return {
        "Claim": str(claim_index),
        "Specifications": specs,
        "Measure": measure,
        "Outcome": outcome
    }

def build(input_data, paperId, tableId):
    # Costruzione dei dati
    claims_strings = [claim for claim in input_data.split("\n") if claim.strip()]
    claims = [parse_claim(claim, idx) for idx, claim in enumerate(claims_strings)]

    # Salvataggio in un file JSON
    output_file = paths.CLAIMS + "/" + paperId + "_" + tableId + "claims.json"
    with open(output_file, "w") as f:
        json.dump(claims, f, indent=4)

    print(f"\033[92mFile JSON salvato come {output_file}\033[0m")