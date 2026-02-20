SYSTEM_PROMPT = """You are an expert data analyst.

Given the database schema below, write a single valid SQL query.

Rules:
- Use only the provided tables and columns
- If column names have spaces, wrap them in double quotes ("")
- Do not hallucinate columns
- Return only SQL
- No explanation
"""


def build_sql_prompt(schema_str: str, question: str) -> str:
    return f"""
Schema:
{schema_str}

Question:
{question}

SQL:
""".strip()


class SQLGenerator:

    def __init__(self, llm_client):
        self.llm = llm_client

    def generate(self, schema_str: str, question: str) -> str:
        prompt = build_sql_prompt(schema_str, question)

        response = self.llm.generate(
            system=SYSTEM_PROMPT,
            prompt=prompt
        )

        return self._clean(response)

    def _clean(self, text: str) -> str:
        """
        Preserve multi-line SQL.
        Only strip markdown fences and trailing junk.
        """

        text = text.strip()

        # remove ```sql fences if present
        if text.startswith("```"):
            lines = text.splitlines()
            lines = [l for l in lines if not l.strip().startswith("```")]
            if lines and lines[0].lower().strip() == "sql":
                lines = lines[1:]
            text = "\n".join(lines)

        text = text.strip()

        # very important: do NOT collapse lines
        if not text.endswith(";"):
            text = text + ";"

        return text
