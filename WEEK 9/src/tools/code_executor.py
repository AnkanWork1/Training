# tools/code_executor.py

import asyncio
from autogen_core import CancellationToken
from autogen_ext.code_executors.docker import DockerCommandLineCodeExecutor
from autogen_ext.tools.code_execution import PythonCodeExecutionTool


class CodeExecutor:
    def __init__(self):
        self._executor = None
        self._tool = None
        self._started = False

    async def start(self):
        if self._started:
            return

        self._executor = DockerCommandLineCodeExecutor()
        await self._executor.start()
        self._tool = PythonCodeExecutionTool(self._executor)
        self._started = True

    async def shutdown(self):
        if self._started and self._executor is not None:
            try:
                await self._executor.stop()
            except Exception:
                # ignore docker cleanup errors
                pass
            self._started = False

    async def execute(self, python_code: str) -> str:
        if not self._started:
            await self.start()

        token = CancellationToken()

        result = await self._tool.run_json(
            {"code": python_code},
            cancellation_token=token
        )

        return self._tool.return_value_as_string(result)


# ---------------------------
# singleton
# ---------------------------

_executor_singleton = CodeExecutor()


def execute_python_snippet(code: str) -> str:
    async def _run():
        try:
            return await _executor_singleton.execute(code)
        finally:
            # IMPORTANT: stop docker before loop closes
            await _executor_singleton.shutdown()

    return asyncio.run(_run())


# ---------------------------
# CLI test
# ---------------------------

if __name__ == "__main__":
    import sys

    print("Enter python code. End with Ctrl+D:\n")
    snippet = sys.stdin.read()

    out = execute_python_snippet(snippet)
    print("\n--- OUTPUT ---")
    print(out)