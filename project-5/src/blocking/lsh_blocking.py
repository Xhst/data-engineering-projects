import json
import pandas as pd
import re
from datasketch import MinHash, MinHashLSH
from nltk.tokenize import word_tokenize
from nltk.util import ngrams

def tokenize(text: str) -> set:
    # Define a set of common noise words
    noise_words = {
        "inc", "ltd", "llc", "corp", "corporation", "co", "company", "srl", "spa", "limited", "ou", "as", "firm",
        "group", "tbk", "hf", "gmbh", "ag", "plc", "pty", "nv", "sa", "bv", "ab", "aps", "oy", "kk", "kabushiki", 
        "ulc", "eeig", "sarl", "sas", "snc", "societa", "gesellschaft", "aktiengesellschaft", "trust", "holdings", 
        "associates", "partners", "enterprise", "enterprises", "ventures", "corporate", "business", "uc", "lp",
        "industries", "solutions", "services", "technologies", "systems", "international", "global", "studios",
        "regional", "private", "public", "joint stock company", "proprietary", "foundation", "chartered", "kaisha",
        "unlimited", "partnership", "llp", "pllc", "society", "incorporated", "vereniging", "foundation",
        "nonprofit", "enterprise limited", "enterprises limited", "kabushiki-gaisha", "financial"
    }   

    # Remove words between parenthesis
    text = re.sub(r"\(.*\)", "", text)

    # Replace dashes with spaces
    text = re.sub(r"[-_]", " ", text)

    # Convert to lowercase, remove unwanted characters
    text = re.sub(r"[^a-zA-Z0-9&\s]", "", text.lower())

    # Tokenize and filter out noise words
    tokens = [token for token in text.split() if token not in noise_words]
    text = ' '.join(tokens)

    tokens = word_tokenize(text)

    return tokens

datafile = "../schema_matching/mediated_schema/aggregated_sources.csv"

df = pd.read_csv(datafile, low_memory=False)

# Normalize data (convert text to lowercase and remove extra spaces)
df['company_name'] = df['company_name'].str.lower().str.strip()


# Initialize LSH with a similarity threshold and number of permutations
lsh = MinHashLSH(threshold=0.8, num_perm=128)

# Create MinHash for each record and add it to LSH
for i, record in df.iterrows():
    tokens = tokenize(str(record['company_name']))  # Choose the appropriate column
    minhash = MinHash(num_perm=128)
    for token in tokens:
        minhash.update(token.encode('utf8'))  # Update MinHash with each token
    lsh.insert(f"[{i}] {record['company_name']}", minhash)  # Use the record index as a unique key

# Perform blocking (query similar records for each record)
blocks = set()

for i, record in df.iterrows():
    tokens = tokenize(str(record['company_name']))
    minhash = MinHash(num_perm=128)
    for token in tokens:
        minhash.update(token.encode('utf8'))
    # Query LSH for candidates with similar MinHashes
    candidates = frozenset(lsh.query(minhash))

    blocks.add(candidates)

with open('./results/lsh_blocking.json', 'w') as f:
        json.dump([list(block) for block in blocks], f, indent=4)
