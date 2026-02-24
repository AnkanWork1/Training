import time
import torch
import csv
import os

from transformers import AutoTokenizer, AutoModelForCausalLM
from llama_cpp import Llama
from sentence_transformers import SentenceTransformer, util

# MODELS that we are using 
MODELS = {
    "base": "TinyLlama/TinyLlama-1.1B-Chat-v1.0",
    "fp16": "/content/week8/MyDrive/Week 8/llm/quantized/model-fp16",
    "int8": "/content/week8/MyDrive/Week 8/llm/quantized/model-int8",
    "int4": "/content/week8/MyDrive/Week 8/llm/quantized/model-int4",
}

GGUF_PATH = "/content/week8/MyDrive/Week 8/llm/quantized/model.gguf"

# multiple questions asked
PROMPTS = [
    "What is a Python list comprehension and when should it be used?",
    "What is a Python generator and how is it different from a list?",
    "What does the Python decorator concept mean?"
]
# refernced answer to check accuracy
GROUND_TRUTH = [
    "A Python list comprehension is a concise syntax for creating a new list by applying an expression to each item of an iterable, optionally filtering elements. It should be used when a simple loop can be expressed clearly in a single readable expression.",
    "A Python generator produces values lazily using the yield keyword instead of storing all values in memory at once. Unlike a list, it generates items one by one and is more memory efficient for large data streams.",
    "A decorator is a function that modifies or extends the behavior of another function or class without changing its source code. It is commonly used for logging, access control, caching and validation."
]

embedder = SentenceTransformer("BAAI/bge-base-en-v1.5")

def semantic_accuracy(preds, refs):
    p_emb = embedder.encode(preds, convert_to_tensor=True)
    r_emb = embedder.encode(refs, convert_to_tensor=True)
    sims = util.cos_sim(p_emb, r_emb)
    return sims.diag().mean().item()

results = []

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

# For models benchmarks
for name, path in MODELS.items():


    print("Testing:", name)

    tokenizer = AutoTokenizer.from_pretrained(path)

    model = AutoModelForCausalLM.from_pretrained(
        path,
        device_map="auto",
        torch_dtype=torch.float16 if DEVICE=="cuda" else torch.float32
    )

    inputs = tokenizer(
        PROMPTS,
        padding=True,
        return_tensors="pt"
    ).to(model.device)

    if DEVICE=="cuda":
        torch.cuda.reset_peak_memory_stats()

    start = time.time()
    output = model.generate(**inputs, max_new_tokens=80)
    end = time.time()

    latency = end - start

    responses = [
        tokenizer.decode(o, skip_special_tokens=True)
        for o in output
    ]

    tokens_generated = sum(len(r.split()) for r in responses)
    speed = tokens_generated / latency

    vram = (
        torch.cuda.max_memory_allocated()/(1024**3)
        if DEVICE=="cuda" else 0
    )

    acc = semantic_accuracy(responses, GROUND_TRUTH)

    print("Tokens/sec:", speed)
    print("Latency:", latency)
    print("VRAM:", vram)
    print("Accuracy:", acc)

    results.append([name, speed, latency, vram, acc])

    del model
    torch.cuda.empty_cache()

#alternate benchmark for gguf
print("Testing: gguf")

llm = Llama(
    model_path=GGUF_PATH,
    n_ctx=2048,
    n_threads=os.cpu_count(),
    verbose=False
)

start = time.time()
outputs = []

for p in PROMPTS:
    out = llm(p, max_tokens=80)
    outputs.append(out["choices"][0]["text"])

end = time.time()

latency = end - start
tokens_generated = sum(len(o.split()) for o in outputs)
speed = tokens_generated / latency

# GGUF CPU VRAM = 0
vram = 0

acc = semantic_accuracy(outputs, GROUND_TRUTH)

print("Tokens/sec:", speed)
print("Latency:", latency)
print("VRAM:", vram)
print("Accuracy:", acc)


results.append(["gguf", speed, latency, vram, acc])

# saving the csv file
with open("/content/week8/MyDrive/Week 8/llm/benchmarks/results.csv", "w") as f:
    writer = csv.writer(f)
    writer.writerow(["Model","Tokens/sec","Latency","VRAM","Accuracy"])
    writer.writerows(results)

print("\nSaved -> /content/week8/MyDrive/Week 8/llm/benchmarks/results.csv")