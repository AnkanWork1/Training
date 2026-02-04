# src/retriever/query_engine_clean.py
import os
import numpy as np
from transformers import AutoModel, AutoTokenizer
from pathlib import Path
import torch
import json
import joblib  # or import pickle

# ===== CONFIG =====
INDEX_PATH = Path("vectorstore/index.faiss")
METADATA_PATH = Path("vectorstore/meta.pkl")
MODEL_NAME = "BAAI/bge-small-en"
TOP_K = 5
MAX_TEXT_LENGTH = 500  # chars to show per chunk

# ===== Load metadata =====

if not os.path.exists(METADATA_PATH):
    raise FileNotFoundError(f"{METADATA_PATH} not found!")

with open(METADATA_PATH, "rb") as f:
    metadata = joblib.load(f)
   # or pickle.load(f)


# ===== Load FAISS index =====
import faiss
index = faiss.read_index(str(INDEX_PATH))
print(f"Loaded FAISS index from {INDEX_PATH}")
print(f"Index dimension: {index.d}")
print(f"Loaded {len(metadata)} metadata entries.")

# ===== Load BAAI embedding model =====
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModel.from_pretrained(MODEL_NAME)
model.eval()

device = "cuda" if torch.cuda.is_available() else "cpu"
model.to(device)

def embed_text(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=512).to(device)
    with torch.no_grad():
        outputs = model(**inputs)
    # Use mean pooling on last hidden state
    embeddings = outputs.last_hidden_state.mean(dim=1).cpu().numpy()
    return embeddings[0]

# ===== Query class =====
class Retriever:
    def __init__(self, index, metadata, top_k=TOP_K):
        self.index = index
        self.metadata = metadata
        self.top_k = top_k

    def search(self, query):
        emb = embed_text(query).astype("float32").reshape(1, -1)
        D, I = self.index.search(emb, self.top_k)
        results = []
        for score, idx in zip(D[0], I[0]):
            data = self.metadata[idx]
            text = data.get("text", "")
            # truncate text for readability
            text = (text[:MAX_TEXT_LENGTH] + "...") if len(text) > MAX_TEXT_LENGTH else text
            results.append({
                "score": float(score),
                "text": text,
                "pdf": data.get("source_pdf"),
                "images": data.get("image_paths", [])[:3],  # first 3 images
            })
        return results

# ===== MAIN =====# ===== MAIN =====
def main():
    r = Retriever(index, metadata)
    query = input("Query > ")
    hits = r.search(query)

    print("\nTop results:")
    print("-" * 60)
    for i, hit in enumerate(hits, 1):
        print(f"Rank : {i}")
        print(f"Score: {hit['score']:.4f}")
        print(f"Text : {hit['text']}")
        print(f"PDF  : {hit['pdf']}")
        print(f"Images: {hit['images']}")
        print("-" * 60)

    show_full = input("Show full text? (y/N) > ").strip().lower()
    if show_full == "y":
        print("\nFull texts of top hits:")
        print("-" * 60)
        for i, hit in enumerate(hits, 1):
            print(f"Rank : {i}")
            print(f"Full Text:\n{hit.get('full_text', hit['text'])}")
            print(f"PDF  : {hit['pdf']}")
            print(f"Images: {hit['images']}")
            print("-" * 60)


if __name__ == "__main__":
    main()
