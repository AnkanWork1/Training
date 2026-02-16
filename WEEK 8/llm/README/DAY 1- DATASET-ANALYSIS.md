# Dataset Analysis – WEEK 8 (Instruction Tuning)

## Dataset overview

This dataset is created for instruction tuning with the following format:

```json
{"instruction": "What is the purpose of the __enter__ and __exit__ methods in a Python class?", "input": "", "output": "The __enter__ and __exit__ methods define the behavior of a context manager, allowing an object to be used with the with statement for resource management."}

{"instruction": "Extract all top-level function names from the code.", "input": "def add(x, y):\n    return x + y\n\ndef sub(x, y):\n    return x - y", "output": "add, sub"}

{"instruction": "Find the unexpected behavior in the following code and explain the execution flow step by step.", "input": "a = [1, 2, 3]\nb = a\nb.append(4)\nprint(a)", "output": "The unexpected behavior is that the list a is modified. Both a and b reference the same list object in memory, so appending to b also changes a."}

The dataset contains three task types:

QA

Reasoning

Extraction

Domain used: Coding
```

## Dataset pipeline

The dataset is prepared using the following steps:

raw.jsonl  →  clean.jsonl  →  train.jsonl / val.jsonl

Step 1 – raw.jsonl

Manually curated instruction samples.

This file may contain:

duplicate samples

inconsistent whitespace

empty outputs

## Step 3 – train / validation split

After cleaning, the dataset is split into:

train.jsonl

val.jsonl

A random split is used.

Validation ratio: 10%

The validation set is kept completely unseen during training.

## Token statistics

Token statistics were computed using:

llm/utils/token_stats.py


Command:

python llm/utils/token_stats.py


The script measures the number of tokens per training sample
(after tokenization) for each record.


### Token statistics result

From the current dataset run:

count : 122
min   : 25
mean  : 55.61
p95   : 102
p99   : 146.53
max   : 150


### Meaning of each metric

#### count

Total number of samples analysed.

count = 122


This means 122 instruction samples are present in the file.

#### min

Minimum number of tokens in any single sample.

min = 25 tokens


This represents the shortest instruction–input–output example.

#### mean

Average token length across all samples.

mean ≈ 55.6 tokens


This shows the dataset is dominated by short to medium length
instructions, which is suitable for low-resource fine-tuning.

#### p95 (95th percentile)
p95 = 102 tokens


95% of the samples have token length less than or equal to 102 tokens.

Only 5% of the samples are longer than this.

#### p99 (99th percentile)
p99 ≈ 146.5 tokens


99% of the samples are shorter than about 147 tokens.

This helps identify extreme long samples.

#### max
max = 150 tokens

The longest single sample in the dataset.

## Why token statistics are important

### Token statistics are used to:

Estimate memory usage during training

Choose a safe max sequence length

Detect abnormal or noisy long samples

Decide whether outlier filtering is required

Since QLoRA and LoRA training is memory-sensitive, controlling
sequence length directly impacts GPU RAM usage.

## Outlier analysis

### The distribution shows:

Most samples are below 102 tokens (p95)

Very few samples reach the maximum of 150 tokens

There is no extreme long-tail behaviour in the current dataset.

## Outlier handling policy

For this dataset:

No samples were removed based on length

All samples are well below the maximum sequence limit used for training

The filtering threshold can be safely set to:

max_allowed_tokens = 256


This keeps all current samples and protects future dataset growth.

## Final dataset used for training

After cleaning and splitting:

train.jsonl → used for fine-tuning

val.jsonl → used for evaluation and loss monitoring

Both files are generated only after the cleaning stage.

## Summary

The dataset is clean and deduplicated

Token lengths are small and consistent

No extreme outliers are present

The dataset is suitable for low-resource QLoRA fine-tuning