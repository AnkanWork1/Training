MODEL_NAME = "/home/omjidubey/Desktop/Training/Week8/src/quantized/model.gguf"
MODEL_TYPE = "gguf"

BASE_URL = "http://127.0.0.1:8080/v1"
API_KEY = "dummy"

DEFAULT_SYSTEM = (
    "You are a precise AI tutor. "
    "Answer correctly, avoid hallucinations, "
    "and stay strictly on the topic."
)

TEMPERATURE = 0.3
TOP_P = 0.9
TOP_K = 40
MAX_TOKENS = 128

BACKEND_URL = "http://127.0.0.1:8000"

LOG_FILE = "src/logs/llm_logs.json"