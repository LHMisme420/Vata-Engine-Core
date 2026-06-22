import threading
from typing import List, Optional

class ThreadIsolatedContext:
    def __init__(self):
        self._local = threading.local()

    def initialize_session(self, session_id: str, allowed_modules: List[str], max_calls: int):
        self._local.session_id = session_id
        self._local.allowed_modules = allowed_modules
        self._local.max_calls = max_calls
        self._local.call_count = 0

    @property
    def session_id(self) -> Optional[str]:
        return getattr(self._local, "session_id", None)

    @property
    def allowed_modules(self) -> List[str]:
        return getattr(self._local, "allowed_modules", [])

    @property
    def call_count(self) -> int:
        return getattr(self._local, "call_count", 0)

    def increment_call_count(self) -> int:
        if not hasattr(self._local, "call_count"):
            raise RuntimeError("VATA Engine Error: Thread context invoked before initialization.")
        self._local.call_count += 1
        if self._local.call_count > getattr(self._local, "max_calls", 0):
            return False
        return True
