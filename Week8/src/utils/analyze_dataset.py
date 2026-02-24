import json
import matplotlib.pyplot as plt
from transformers import AutoTokenizer

TRAIN_PATH = "data/train.jsonl"

tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")

instruction_lens = []
input_lens = []
output_lens = []
total_lens = []

def token_len(text):
    return len(tokenizer.encode(text)) if text else 0

print("Reading dataset...")

with open(TRAIN_PATH, "r", encoding="utf-8") as f:
    for line in f:
        obj = json.loads(line)

        inst = token_len(obj["instruction"])
        inp = token_len(obj["input"])
        out = token_len(obj["output"])

        instruction_lens.append(inst)
        input_lens.append(inp)
        output_lens.append(out)
        total_lens.append(inst + inp + out)

print("Samples:", len(total_lens))
print("Avg instruction tokens:", sum(instruction_lens)//len(instruction_lens))
print("Avg input tokens:", sum(input_lens)//len(input_lens))
print("Avg output tokens:", sum(output_lens)//len(output_lens))
print("Max total tokens:", max(total_lens))

plt.figure()
plt.hist(total_lens, bins=50)
plt.title("Token Length Distribution")
plt.savefig("token_distribution.png")

plt.figure()
plt.hist(instruction_lens, bins=50)
plt.title("Instruction Distribution")
plt.savefig("instruction_distribution.png")

print("Graphs saved.")
