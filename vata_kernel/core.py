import sys
from pathlib import Path
from typing import Any, Dict, List, Optional
from .isolation import ThreadIsolatedContext
from .crypto import CryptographicAnchor
from .forensics import VATAForensicTree

class VATAEngineException(Exception):
    """Raised when an active security parameter is breached or unauthenticated."""
    pass

class VATAGatewayEngine:
    """
    The Central VATA Kernel Supervisor.
    Orchestrates thread-isolation planes and cryptographic validation logic.
    """
    def __init__(self, safe_workspace_dir: str, secret_key: bytes):
        self.workspace = Path(safe_workspace_dir).resolve()
        self.isolation_plane = ThreadIsolatedContext()
        self.crypto_plane = CryptographicAnchor(secret_key)
        self.forensic_plane = VATAForensicTree()

    def execute_session_block(self, session_id: str, allowed_modules: List[str], max_calls: int):
        return VATASessionBoundary(self, session_id, allowed_modules, max_calls)


class VATASessionBoundary:
    def __init__(self, engine: VATAGatewayEngine, session_id: str, allowed_modules: List[str], max_calls: int):
        self.engine = engine
        self.session_id = session_id
        self.allowed_modules = allowed_modules
        self.max_calls = max_calls
        self.log_buffer: List[str] = []

    def __enter__(self):
        self.engine.isolation_plane.initialize_session(
            session_id=self.session_id,
            allowed_modules=self.allowed_modules,
            max_calls=self.max_calls
        )
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.log_buffer:
            root_badge = self.engine.forensic_plane.generate_merkle_root(self.log_buffer)
            print(f"\n[***] SFS FORENSIC ENGINE: Session [{self.session_id}] compiled successfully.")
            print(f"[***] IMMUTABLE MERKLE ROOT BADGE: {root_badge}")
        self.engine.isolation_plane.initialize_session("", [], 0)

    def intercept_module_invocation(self, target_module_name: str) -> None:
        base_module = target_module_name.split('.')[0]
        if base_module not in self.engine.isolation_plane.allowed_modules:
            raise VATAEngineException(
                f"CRITICAL FAULT: Session [{self.session_id}] attempted unauthorized module: '{target_module_name}'"
            )
        self.log_buffer.append(f"EXEC_SUCCESS: Isolated invocation of module -> {target_module_name}")

    def verify_and_log_call(self) -> None:
        within_bounds = self.engine.isolation_plane.increment_call_count()
        if not within_bounds:
            raise VATAEngineException(
                f"EXHAUSTED RESOURCE: Session [{self.session_id}] overflowed limit: {self.max_calls}"
            )
        self.log_buffer.append(f"METRIC_LOG: Verified operational tracking counter iteration incremented.")
