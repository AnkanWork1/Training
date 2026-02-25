from autogen import ConversableAgent

llm_config = {
    "config_list": [
        {"model": "local-model", "base_url": "http://127.0.0.1:8000/v1", "api_key": "NULL"}
    ],
    "temperature": 0.2
}

answer_agent = ConversableAgent(
    name="answer_agent",
    system_message=(
        "You are an Answer Agent. "
        "You ONLY answer using the provided summary. "
        "Use very simple words. "
        "Explain like you are talking to a beginner."
    ),
    llm_config=llm_config,
    max_consecutive_auto_reply=10
)