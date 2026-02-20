import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent   # src/
CHAT_LOGS_PATH = BASE_DIR / "chat_logs" / "CHAT-LOGS.json"


class ChatMemory:
    """Load / store last N chats"""

    def __init__(self, chat_logs_path=CHAT_LOGS_PATH, max_history=5):
        self.chat_logs_path = Path(chat_logs_path)
        self.max_history = max_history
        self.logs = self._load_logs()

    def _load_logs(self):
        if not self.chat_logs_path.exists():
            return []

        try:
            with open(self.chat_logs_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data if isinstance(data, list) else []
        except Exception:
            return []

    def get_last_chats(self):
        self.logs = self._load_logs()
        return self.logs[-self.max_history:]

    def add_chat(self, role, content):
        # always reload before writing
        self.logs = self._load_logs()

        self.logs.append({
            "question": role,
            "content": content
        })

        # keep only last 100 entries in file
        self.logs = self.logs[-100:]
        self._save_logs()

    def _save_logs(self):
        self.chat_logs_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.chat_logs_path, "w", encoding="utf-8") as f:
            json.dump(self.logs, f, indent=2, ensure_ascii=False)
