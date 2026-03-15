import os
import fnmatch
import autogen


class LocalSearchAgent:
    """
    Local search agent

    Searches text inside local files.

    Expected task format:

    {
        "task_type": ["search"],
        "payload": {
            "root_dir": "data",
            "query": "Ankan",
            "patterns": ["*.txt", "*.md", "*.py", "*.csv"]
        }
    }
    """

    def __init__(self):
        self._logging_session = None

    # -------------------------
    # Optional runtime logging
    # -------------------------
    def start_logging_sqlite(self, dbname="logs.db"):
        self._logging_session = autogen.runtime_logging.start(
            config={"dbname": dbname}
        )
        return self._logging_session

    def stop_logging(self):
        try:
            autogen.runtime_logging.stop()
        except Exception:
            pass

    def run(self, task: dict):

        payload = task.get("payload", {})

        root_dir = payload.get("root_dir", ".")
        query = payload.get("query")
        patterns = payload.get("patterns", ["*.txt", "*.md", "*.py", "*.csv"])
        print(f"Searching for '{query}' in '{root_dir}' with patterns {patterns}...")
        if not query:
            return {"error": "No search query provided"}

        results = []

        for root, _, files in os.walk(root_dir):
            for file in files:
                if not any(fnmatch.fnmatch(file, p) for p in patterns):
                    continue

                path = os.path.join(root, file)

                try:
                    with open(path, "r", encoding="utf-8", errors="ignore") as f:
                        for line_no, line in enumerate(f, start=1):
                            if query.lower() in line.lower():
                                results.append(
                                    {
                                        "file": path,
                                        "line_no": line_no,
                                        "line": line.strip()
                                    }
                                )
                except Exception:
                    continue

        return results


# -------------------------
# CLI test
# -------------------------
if __name__ == "__main__":

    agent = LocalSearchAgent()
    agent.start_logging_sqlite("logs.db")

    root = input("Root directory: ").strip() or "."
    q = input("Search text: ").strip()

    task = {
        "task_type": ["search"],
        "payload": {
            "root_dir": root,
            "query": q
        }
    }

    out = agent.run(task)
    print("output:")
    for r in out:
        print(r)

    agent.stop_logging()