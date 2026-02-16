import json
import random
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]

SRC = BASE / "data" / "clean.jsonl"
TRAIN = BASE / "data" / "train.jsonl"
VAL = BASE / "data" / "val.jsonl"

VAL_RATIO = 0.1

def load(p):
    with open(p) as f:
        return [json.loads(l) for l in f]

def save(p, rows):
    with open(p, "w") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

if __name__ == "__main__":
    rows = load(SRC)
    random.shuffle(rows)

    n_val = int(len(rows) * VAL_RATIO)

    val = rows[:n_val]
    train = rows[n_val:]

    save(TRAIN, train)
    save(VAL, val)

    print("train:", len(train))
    print("val:", len(val))
