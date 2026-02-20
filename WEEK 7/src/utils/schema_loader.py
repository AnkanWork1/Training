import sqlite3
from typing import Dict, List


def load_sqlite_schema(db_path: str) -> Dict[str, List[str]]:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';"
    )
    tables = [row[0] for row in cursor.fetchall()]

    schema = {}

    for table in tables:
        cursor.execute(f'PRAGMA table_info("{table}");')
        cols = [row[1] for row in cursor.fetchall()]
        schema[table] = cols

    conn.close()
    return schema


def format_schema_for_prompt(schema: Dict[str, List[str]]) -> str:
    lines = []
    for table, cols in schema.items():
        lines.append(f"Table {table}: {', '.join(cols)}")
    return "\n".join(lines)
