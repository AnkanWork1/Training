import argparse
import sqlite3
import sqlparse

from utils.schema_loader import load_sqlite_schema, format_schema_for_prompt
from generator.sql_generator import SQLGenerator
from memory.memory_store import ChatMemory


# -------------------------------
# Simple LLM adapter (plug yours)
# -------------------------------
import requests

class OllamaLLM:

    def __init__(self, model="qwen2.5:7b-instruct"):
        self.model = model
        self.url = "http://localhost:11434/api/generate"

    def generate(self, system: str, prompt: str) -> str:
        payload = {
            "model": self.model,
            "prompt": f"{system}\n\n{prompt}",
            "options": {
                "temperature": 0
            },
            "stream": False
        }


        r = requests.post(self.url, json=payload, timeout=120)
        r.raise_for_status()

        return r.json()["response"]

# -------------------------------
# SQL Validator
# -------------------------------
def validate_sql(sql: str, schema):
    parsed = sqlparse.parse(sql)

    if not parsed:
        raise ValueError("Invalid SQL")

    stmt = parsed[0]
    stmt_type = stmt.get_type()

    if stmt_type != "SELECT":
        raise ValueError("Only SELECT queries are allowed.")

    forbidden = ["INSERT", "UPDATE", "DELETE", "DROP", "ALTER", "TRUNCATE"]
    upper = sql.upper()

    for f in forbidden:
        if f in upper:
            raise ValueError(f"Forbidden keyword detected: {f}")

    # very important safety check
    if ";" in sql.strip()[:-1]:
        raise ValueError("Multiple statements are not allowed.")


# -------------------------------
# Safe executor
# -------------------------------
def execute_sqlite(db_path, sql):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute(sql)
    rows = cursor.fetchall()
    cols = [d[0] for d in cursor.description]

    conn.close()
    return cols, rows


# -------------------------------
# Result summarizer
# -------------------------------
def summarize_result(question, columns, rows):
    if not rows:
        return "The query returned no rows."

    summary = []

    summary.append(f"Result for: {question}")
    summary.append(f"Returned {len(rows)} rows.")

    # small table heuristic
    if len(rows) <= 10:
        for r in rows:
            row_str = ", ".join(
                f"{col}={val}" for col, val in zip(columns, r)
            )
            summary.append(row_str)
    else:
        summary.append("Showing first 5 rows:")
        for r in rows[:5]:
            row_str = ", ".join(
                f"{col}={val}" for col, val in zip(columns, r)
            )
            summary.append(row_str)

    return "\n".join(summary)


# -------------------------------
# Pipeline
# -------------------------------
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--db", required=True)
    parser.add_argument("--question", required=True)

    args = parser.parse_args()

    schema = load_sqlite_schema(args.db)
    schema_str = format_schema_for_prompt(schema)

    llm = OllamaLLM()

    generator = SQLGenerator(llm)

    sql = generator.generate(schema_str, args.question)

    print("\n===== GENERATED SQL =====")
    print(sql)

    print("\n===== VALIDATING =====")
    validate_sql(sql, schema)
    print("SQL is valid.")

    print("\n===== EXECUTING =====")
    columns, rows = execute_sqlite(args.db, sql)

    print("\n===== RESULT =====")
    print(columns)
    for r in rows:
        print(r)

    print("\n===== SUMMARY =====")
    summary = summarize_result(args.question, columns, rows)
    print(summary)



# -------------------------------------------------
# Programmatic entry for Day-5 orchestrator
# -------------------------------------------------

def run_sql_pipeline(db_path: str, question: str):

    memory = ChatMemory()

    schema = load_sqlite_schema(db_path)
    schema_str = format_schema_for_prompt(schema)

    llm = OllamaLLM()
    generator = SQLGenerator(llm)

    sql = generator.generate(schema_str, question)

    validate_sql(sql, schema)

    columns, rows = execute_sqlite(db_path, sql)

    summary = summarize_result(question, columns, rows)

    # -----------------------------
    # chat log
    # -----------------------------
    memory.add_chat(
        role=question,
        content={
            "type": "sql_pipeline",
            "sql": sql,
            "summary": summary
        }
    )

    return {
        "sql": sql,
        "columns": columns,
        "rows": rows,
        "summary": summary
    }


if __name__ == "__main__":
    main()
