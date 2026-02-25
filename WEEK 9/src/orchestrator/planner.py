from autogen import ConversableAgent
from llm_config import llm_config

planner_agent = ConversableAgent(
    name="planner",
    system_message=(
        "You are a Planner Agent. "
        "Your job is to break the user query into clear step-by-step tasks "
        "for the Worker Agents."
    ),
    llm_config=llm_config,
    max_consecutive_auto_reply=10
)

def generate_tasks(user_query, memory):
    """Generate task list from user query."""
    memory.append({"role": "user", "content": user_query})
    tasks_text = planner_agent.generate_reply(messages=list(memory))
    memory.append({"role": "assistant", "content": tasks_text})
    return tasks_text