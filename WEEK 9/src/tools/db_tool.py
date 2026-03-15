import sqlite3
import autogen


class DBAgent:
    """
    DB Agent
    --------
    Only executes SQL.
    No text to SQL conversion.
    Orchestrator must send proper SQL in task payload.
    Supports AutoGen runtime logging.
    """

    def __init__(self, db_path: str):
        self.db_path = "/home/ankanguha/Desktop/Training/WEEK 7/src/data/db/customers.db"
        self._logging_session_id = None

    # -----------------------------
    # Runtime logging helpers
    # -----------------------------
    def start_logging_sqlite(self, dbname="logs.db"):
        self._logging_session_id = autogen.runtime_logging.start(
            config={"dbname": dbname}
        )
        return self._logging_session_id

    def stop_logging(self):
        autogen.runtime_logging.stop()

    # -----------------------------
    # Core runner
    # -----------------------------
    def run(self, task: dict):
        """
        task format:

        {
          "task_type": ["sql"],
          "payload": {
              "sql": "SELECT * FROM table_name"
          }
        }
        """

        payload = task.get("payload", {})

        sql = payload.get("sql") or payload.get("sql_query")

        if not sql:
            return "[DB_AGENT] No SQL provided in task payload."

        try:
            conn = sqlite3.connect(self.db_path)
            cur = conn.cursor()

            cur.execute(sql)

            # If SELECT, return rows
            if sql.strip().lower().startswith("select"):
                columns = [desc[0] for desc in cur.description]
                rows = cur.fetchall()

                result = [
                    dict(zip(columns, row)) for row in rows
                ]

                conn.close()
                return result

            # Otherwise commit (insert / update / delete / create)
            conn.commit()
            affected = cur.rowcount
            conn.close()

            return {
                "status": "ok",
                "rows_affected": affected
            }

        except Exception as e:
            return f"[DB_AGENT ERROR] {e}"


# -----------------------------
# Simple CLI test
# -----------------------------
if __name__ == "__main__":

    agent = DBAgent("sample.db")

    agent.start_logging_sqlite("logs.db")

    # create table
    print(agent.run({
        "task_type": ["sql"],
        "payload": {
            "sql": """
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY,
                name TEXT,
                price INTEGER
            )
            """
        }
    }))

    # insert
    print(agent.run({
        "task_type": ["sql"],
        "payload": {
            "sql": "INSERT INTO products(name,price) VALUES ('pen',10)"
        }
    }))

    # select
    print(agent.run({
        "task_type": ["sql"],
        "payload": {
            "sql": "SELECT * FROM products"
        }
    }))

    agent.stop_logging()