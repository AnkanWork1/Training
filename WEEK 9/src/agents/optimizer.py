from autogen import ConversableAgent


class Optimizer:

    def __init__(self, llm_config):

        self.agent = ConversableAgent(
            name="optimizer_agent",
            system_message="""
You are an optimizer.

Improve the solution based on feedback.
""",
            llm_config=llm_config
        )

    def run(self, input_text):

        print("[Optimizer] Improving solution...")

        response = self.agent.generate_reply(
            messages=[{"role": "user", "content": input_text}]
        )

        return response