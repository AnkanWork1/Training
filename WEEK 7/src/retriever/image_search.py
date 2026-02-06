from pathlib import Path
import faiss
import joblib
import numpy as np

from embeddings.clip_embedder import CLIPEmbedder


class ImageRetriever:

    def __init__(self, vector_dir: str, device=None):

        self.vector_dir = Path(vector_dir)
        self.index_path = self.vector_dir / "index.faiss"
        self.meta_path = self.vector_dir / "meta.pkl"

        if not self.index_path.exists():
            raise RuntimeError("index.faiss not found")

        if not self.meta_path.exists():
            raise RuntimeError("meta.pkl not found")

        self.index = faiss.read_index(str(self.index_path))
        self.metas = joblib.load(self.meta_path)

        self.embedder = CLIPEmbedder(device=device)

    def search_by_text(self, query: str, top_k=5):

        q = self.embedder.embed_text(query)
        q = np.atleast_2d(q).astype("float32")

        scores, ids = self.index.search(q, top_k)

        results = []
        for rank, idx in enumerate(ids[0]):
            if idx == -1:
                continue

            m = self.metas[idx]

            results.append({
                "score": float(scores[0][rank]),
                "file": m.get("file"),
                "image_path": m.get("image_path")
            })

        return results

    def search_by_image(self, image_path: str, top_k=5):

        q = self.embedder.embed_image(image_path)
        q = np.atleast_2d(q).astype("float32")

        scores, ids = self.index.search(q, top_k)

        results = []
        for rank, idx in enumerate(ids[0]):
            if idx == -1:
                continue

            m = self.metas[idx]

            results.append({
                "score": float(scores[0][rank]),
                "file": m.get("file"),
                "image_path": m.get("image_path")
            })

        return results
