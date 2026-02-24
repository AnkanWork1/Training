import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel

BASE_MODEL = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
ADAPTER_DIR = "./adapters/checkpoint-81"
OUT_DIR = "merged/full-model"

tokenizer = AutoTokenizer.from_pretrained("./tokenizer")

model = AutoModelForCausalLM.from_pretrained(
    BASE_MODEL,
    torch_dtype=torch.float16,
    device_map="cpu"
)

model = PeftModel.from_pretrained(model, ADAPTER_DIR)

model = model.merge_and_unload()

model.save_pretrained(OUT_DIR, safe_serialization=True)
tokenizer.save_pretrained(OUT_DIR)

print("Merged model written to:", OUT_DIR)
