import torch
import numpy as np
from transformers import AutoTokenizer, AutoModel


class Embedder:
    def __init__(self, model_name: str = "bert-base-uncased"):
        self.model_name = model_name
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModel.from_pretrained(self.model_name)
        self.device = self.assign_device("cuda")
        self.model = self.model.to(self.device)


    def get_sentence_embedding(self, sentence: str) -> np.ndarray:
        tokens = self.tokenizer(sentence, return_tensors="pt", padding=True, truncation=True, max_length=512)
        tokens = {key: val.to(self.device) for key, val in tokens.items()}
        
        with torch.no_grad():
            outputs = self.model(**tokens)
        
        embeddings = outputs.last_hidden_state
        mask = tokens['attention_mask'].unsqueeze(-1)
        masked_embeddings = embeddings * mask
        sentence_embedding = masked_embeddings.sum(dim=1) / mask.sum(dim=1)
        
        return sentence_embedding.squeeze().cpu().numpy()
    

    def assign_device(self, device_name: str):
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