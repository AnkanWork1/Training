from uuid import uuid4
from typing import Optional, List, Dict

from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from openai import OpenAI

from deploy.config import (
    MODEL_NAME, BASE_URL, API_KEY,
    TEMPERATURE, TOP_P, TOP_K, MAX_TOKENS,
    MODEL_TYPE, DEFAULT_SYSTEM
)

from deploy.model_loader import serve_model
from deploy.logger import get_logger

# logger(in json form)

logger = get_logger()

# FastAPI App

app = FastAPI(title="Quantised LLM Server")

# Load GGUF / HF model server

serve_model(MODEL_NAME, MODEL_TYPE)

# OpenAI compatible client (llama.cpp server)

client = OpenAI(
    base_url=BASE_URL,
    api_key=API_KEY,
)

# Chat memory
CHAT_SESSIONS: Dict[str, List[dict]] = {}

# Request schema

class LLMRequest(BaseModel):
    prompt: str
    system_prompt: Optional[str] = None
    chat_id: Optional[str] = None
    temperature: float = TEMPERATURE
    top_p: float = TOP_P
    top_k: int = TOP_K
    max_tokens: int = MAX_TOKENS


# message builder

def build_messages(system_prompt: Optional[str], user_prompt: str):

    messages = []

    sys_msg = system_prompt if system_prompt else DEFAULT_SYSTEM
    messages.append({"role": "system", "content": sys_msg})

    user_prompt = (
        "Answer clearly and correctly.\n"
        f"Question: {user_prompt}"
    )

    messages.append({"role": "user", "content": user_prompt})

    return messages


# stream function

def stream_llm(messages: List[dict], req: LLMRequest, request_id: str):

    logger.info(
        "stream_start",
        extra={
            "request_id": request_id,
            "endpoint": "stream",
            "model": MODEL_NAME,
            "message_count": len(messages),
        },
    )

    stream = client.chat.completions.create(
        model=MODEL_NAME,
        messages=messages,
        temperature=req.temperature,
        top_p=req.top_p,
        max_tokens=req.max_tokens,
        extra_body={"top_k": req.top_k},
        stream=True,
    )

    for chunk in stream:
        if chunk.choices:
            delta = chunk.choices[0].delta
            if delta and delta.content:
                yield delta.content


#Single generation

@app.post("/generate")
def generate(req: LLMRequest):

    request_id = str(uuid4())

    logger.info(
        "generate_start",
        extra={"request_id": request_id, "endpoint": "/generate"},
    )

    messages = build_messages(req.system_prompt, req.prompt)

    return StreamingResponse(
        stream_llm(messages, req, request_id),
        media_type="text/plain",
    )


# infinite chat with memory

@app.post("/chat")
def chat(req: LLMRequest):

    request_id = str(uuid4())
    chat_id = req.chat_id or str(uuid4())

    history = CHAT_SESSIONS.setdefault(chat_id, [])

    if not history:
        system_text = req.system_prompt if req.system_prompt else DEFAULT_SYSTEM
        history.append({"role": "system", "content": system_text})

    messages = history + [{"role": "user", "content": req.prompt}]

    logger.info(
        "chat_start",
        extra={
            "request_id": request_id,
            "endpoint": "/chat",
            "chat_id": chat_id,
        },
    )

    def generator():

        buffer = []

        for token in stream_llm(messages, req, request_id):
            buffer.append(token)
            yield token

        history.extend([
            {"role": "user", "content": req.prompt},
            {"role": "assistant", "content": "".join(buffer)},
        ])

        logger.info(
            "chat_complete",
            extra={
                "request_id": request_id,
                "endpoint": "/chat",
                "chat_id": chat_id,
                "turns": len(history),
            },
        )

    return StreamingResponse(generator(), media_type="text/plain")