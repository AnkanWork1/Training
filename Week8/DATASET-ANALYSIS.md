# DATASET ANALYSIS — Instruction Tuning Dataset

## 1. Overview

This document describes the dataset preparation, cleaning process, token analysis, and distribution insights for the Week-8 LLM fine-tuning pipeline.

The dataset is designed for instruction tuning using a coding-focused domain.  
Each sample follows the structure:

`{"instruction": "...", "input": "...", "output": "..."}`


The objective was to build a clean and balanced dataset suitable for LoRA / QLoRA fine-tuning.

---

## 2. Dataset Source

The dataset used for instruction tuning was downloaded from the Hugging Face Hub:

Dataset Name: **tatsu-lab/alpaca**

It is an instruction-following dataset designed for supervised fine-tuning of Large Language Models (LLMs).  
The dataset already follows an instruction-based structure, which makes it suitable for LoRA / QLoRA training.

Download Method:

The dataset was programmatically downloaded using the Hugging Face `datasets` library:

```python
from datasets import load_dataset
dataset = load_dataset("tatsu-lab/alpaca")
```
---

## 3. Dataset Summary

| Metric | Value |
|---|---|
| Total Training Samples | 1080 |
| Validation Samples | 120 |
| Domain | Coding / Programming |
| Format | Instruction Tuning JSONL |

The dataset was cleaned and filtered to ensure stable training performance.

![CLI view](src/images/s1.png)

---

## 4. Data Cleaning Process

The following preprocessing steps were applied:

### Duplicate Removal
Duplicate samples were identified using instruction + input + output matching and removed.

### Empty Sample Filtering
Samples with missing instructions or outputs were discarded.

### Token Length Filtering (Outlier Removal)
Token length analysis was performed using a tokenizer.

Rules applied:

- Samples with fewer than **10 tokens** were removed (low-information noise).
- Samples exceeding **512 tokens** were removed to avoid memory instability.

This ensures:

- Stable GPU memory usage
- Faster training
- Reduced padding overhead



---

## 5. Token Length Analysis

Token statistics computed from the training dataset:

| Metric | Tokens |
|---|---|
| Avg Instruction Tokens | 13 |
| Avg Input Tokens | 6 |
| Avg Output Tokens | 52 |
| Max Total Tokens | 442 |

### Observations

- Instructions are short and concise, enabling efficient prompt understanding.
- Inputs are lightweight, mostly small code snippets or context.
- Outputs are medium-length, ideal for instruction tuning tasks.
- Maximum sequence length (442) remains safely below the 512-token threshold.

![CLI view](src/images/s2.png)
---

## 6. Distribution Analysis

Token distribution graphs were generated:

- `token_distribution.png`
- `instruction_distribution.png`

These graphs confirm that most samples fall within a stable token range, with no extreme outliers after filtering.

---

## 7. Dataset Suitability for Fine-Tuning

Based on analysis:

### Strengths

- Balanced instruction-to-output ratio
- Efficient token length distribution
- No extreme long-context samples
- Optimized for low-resource LoRA training

### Expected Training Benefits

- Stable gradient updates
- Faster convergence
- Lower VRAM consumption
- Better generalization during instruction tuning

---

## 8. Conclusion

The dataset is clean, curated, and optimized for instruction-based fine-tuning.  
Token length constraints and outlier removal ensure compatibility with Colab-friendly models such as TinyLlama, Phi, and Qwen.

This dataset is ready for:

- LoRA / QLoRA training
- Quantisation experiments
- Optimized inference benchmarking
