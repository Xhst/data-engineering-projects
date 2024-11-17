import torch


from transformers import AutoTokenizer, AutoModel
from sklearn.metrics.pairwise import cosine_similarity


# Load pre-trained model
model_name = "bert-base-uncased"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name)

# Compute vector from sentence (embedding)
def get_sentence_embedding(sentence):
    tokens = tokenizer(sentence, return_tensors="pt", padding=True, truncation=True, max_length=512)
    with torch.no_grad():
        outputs = model(**tokens)
    # Use average of embeddings (excluding special tokens like [CLS] and [SEP])
    embeddings = outputs.last_hidden_state
    mask = tokens['attention_mask'].unsqueeze(-1)
    masked_embeddings = embeddings * mask
    sentence_embedding = masked_embeddings.sum(dim=1) / mask.sum(dim=1)
    return sentence_embedding.squeeze().numpy()
