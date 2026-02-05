from retriever.hybrid_retriever import HybridRetriever
from pipelines.context_builder import build_context
import joblib

META_PATH = "vectorstore/meta.pkl"


def main():

    r = HybridRetriever()

    query = input("Query > ")

    # example filters
    filters = {}

    ids = r.search(query, filters=filters)

    with open(META_PATH, "rb") as f:
        metadata = joblib.load(f)

    context = build_context(metadata, ids)

    print("\nFinal context (traceable):")
    print("-" * 60)

    for c in context:
        print("Rank:", c["rank"])
        print("PDF :", c["source_pdf"])
        print("Chunk:", c["chunk_id"])
        print("Text :", c["text"][:400])
        print("-" * 60)


if __name__ == "__main__":
    main()
