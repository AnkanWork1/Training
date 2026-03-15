from autogen import ConversableAgent


class Critic:

    def __init__(self, llm_config):

        self.agent = ConversableAgent(
            name="critic_agent",
            system_message="""
You are a critic.

Your job:
Find problems in the solution.

Return:
- mistakes
- missing parts
- suggestions
""",
            llm_config=llm_config
        )

    def run(self, solution):

        print("[Critic] Reviewing solution...")

        response = self.agent.generate_reply(
            messages=[{"role": "user", "content": solution}]
        )

        return response