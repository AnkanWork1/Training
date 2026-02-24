# TRAINING REPORT — QLoRA Fine-Tuning

## 1. Introduction

This report describes the parameter-efficient fine-tuning process performed using QLoRA
on a TinyLlama instruction model. The objective was to adapt the base model to a custom
instruction-tuning dataset while minimizing GPU memory usage.

The training was performed using 4-bit quantization and LoRA adapters.

---

## 2. Model Used

Base Model:
`TinyLlama-1.1B-Chat-v1.0`

Reason for selection:

- Lightweight and Colab-friendly
- Instruction-tuned architecture
- Suitable for low-resource fine-tuning

---

## 3. Dataset Used

The dataset was prepared in Day-1 and follows instruction-tuning format:

`{"instruction": "...", "input": "...", "output": "..."}`


Dataset Details:

- Domain: Coding / Programming
- Train Samples: 1080
- Validation Samples: 120

Data was cleaned and curated using:

- Duplicate removal
- Token length filtering
- Outlier removal (>512 tokens)

---

## 4. Training Method — QLoRA

QLoRA (Quantized Low Rank Adaptation) was used to fine-tune the model efficiently.

Key Concepts:

- The base model was loaded in 4-bit precision to reduce VRAM usage.
- Only LoRA adapter layers were trained.
- The original model weights remained frozen.

Benefits:

- Trainable parameters reduced to ~1%
- Faster training
- Lower memory consumption

---

## 5. Training Configuration

| Parameter | Value |
|---|---|
| LoRA Rank (r) | 16 |
| Learning Rate | 2e-4 |
| Batch Size | 4 |
| Epochs | 3 |
| Quantization | 4-bit (nf4) |
| Trainer | TRL SFTTrainer |

---

## 6. Training Steps Performed

### Step 1 — Model Loading

The TinyLlama model was loaded using 4-bit quantization with BitsAndBytesConfig.

Purpose:

- Reduce GPU memory usage
- Enable QLoRA training on Colab


### Step 2 — LoRA Adapter Injection

LoRA layers were added using PEFT configuration:

- r = 16
- lora_alpha = 32
- dropout = 0.05

Only adapter layers were set as trainable.


### Step 3 — Dataset Formatting

Instruction, input, and output fields were combined into a training prompt:

```
Instruction:

...

Input:

...

Response:
```

This format helps the model learn structured instruction-following behaviour.


### Step 4 — Training Execution

Training was executed using SFTTrainer with:

- batch size = 4
- epochs = 3
- learning rate = 2e-4

During training:

- Loss decreased gradually
- No GPU memory overflow occurred


### Step 5 — Adapter Saving

After training, only LoRA adapter weights were saved.

Saved files:
```path
/adapters/

    adapter_model.safetensors

    adapter_config.json
```

The base model weights were not modified.

---

## 7. Training Results

Observations:

- Trainable parameters ≈ 1% of total model parameters
- Stable training behaviour
- Gradual loss reduction observed
- Efficient memory usage with 4-bit loading

---

## 8. Advantages of QLoRA Training

Compared to full fine-tuning:

- Requires significantly less VRAM
- Faster training
- Smaller output files
- Easy adapter reuse

---

## 9. Output Artifacts

Generated during training:

- lora_train.ipynb
- adapter_model.safetensors
- adapter_config.json

