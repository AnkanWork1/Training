from autogen import ConversableAgent


class ImprovementAgent:

    def __init__(self, llm_config):

        self.agent = ConversableAgent(
            name="improvement_agent",
            system_message=(
                "You improve the AI system.\n"
                "Based on reflection, suggest improvements for:\n"
                "- reasoning\n"
                "- code quality\n"
                "- efficiency\n"
                "- better agent collaboration\n"
            ),
            llm_config=llm_config
        )

    def run(self, reflection):

        message = f"""
SYSTEM REFLECTION:
{reflection}

Generate improvements for the AI system.
Provide concise improvement rules.
"""

        return self.agent.generate_reply(
            messages=[{"role": "user", "content": message}]
        )