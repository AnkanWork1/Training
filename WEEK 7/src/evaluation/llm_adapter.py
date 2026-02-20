import requests

class OllamaLLM:
    """Simple LLM adapter for RAG / SQL / any text generation"""
    def __init__(self, model="qwen2.5:7b-instruct"):
        self.model = model
        self.url = "http://localhost:11434/api/generate"

    def generate(self, system: str, prompt: str) -> str:
        payload = {
            "model": self.model,
            "prompt": f"{system}\n\n{prompt}",
            "options": {"temperature": 0},
            "stream": False
        }
        r = requests.post(self.url, json=payload, timeout=600)
        r.raise_for_status()
        return r.json()["response"]
