import sys
from typing import Any, Dict, List, Callable
from vata_kernel.core import VATAGatewayEngine, VATAEngineException

class VATAGovernedAgentWrapper:
    """
    Enterprise SDK Adapter Pattern.
    Wraps standard multi-agent execution loops with the VATA Kernel Engine.
    """
    def __init__(self, workspace_dir: str, vata_secret_key: bytes):
        self.kernel = VATAGatewayEngine(workspace_dir, vata_secret_key)

    def execute_governed_task(
        self, 
        session_id: str, 
        allowed_modules: List[str], 
        max_calls: int, 
        agent_run_callable: Callable[..., Any],
        *args, 
        **kwargs
    ) -> Dict[str, Any]:
        print(f"\n[VATA GATEWAY] Intercepting execution routing for Session: {session_id}")
        
        result_payload = {
            "session_id": session_id,
            "status": "FAILED",
            "merkle_root": None,
            "output": None,
            "error": None
        }

        try:
            with self.kernel.execute_session_block(
                session_id=session_id, 
                allowed_modules=allowed_modules, 
                max_calls=max_calls
            ) as session:
                
                # Execute the underlying agent task loop safely inside the context boundary
                agent_output = agent_run_callable(session, *args, **kwargs)
                
                result_payload["status"] = "SUCCESS"
                result_payload["output"] = agent_output
                
        except VATAEngineException as security_exception:
            print(f"[VATA ALERT] Hard boundary breach neutralized on Session {session_id}!")
            result_payload["error"] = str(security_exception)
            
        except Exception as runtime_error:
            print(f"[SYSTEM ERROR] Standard agent exception caught inside sandbox.")
            result_payload["error"] = f"Runtime Crash: {str(runtime_error)}"

        return result_payload
