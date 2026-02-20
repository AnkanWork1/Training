from retriever.multimodal_retriever import main as multimodal_main
from pipelines.sql_pipeline import main as sql_main
import subprocess
import sys
import json
import tempfile
import os


class RetrievalDispatcher:

    def run_text(self, query: str):
        return self._run_multimodal(query)

    def run_image(self, image_path: str):
        return self._run_multimodal(image_path)

    def run_sql(self, db: str, question: str):
        return self._run_sql_pipeline(db, question)

    # -------------------------

    def _run_multimodal(self, query):
        """
        Calls your existing CLI exactly as-is.
        No code changes in retriever.
        """

        cmd = [
            sys.executable,
            "-m",
            "retriever.multimodal_retriever",
            "--query",
            query
        ]

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True
        )

        return {
            "stdout": result.stdout,
            "stderr": result.stderr
        }

    def _run_sql_pipeline(self, db, question):

        cmd = [
            sys.executable,
            "-m",
            "pipelines.sql_pipeline",
            "--db", db,
            "--question", question
        ]

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True
        )

        return {
            "stdout": result.stdout,
            "stderr": result.stderr
        }
