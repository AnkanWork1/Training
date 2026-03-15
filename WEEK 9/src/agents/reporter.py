from autogen import ConversableAgent

class Reporter:

    def __init__(self, llm_config):

        self.agent = ConversableAgent(
            name="reporter",
            system_message=(
                "You are the final reporting agent of a multi-agent AI system.\n"
                "Generate the final answer for the user.\n\n"
                "If the task is coding:\n"
                "- ALWAYS include the final code.\n"
                "- Show the code first.\n"
                "- Then explain briefly."
            ),
            llm_config=llm_config
        )

    def run(self,query, plan, research, analysis, code, improved, validation):

        print("[Reporter] Generating final report...")

        message = f"""

        User Query:
{query}
PLAN:
{plan}

RESEARCH:
{research}

ANALYSIS:
{analysis}

ORIGINAL CODE:
{code}

IMPROVED CODE:
{improved}

VALIDATION:
{validation}

Generate the FINAL answer for the user.
If this is a coding task, include the final code.
"""

        return self.agent.generate_reply(
            messages=[{"role": "user", "content": message}]
        )