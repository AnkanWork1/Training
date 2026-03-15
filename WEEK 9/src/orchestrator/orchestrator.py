from tools.code_executor import execute_python_snippet as execute_code
from tools.file_tool import FileAgent
from tools.db_tool import DBAgent
from tools.shell_tool import ShellAgent
from tools.search_tool import LocalSearchAgent


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