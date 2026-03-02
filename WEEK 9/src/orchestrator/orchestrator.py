from src.tools.code_executor import execute_python_snippet as execute_code
from src.tools.file_agent import FileAgent
from src.tools.db_agent import DBAgent
from src.tools.shell_agent import ShellAgent
from src.tools.search_agent import LocalSearchAgent


_shell = ShellAgent()
_search = LocalSearchAgent()
_file = FileAgent()
_db = DBAgent("sample.db")


def route(task: dict):

    types = task.get("task_type")

    if isinstance(types, str):
        types = [types]

    payload = task.get("payload", {})

    results = {}

    for t in types:

        t = t.lower()

        if t == "code":
            # ✔ pass only python code string
            results["code"] = execute_code(payload["code"])

        elif t == "file":
            # ✔ pass only file payload
            results["file"] = _file.run(payload)

        elif t == "sql":
            # ✔ pass only sql payload
            results["sql"] = _db.run(payload)

        elif t == "shell":
            # ✔ pass only shell payload
            results["shell"] = _shell.run(payload)

        elif t == "search":
            # ✔ pass only search payload
            results["search"] = _search.run(payload)

        else:
            results[t] = f"Unknown task type: {t}"

    return results