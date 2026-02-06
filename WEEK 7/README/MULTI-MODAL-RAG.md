Below is a **single clean Markdown file** for your repo.

It is written strictly for your setup
(terminal-only, local pipeline, CLIP + BLIP + Tesseract, multimodal retriever).

You can directly save this as:

```
MULTIMODAL-RAG.md
```

---

```md
# DAY 3 — IMAGE-RAG (MULTIMODAL RAG)

Enterprise-grade Multimodal Retrieval-Augmented Generation pipeline  
(Text + Image + OCR + Caption + Multimodal Vector Search)

This document describes the complete data flow, query execution flows,
models used, algorithms used and CLI commands for DAY-3.

This system is designed to run fully locally from terminal.

---

## 1. Goal of DAY-3

Build a multimodal RAG pipeline which supports:

- image ingestion
- OCR extraction
- caption generation
- vision + text embedding
- multimodal vector indexing
- multimodal retrieval

Supported query modes:

- Text → Image
- Image → Image
- Image → Text (Image-RAG)

---

## 2. High level architecture

```

```
                 ┌─────────────────────┐
                 │   User Query (Q)     │
                 └─────────┬───────────┘
                           │
                 ┌─────────▼───────────┐
                 │ Query Router         │
                 │ (text or image ?)   │
                 └──────┬──────────────┘
          ┌─────────────┴─────────────┐
          │                           │
   Text query path              Image query path
```

```

---

## 3. Ingestion pipeline (offline)

File:  
`/pipelines/image_ingest.py`

---

### 3.1 Ingestion data flow

```

Image / scanned PDF
|
v
Image extraction (pdf → images)
|
v
OCR (Tesseract)
|
v
Caption generation (BLIP)
|
v
CLIP image embedding
|
v
Store into multimodal index
(text + image metadata)

```

---

### 3.2 Detailed ingestion flow

```

Input image
|
|----> OCR using Tesseract
|           |
|           v
|       extracted text
|
|----> BLIP caption model
|           |
|           v
|       image caption
|
|----> CLIP image encoder
|
v
image embedding vector

```

---

### 3.3 What is stored per image

For each image entry:

```

{
image_embedding,
ocr_text,
caption,
file_path,
page_no,
document_id,
modality = "image"
}

```

OCR text and caption are also optionally chunked and indexed
in the text index.

---

## 4. Models used

### 4.1 CLIP (multimodal embedding)

Model:

```

openai/clip-vit-base-patch32

```

Used for:

- image embedding
- text embedding for cross-modal retrieval

---

### 4.2 BLIP (image captioning)

Model (typical):

```

Salesforce/blip-image-captioning-base

```

Used for:

- converting image → descriptive natural language

---

### 4.3 OCR

Engine:

```

Tesseract OCR

```

Used for:

- extracting text from scanned images / diagrams / forms

---

### 4.4 Text embedding model (if present in pipeline)

(Already used in previous days)

Typical:

```

sentence-transformers/all-MiniLM-L6-v2
or
BAAI/bge-small-en-v1.5

```

---

### 4.5 Reranker (if used later in hybrid flow)

Cross-encoder:

```

cross-encoder/ms-marco-MiniLM-L-6-v2

```

(Used in later stages, not mandatory for image-only retrieval)

---

## 5. Algorithms used (complete list)

---

### 5.1 CLIP contrastive embedding

Algorithm:

```

Contrastive representation learning
(image, text) pairs

```

Used to project:

- image
- text

into the same vector space.

---

### 5.2 OCR algorithm

Tesseract internally uses:

- LSTM based sequence recognition
- character segmentation + language model decoding

---

### 5.3 BLIP captioning

Algorithm:

```

Vision encoder + language decoder (Transformer)
trained with image-text pretraining and caption loss

```

---

### 5.4 Vector similarity search

Used in:

- image index
- multimodal index

Algorithms:

- cosine similarity
- inner product
- FAISS ANN search

Index structures (depending on config):

- Flat index
- HNSW
- IVF

---

### 5.5 Text retrieval (if combined)

- BM25
- dense embedding retrieval
- hybrid merging

---

### 5.6 Fusion / merging

Algorithm:

- score normalization
- rank merging
- simple top-k union

---

### 5.7 (Optional) MMR

Used in later stages to reduce redundancy.

Algorithm:

```

