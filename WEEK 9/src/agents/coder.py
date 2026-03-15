from autogen import ConversableAgent


class Coder:

    def __init__(self, llm_config):

        self.agent = ConversableAgent(
            name="coder_agent",
            system_message="""
You are a coding agent.

Your job:
Generate code solutions.

Return:
- explanation
- code block
""",
            llm_config=llm_config
        )

    def run(self, task):

        print("[Coder] Generating code...")

        response = self.agent.generate_reply(
            messages=[{"role": "user", "content": task}]
        )

        return response