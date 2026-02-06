from embeddings.multimodal_embedder import MultimodalEmbedder
from retriever.hybrid_retriever import HybridRetriever


class ImageToTextRetriever:

    def __init__(self):
        self.mm = MultimodalEmbedder()
        self.text_retriever = HybridRetriever()

    def search(self, image_path: str, top_k=5):

        # 1. generate caption from image
        caption = self.mm.generate_caption(image_path)

        # IMPORTANT:
        # do NOT dump full OCR here – it will hurt retrieval
        # (your HybridRetriever already does long-text matching well)
        query = caption.strip()

        # 2. retrieve text chunk ids
        ids = self.text_retriever.search(query)

        # 3. limit to top_k
        ids = ids[:top_k]

        # 4. return full metadata entries
        results = []
        for idx in ids:
            results.append(self.text_retriever.metadata[idx])

        return results
