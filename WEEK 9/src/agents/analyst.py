from autogen import ConversableAgent


class Analyst:

    def __init__(self, llm_config):

        self.agent = ConversableAgent(
            name="analyst_agent",
            system_message="""
You are a data analyst.

Analyze information and extract insights.
""",
            llm_config=llm_config
        )

    def run(self, research):

        print("[Analyst] Analyzing information...")

        response = self.agent.generate_reply(
            messages=[{"role": "user", "content": research}]
        )

        return response