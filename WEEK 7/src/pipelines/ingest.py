from pathlib import Path
import yaml
import json
import numpy as np
from utils.md_loader import load_enterprise_markdown
from utils.chunker import chunk_documents
from embeddings.embedder import LocalEmbedder
from vectorstore.faiss_store import FaissStore

# ----------------------------
# Paths
# ----------------------------
ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / "data/raw/archive(1)/EnterpriseRAG_2025_02_markdown"
VECTOR_DIR = ROOT / "vectorstore"
CHUNKS_PATH = ROOT / "data/chunks/chunks.json"
EMBED_PATH = ROOT / "data/chunks/embeddings.npy"
META_PATH = ROOT / "data/chunks/metas.json"

# ----------------------------
# Main function
# ----------------------------
def main():
    # Load config
    cfg_path = ROOT / "config/model.yaml"
    if cfg_path.exists():
        cfg = yaml.safe_load(cfg_path.read_text())
        print(f"Loaded config from {cfg_path}")
    else:
        cfg = {"embedding_model": "BAAI/bge-small-en"}  # default
        print("Config not found. Using default embedding model.")

    # ----------------------------
    # Load or create chunks
    # ----------------------------
    if CHUNKS_PATH.exists():
        print(f"Loading chunks from {CHUNKS_PATH} ...")
        with open(CHUNKS_PATH, "r", encoding="utf-8") as f:
            chunks = json.load(f)
        print(f"Loaded {len(chunks)} chunks from disk.")
    else:
        print("No stored chunks found. Creating chunks from documents ...")
        docs = load_enterprise_markdown(RAW_DIR)
        print(f"Loaded {len(docs)} documents.")

        chunks = chunk_documents(docs)
        print(f"Total chunks created: {len(chunks)}")

        # Ensure folder exists
        CHUNKS_PATH.parent.mkdir(parents=True, exist_ok=True)
        # Save chunks
        with open(CHUNKS_PATH, "w", encoding="utf-8") as f:
            json.dump(chunks, f, ensure_ascii=False, indent=2)
        print(f"Chunks saved to {CHUNKS_PATH}")

    # ----------------------------
    # Prepare texts and metadata
    # ----------------------------
    texts = [c["text"] for c in chunks]  # only first 1000 for testing
    metas = [{"text": c["text"], **c["metadata"]} for c in chunks]


    # ----------------------------
    # Generate embeddings
    # ----------------------------
    embedder = LocalEmbedder(model_name=cfg.get("embedding_model", "BAAI/bge-small-en"))
    batch_size = 500
    all_embeddings = []

    for i in range(0, len(texts), batch_size):
        batch_texts = texts[i:i + batch_size]
        print(f"Embedding batch {i} to {i + len(batch_texts)} ...")
        batch_embeddings = embedder.embed(batch_texts)
        all_embeddings.extend(batch_embeddings)

    all_embeddings = np.array(all_embeddings)
    print(f"Embeddings generated. Shape: {all_embeddings.shape}")

    # ----------------------------
    # Save embeddings and metadata
    # ----------------------------
    np.save(EMBED_PATH, all_embeddings)
    print(f"Embeddings saved to {EMBED_PATH}")

    with open(META_PATH, "w", encoding="utf-8") as f:
        json.dump(metas, f, ensure_ascii=False, indent=2)
    print(f"Metadata saved to {META_PATH}")

    # ----------------------------
    # Store in FAISS
    # ----------------------------
    store = FaissStore(dim=all_embeddings.shape[1])
    store.add(all_embeddings, metas)
    store.save(VECTOR_DIR)
    print(f"Vector store saved at {VECTOR_DIR}")

# ----------------------------
# Entry point
# ----------------------------
if __name__ == "__main__":
    main()
