from autogen import ConversableAgent
from llm_config import llm_config

reflection_agent = ConversableAgent(
    name="reflection",
    system_message=(
        "You are a Reflection Agent. "
        "Your job is to review the outputs of the Worker Agents, "
        "combine them, improve clarity, and remove inconsistencies."
    ),
    llm_config=llm_config,
    max_consecutive_auto_reply=10
)

def reflect(worker_outputs, memory):
    """Combine and improve worker outputs."""
    memory.append({"role": "user", "content": "\n".join(worker_outputs)})
    reflection = reflection_agent.generate_reply(messages=list(memory))
    memory.append({"role": "assistant", "content": reflection})
    return reflection