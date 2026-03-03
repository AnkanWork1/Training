# src/llm_client.py

import requests


class LLMClient:

    def __init__(self, llm_config: dict):

        cfg = llm_config["config_list"][0]

        self.base_url = cfg["base_url"].rstrip("/")
        self.model = cfg["model"]
        self.max_tokens = cfg.get("max_tokens", 256)
        self.api_key = cfg.get("api_key", "none")

    def generate(self, prompt: str) -> str:

        url = f"{self.base_url}/chat/completions"

        payload = {
            "model": self.model,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "max_tokens": self.max_tokens
        }

        headers = {
            "Content-Type": "application/json"
        }

        r = requests.post(url, json=payload, headers=headers, timeout=300)
        r.raise_for_status()

        data = r.json()

        return data["choices"][0]["message"]["content"]