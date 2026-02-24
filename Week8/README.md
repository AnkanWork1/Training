# Quantised LLM Deployment — TinyLlama (Week8 Project)

This project demonstrates the **complete lifecycle of an LLM**:

✔ Dataset preparation  
✔ QLoRA Fine-Tuning  
✔ Model Quantisation (INT8 / INT4 / GGUF)  
✔ Inference Benchmarking  
✔ FastAPI Deployment  
✔ Streaming Chat API  
✔ CLI + Streamlit UI  
✔ Dockerised Local Server

The goal was to build a **fully deployable local LLM system** optimized for CPU inference.

---

# Project Overview

This project uses **TinyLlama-1.1B** as the base model.

Pipeline:
`Dataset → LoRA Fine-Tune → Quantisation → Benchmark → Deployment → UI`


We converted the model into multiple formats:

- FP16 (reference model)
- INT8 (bitsandbytes)
- INT4 (bitsandbytes)
- GGUF (llama.cpp CPU optimized)

---

# Project Structure
```
src/
├── deploy/ # FastAPI server + UI + CLI
├── quantized/ # FP16 / INT8 / INT4 / GGUF models
├── benchmarks/ # inference results
├── data/ # training dataset
├── logs/ # runtime logs
├── inference/ # benchmarking scripts
├── images/ #some screenshots 
├── notebook/ #Collab Files
├── adapter/ #  Model trained with my data
└── utils/ # dataset tools
```

---

# ⚡ Features

## Model Features
- Quantised GGUF model
- Infinite chat memory
- System + User prompts
- Top-k / Top-p / Temperature control
- Streaming token output

## Backend Features
- FastAPI server
- OpenAI compatible endpoint
- llama.cpp integration
- JSON logging
- Request IDs

## Frontend
- Streamlit Chat UI
- CLI interactive mode

---

# Running Locally

## 1 Start LLM Server (llama.cpp)

`./llama.cpp/build/bin/llama-server     --model src/quantized/model.gguf    --port 8080`



## 2 Start FastAPI

`uvicorn src.deploy.app:app --reload`


- Server runs at:


`http://localhost:8000`




## 3 Launch Streamlit UI


`streamlit run src/deploy/ui.py`


---

# API Endpoints

## 🔹 Generate (single prompt)


`POST /generate`


Stateless generation.



## 🔹 Chat (memory enabled)


`POST /chat`


Maintains conversation history using `chat_id`.

---

# 🎛️ Generation Controls

| Parameter | Meaning |
|---|---|
| Temperature | Creativity level |
| Top-p | Probability sampling |
| Top-k | Token filtering |
| Max Tokens | Output length |

---

# 📊 Benchmark Results

| Model | Tokens/sec | VRAM | Accuracy |
|---|---|---|---|
| Base | High | Medium | High |
| FP16 | High | Medium | High |
| INT8 | Medium | Low | High |
| INT4 | Fast | Very Low | Medium |
| GGUF | CPU Optimized | 0 GPU | Slightly Lower |

GGUF achieved the best **CPU inference speed**.

---

# Key Learnings

- QLoRA reduces trainable params to ~1%
- Quantisation drastically lowers memory usage
- GGUF is ideal for CPU deployment
- Streaming improves user experience
- Chat vs Generate endpoints serve different use cases
