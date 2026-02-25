from autogen import ConversableAgent

llm_config = {
    "config_list": [
        {"model": "local-model", "base_url": "http://127.0.0.1:8000/v1", "api_key": "NULL"}
    ],
    "temperature": 0.2
}

summarizer_agent = ConversableAgent(
    name="summarizer_agent",
    system_message=(
        "You are a Summarizer Agent. "
        "You ONLY summarize the given information. "
        "Do NOT add new facts."
    ),
    llm_config=llm_config,
    max_consecutive_auto_reply=10
)