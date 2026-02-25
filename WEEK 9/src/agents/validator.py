from autogen import ConversableAgent
from llm_config import llm_config

validator_agent = ConversableAgent(
    name="validator",
    system_message=(
        "You are a Validator Agent. "
        "Your job is to check the combined answer for factual errors "
        "and logical inconsistencies."
    ),
    llm_config=llm_config,
    max_consecutive_auto_reply=10
)

def validate(answer_text, memory):
    """Validate the final answer."""
    memory.append({"role": "user", "content": answer_text})
    validation = validator_agent.generate_reply(messages=list(memory))
    memory.append({"role": "assistant", "content": validation})
    return validation