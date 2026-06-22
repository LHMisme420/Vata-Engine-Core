import re
from typing import Any, Dict, List, Callable
from vata_kernel.core import VATAGatewayEngine, VATAEngineException

class VATAGovernedAgentWrapper:
    """
    Upgraded Enterprise VATA SDK Adapter.
    Injects specific runtime controls to block input exploits.
    """
    def __init__(self, workspace_dir: str, vata_secret_key: bytes):
        self.kernel = VATAGatewayEngine(workspace_dir, vata_secret_key)
        # Matches nested brackets or dot-notated attribute lookups in text inputs
        self._malicious_template_pattern = re.compile(r"\{[^{}]*\{|\}\s*\}|\.[a-zA-Z_]")

    def sanitize_input_template(self, raw_input_string: str) -> str:
        """VATA Input Shield: Blocks recursive formatting hacks and attribute access tricks."""
        if self._malicious_template_pattern.search(raw_input_string):
            raise VATAEngineException(
                f"SECURITY EXCEPTION: Malicious template pattern detected in input text payload. "
                "Bypassing nested bracket evaluation hooks."
            )
        return raw_input_string

    def enforce_serialization_boundary(self, serialization_dictionary: Dict[str, Any]) -> None:
        """VATA Serialization Gate: Explicitly bans broad object allowlists."""
        if serialization_dictionary.get("allowed_objects") == "all" or "lc" in serialization_dictionary:
            raise VATAEngineException(
                "SECURITY EXCEPTION: Prohibited serialization policy configuration. "
                "Global object revival blocklists are active."
            )

    def execute_governed_task(
        self, 
        session_id: str, 
        allowed_modules: List[str], 
        max_calls: int, 
        agent_run_callable: Callable[..., Any],
        *args, 
        **kwargs
    ) -> Dict[str, Any]:
        print(f"\n[VATA GATEWAY] Activating Active Interceptors for Session: {session_id}")
        
        result_payload = {"session_id": session_id, "status": "FAILED", "output": None, "error": None}

        try:
            with self.kernel.execute_session_block(session_id, allowed_modules, max_calls) as session:
                agent_output = agent_run_callable(session, *args, **kwargs)
                result_payload["status"] = "SUCCESS"
                result_payload["output"] = agent_output
                
        except VATAEngineException as security_exception:
            print(f"[VATA ALERT] Exploit signature caught and neutralized on Session {session_id}!")
            result_payload["error"] = str(security_exception)
        except Exception as error:
            result_payload["error"] = f"Runtime Error: {str(error)}"

        return result_payload
