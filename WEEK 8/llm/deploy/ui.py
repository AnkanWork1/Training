import streamlit as st
import requests
import uuid
from datetime import datetime
import os

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

# ---------------- Page ----------------
st.set_page_config(
    page_title="Quantised LLM Console",
    layout="wide"
)

# ---------------- Style ----------------
st.markdown("""
<style>
.main-title {
    font-size: 28px;
    font-weight: 700;
    padding-bottom: 5px;
}

.sub-title {
    color: #888;
    font-size: 14px;
    margin-bottom: 15px;
}

.chat-box {
    background: #0e1117;
    border-radius: 12px;
    padding: 14px;
    height: 70vh;
    overflow-y: auto;
}

.status-bar {
    font-size: 12px;
    color: #999;
    padding-top: 6px;
}

.control-box {
    background: #111827;
    padding: 16px;
    border-radius: 12px;
}

.stChatMessage {
    padding-left: 4px;
    padding-right: 4px;
}
</style>
""", unsafe_allow_html=True)


# ---------------- Header ----------------
st.markdown('<div class="main-title">⚙ Quantised LLM – Playground</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Streaming • chat & single-shot generation</div>', unsafe_allow_html=True)


# ---------------- Session ----------------
if "chat_id" not in st.session_state:
    st.session_state.chat_id = str(uuid.uuid4())

if "messages" not in st.session_state:
    st.session_state.messages = []


# ---------------- Layout ----------------
left, right = st.columns([3.5, 1.6])


# =========================
# Chat panel
# =========================
with left:

    chat_container = st.container()

    with chat_container:
        for role, content in st.session_state.messages:
            with st.chat_message(role):
                st.markdown(content)

    user_input = st.chat_input("Send a prompt to the model...")


# =========================
# Control panel
# =========================
with right:

    st.markdown("### 🎛 Generation settings")

    with st.container():
        st.markdown('<div class="control-box">', unsafe_allow_html=True)

        mode = st.selectbox("Mode", ["Chat", "Generate"])

        system_prompt = st.text_area(
            "System prompt",
            placeholder="You are a helpful assistant…",
            height=90
        )

        temperature = st.slider("Temperature", 0.0, 1.5, 0.7, 0.1)
        top_p = st.slider("Top-p", 0.1, 1.0, 0.9, 0.05)
        top_k = st.slider("Top-k", 1, 100, 40, 1)
        max_tokens = st.slider("Max tokens", 64, 1024, 256, 32)

        col_a, col_b = st.columns(2)

        with col_a:
            clear = st.button("🧹 Clear session", use_container_width=True)

        with col_b:
            new_chat = st.button("🆕 New chat id", use_container_width=True)

        st.markdown('</div>', unsafe_allow_html=True)


# ---------------- Buttons ----------------
if clear:
    st.session_state.messages = []
    st.session_state.chat_id = str(uuid.uuid4())
    st.rerun()

if new_chat:
    st.session_state.chat_id = str(uuid.uuid4())


# =========================
# Request / streaming
# =========================
if user_input:

    st.session_state.messages.append(("user", user_input))

    payload = {
        "prompt": user_input,
        "system_prompt": system_prompt if system_prompt else None,
        "temperature": temperature,
        "top_p": top_p,
        "top_k": top_k,
        "max_tokens": max_tokens,
    }

    if mode == "Chat":
        payload["chat_id"] = st.session_state.chat_id
        endpoint = "/chat"
    else:
        endpoint = "/generate"

    with left:
        with st.chat_message("assistant"):

            placeholder = st.empty()
            full_response = ""

            try:
                with requests.post(
                    f"{BACKEND_URL}{endpoint}",
                    json=payload,
                    stream=True,
                    timeout=600
                ) as response:

                    for chunk in response.iter_content(
                        chunk_size=None,
                        decode_unicode=True
                    ):
                        if chunk:
                            full_response += chunk
                            placeholder.markdown(full_response)

            except Exception as e:
                full_response = f"❌ Backend error: {e}"
                placeholder.markdown(full_response)

    st.session_state.messages.append(("assistant", full_response))


# ---------------- Footer ----------------
with right:
    st.markdown(
        f'<div class="status-bar">Session: {st.session_state.chat_id[:8]} · '
        f'{datetime.now().strftime("%H:%M:%S")}</div>',
        unsafe_allow_html=True
    )