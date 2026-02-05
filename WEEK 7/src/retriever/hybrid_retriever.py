import faiss
import joblib
import numpy as np
from pathlib import Path
from rank_bm25 import BM25Okapi

from transformers import AutoTokenizer, AutoModel
import torch

from retriever.reranker import CrossEncoderReranker


# ----------------------------
# Config
# ----------------------------
INDEX_PATH = Path("vectorstore/index.faiss")
META_PATH = Path("vectorstore/meta.pkl")

EMBED_MODEL = "BAAI/bge-small-en"

TOP_K = 5
FAISS_CANDIDATES = 50
BM25_CANDIDATES = 50


# ----------------------------
# Embedding model (same as ingest)
# ----------------------------
class Embedder:

    def __init__(self, model_name):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"

        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModel.from_pretrained(model_name).to(self.device)
        self.model.eval()

    def embed(self, text):
        inputs = self.tokenizer(
            text,
            return_tensors="pt",
            truncation=True,
            max_length=512
        ).to(self.device)

        with torch.no_grad():
            out = self.model(**inputs)

        emb = out.last_hidden_state.mean(dim=1)
        return emb.cpu().numpy().astype("float32")[0]


# ----------------------------
# MMR
# ----------------------------
def mmr(query_emb, doc_embs, lambda_mult=0.5, k=5):
    selected = []
    candidates = list(range(len(doc_embs)))

    def cos(a, b):
        return np.dot(a, b) / (
            np.linalg.norm(a) * np.linalg.norm(b) + 1e-9
        )

    while len(selected) < k and candidates:
        best = None
        best_score = -1e9

        for idx in candidates:
            sim_to_query = cos(query_emb, doc_embs[idx])

            if not selected:
                score = sim_to_query
            else:
                sim_to_selected = max(
                    cos(doc_embs[idx], doc_embs[j]) for j in selected
                )
                score = lambda_mult * sim_to_query - (1 - lambda_mult) * sim_to_selected

            if score > best_score:
                best_score = score
                best = idx

        selected.append(best)
        candidates.remove(best)

    return selected


# ----------------------------
# Hybrid Retriever
# ----------------------------
class HybridRetriever:

    def __init__(self):

        self.index = faiss.read_index(str(INDEX_PATH))

        with open(META_PATH, "rb") as f:
            self.metadata = joblib.load(f)

        print("Loaded FAISS + metadata")

        self.embedder = Embedder(EMBED_MODEL)
        self.reranker = CrossEncoderReranker()

        # ---- build BM25 index
        print("Building BM25 index ...")
        tokenized = [
            m["text"].lower().split()
            for m in self.metadata
        ]

        self.bm25 = BM25Okapi(tokenized)

    # ----------------------------------

    def search(self, query, filters=None):

        if filters is None:
            filters = {}

        # -------- semantic search
        q_emb = self.embedder.embed(query)

        D, I = self.index.search(
            np.array([q_emb]), FAISS_CANDIDATES
        )

        faiss_ids = I[0].tolist()

        # -------- bm25
        bm25_scores = self.bm25.get_scores(query.lower().split())
        bm25_ids = np.argsort(bm25_scores)[::-1][:BM25_CANDIDATES].tolist()

        # -------- merge
        merged = []
        seen = set()

        for i in faiss_ids + bm25_ids:
            if i not in seen:
                merged.append(i)
                seen.add(i)

        # -------- filters (simple metadata filter)
        filtered = []
        for idx in merged:
            meta = self.metadata[idx]

            ok = True
            for k, v in filters.items():
                if meta.get(k) != v:
                    ok = False
                    break

            if ok:
                filtered.append(idx)

        # -------- rerank
        texts = [self.metadata[i]["text"] for i in filtered]

        if len(texts) == 0:
            return []

        scores = self.reranker.rerank(query, texts)

        ranked = list(zip(filtered, scores))
        ranked.sort(key=lambda x: x[1], reverse=True)

        ranked_ids = [x[0] for x in ranked]

        # -------- MMR (diversity)
        doc_embs = []
        for i in ranked_ids:
            doc_embs.append(self.embedder.embed(self.metadata[i]["text"]))

        doc_embs = np.array(doc_embs)

        mmr_ids = mmr(q_emb, doc_embs, k=min(TOP_K, len(ranked_ids)))

        final = [ranked_ids[i] for i in mmr_ids]

        return final

# ----------------------------
# CLI
# ----------------------------
def main():

    retriever = HybridRetriever()

    print("\nHybrid Retriever ready.")
    print("Type a query and press enter.\n")

    while True:
        q = input("Query > ").strip()

        if q.lower() in ["exit", "quit"]:
            break

        results = retriever.search(q)

        print("\nTop results:")
        print("-" * 60)

        for rank, idx in enumerate(results, 1):
            meta = retriever.metadata[idx]

            text = meta["text"]
            text = text[:400] + "..." if len(text) > 400 else text

            print(f"Rank : {rank}")
            print(f"Text : {text}")
            print(f"PDF  : {meta.get('source_pdf')}")
            print(f"Chunk: {meta.get('chunk_id')}")
            print("-" * 60)


if __name__ == "__main__":
    main()
