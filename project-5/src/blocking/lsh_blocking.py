import json
import pandas as pd
import re
from datasketch import MinHash, MinHashLSH
from nltk.tokenize import word_tokenize


def remove_noise_words(text: str) -> str:
     # Define a set of common noise words
    noise_words = {
        "inc", "ltd", "llc", "corp", "corporation", "co", "company", "srl", "spa", "limited", "ou", "as", "firm",
        "group", "tbk", "hf", "gmbh", "ag", "plc", "pty", "nv", "sa", "bv", "ab", "aps", "oy", "kk", "kabushiki", 
        "ulc", "eeig", "sarl", "sas", "snc", "societa", "gesellschaft", "aktiengesellschaft", "trust", "holdings", 
        "associates", "partners", "enterprise", "enterprises", "ventures", "corporate", "business", "uc", "lp",
        "industries", "solutions", "services", "technologies", "systems", "international", "global", "studios",
        "regional", "private", "public", "joint stock company", "proprietary", "foundation", "chartered", "kaisha",
        "unlimited", "partnership", "llp", "pllc", "society", "incorporated", "vereniging", "foundation",
        "nonprofit", "kabushiki-gaisha", "financial"
    }   

    # Split the text into tokens and remove noise words
    tokens = [token for token in text.split() if token not in noise_words]

    # Return the filtered text
    return ' '.join(tokens)

    
def tokenize(record: pd.Series) -> set:
    text = str(record['company_name'])

    # Remove words between parenthesis
    text = re.sub(r"\(.*\)", "", text)

    # Replace dashes with spaces
    text = re.sub(r"[-_]", " ", text)

    # Convert to lowercase, remove unwanted characters
    text = re.sub(r"[^a-zA-Z0-9&\s]", "", text.lower().strip())

    text = remove_noise_words(text)

    tokens = word_tokenize(text)

    return tokens


def lsh_blocking(df: pd.DataFrame, outputfile: str, threshold=0.8, num_perm=128, tokenizer=tokenize):
    # Initialize LSH with a similarity threshold and number of permutations
    lsh = MinHashLSH(threshold=threshold, num_perm=num_perm)

    # Create MinHash for each record and add it to LSH
    for i, record in df.iterrows():
        tokens = tokenizer(record)  
        minhash = MinHash(num_perm=num_perm)
        for token in tokens:
            minhash.update(token.encode('utf8'))  
        lsh.insert(f"[{i}] {record['company_name']}", minhash)  # Use the record index as a unique key

    # Perform blocking (query similar records for each record)
    blocks = set()
    for i, record in df.iterrows():
        tokens = tokenizer(record)
        minhash = MinHash(num_perm=num_perm)
        for token in tokens:
            minhash.update(token.encode('utf8'))
        # Query LSH for candidates with similar MinHashes
        candidates = frozenset(lsh.query(minhash))
        blocks.add(candidates)

    with open(outputfile, 'w') as f:
        json.dump([list(block) for block in blocks], f, indent=4)


if __name__ == "__main__":
    datafile = "../schema_matching/mediated_schema/aggregated_sources.csv"
    outputfile = "./results/lsh_blocking.json"

    df = pd.read_csv(datafile, low_memory=False)
    lsh_blocking(df, outputfile)



