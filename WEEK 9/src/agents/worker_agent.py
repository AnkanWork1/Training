from autogen import ConversableAgent
from llm_config import llm_config

worker_agent = ConversableAgent(
    name="worker",
    system_message=(
        "You are a Worker Agent. "
        "Your job is to execute one task from the Planner. "
        "Provide factual outputs only."
    ),
    llm_config=llm_config,
    max_consecutive_auto_reply=10
)

def run_task(task_text, memory):
    """Run a single task and return output."""
    memory.append({"role": "user", "content": task_text})
    result = worker_agent.generate_reply(messages=list(memory))
    memory.append({"role": "assistant", "content": result})
    return result