import json
import pandas as pd
import re
from datasketch import MinHash, MinHashLSH
from nltk.tokenize import word_tokenize
from unidecode import unidecode


def remove_noise_words(text: str) -> str:
    # Define a set of common noise words
    noise_words = {
        "inc", "ltd", "llc", "corp", "corporation", "co", "company", "srl", "spa", "limited", "ou", "as", "firm",
        "group", "tbk", "hf", "gmbh", "ag", "plc", "pty", "nv", "sa", "saa", "bv", "ab", "aps", "oy", "kk", "kabushiki", 
        "ulc", "eeig", "sarl", "sas", "snc", "societa", "gesellschaft", "aktiengesellschaft", "trust", "holdings", "llp",
        "associates", "partners", "enterprise", "enterprises", "ventures", "corporate", "uc", "lp", "constructions",
        "industries", "solutions", "services", "technologies", "systems", "global", "studios", "construction", "pllc",
        "regional", "private", "public", "joint stock company", "proprietary", "foundation", "chartered", "kaisha",
        "unlimited", "partnership", "society", "incorporated", "vereniging", "foundation", "grupo",  "technology",
        "nonprofit", "kabushiki", "gaisha", "financial", "gayrimenkul", "yatirim", "ortakligi", "gyo", "gruppo", "groupe",
        "gruppen", "holdings", "holding", "finance", "finances", "careers", "consultants", "consult", "consults"
    }   

    # Split the text into tokens and remove noise words
    tokens = [token for token in text.split() if token not in noise_words]

    # Return the filtered text
    return ' '.join(tokens)


def split_pascal_case(text):
    """
    Splits a PascalCase string into separate words.
    
    Args:
    text (str): The PascalCase string to split.
    
    Returns:
    str: The string with words separated by spaces.
    """
    return re.sub(r'(?<!^)(?<![A-Z])(?=[A-Z])', ' ', text)


def get_acronym(record: pd.Series) -> str:
    text = str(record['company_name'])
    text = clean_text(text)
    tokens = text.split()

    first_letters = [token[0] for token in tokens]
    acronym = "".join(first_letters)

    return acronym


def clean_text(text: str) -> str:
    # Remove words between parenthesis
    text = re.sub(r"\(.*\)", "", text)

    # Replace dashes with spaces
    text = re.sub(r"[-_]", " ", text)

    # Split pascal case
    text = split_pascal_case(text)

    # Remove accents and special characters
    text = unidecode(text)

    # Convert to lowercase, remove extra spaces and punctuation
    text = re.sub(r"[^a-zA-Z0-9&\s]", "", text.lower().strip())

    # Remove words that are usally not relevant for matching
    text = remove_noise_words(text)

    return text
    
def tokenize(record: pd.Series) -> set[str]:
    text = str(record['company_name'])

    text = clean_text(text)

    tokens = word_tokenize(text)

    return tokens

def bigram_tokenize(record: pd.Series) -> set[str]:
    text = str(record['company_name'])

    text = clean_text(text)

    tokens = set()
    for i in range(len(text) - 1):
        tokens.add(text[i:i+2])

    return tokens


def lsh_blocking(df: pd.DataFrame, outputfile: str, threshold=0.75, num_perm=128, tokenizer=tokenize, use_acronym=False):
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
        
        query = lsh.query(minhash)

        if use_acronym:
            acronym = get_acronym(record)

            minhash_acronym = MinHash(num_perm=num_perm)
            minhash_acronym.update(acronym.encode('utf8'))
            
            acronym_query = lsh.query(minhash_acronym)

            query += acronym_query
        
        # Query LSH for candidates with similar MinHashes
        candidates = frozenset(query)
        blocks.add(candidates)

    with open(outputfile, 'w') as f:
        json.dump([list(block) for block in blocks], f, indent=4)
    
    print(f"Blocking completed, results written on {outputfile}")


if __name__ == "__main__":
    datafile = "../schema_matching/mediated_schema/aggregated_sources.csv"

    df = pd.read_csv(datafile, low_memory=False)
    
    lsh_blocking(df, "./results/lsh_words_blocking.json")
    lsh_blocking(df, "./results/lsh_bigram_blocking.json", tokenizer=bigram_tokenize)
    lsh_blocking(df, "./results/lsh_words_aq_blocking_.json", use_acronym=True)
    lsh_blocking(df, "./results/lsh_bigram_aq_blocking.json", tokenizer=bigram_tokenize, use_acronym=True)



