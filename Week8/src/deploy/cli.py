import requests
import uuid

from src.deploy.config import BACKEND_URL

# Default Setting
SYSTEM_PROMPT = "You are a helpful AI assistant."
TEMPERATURE = 0.7
TOP_P = 0.9
TOP_K = 40
MAX_TOKENS = 128

print("\nQuantised LLM CLI Started")
print("Type '/exit' to quit")
print("Type '/mode chat' or '/mode generate' to switch\n")

mode = "chat"
chat_id = str(uuid.uuid4())

def stream_response(endpoint, payload):
    """Stream tokens from backend"""
    with requests.post(
        f"{BACKEND_URL}{endpoint}",
        json=payload,
        stream=True,
    ) as response:

        full_text = ""

        for chunk in response.iter_lines(decode_unicode=True):
            if not chunk:
                continue

            print(chunk, end="", flush=True)
            full_text += chunk

        print("\n")
        return full_text


while True:

    user_input = input("User > ")

    if user_input.lower() == "/exit":
        print(" Exiting CLI ")
        break

    if user_input.startswith("/mode"):
        parts = user_input.split()
        if len(parts) == 2:
            mode = parts[1]
            print(f"Mode changed to: {mode}")
        continue

    payload = {
        "prompt": user_input,
        "system_prompt": SYSTEM_PROMPT,
        "temperature": TEMPERATURE,
        "top_p": TOP_P,
        "top_k": TOP_K,
        "max_tokens": MAX_TOKENS,
    }

    if mode == "chat":
        payload["chat_id"] = chat_id
        endpoint = "/chat"
    else:
        endpoint = "/generate"

    print("Ans >", end=" ", flush=True)

    stream_response(endpoint, payload)