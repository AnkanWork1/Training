import argparse
from retriever.multimodal_retriever import MultimodalRetriever
from memory.memory_store import ChatMemory
from evaluation.llm_adapter import OllamaLLM
from retriever.multimodal_retriever import is_image_path
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import os
from embeddings.image_ocr_blip import MultimodalEmbedder

# -------------------------------
# Embedding function (dummy, replace with real)
# -------------------------------
def text_to_embedding(text):
    # For Ollama, you could have a dedicated embedding model if available
    # Here we just mock a random embedding for demonstration
    return np.random.rand(1, 768)

# -------------------------------
# Generate answer
# -------------------------------
def generate_answer(query, top_k=10):
    retriever = MultimodalRetriever()
    chunks = retriever.search(query, top_k=top_k)

    memory = ChatMemory()
    last_chats = memory.get_last_chats()

    context_texts = []
    for c in chunks:
        if c["modality"] == "text":
            txt = (c.get("text") or "")[:1200]
            print(c.get("text"))
            context_texts.append(
                f"Text Chunk [{c.get('chunk_id')}]: {txt}"
            )
    chat_history = ""
    for m in last_chats:
        q = m.get("question")
        a = m.get("content")
        chat_history += f"Q: {q}\nA: {a}\n"

    if is_image_path(query):
        user_question = MultimodalEmbedder().build_query_from_image(query)
    else:
        user_question = query


    prompt = f"""
You are an assistant that only answers using the provided context. Do not hallucinate.
If the question is unrelated to the context, respond with "Not found".

Context Chunks:
{chr(10).join(context_texts)}

Chat History (last 5 messages):
{chat_history}

Question: {user_question}

Answer strictly based on the chunks above:
"""

    llm = OllamaLLM()
    answer_text = llm.generate(
        system="You are a helpful assistant.",
        prompt=prompt
    )

    # ----------------------------
    # pick TOP-1 image (if any)
    # ----------------------------
    if "Not found"  in answer_text:
        
        top_image = None
        count=0
        for c in chunks:
            if c["modality"] == "image" :
                top_image = c["image_path"]
                count=count+1
                if count>1:
                    break

    # ----------------------------
    # store memory
    # ----------------------------
    memory.add_chat(query, answer_text)

    return {
        "answer": answer_text,
        "image": top_image,
        "chunks": chunks
    }

# -------------------------------
# Compute metrics
# -------------------------------

def compute_metrics(answer, chunks):
    chunk_texts = [c.get("text","") for c in chunks if c["modality"]=="text"]
    if not chunk_texts:
        return {
            "context_match_score": 0.0,
            "faithfulness_score": 0.0,
            "hallucination_detected": True,
            "confidence_score": 0.0
        }

    # Context match
    answer_emb = text_to_embedding(answer)
    chunk_embs = [text_to_embedding(t) for t in chunk_texts]

    # === FIX: flatten 3D embeddings to 2D ===
    if answer_emb.ndim == 3:
        answer_emb = answer_emb.mean(axis=1)  # mean pooling over sequence
    chunk_embs = np.array(chunk_embs)
    if chunk_embs.ndim == 3:
        chunk_embs = chunk_embs.mean(axis=1)  # mean pooling

    context_match_score = max(cosine_similarity(answer_emb, chunk_embs)[0])

    # Faithfulness (simplified heuristic)
    faithfulness_score = 1.0 if "Not found" not in answer else 0.0
    hallucination_detected = faithfulness_score < 0.8
    confidence_score = round((context_match_score + faithfulness_score)/2, 2)

    return {
        "context_match_score": round(context_match_score, 2),
        "faithfulness_score": faithfulness_score,
        "hallucination_detected": hallucination_detected,
        "confidence_score": confidence_score
    }


# -------------------------------
# Full pipeline
# -------------------------------
def context_answer_generator(query, top_k=10):
    result = generate_answer(query, top_k=top_k)

    answer = result["answer"]
    image  = result["image"]
    chunks = result["chunks"]
    metrics = compute_metrics(answer, chunks)
    return {
        "answer": answer,
        "metrics": metrics,
        "chunks_used": chunks,
        "image_used": image
    }

# -------------------------------
# CLI
# -------------------------------
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--query", required=True)
    parser.add_argument("--top_k", type=int, default=10)
    args = parser.parse_args()

    result = context_answer_generator(args.query, args.top_k)
    print("\nAnswer:", result["answer"])
    print("\nMetrics:", result["metrics"])
    print("image used:", result["image_used"])
