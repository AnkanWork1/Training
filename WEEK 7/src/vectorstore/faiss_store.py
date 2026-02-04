import faiss
import numpy as np
import pickle
from pathlib import Path

class FaissStore:

    def __init__(self, dim: int):
        self.index = faiss.IndexFlatL2(dim)
        self.metadatas = []

    def add(self, vectors, metadatas):
        vecs = np.array(vectors).astype("float32")
        self.index.add(vecs)
        self.metadatas.extend(metadatas)

    def save(self, path: Path):
        path.mkdir(parents=True, exist_ok=True)
        faiss.write_index(self.index, str(path / "index.faiss"))
        with open(path / "meta.pkl", "wb") as f:
            pickle.dump(self.metadatas, f)

    @staticmethod
    def load(path: Path):
        store = FaissStore(1)
        store.index = faiss.read_index(str(path / "index.faiss"))
        with open(path / "meta.pkl", "rb") as f:
            store.metadatas = pickle.load(f)
        return store
