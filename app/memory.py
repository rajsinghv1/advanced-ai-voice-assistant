
from typing import Dict, List
from threading import Lock

class ConversationMemory:
    def __init__(self):
        self.sessions: Dict[str, List[dict]] = {}
        self.lock = Lock()

    def get_history(self, session_id: str):
        with self.lock:
            return self.sessions.get(session_id, []).copy()

    def add_message(self, session_id: str, role: str, content: str):
        with self.lock:
            if session_id not in self.sessions:
                self.sessions[session_id] = []

            self.sessions[session_id].append({
                "role": role,
                "content": content
            })

    def clear_history(self, session_id: str):
        with self.lock:
            self.sessions.pop(session_id, None)


memory = ConversationMemory()
