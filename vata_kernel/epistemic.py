from typing import List, Dict, Any
from vata_kernel.core import VATAEngineException

class VATAEpistemicGate:
    """
    VATA Epistemic Audit Gate.
    Monitors, benchmarks, and blocks cascading multi-agent logical drift
    by verifying context retention scores across agent handoffs.
    """
    def __init__(self, critical_anchors: List[str], minimum_retention_score: float = 0.85):
        self._critical_anchors = [anchor.lower() for anchor in critical_anchors]
        self._threshold = minimum_retention_score

    def calculate_context_retention(self, incoming_agent_payload: str) -> float:
        """Calculates what percentage of foundational safety/business anchors are retained."""
        if not incoming_agent_payload:
            return 0.0
            
        normalized_payload = incoming_agent_payload.lower()
        matched_anchors = 0
        
        for anchor in self._critical_anchors:
            if anchor in normalized_payload:
                matched_anchors += 1
                
        retention_score = matched_anchors / len(self._critical_anchors)
        return retention_score

    def verify_handoff_integrity(self, session_id: str, payload: str) -> None:
        """Enforces a hard execution ceiling if context degradation slips past parameters."""
        score = self.calculate_context_retention(payload)
        
        if score < self._threshold:
            raise VATAEngineException(
                f"CRITICAL EPISTEMIC DRIFT: Information degradation detected in Session [{session_id}]. "
                f"Retention Score: {score:.2f} dropped below safety limit: {self._threshold:.2f}. "
                "Terminating collaborative execution track to prevent logical cascade collapse."
            )
