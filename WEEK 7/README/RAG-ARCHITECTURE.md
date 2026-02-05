# DAY 1 — LOCAL RAG SYSTEM + PIPELINE ARCHITECTURE

This single file contains **all required specifications for Day-1**:
architecture, concepts, folder structure, exercises, pipeline definition and
deliverables for a **fully local, terminal-first RAG system**.

---

## Learning Outcomes

- RAG architecture (Retriever → Generator)
- Local LLM loading and inference
- Embedding generation
- Document chunking strategies
- Semantic indexing (HNSW / IVF / Flat)

---

## Mandatory Folder Structure

src/
data/
raw/
cleaned/
chunks/
embeddings/

vectorstore/

retriever/
generator/
pipelines/
prompts/
models/
evaluation/
utils/
config/
logs/


---

## Topics to Learn

- RAG architecture fundamentals
- Chunk size vs. token limits
- Overlap strategy
- Embedding pipelines
- Metadata tagging
- Vector index structures

---

# 1. RAG Architecture Fundamentals

RAG (Retrieval-Augmented Generation) is composed of two main stages:

Retriever → Generator


High-level flow:



User Query
↓
Retriever (Vector Search)
↓
Top-K relevant chunks
↓
Prompt Builder
↓
Local LLM
↓
Final Answer


---

# 2. Local RAG Pipeline Architecture (End-to-End)


             ┌──────────────┐
             │  Raw Files   │
             │ PDF / TXT    │
             │ CSV / DOCX   │
             └──────┬───────┘
                    ↓
            ┌──────────────┐
            │ Loader        │
            │ + Cleaner     │
            └──────┬───────┘
                    ↓
            ┌──────────────┐
            │ Chunking      │
            │ 500–800 tok   │
            └──────┬───────┘
                    ↓
            ┌──────────────┐
            │ Metadata      │
            │ enrichment    │
            └──────┬───────┘
                    ↓
            ┌──────────────┐
            │ Embedder      │
            │ (local model) │
            └──────┬───────┘
                    ↓
            ┌──────────────┐
            │ Vector Store  │
            │ FAISS/Qdrant  │
            └──────┬───────┘
                    ↓


User Query ───▶ ┌──────────────┐
│ Retriever │
└──────┬───────┘
↓
┌──────────────┐
│ Prompt Build │
└──────┬───────┘
↓
┌──────────────┐
│ Local LLM │
└──────────────┘


This design is fully local and suitable for terminal-only usage.

---

# 3. Local LLM Loading and Inference

The generator module loads a local model (for example using:

- llama.cpp
- vLLM
- HuggingFace Transformers

Inference flow:



prompt → tokenizer → local LLM → generated tokens


No external API calls are used.

---

# 4. Document Ingestion & Cleaning

Supported input formats:

- PDF
- TXT
- CSV
- DOCX

Responsibilities:

- extract text
- normalize whitespace
- remove broken line breaks
- remove obvious headers and footers (best-effort)

Cleaned output:



src/data/cleaned/


---

# 5. Chunking Strategy

Documents are split using **token-based chunking**.

Target chunk size:



500–800 tokens


Chunks are written to:



src/data/chunks/


Each chunk contains:

- chunk text
- document id
- chunk id

---

# 6. Chunk Size vs Token Limits

## Token

A token is a sub-word unit produced by the tokenizer of:

- embedding model
- LLM

Tokens are not equal to words.

---

## Chunk

A chunk is a continuous segment of document text that is embedded as one unit.

---

## Why chunk size must consider token limits

Both:

- embedding models
- LLMs

have a maximum token limit.

If a chunk is too large:

- embeddings become less focused
- fewer chunks fit into the prompt context

If a chunk is too small:

- semantic meaning is lost

Hence:



500–800 tokens


is a practical balance.

---

# 7. Overlap Strategy

Chunks must overlap.

Example:



chunk_1 : tokens 0 – 700
chunk_2 : tokens 600 – 1300


Typical overlap:



50 – 150 tokens


Purpose:

- prevent cutting important sentences
- improve retrieval recall

---

# 8. Metadata Tagging

Each chunk must be enriched with metadata.

Mandatory fields:



{
"source": "file_name.pdf",
"page": 12,
"chunk_id": "file_name_p12_c03",
"tags": ["domain", "topic"]
}


Metadata is stored inside the vector database.

Benefits:

- filtering
- traceability
- debugging
- evaluation

---

# 9. Embedding Pipeline

Location:



/embeddings/embedder.py


Responsibilities:

- load a local embedding model
- batch encode chunks
- return dense vectors

Pipeline:
chunk text
→ tokenizer
→ embedding model
→ vector


Embeddings are stored in:



src/data/embeddings/


---

# 10. Vector Store Layer

Supported backends:

- FAISS (local file index)
- Qdrant (local service or embedded mode)

Stored object:



(vector, chunk_text, metadata)


Index location:



/vectorstore/index.faiss


---

# 11. Vector Index Structures

## Flat index

- brute-force nearest neighbor search
- highest accuracy
- slow for large datasets

---

## IVF (Inverted File Index)

- clusters vectors
- searches only selected clusters
- faster than Flat

---

## HNSW (Hierarchical Navigable Small World)

- graph-based approximate search
- very fast
- high recall
- commonly used in production

---

# 12. Retriever Module

Location:



/retriever/query_engine.py


Responsibilities:



user query
→ embed query
→ vector similarity search
→ top-k chunks
→ return text + metadata


---

# 13. Generator Module

Location:



/generator/


Responsibilities:

- receive retrieved chunks
- build final prompt
- run local LLM inference
- return answer

---

# 14. Prompt Templates

Location:



/prompts/


Prompt must contain:

- system instruction
- retrieved context
- user question

---

# 15. Ingestion & Chunking Pipeline

Location:



/pipelines/ingest.py


Mandatory pipeline order:



load_documents()
→ clean_text()
→ split_into_chunks(500–800 tokens, overlap)
→ attach_metadata()
→ generate_embeddings()
→ store_vectors()


---

# 16. Exercise (Day-1)

Build a local ingestion and chunking pipeline.

The pipeline must:

- load PDFs, TXT, CSV, DOCX
- clean text
- split into 500–800 token chunks
- add metadata (source, page number, tags)
- generate embeddings locally
- store vectors in FAISS or Qdrant
- build a retriever module

---

# 17. Validation Checklist

- ✔ Documents loaded
- ✔ Chunks created
- ✔ Embeddings generated
- ✔ Vector DB initialized

---

# 18. Mandatory Deliverables



/pipelines/ingest.py
/embeddings/embedder.py
/vectorstore/index.faiss
/retriever/query_engine.py
RAG-ARCHITECTURE.md (this file)