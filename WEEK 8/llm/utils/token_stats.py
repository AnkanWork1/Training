from pathlib import Path
import json
import numpy as np
import matplotlib.pyplot as plt
from transformers import AutoTokenizer

BASE_DIR = Path(__file__).resolve().parent.parent   # -> llm/
DATA_PATH = BASE_DIR / "data" / "train.jsonl"

tokenizer = AutoTokenizer.from_pretrained("gpt2")

lengths = []

with open(DATA_PATH, "r") as f:
    for line in f:
        r = json.loads(line)
        text = (
            r["instruction"] + "\n" +
            r["input"] + "\n" +
            r["output"]
        )
        lengths.append(len(tokenizer.encode(text)))

arr = np.array(lengths)

print("count:", len(arr))
print("min:", arr.min())
print("mean:", arr.mean())
print("p95:", np.percentile(arr, 95))
print("p99:", np.percentile(arr, 99))
print("max:", arr.max())

plt.hist(arr, bins=50)
plt.savefig("token_distribution.png")
