from collections import defaultdict, deque


class SessionMemory:
    def __init__(self, max_turns=6):
        self.store = defaultdict(lambda: deque(maxlen=max_turns))

    def add(self, session_id, role, content):
        self.store[session_id].append({
            "role": role,
            "content": content
        })

    def get(self, session_id):
        return list(self.store[session_id])
