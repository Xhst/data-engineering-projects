import torch
import numpy as np
from sentence_transformers import SentenceTransformer


class Embedder:
    def __init__(self, model_name: str = "paraphrase-MPNet-base-v2"):
        self.model_name = model_name
        self.model = SentenceTransformer(self.model_name)
        self.device = self.assign_device("cpu")
        self.model = self.model.to(self.device)
        self.embedding_size = self.model.get_sentence_embedding_dimension()


    def get_sentence_embedding(self, sentence: str) -> np.ndarray:
        return self.model.encode(sentence)
    

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