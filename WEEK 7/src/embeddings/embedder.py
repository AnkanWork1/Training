# embeddings/embedder.py
from sentence_transformers import SentenceTransformer

class LocalEmbedder:
    def __init__(self, model_name="BAAI/bge-small-en"):  # Example: BGE-small
        """
        Local text embeddings using Hugging Face SentenceTransformer
        Default: BGE-small
        """
        self.model = SentenceTransformer(model_name)

    def embed(self, texts):
        """
        Embed a list of texts
        """
        embeddings = self.model.encode(texts, show_progress_bar=True, batch_size=64)
        return embeddings
