import subprocess
import autogen


class ShellAgent:
    """
    Shell agent
    -----------
    Only executes shell commands.
    No LLM.
    Used by orchestrator.

    Expected task format:

    {
        "task_type": ["shell"],
        "payload": {
            "command": "ls -l"
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

    # -------------------------
    # main run
    # -------------------------
    def run(self, task: dict):

        payload = task.get("payload", {})
        command = payload.get("command")

        if not command:
            return {"error": "No shell command provided"}

        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True
            )

            return {
                "returncode": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr
            }

        except Exception as e:
            return {"error": str(e)}


# -------------------------
# CLI test
# -------------------------
if __name__ == "__main__":

    agent = ShellAgent()
    agent.start_logging_sqlite("logs.db")

    while True:
        cmd = input("\nShell command (or exit): ").strip()
        if cmd.lower() == "exit":
            break

        task = {
            "task_type": ["shell"],
            "payload": {
                "command": cmd
            }
        }

        out = agent.run(task)
        print(out)

    agent.stop_logging()