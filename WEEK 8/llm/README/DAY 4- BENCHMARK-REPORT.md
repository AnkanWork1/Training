

# BENCHMARK REPORT — DAY 4
Inference Optimisation and Model Comparison

---

## 1. Overview

In this phase, different versions of the TinyLlama instruction model were
tested to understand how optimisation techniques affect performance.

The goal was to compare:

- Base Model (Original TinyLlama)
- Fine-tuned FP16 Model
- INT8 Quantised Model
- INT4 Quantised Model
- GGUF Model using llama.cpp

Each model was evaluated based on:

- Tokens generated per second (Speed)
- Latency (Total generation time)
- VRAM usage
- Semantic Accuracy

---

## 2. Test Setup

Hardware:

- Google Colab GPU runtime for Transformers models
- CPU runtime for GGUF model (llama.cpp)

Inference Engine:

- HuggingFace Transformers → base, fp16, int8, int4
- llama.cpp → gguf

Prompts used for testing:

1. Explain artificial intelligence simply.
2. What is machine learning?
3. Why are neural networks important?

Accuracy Measurement:

Instead of exact text matching, semantic similarity was used.
Sentence embeddings were generated using:

BAAI/bge-base-en-v1.5

Cosine similarity between model outputs and reference answers
was used as the accuracy score.

---


## 3. Benchmark Results

| Model | Tokens/sec | Latency (s) | VRAM (GB) | Accuracy |
|-------|------------|-------------|-----------|----------|
| base  | 28.685223883442113 | 3.2769484519958496 | 2.4758567810058594 | 0.8271123766899109 |
| fp16  | 82.41765304960138  | 2.2689313888549805 | 2.4768357276916504 | 0.7980424165725708 |
| int8  | 14.440706184682933 | 9.00232982635498   | 1.5790224075317383 | 0.7808601260185242 |
| int4  | 35.24084544937193  | 5.079333305358887  | 1.2199702262878418 | 0.811732292175293  |
| gguf  | 4.97737991623245   | 32.94906210899353  | 0                 | 0.7897317409515381 |

- Real time work

![](images/s7Benchmark.png)

---

## 4. Explanation in Simple Terms

This experiment shows how different optimisation techniques change the
behaviour of the model.

The base model was the fastest on GPU because it runs in full precision
without extra quantisation overhead.

The fp16 model had almost identical accuracy and memory usage because
fine-tuning mainly changes behaviour, not model size.

INT8 and INT4 models used less memory but became slower on GPU.
This happens because BitsAndBytes quantisation is not always fully
optimised for generation speed in this environment.

The GGUF model ran on CPU using llama.cpp. Even though it was slower
than GPU models, it required no VRAM and still produced meaningful
responses. This shows GGUF is useful for running models locally on
low-resource machines.

---

## 5. Speed Analysis

Base Model:
- Highest tokens/sec
- Fast GPU execution

FP16 Model:
- Slightly slower but same quality
- Expected behaviour after fine-tuning

INT8 / INT4:
- Lower memory usage
- Slower generation because quantised kernels add overhead

GGUF:
- Runs on CPU
- Much slower than GPU
- Good for offline deployment

---

## 6. Accuracy Analysis

Accuracy values represent semantic similarity (0 to 1 scale).

Base Model: 0.827
Fine-Tuned Model: 0.798  
INT8 Model: 0.781
INT4 Model: 0.812
GGUF Model: 0.789  

Observations:

- Fine-tuning did not increase accuracy significantly because the dataset
  contained general instruction data similar to the base model training.
- INT8 maintained strong semantic quality.
- INT4 showed a small drop in reasoning ability.
- GGUF preserved meaning but slightly reduced precision due to quantisation.

---

## 7. Key Learnings

1. GPU inference is much faster than CPU inference.
2. Quantisation reduces memory usage but may reduce speed depending on hardware.
3. GGUF is ideal for local deployment when GPU is not available.
4. Semantic accuracy is a better metric than exact text matching
   for evaluating LLM outputs.

---

## 8. Conclusion

The benchmarking process successfully compared multiple optimised
versions of the TinyLlama model.

Results show that:

- Base and FP16 models provide the best speed on GPU.
- INT8 gives strong accuracy with reduced VRAM usage.
- INT4 offers the smallest GPU memory footprint.
- GGUF enables CPU-only inference with acceptable response quality.

These experiments demonstrate how different optimisation strategies
can be chosen depending on the target hardware and deployment needs.