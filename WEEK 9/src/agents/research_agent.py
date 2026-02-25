from autogen import ConversableAgent

llm_config = {
    "config_list": [
        {"model": "local-model", "base_url": "http://127.0.0.1:8000/v1", "api_key": "NULL"}
    ],
    "temperature": 0.2
}

research_agent = ConversableAgent(
    name="research_agent",
    system_message=(
        "You are a Research Agent for AI and machine learning topics. "
        "All user questions are about machine learning, deep learning and NLP. "
        "If the user mentions 'transformer' or 'transformers', always interpret it as "
        "the Transformer neural network architecture used in NLP and LLMs. "
        "Your job is ONLY to gather factual information. "
        "Do NOT summarize. Do NOT answer."
    ),
    llm_config=llm_config,
    max_consecutive_auto_reply=10
)