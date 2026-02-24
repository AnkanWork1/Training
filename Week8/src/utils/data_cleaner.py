import json
import random
from datasets import load_from_disk
from transformers import AutoTokenizer

# ===== CONFIG =====
RAW_PATH = "raw_data/alpaca"
TRAIN_PATH = "data/train.jsonl"
VAL_PATH = "data/val.jsonl"

TARGET_SAMPLES = 1200
VAL_RATIO = 0.1

tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")

def token_len(text):
    if not text:
        return 0
    return len(tokenizer.encode(text))


print("Loading dataset...")
ds = load_from_disk(RAW_PATH)["train"]

clean_data = []
seen = set()

print("Cleaning dataset...")

for row in ds:

    instruction = row["instruction"].strip()
    input_text = row["input"].strip()
    output = row["output"].strip()

    if not instruction or not output:
        continue

    key = instruction + input_text + output
    if key in seen:
        continue
    seen.add(key)

    total_tokens = (
        token_len(instruction)
        + token_len(input_text)
        + token_len(output)
    )

    # remove outliers
    if total_tokens < 10:
        continue
    if total_tokens > 512:
        continue

    sample = {
        "instruction": instruction,
        "input": input_text,
        "output": output
    }

    clean_data.append(sample)

    if len(clean_data) >= TARGET_SAMPLES:
        break


print("Total cleaned samples:", len(clean_data))

random.shuffle(clean_data)

split_index = int(len(clean_data) * (1 - VAL_RATIO))

train_data = clean_data[:split_index]
val_data = clean_data[split_index:]


def save_jsonl(path, data):
    with open(path, "w", encoding="utf-8") as f:
        for item in data:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")


save_jsonl(TRAIN_PATH, train_data)
save_jsonl(VAL_PATH, val_data)

print("Train size:", len(train_data))
print("Val size:", len(val_data))
print("Saved JSONL files.")
