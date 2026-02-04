from langchain.text_splitter import RecursiveCharacterTextSplitter

def chunk_documents(docs, chunk_size=800, chunk_overlap=120):
    """
    Split each document into token-aware chunks.
    Returns list of chunks with metadata.
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )

    all_chunks = []

    for d in docs:
        chunks = splitter.split_text(d["text"])
        for i, c in enumerate(chunks):
            all_chunks.append({
                "text": c,
                "metadata": {
                    **d["metadata"],
                    "chunk_id": i
                }
            })

    return all_chunks
