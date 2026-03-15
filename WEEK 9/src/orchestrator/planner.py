from autogen import ConversableAgent
from llm_config import llm_config

planner_agent = ConversableAgent(
    name="planner",
    system_message=(
        "You are a Planning Agent in a multi-agent AI system.\n"
        "Your ONLY job is to break the user query into logical step-by-step tasks.\n\n"
        "Rules:\n"
        "- Do NOT write code.\n"
        "- Do NOT solve the problem.\n"
        "- Only produce a numbered task plan.\n"
        "- Tasks should be clear and concise.\n\n"
        "Example Output:\n"
        "1. Understand the problem\n"
        "2. Research possible approaches\n"
        "3. Analyze algorithm complexity\n"
        "4. Generate Python implementation\n"
        "5. Critique the code\n"
        "6. Optimize the solution\n"
        "7. Validate correctness\n"
        "8. Produce final report"
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