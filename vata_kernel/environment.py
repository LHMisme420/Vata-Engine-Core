import os
import hashlib
from typing import Dict, Set, Optional
from vata_kernel.core import VATAEngineException

class VATAEnvironmentGuard:
    """
    VATA Environment Guard.
    Snapshots, masks, and protects host-level environment states from 
    unauthorized extraction or runtime variable mutation.
    """
    def __init__(self, sensitive_keys: Optional[Set[str]] = None):
        self._sensitive_keys = sensitive_keys or {"AWS_SECRET_ACCESS_KEY", "DATABASE_URL", "VATA_SECRET_KEY"}
        self._baseline_snapshot = self._take_snapshot()
        self._baseline_hash = self._calculate_state_hash(self._baseline_snapshot)

    def _take_snapshot(self) -> Dict[str, str]:
        """Captures a clean copy of current environment states."""
        return {k: v for k, v in os.environ.items()}

    def _calculate_state_hash(self, snapshot: Dict[str, str]) -> str:
        """Computes a deterministic hash of the environment schema to detect injection drift."""
        sorted_keys = sorted(snapshot.keys())
        serialized = "".join(f"{k}={snapshot[k]}" for k in sorted_keys)
        return hashlib.sha256(serialized.encode('utf-8')).hexdigest()

    def enforce_environment_integrity(self) -> None:
        """Validates that no out-of-band environment alterations or persistence hooks occurred."""
        current_snapshot = self._take_snapshot()
        current_hash = self._calculate_state_hash(current_snapshot)
        
        if current_hash != self._baseline_hash:
            # Locate the exact injected or modified key
            added = set(current_snapshot.keys()) - set(self._baseline_snapshot.keys())
            modified = {k for k in current_snapshot if k in self._baseline_snapshot and current_snapshot[k] != self._baseline_snapshot[k]}
            
            raise VATAEngineException(
                f"CRITICAL STATE DRIFT: Unauthorized environment modification detected! "
                f"Injected Keys: {list(added)}, Modified Keys: {list(modified)}. Terminating session."
            )

    def get_masked_environment(self) -> Dict[str, str]:
        """Returns a sanitized environment block with high-value secrets redacted for untrusted agents."""
        current = self._take_snapshot()
        for key in self._sensitive_keys:
            if key in current:
                current[key] = "[REDACTED_BY_VATA_KERNEL_SHIELD]"
        return current
