# memory/session_memory.py

from typing import List, Dict


class SessionMemory:

    def __init__(self):
        self._messages: List[Dict[str, str]] = []

    def add_message(self, role: str, content: str):
        self._messages.append({
            "role": role,
            "content": content
        })

    def get_messages(self) -> List[Dict[str, str]]:
        return list(self._messages)

    def last_n(self, n: int):
        return self._messages[-n:]

    def clear(self):
        self._messages = []