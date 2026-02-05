# Day 2 — Advanced Retrieval & Context Engineering

This document describes the complete flow, design decisions, and components required to complete **Day 2 – Advanced Retrieval + Context Engineering** for the Enterprise RAG system.

It also explicitly answers the questions that came up during implementation.

---

## Target capability

Query example:

```
query = "Explain how credit underwriting works"
filters = {"year": "2024", "type": "policy"}
top_k = 5
```

System must support:

* Hybrid retrieval (semantic + keyword)
* Reranking
* Deduplication
* MMR (diversity)
* Traceable context
* Context window optimization

---

## High‑level pipeline

```
User query
   ↓
Bi‑encoder embedding (BAAI/bge-small-en)
   ↓
FAISS semantic search
   ↓
BM25 keyword search (fallback)
   ↓
Merge candidate IDs
   ↓
Metadata filters
   ↓
Deduplication
   ↓
Cross‑encoder reranker
   ↓
MMR (diversity selection)
   ↓
Context builder
   ↓
LLM
```

---

## Why this pipeline exists

* Semantic retrieval alone misses exact terms.
* Keyword retrieval alone misses semantic meaning.
* Reranking fixes approximate retrieval.
* MMR avoids repeated / near‑duplicate chunks.
* Context builder ensures traceability and context size control.

---

## Component breakdown

---

### 1. Bi‑encoder retrieval (semantic)

Used model:

```
BAAI/bge-small-en
```

Role:

* Encodes query and chunks independently
* Uses FAISS for nearest neighbour search

Why:

* Fast
* Embeddings can be precomputed

Used for:

* First stage candidate retrieval

---

### 2. Keyword fallback (BM25)

BM25 is used as keyword fallback.

Important:
BM25 does NOT use embeddings.

BM25 works on:

* tokenized chunk texts

You must build a separate BM25 index over chunk texts.

Used when:

* query contains exact terms
* rare words
* codes, names, document identifiers

---

### 3. Hybrid retrieval

Candidates are collected from:

* FAISS results (semantic)
* BM25 results (keyword)

Then merged and deduplicated.

This increases recall.

---

### 4. Filtering

After merging, apply metadata filters:

Example:

```
{"year": "2024", "type": "policy"}
```

Filtering is applied before reranking.

---

### 5. Deduplication

Deduplication removes:

* same chunk IDs
* near duplicate chunks

Position in pipeline:

Deduplication is done BEFORE reranking.

Reason:

* reranking duplicate chunks wastes compute
* reranker scores should be computed only once per unique chunk

---

### 6. Reranking (cross‑encoder)

Cross‑encoder input:

```
[query] + [chunk]
```

Unlike bi‑encoder, the model reads both together.

Role:

* produces accurate relevance score

Important:

* cross‑encoder cannot be indexed
* only used on small candidate set

---

### 7. MMR (Max Marginal Relevance)

MMR is applied after reranking.

Role:

* select chunks that are both:

  * relevant to query
  * diverse from each other

MMR formula intuition:

```
score = λ * relevance – (1-λ) * redundancy
```

MMR prevents:

* multiple chunks from same paragraph
* repetitive sections

---

### 8. Context builder

Context builder prepares the final prompt context for the LLM.

Responsibilities:

* order chunks
* attach traceable metadata
* trim by token budget
* format context

---

### 9. Traceable context sources

Each chunk passed to the LLM must contain:

* source document
* page or section
* chunk id

Example:

```
[Source: report.pdf | page 12 | chunk 4821]
```

This enables:

* auditability
* debugging
* grounding

---

### 10. Context window optimization

Since LLM has limited tokens:

* only top ranked + MMR selected chunks are kept
* context is trimmed to fit token budget

---

### 11. LLM usage in this pipeline

LLM is NOT used for retrieval.

LLM is used only for:

* final answer generation

LLM receives:

* the user query
* the selected chunk context

LLM never sees the full corpus.

## Cross‑encoder vs Bi‑encoder

Bi‑encoder:

* encodes query and chunk separately
* used for FAISS retrieval

Cross‑encoder:

* encodes query and chunk together
* used only for reranking

---

## Required project files

```
/retriever/hybrid_retriever.py
/retriever/reranker.py
/pipelines/context_builder.py
RETRIEVAL-STRATEGIES.md
```
