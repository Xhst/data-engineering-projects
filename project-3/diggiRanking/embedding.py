import torch
import numpy as np

from transformers import AutoTokenizer, AutoModel
from sklearn.metrics.pairwise import cosine_similarity



# SciBERT is a pre-trained on a large corpus of scientific articles
# (biomedical, computer science and other scientific areas)

# Load pre-trained model
model_name = "allenai/scibert_scivocab_uncased"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name)

# Compute vector from sentence (embedding)
def get_sentence_embedding(sentence: str) -> np.ndarray:

    # Choose device
    device = assign_device("cuda")
    model = model.to(device)

    tokens = tokenizer(sentence, return_tensors="pt", padding=True, truncation=True, max_length=512)
    with torch.no_grad():
        outputs = model(**tokens)
    # Use average of embeddings (excluding special tokens like [CLS] and [SEP])
    embeddings = outputs.last_hidden_state
    mask = tokens['attention_mask'].unsqueeze(-1)
    masked_embeddings = embeddings * mask
    sentence_embedding = masked_embeddings.sum(dim=1) / mask.sum(dim=1)
    return sentence_embedding.squeeze().numpy()


def assign_device(device_name: str):
    """Assign the appropriate computing device for embeddings."""
    if device_name == "cuda" and torch.cuda.is_available():
        device = torch.device("cuda")
        print("Using GPU (CUDA).")
    elif device_name == "mps" and torch.backends.mps.is_available():
        device = torch.device("mps")
        print("Using Apple Silicon GPU (MPS).")
    else:
        device = torch.device("cpu")
        print("Using CPU.")
    return device