Maximal Marginal Relevance

```

---

## 6. Multimodal indexing design

Two logical vector spaces:

```

Text embedding index
Image embedding index (CLIP)

```

But CLIP enables both text and image queries to use the same space.

```

CLIP(image) ----┐
├──> image vector index
CLIP(text)  ----┘

```

---

## 7. Query execution flows

---

# 7.1 Text → Image

Used when user types a textual description and wants images.

### Flow

```

User text query
|
v
CLIP text encoder
|
v
Text embedding in CLIP space
|
v
FAISS search over image embeddings
|
v
Top-k image matches

```

---

### Flow chart

```

Text Query
|
v
CLIP Text Encoder
|
v
Embedding
|
v
Image Vector Index (FAISS)
|
v
Images

```

---

# 7.2 Image → Image

Used when user provides an image and wants similar images.

---

### Flow

```

Input image
|
v
CLIP image encoder
|
v
Image embedding
|
v
FAISS image index
|
v
Similar images

```

---

### Flow chart

```

Image Query
|
v
CLIP Image Encoder
|
v
Embedding
|
v
Image Vector Index
|
v
Images

```

---

# 7.3 Image → Text (Image-RAG)

Used when user wants explanations / related text from an image.

---

### Flow

```

Input image
|
v
CLIP image encoder
|
v
Image embedding
|
v
Search image index
|
v
Nearest images
|
v
Join metadata (doc_id, page, chunk ids)
|
v
Return OCR text + captions + related text chunks

```

---

### Flow chart

```

Image Query
|
v
CLIP Image Encoder
|
v
Embedding
|
v
Image Index
|
v
Image hits
|
v
Metadata join
|
v
OCR text + captions + document chunks

```

---

# 7.4 Text → Text (still supported)

This comes from previous days.

```

BM25 + dense embeddings + reranker

```

---

## 8. How multimodal works internally

The key idea is:

```

CLIP maps text and images into one shared embedding space.

```

So:

```

CLIP(text query) ≈ CLIP(image)

```

and

```

CLIP(image query) ≈ CLIP(image)

```

This enables:

- text → image
- image → image
- image → text (via metadata mapping)

The RAG part happens only after retrieval:

```

retrieved images → OCR / captions / chunks → LLM

```

---

## 9. CLI commands (your actual two multimodal commands)

---

### 9.1 Text → multimodal retrieval

```

python -m retriever.multimodal_retriever 
--query "augmented reality customer standing"

```

This executes:

- text → CLIP
- search image index
- search text index
- return mixed results

---

### 9.2 Image → multimodal retrieval

```

python -m retriever.multimodal_retriever 
--query "/absolute/path/to/image.jpeg"

```

This executes:

- image → CLIP
- image similarity search
- image → text join
- return images + text

---

## 10. Deliverables mapping

| File | Responsibility |
------|---------------
pipelines/image_ingest.py | OCR, BLIP captions, CLIP embeddings, storage
embeddings/clip_embedder.py | CLIP text & image embedding
retriever/image_search.py | image similarity search
retriever/multimodal_retriever.py | query routing + multimodal fusion
MULTIMODAL-RAG.md | system documentation

---

## 11. Important engineering notes

---

### 11.1 Normalization

CLIP embeddings must be L2 normalized before FAISS search.

---

### 11.2 Self-match in image → image

The top-1 hit is usually the same image.
This is expected behaviour.

---

### 11.3 Metadata is critical

Multimodal RAG is not only vector search.

The real RAG step depends on:

```

image_id → document_id → page → text chunks

```

Without metadata joins, Image-RAG is impossible.

---

## 12. Summary

DAY-3 builds a true multimodal retrieval system:

- OCR + caption + embeddings during ingestion
- shared embedding space using CLIP
- multimodal vector search
- image driven RAG
- multi-path query execution

This day introduces the foundation required for:

- multimodal reranking
- cross-modal fusion
- visual question answering pipelines
```

##13. Testing

