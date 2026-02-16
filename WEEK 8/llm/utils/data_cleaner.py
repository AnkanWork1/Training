# utils/data_cleaner.py
import json
from pathlib import Path
from transformers import AutoTokenizer


MAX_TOKENS = 2048
TOKEN_LIMIT = 147
tokenizer = AutoTokenizer.from_pretrained("gpt2")
BASE_DIR = Path(__file__).resolve().parent.parent

def load_jsonl(path):
    with open(path) as f:
        for line in f:
            yield json.loads(line)

def save_jsonl(path, rows):
    with open(path, "w") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
def basic_clean(rows):
    cleaned = []
    seen = set()

    for r in rows:
        inst = r["instruction"].strip()
        inp = r.get("input","").strip()
        outp = r["output"].strip()

        if not outp:
            continue

        key = (inst, inp, outp)
        if key in seen:
            continue

        # ---------- NEW PART (token filter) ----------
        text = inst + "\n" + inp + "\n" + outp
        token_len = len(tokenizer.encode(text))

        if token_len > TOKEN_LIMIT:
            continue
        # --------------------------------------------

        seen.add(key)

        cleaned.append({
            "instruction": inst,
            "input": inp,
            "output": outp
        })

    return cleaned

if __name__ == "__main__":
    src = Path(BASE_DIR/"data/raw.jsonl")
    dst = Path(BASE_DIR/"data/clean.jsonl")

    rows = list(load_jsonl(src))
    rows = basic_clean(rows)
    save_jsonl(dst, rows)

    print("Final samples:", len(rows))
