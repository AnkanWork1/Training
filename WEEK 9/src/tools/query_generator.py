import json
import re
from autogen import ConversableAgent
from src.llm_config import llm_config


query_generator = ConversableAgent(
    name="query_generator",
    system_message="""
You are a query generator.

Your job is to analyze the user request and convert it to JSON ONLY.

You MUST decide correct task_type.

Rules:

If the request involves:
- creating or running python code -> code
- querying a database or using SQL -> sql
- reading or writing files (txt, csv, py, etc) -> file
- shell / terminal commands -> shell
- searching content / keywords in files or folders -> search

Multiple types may be used.

Return ONLY valid JSON.

Format:

{
  "task_type": ["file"],
  "payload": {...},
  "description": "..."
}

No markdown.
No comments.
No explanation.
""",
    llm_config=llm_config,
    max_consecutive_auto_reply=1,
)


def _clean_json(text: str):
    text = text.strip()

    if "```" in text:
        text = re.sub(r"```.*?\n", "", text, flags=re.DOTALL)
        text = text.replace("```", "")

    match = re.search(r"\{.*\}", text, re.DOTALL)
    if not match:
        raise ValueError("No JSON object found")

    return match.group(0)


# -------------------------------
#  VERY IMPORTANT PART
# -------------------------------

def _fix_task_type(user_query: str, task: dict) -> dict:
    """
    Heuristic correction layer so wrong LLM output
    never breaks routing.
    """

    q = user_query.lower()

    forced = set(task.get("task_type", []))

    # ---- file operations
    if any(x in q for x in ["file", "read", "write", "save", ".txt", ".csv", ".py"]):
        forced.add("file")

    # ---- searching in file / folder
    if any(x in q for x in ["find", "search", "grep", "contains", "where the word"]):
        forced.add("search")

    # ---- sql / db
    if any(x in q for x in ["sql", "database", "table", "select", "from", "where"]):
        forced.add("sql")

    # ---- python / code
    if any(x in q for x in ["python", "code", "script", "function", "program"]):
        forced.add("code")

    # ---- shell
    if any(x in q for x in ["terminal", "shell", "bash", "ls", "grep "]):
        forced.add("shell")

    if not forced:
        forced.add("code")

    task["task_type"] = sorted(forced)
    return task


# -------------------------------

def generate_task(user_query: str) -> dict:

    reply = query_generator.generate_reply(
        messages=[{"role": "user", "content": user_query}]
    )

    try:
        if isinstance(reply, dict):
            task = reply
        else:
            cleaned = _clean_json(reply)
            task = json.loads(cleaned)

    except Exception as e:
        task = {
            "task_type": [],
            "payload": {"raw_query": user_query},
            "description": f"fallback due to bad llm json: {e}"
        }

    # >>> FIX the task_type here
    task = _fix_task_type(user_query, task)

    return task