###13.1 received images
(.venv) ankanguha@HESTABIT-416:~/Desktop/Training/WEEK 7/src$ python -m retriever.multimodal_retriever   --query "/home/ankanguha/Desktop/Training/WEEK 7/src/data/raw/archive(1)/EnterpriseRAG_2025_02_markdown/30f64d1043f4cb425eb636763580ae27094ffef1/_page_0_Picture_1.jpeg"
Loading multimodal retriever ...
Loaded FAISS + metadata
Loading weights: 100%|█| 199/199 [00:00<00:00, 6111.28it/s, Materializing param=pooler.
BertModel LOAD REPORT from: BAAI/bge-small-en
Key                     | Status     |  | 
------------------------+------------+--+-
embeddings.position_ids | UNEXPECTED |  | 

Notes:
- UNEXPECTED	:can be ignored when loading from different task/architecture; not ok if you expect identical arch.
Warning: You are sending unauthenticated requests to the HF Hub. Please set a HF_TOKEN to enable higher rate limits and faster downloads.
Loading weights: 100%|█| 201/201 [00:00<00:00, 5330.43it/s, Materializing param=roberta
XLMRobertaForSequenceClassification LOAD REPORT from: BAAI/bge-reranker-base
Key                             | Status     |  | 
--------------------------------+------------+--+-
roberta.embeddings.position_ids | UNEXPECTED |  | 

Notes:
- UNEXPECTED	:can be ignored when loading from different task/architecture; not ok if you expect identical arch.
Building BM25 index ...
Loading weights: 100%|█| 398/398 [00:00<00:00, 11338.27it/s, Materializing param=visual
CLIPModel LOAD REPORT from: openai/clip-vit-base-patch32
Key                                  | Status     |  | 
-------------------------------------+------------+--+-
text_model.embeddings.position_ids   | UNEXPECTED |  | 
vision_model.embeddings.position_ids | UNEXPECTED |  | 

Notes:
- UNEXPECTED	:can be ignored when loading from different task/architecture; not ok if you expect identical arch.
Loading weights: 100%|█| 398/398 [00:00<00:00, 8574.45it/s, Materializing param=visual_
CLIPModel LOAD REPORT from: openai/clip-vit-base-patch32
Key                                  | Status     |  | 
-------------------------------------+------------+--+-
text_model.embeddings.position_ids   | UNEXPECTED |  | 
vision_model.embeddings.position_ids | UNEXPECTED |  | 

Notes:
- UNEXPECTED	:can be ignored when loading from different task/architecture; not ok if you expect identical arch.
The image processor of type `CLIPImageProcessor` is now loaded as a fast processor by default, even if the model checkpoint was saved with a slow processor. This is a breaking change and may produce slightly different outputs. To continue using the slow processor, instantiate this class with `use_fast=False`. 
The image processor of type `BlipImageProcessor` is now loaded as a fast processor by default, even if the model checkpoint was saved with a slow processor. This is a breaking change and may produce slightly different outputs. To continue using the slow processor, instantiate this class with `use_fast=False`. 
Loading weights: 100%|█| 473/473 [00:00<00:00, 9158.25it/s, Materializing param=vision_
The tied weights mapping and config for this model specifies to tie text_decoder.cls.predictions.bias to text_decoder.cls.predictions.decoder.bias, but both are present in the checkpoints, so we will NOT tie them. You should update the config with `tie_word_embeddings=False` to silence this warning
The tied weights mapping and config for this model specifies to tie text_decoder.bert.embeddings.word_embeddings.weight to text_decoder.cls.predictions.decoder.weight, but both are present in the checkpoints, so we will NOT tie them. You should update the config with `tie_word_embeddings=False` to silence this warning
BlipForConditionalGeneration LOAD REPORT from: Salesforce/blip-image-captioning-base
Key                                       | Status     |  | 
------------------------------------------+------------+--+-
text_decoder.bert.embeddings.position_ids | UNEXPECTED |  | 

Notes:
- UNEXPECTED	:can be ignored when loading from different task/architecture; not ok if you expect identical arch.
Loaded FAISS + metadata
Loading weights: 100%|█| 199/199 [00:00<00:00, 5843.33it/s, Materializing param=pooler.
BertModel LOAD REPORT from: BAAI/bge-small-en
Key                     | Status     |  | 
------------------------+------------+--+-
embeddings.position_ids | UNEXPECTED |  | 

Notes:
- UNEXPECTED	:can be ignored when loading from different task/architecture; not ok if you expect identical arch.
Loading weights: 100%|█| 201/201 [00:00<00:00, 5729.11it/s, Materializing param=roberta
XLMRobertaForSequenceClassification LOAD REPORT from: BAAI/bge-reranker-base
Key                             | Status     |  | 
--------------------------------+------------+--+-
roberta.embeddings.position_ids | UNEXPECTED |  | 

Notes:
- UNEXPECTED	:can be ignored when loading from different task/architecture; not ok if you expect identical arch.
Building BM25 index ...
Multimodal retriever ready.


Results
============================================================

[1] modality: image
Image : /home/ankanguha/Desktop/Training/WEEK 7/src/data/raw/archive(1)/EnterpriseRAG_2025_02_markdown/30f64d1043f4cb425eb636763580ae27094ffef1/_page_0_Picture_1.jpeg
File  : _page_0_Picture_1.jpeg
Score : 0.9999973773956299

[2] modality: image
Image : /home/ankanguha/Desktop/Training/WEEK 7/src/data/raw/archive(1)/EnterpriseRAG_2025_02_markdown/e7a45fed0d7ebfd13a524e7fcc443318bac654e2/_page_13_Picture_16.jpeg
File  : _page_13_Picture_16.jpeg
Score : 0.5948107242584229

[3] modality: image
Image : /home/ankanguha/Desktop/Training/WEEK 7/src/data/raw/archive(1)/EnterpriseRAG_2025_02_markdown/e7a45fed0d7ebfd13a524e7fcc443318bac654e2/_page_33_Picture_16.jpeg
File  : _page_33_Picture_16.jpeg
Score : 0.5565123558044434

[4] modality: image
Image : /home/ankanguha/Desktop/Training/WEEK 7/src/data/raw/archive(1)/EnterpriseRAG_2025_02_markdown/e7a45fed0d7ebfd13a524e7fcc443318bac654e2/_page_26_Picture_21.jpeg
File  : _page_26_Picture_21.jpeg
Score : 0.5478774309158325

[5] modality: image
Image : /home/ankanguha/Desktop/Training/WEEK 7/src/data/raw/archive(1)/EnterpriseRAG_2025_02_markdown/e7a45fed0d7ebfd13a524e7fcc443318bac654e2/_page_20_Picture_24.jpeg
File  : _page_20_Picture_24.jpeg
Score : 0.540486752986908

[6] modality: text
PDF   : /home/ankanguha/Desktop/Training/WEEK 7/src/data/raw/archive(1)/EnterpriseRAG_2025_02_markdown/e7a45fed0d7ebfd13a524e7fcc443318bac654e2.pdf
Chunk : 804
Text  : | Napkins                                                                                                           | 2,749        | 79         | 2,828                                                                        |
| Table covers                                                                                                      | 662          | 0          | 662                          

[7] modality: text
PDF   : /home/ankanguha/Desktop/Training/WEEK 7/src/data/raw/archive(1)/EnterpriseRAG_2025_02_markdown/674a255d82495ef40189645697460801193e5a2d.pdf
Chunk : 256
Text  : The following table contains the expectations and concerns of the key stakeholders, as identified by the Group, and the corresponding management response:

[8] modality: text
PDF   : /home/ankanguha/Desktop/Training/WEEK 7/src/data/raw/archive(1)/EnterpriseRAG_2025_02_markdown/1af8f906e34af6e0acfe4f73e37093bbe34700f3.pdf
Chunk : 1325
Text  : | Bookies Card Pty Ltd

[9] modality: text
PDF   : /home/ankanguha/Desktop/Training/WEEK 7/src/data/raw/archive(1)/EnterpriseRAG_2025_02_markdown/6159f86f38ec4f82453d99a01c22f1847de133c6.pdf
Chunk : 2022
Text  : PARTIAL DRAWS AND MULTIPLE PRESENTATIONS ARE ALLOWED.

[10] modality: text
PDF   : /home/ankanguha/Desktop/Training/WEEK 7/src/data/raw/archive(1)/EnterpriseRAG_2025_02_markdown/30f64d1043f4cb425eb636763580ae27094ffef1.pdf
Chunk : 109
Text  : Table of Contents
(.venv) ankanguha@HESTABIT-416:~/Desktop/Training/WEEK 7/src$ 


###13.2 received text

(.venv) ankanguha@HESTABIT-416:~/Desktop/Training/WEEK 7/src$ python -m retriever.multimodal_retriever \
  --query "augmented reality customer standing"
Loading multimodal retriever ...
Loaded FAISS + metadata
Loading weights: 100%|█| 199/199 [00:00<00:00, 5745.86it/s, Materializing param=pooler.
BertModel LOAD REPORT from: BAAI/bge-small-en
Key                     | Status     |  | 
------------------------+------------+--+-
embeddings.position_ids | UNEXPECTED |  | 

Notes:
- UNEXPECTED	:can be ignored when loading from different task/architecture; not ok if you expect identical arch.
Loading weights: 100%|█| 201/201 [00:00<00:00, 5449.37it/s, Materializing param=roberta
XLMRobertaForSequenceClassification LOAD REPORT from: BAAI/bge-reranker-base
Key                             | Status     |  | 
--------------------------------+------------+--+-
roberta.embeddings.position_ids | UNEXPECTED |  | 

Notes:
- UNEXPECTED	:can be ignored when loading from different task/architecture; not ok if you expect identical arch.
Building BM25 index ...
Loading weights: 100%|█| 398/398 [00:00<00:00, 9905.90it/s, Materializing param=visual_
CLIPModel LOAD REPORT from: openai/clip-vit-base-patch32
Key                                  | Status     |  | 
-------------------------------------+------------+--+-
text_model.embeddings.position_ids   | UNEXPECTED |  | 
vision_model.embeddings.position_ids | UNEXPECTED |  | 

Notes:
- UNEXPECTED	:can be ignored when loading from different task/architecture; not ok if you expect identical arch.
Warning: You are sending unauthenticated requests to the HF Hub. Please set a HF_TOKEN to enable higher rate limits and faster downloads.
Loading weights: 100%|█| 398/398 [00:00<00:00, 6897.22it/s, Materializing param=visual_
CLIPModel LOAD REPORT from: openai/clip-vit-base-patch32
Key                                  | Status     |  | 
-------------------------------------+------------+--+-
text_model.embeddings.position_ids   | UNEXPECTED |  | 
vision_model.embeddings.position_ids | UNEXPECTED |  | 

Notes:
- UNEXPECTED	:can be ignored when loading from different task/architecture; not ok if you expect identical arch.
The image processor of type `CLIPImageProcessor` is now loaded as a fast processor by default, even if the model checkpoint was saved with a slow processor. This is a breaking change and may produce slightly different outputs. To continue using the slow processor, instantiate this class with `use_fast=False`. 
The image processor of type `BlipImageProcessor` is now loaded as a fast processor by default, even if the model checkpoint was saved with a slow processor. This is a breaking change and may produce slightly different outputs. To continue using the slow processor, instantiate this class with `use_fast=False`. 
Loading weights: 100%|█| 473/473 [00:00<00:00, 9915.46it/s, Materializing param=vision_
The tied weights mapping and config for this model specifies to tie text_decoder.cls.predictions.bias to text_decoder.cls.predictions.decoder.bias, but both are present in the checkpoints, so we will NOT tie them. You should update the config with `tie_word_embeddings=False` to silence this warning
The tied weights mapping and config for this model specifies to tie text_decoder.bert.embeddings.word_embeddings.weight to text_decoder.cls.predictions.decoder.weight, but both are present in the checkpoints, so we will NOT tie them. You should update the config with `tie_word_embeddings=False` to silence this warning
BlipForConditionalGeneration LOAD REPORT from: Salesforce/blip-image-captioning-base
Key                                       | Status     |  | 
------------------------------------------+------------+--+-
text_decoder.bert.embeddings.position_ids | UNEXPECTED |  | 

Notes:
- UNEXPECTED	:can be ignored when loading from different task/architecture; not ok if you expect identical arch.
Loaded FAISS + metadata
Loading weights: 100%|█| 199/199 [00:00<00:00, 5110.15it/s, Materializing param=pooler.
BertModel LOAD REPORT from: BAAI/bge-small-en
Key                     | Status     |  | 
------------------------+------------+--+-
embeddings.position_ids | UNEXPECTED |  | 

Notes:
- UNEXPECTED	:can be ignored when loading from different task/architecture; not ok if you expect identical arch.
Loading weights: 100%|█| 201/201 [00:00<00:00, 5337.14it/s, Materializing param=roberta
XLMRobertaForSequenceClassification LOAD REPORT from: BAAI/bge-reranker-base
Key                             | Status     |  | 
--------------------------------+------------+--+-
roberta.embeddings.position_ids | UNEXPECTED |  | 

Notes:
- UNEXPECTED	:can be ignored when loading from different task/architecture; not ok if you expect identical arch.
Building BM25 index ...
Multimodal retriever ready.


Results
============================================================

[1] modality: text
PDF   : /home/ankanguha/Desktop/Training/WEEK 7/src/data/raw/archive(1)/EnterpriseRAG_2025_02_markdown/0f111d244aee3d976684995a222fa177a64571c4.pdf
Chunk : 43
Text  : a customer is standing and game developers need precise 3D location data to deliver next generation augmented reality experiences.

[2] modality: text
PDF   : /home/ankanguha/Desktop/Training/WEEK 7/src/data/raw/archive(1)/EnterpriseRAG_2025_02_markdown/c74139ce26a6f803725f5074a8a0f539abb99c09.pdf
Chunk : 4871
Text  : ### Due from customers

#### tab. A8.1 – Due from customers

[3] modality: text
PDF   : /home/ankanguha/Desktop/Training/WEEK 7/src/data/raw/archive(1)/EnterpriseRAG_2025_02_markdown/0a61a353b1ea9fd9b8f63b60239634ca3007d58f.pdf
Chunk : 104
Text  : their bespoke customer benefits.

[4] modality: text
PDF   : /home/ankanguha/Desktop/Training/WEEK 7/src/data/raw/archive(1)/EnterpriseRAG_2025_02_markdown/c74139ce26a6f803725f5074a8a0f539abb99c09.pdf
Chunk : 2400
Text  : By achieving this security standard, Poste Italiane's Privacy function is able to demonstrate compliance of certified services with GDPR and other data privacy requirements.

Poste Italiane obtains the ISO 27701 certification

{367}------------------------------------------------

![](_page_367_Picture_2.jpeg)

LEARN ABOUT THE ARTWORK WITH AUGMENTED REALITY Scan the QR code with your smartphone an

[5] modality: text
PDF   : /home/ankanguha/Desktop/Training/WEEK 7/src/data/raw/archive(1)/EnterpriseRAG_2025_02_markdown/1af8f906e34af6e0acfe4f73e37093bbe34700f3.pdf
Chunk : 1337
Text  : | eBet Technologies Inc

[6] modality: image
Image : /home/ankanguha/Desktop/Training/WEEK 7/src/data/raw/archive(1)/EnterpriseRAG_2025_02_markdown/8f5e29eea4f4a3e944707c71148439ca1fd4b2d8/_page_6_Picture_24.jpeg
File  : _page_6_Picture_24.jpeg
Score : 0.2820552885532379

[7] modality: image
Image : /home/ankanguha/Desktop/Training/WEEK 7/src/data/raw/archive(1)/EnterpriseRAG_2025_02_markdown/980742aa08ea64d552c153bcefbd7e8243fb9efd/_page_26_Picture_7.jpeg
File  : _page_26_Picture_7.jpeg
Score : 0.2795891761779785

[8] modality: image
Image : /home/ankanguha/Desktop/Training/WEEK 7/src/data/raw/archive(1)/EnterpriseRAG_2025_02_markdown/12bff07b957b1c8f8cad9d917ca18005720cce9b/_page_32_Picture_3.jpeg
File  : _page_32_Picture_3.jpeg
Score : 0.27472373843193054

[9] modality: image
Image : /home/ankanguha/Desktop/Training/WEEK 7/src/data/raw/archive(1)/EnterpriseRAG_2025_02_markdown/e6ce8ed579e95d2cfeabbbed872beb0c3f8396d7/_page_113_Picture_0.jpeg
File  : _page_113_Picture_0.jpeg
Score : 0.2744934558868408

[10] modality: image
Image : /home/ankanguha/Desktop/Training/WEEK 7/src/data/raw/archive(1)/EnterpriseRAG_2025_02_markdown/12bff07b957b1c8f8cad9d917ca18005720cce9b/_page_30_Picture_1.jpeg
File  : _page_30_Picture_1.jpeg
Score : 0.2732240855693817

