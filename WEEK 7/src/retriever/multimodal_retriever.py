# retriever/multimodal_retriever.py

from pathlib import Path
import os


from retriever.hybrid_retriever import HybridRetriever
from retriever.image_search import ImageRetriever
from retriever.image_to_text import ImageToTextRetriever


def is_image_path(x: str):
    if not isinstance(x, str):
        return False

    x = x.lower()

    return x.endswith((".png", ".jpg", ".jpeg", ".bmp", ".webp", ".tiff"))


class MultimodalRetriever:

    def __init__(
        self,
        image_vector_dir="vectorstore/image"
    ):
        """
        text store:
            HybridRetriever already uses fixed paths:
                vectorstore/index.faiss
                vectorstore/meta.pkl
        """

        print("Loading multimodal retriever ...")

        self.text_retriever = HybridRetriever()
        self.image_retriever = ImageRetriever(image_vector_dir)
        self.image_to_text = ImageToTextRetriever()

        print("Multimodal retriever ready.\n")

    # -----------------------------------------------------

    def search(self, query, top_k=5):
        """
        query:
            str  (text or image path)
        """

        if is_image_path(query):
            return self._search_image(query, top_k)

        return self._search_text(query, top_k)

    # -----------------------------------------------------

    def _search_text(self, query, top_k):

        results = []

        # ---------------- text -> text
        text_ids = self.text_retriever.search(query)

        for idx in text_ids[:top_k]:
            m = self.text_retriever.metadata[idx]

            results.append({
                "modality": "text",
                "score": None,
                "text": m.get("text"),
                "source_pdf": m.get("source_pdf"),
                "chunk_id": m.get("chunk_id")
            })

        # ---------------- text -> image
        img_hits = self.image_retriever.search_by_text(query, top_k=top_k)

        for h in img_hits:
            results.append({
                "modality": "image",
                "score": h.get("score"),
                "image_path": h.get("image_path"),
                "file": h.get("file")
            })

        return results

    # -----------------------------------------------------

    def _search_image(self, image_path, top_k):

        results = []

        # ---------------- image -> image
        img_hits = self.image_retriever.search_by_image(
            image_path,
            top_k=top_k
        )

        for h in img_hits:
            results.append({
                "modality": "image",
                "score": h.get("score"),
                "image_path": h.get("image_path"),
                "file": h.get("file")
            })

        # ---------------- image -> text
        text_hits = self.image_to_text.search(
            image_path,
            top_k=top_k
        )

        for m in text_hits:
            results.append({
                "modality": "text",
                "score": m.get("score"),
                "text": m.get("text"),
                "source_pdf": m.get("source_pdf"),
                "chunk_id": m.get("chunk_id")
            })

        return results


# ---------------------------------------------------------
# CLI
# ---------------------------------------------------------

def main():

    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--query", required=True)
    parser.add_argument("--top_k", type=int, default=5)
    parser.add_argument(
        "--image_vector_dir",
        default="vectorstore/image"
    )

    args = parser.parse_args()

    r = MultimodalRetriever(
        image_vector_dir=args.image_vector_dir
    )

    res = r.search(args.query, top_k=args.top_k)

    print("\nResults")
    print("=" * 60)

    for i, x in enumerate(res, 1):

        print(f"\n[{i}] modality:", x["modality"])

        if x["modality"] == "text":
            print("PDF   :", x.get("source_pdf"))
            print("Chunk :", x.get("chunk_id"))
            print("Text  :", (x.get("text") or "")[:400])

        else:
            print("Image :", x.get("image_path"))
            print("File  :", x.get("file"))
            print("Score :", x.get("score"))


if __name__ == "__main__":
    main()
