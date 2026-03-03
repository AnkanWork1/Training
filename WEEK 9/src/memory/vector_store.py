import os
import json
import sqlite3
from datetime import datetime
from typing import Dict, List

import numpy as np
import faiss

from sklearn.feature_extraction.text import TfidfVectorizer


class VectorStore:

    def __init__(
        self,
        db_path: str = "src/memory/long_term.db",
        index_path: str = "src/memory/faiss.index"
    ):

        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        self.db_path = db_path
        self.index_path = index_path

        self.conn = sqlite3.connect(self.db_path)
        self._create_tables()

        # load all existing texts for rebuilding vectorizer
        self.texts: List[str] = self._load_all_texts()

        self.vectorizer = TfidfVectorizer(max_features=2048)

        if len(self.texts) > 0:
            X = self.vectorizer.fit_transform(self.texts)
            self.dim = X.shape[1]
            self.index = faiss.IndexFlatL2(self.dim)
            self.index.add(X.toarray().astype("float32"))
        else:
            self.dim = 2048
            self.index = faiss.IndexFlatL2(self.dim)

    # -------------------------------------------------

    def _create_tables(self):

        self.conn.execute("""
        CREATE TABLE IF NOT EXISTS memories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            type TEXT,
            content TEXT,
            summary TEXT,
            metadata TEXT
        )
        """)

        self.conn.execute("""
        CREATE TABLE IF NOT EXISTS vector_map (
            vector_id INTEGER,
            memory_id INTEGER
        )
        """)

        self.conn.commit()

    # -------------------------------------------------

    def _load_all_texts(self) -> List[str]:

        cur = self.conn.cursor()
        cur.execute("SELECT content FROM memories ORDER BY id")
        rows = cur.fetchall()
        return [r[0] for r in rows]

    # -------------------------------------------------

    def _rebuild_index(self):

        if len(self.texts) == 0:
            return

        X = self.vectorizer.fit_transform(self.texts)
        X = X.toarray().astype("float32")

        self.dim = X.shape[1]
        self.index = faiss.IndexFlatL2(self.dim)
        self.index.add(X)

    # -------------------------------------------------

    def add_memory(
        self,
        text: str,
        memory_type: str = "episodic",
        summary: str | None = None,
        metadata: Dict | None = None
    ) -> int:

        ts = datetime.utcnow().isoformat()

        cur = self.conn.cursor()

        cur.execute("""
        INSERT INTO memories(timestamp, type, content, summary, metadata)
        VALUES(?,?,?,?,?)
        """, (
            ts,
            memory_type,
            text,
            summary,
            json.dumps(metadata or {})
        ))

        memory_id = cur.lastrowid

        self.texts.append(text)

        # rebuild vectorizer + index (simple but reliable for Day-4)
        self._rebuild_index()

        vector_id = self.index.ntotal - 1

        cur.execute("""
        INSERT INTO vector_map(vector_id, memory_id)
        VALUES(?,?)
        """, (vector_id, memory_id))

        self.conn.commit()

        return memory_id

    # -------------------------------------------------

    def search(self, query: str, k: int = 5) -> List[Dict]:

        if self.index.ntotal == 0:
            return []

        qv = self.vectorizer.transform([query])
        qv = qv.toarray().astype("float32")

        k = min(k, self.index.ntotal)

        distances, indices = self.index.search(qv, k)

        cur = self.conn.cursor()
        results = []

        for vector_id, dist in zip(indices[0], distances[0]):

            cur.execute(
                "SELECT memory_id FROM vector_map WHERE vector_id=?",
                (int(vector_id),)
            )

            row = cur.fetchone()
            if not row:
                continue

            memory_id = row[0]

            cur.execute("""
            SELECT id,timestamp,type,content,summary,metadata
            FROM memories
            WHERE id=?
            """, (memory_id,))

            mem = cur.fetchone()
            if not mem:
                continue

            results.append({
                "id": mem[0],
                "timestamp": mem[1],
                "type": mem[2],
                "content": mem[3],
                "summary": mem[4],
                "metadata": json.loads(mem[5] or "{}"),
                "distance": float(dist)
            })

        return results

    # -------------------------------------------------

    def close(self):
        self.conn.close()