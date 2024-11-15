import argparse
import os
import json
import time
from transformers import AutoTokenizer, AutoModel
import torch
import asyncio
import websockets

# Initialize the model and tokenizer
model_name = "distilbert-base-uncased"  # Consider alternatives like 'all-MiniLM-L6-v2' for better sentence embeddings
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name)


def embed_text(text, device):
    """Embed the given text using a pre-trained transformer model."""
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True).to(device)
    model.to(device)
    with torch.no_grad():
        outputs = model(**inputs)
    # Use the mean of the token embeddings as the sentence embedding
    embedding = outputs.last_hidden_state.mean(dim=1).squeeze().cpu().numpy()
    # Convert the embedding to a list
    embedding_list = embedding.tolist()
    return embedding_list


def assign_device(device_name):
    """Assign the appropriate computing device."""
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


async def handle_connection(websocket, device):
    """Handle incoming WebSocket connections for embedding requests."""
    async for message in websocket:
        request = json.loads(message)
        method = request.get("method")
        data = request.get("data")

        if method == "embed_metric":
            # Embedding for a metric string
            if not isinstance(data, str):
                response = {"status": "error", "message": "Data must be a single string for 'embed_metric'."}
            else:
                embedding = embed_text(data, device)
                response = {"status": "success", "embedding": embedding}

        elif method == "embed_table_data":
            # Embedding for a list of table strings
            if not isinstance(data, list):
                response = {"status": "error", "message": "Data must be a list of strings for 'embed_table_data'."}
            else:
                embeddings = {f"table_{i}": embed_text(table, device) for i, table in enumerate(data)}
                response = {"status": "success", "embeddings": embeddings}

        else:
            response = {"status": "error", "message": "Unsupported method. Use 'embed_metric' or 'embed_table_data'."}

        await websocket.send(json.dumps(response))


async def main_websocket_server(device, host, port):
    """Start the WebSocket server."""
    print(f"Starting WebSocket server on ws://{host}:{port}")
    async with websockets.serve(lambda ws, p: handle_connection(ws, p, device), host, port):
        await asyncio.Future()  # Run foreverq


def main():
    # Set up argument parsing
    parser = argparse.ArgumentParser(description="Start a WebSocket server for text embedding.")
    parser.add_argument("--device", type=str, choices=["cpu", "cuda", "mps"], default="cpu",
                        help="Computing device to use (cpu, cuda, or mps)")
    
    args = parser.parse_args()

    # Assign the device
    device = assign_device(args.device)

    # Start the WebSocket server
    asyncio.run(main_websocket_server(device, host="127.0.0.1", port="3001"))


if __name__ == "__main__":
    main()

