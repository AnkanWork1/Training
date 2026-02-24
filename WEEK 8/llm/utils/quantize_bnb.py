import os
import time
import subprocess
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
from peft import PeftModel

from pathlib import Path

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel


# -----------------------------
# Config
# -----------------------------

MODEL_NAME  = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
ADAPTER_DIR = "/content/week8/MyDrive/Week 8/llm/adapters/checkpoint-81"

MERGED_DIR  = "/content/week8/MyDrive/Week 8/llm/merged-fp16"
INT8_DIR    = "/content/week8/MyDrive/Week 8/llm/quantized/model-int8"
INT4_DIR    = "/content/week8/MyDrive/Week 8/llm/quantized/model-int4"
GGUF_PATH   = "/content/week8/MyDrive/Week 8/llm/quantized/model.gguf"
REPORT_PATH = "/content/week8/MyDrive/Week 8/llm/QUANTISATION-REPORT.md"

PROMPT = "Explain quantization in simple words."


# -----------------------------
# Utilities
# -----------------------------

def ensure_dir(path: str):
    Path(path).mkdir(parents=True, exist_ok=True)


def folder_size_mb(path: str) -> float:
    total = 0
    for p in Path(path).rglob("*"):
        if p.is_file():
            total += p.stat().st_size
    return total / 1024 / 1024


def measure_generation_time(model, tokenizer, max_new_tokens=128):
    inputs = tokenizer(PROMPT, return_tensors="pt").to(model.device)

    if torch.cuda.is_available():
        torch.cuda.synchronize()

    t0 = time.time()
    with torch.no_grad():
        model.generate(**inputs, max_new_tokens=max_new_tokens)

    if torch.cuda.is_available():
        torch.cuda.synchronize()

    return time.time() - t0


# -----------------------------
# Step 1 : merge LoRA
# -----------------------------

def merge_lora_to_fp16(
    base_model_name: str,
    adapter_dir: str,
    output_dir: str
):
    ensure_dir(output_dir)

    base = AutoModelForCausalLM.from_pretrained(
        base_model_name,
        torch_dtype=torch.float16,
        device_map="auto"
    )

    model = PeftModel.from_pretrained(base, adapter_dir)
    model = model.merge_and_unload()

    tokenizer = AutoTokenizer.from_pretrained(
        base_model_name,
        use_fast=False
    )

    model.save_pretrained(output_dir, safe_serialization=True)
    tokenizer.save_pretrained(output_dir)

    return output_dir



# -----------------------------
# Step 2 : INT8
# -----------------------------

def quantize_int8(merged_dir: str, out_dir: str):
    ensure_dir(out_dir)

    bnb_config = BitsAndBytesConfig(
        load_in_8bit=True
    )

    model = AutoModelForCausalLM.from_pretrained(
        merged_dir,
        quantization_config=bnb_config,
        device_map="auto"
    )

    tokenizer = AutoTokenizer.from_pretrained(merged_dir)

    t = measure_generation_time(model, tokenizer)

    model.save_pretrained(out_dir)
    tokenizer.save_pretrained(out_dir)

    return t



# -----------------------------
# Step 3 : INT4
# -----------------------------

def quantize_int4(merged_dir: str, out_dir: str):
    ensure_dir(out_dir)

    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_compute_dtype=torch.float16,
        bnb_4bit_quant_type="nf4"
    )

    model = AutoModelForCausalLM.from_pretrained(
        merged_dir,
        quantization_config=bnb_config,
        device_map="auto"
    )

    tokenizer = AutoTokenizer.from_pretrained(merged_dir)

    t = measure_generation_time(model, tokenizer)

    model.save_pretrained(out_dir)
    tokenizer.save_pretrained(out_dir)

    return t



# -----------------------------
# Step 4 : GGUF (q4_0)
# -----------------------------

def build_llama_cpp():
    if not Path("llama.cpp").exists():
        subprocess.check_call(
            ["git", "clone", "https://github.com/ggerganov/llama.cpp.git"]
        )

    subprocess.check_call(
        ["pip", "install", "-r", "llama.cpp/requirements.txt"]
    )

    build_dir = Path("llama.cpp/build")
    if not build_dir.exists():
        build_dir.mkdir(parents=True, exist_ok=True)
        subprocess.check_call(
            ["cmake", "-S", "llama.cpp", "-B", "llama.cpp/build"]
        )
        subprocess.check_call(
            ["cmake", "--build", "llama.cpp/build", "--config", "Release"]
        )


def convert_to_gguf_q4(merged_dir: str, out_gguf: str):
    build_llama_cpp()

    fp16_gguf = "/content/model-fp16.gguf"

    subprocess.check_call([
        "python",
        "llama.cpp/convert_hf_to_gguf.py",
        merged_dir,
        "--outfile",
        fp16_gguf
    ])

    subprocess.check_call([
        "llama.cpp/build/bin/llama-quantize",
        fp16_gguf,
        out_gguf,
        "q4_0"
    ])


# -----------------------------
# Step 5 : report
# -----------------------------

def write_report(
    merged_dir,
    int8_dir,
    int4_dir,
    gguf_path,
    t_int8,
    t_int4,
    report_path
):
    with open(report_path, "w") as f:
        f.write("# Quantisation report\n\n")
        f.write("| Format | Size (MB) | Generation time (128 tokens, s) |\n")
        f.write("|-------|-----------|----------------------------------|\n")
        f.write(f"| FP16 | {folder_size_mb(merged_dir):.2f} | baseline |\n")
        f.write(f"| INT8 | {folder_size_mb(int8_dir):.2f} | {t_int8:.2f} |\n")
        f.write(f"| INT4 | {folder_size_mb(int4_dir):.2f} | {t_int4:.2f} |\n")
        f.write(
            f"| GGUF (q4_0) | {Path(gguf_path).stat().st_size / 1024 / 1024:.2f} | n/a |\n"
        )


# -----------------------------
# Orchestration only
# -----------------------------

def run_pipeline():

    ensure_dir("/content/quantized")

    merge_lora_to_fp16(
        MODEL_NAME,
        ADAPTER_DIR,
        MERGED_DIR
    )

    t8 = quantize_int8(MERGED_DIR, INT8_DIR)
    t4 = quantize_int4(MERGED_DIR, INT4_DIR)

    convert_to_gguf_q4(MERGED_DIR, GGUF_PATH)

    write_report(
        MERGED_DIR,
        INT8_DIR,
        INT4_DIR,
        GGUF_PATH,
        t8,
        t4,
        REPORT_PATH
    )


if __name__ == "__main__":
    run_pipeline()
