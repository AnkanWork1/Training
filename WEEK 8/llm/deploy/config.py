import os

MODEL_NAME = os.getenv("MODEL_NAME", "/app/quantized/model.gguf")
MODEL_TYPE = os.getenv("MODEL_TYPE", "gguf")
BASE_URL = os.getenv("BASE_URL", "http://backend:8080/v1")  # inside Docker
API_KEY = os.getenv("API_KEY", "dummy")

DEFAULT_SYSTEM = (
    "You are a precise AI tutor. Answer correctly, avoid hallucinations, "
    "and stay strictly on the topic."
)
TEMPERATURE = float(os.getenv("TEMPERATURE", 0.3))
TOP_P = float(os.getenv("TOP_P", 0.9))
TOP_K = int(os.getenv("TOP_K", 40))
MAX_TOKENS = int(os.getenv("MAX_TOKENS", 128))
BACKEND_URL = os.getenv("BACKEND_URL", "http://backend:8000")
LOG_FILE = os.getenv("LOG_FILE", "logs/llm_logs.json")

# ---- Add this for llama.cpp server path ----
LLAMA_SERVER_PATH = os.getenv("LLAMA_SERVER_PATH", "/app/llama-server")