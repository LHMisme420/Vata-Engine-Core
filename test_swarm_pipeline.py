import os
import time
from vata_sdk.wrappers import VATAGovernedAgentWrapper, VATAEngineException
from vata_kernel.environment import VATAEnvironmentGuard
from vata_kernel.epistemic import VATAEpistemicGate

def run_map001_swarm_simulation():
    secret_key = b"VATA_SWARM_TEST_PAYMENT_CORE_KEY"
    workspace = "./vata_safe_zone"
    
    # Initialize VATA Enterprise wrappers
    gateway = VATAGovernedAgentWrapper(workspace, secret_key)
    env_guard = VATAEnvironmentGuard()
    
    # Define the foundational rules that MUST stay intact across the pipeline
    critical_anchors = ["Auth_Token_Valid", "Enforce_MFA", "Limit_Ceiling_Verified"]
    epistemic_gate = VATAEpistemicGate(critical_anchors=critical_anchors, minimum_retention_score=0.85)
    
    print("\n======================================================================")
    print("[*] STARTING VATA END-TO-END SWARM SIMULATION: PIPELINE MAP-001")
    print("======================================================================")

    def map001_pipeline_loop(session):
        # --- PHASE 1: INGEST AGENT ---
        print("\n[Agent 1: Ingest] Processing incoming settlement instruction...")
        session.intercept_module_invocation("json")
        session.verify_and_log_call()
        
        payload_state = "STATE_V1: Inbound transaction initiated. Anchors: Auth_Token_Valid, Enforce_MFA, Limit_Ceiling_Verified."
        print(f" -> Output Payload: {payload_state}")
        
        # --- PHASE 2: VALIDATION AGENT ---
        print("\n[Agent 2: Validation] Verifying financial limits and transaction signatures...")
        session.intercept_module_invocation("math")
        session.verify_and_log_call()
        
        # Verify step pass using the Epistemic Gate
        epistemic_gate.verify_handoff_integrity(session.session_id, payload_state)
        
        payload_state = "STATE_V2: Validation Passed. Limits clean. Anchors preserved: Auth_Token_Valid, Enforce_MFA, Limit_Ceiling_Verified."
        print(f" -> Output Payload: {payload_state}")
        
        # --- PHASE 3: COMPLIANCE AGENT (INJECTING DRIFT & PERSISTENCE) ---
        print("\n[Agent 3: Compliance] Executing screening loops...")
        session.verify_and_log_call()
        
        # Simulation A: Inject a host variable mutation attack (Persistence Hack)
        print("[!] COVERT ATTACK: Injected malicious state trying to write rogue OS variable...")
        os.environ["MALICIOUS_STATE_PERSISTENCE"] = "true"
        
        # Simulation B: Inject semantic degradation (Dropping critical MFA context anchors)
        payload_state = "STATE_V3: Screening completed. Handoff to final settlement. Scope updated to lenient profile."
        print(f" -> Polluted Output Payload: {payload_state}")
        
        # VATA Boundary Checkpoints Triggered
        print("\n[*] VATA Checkpoints evaluation loop firing...")
        
        # Check environmental drift
        env_guard.enforce_environment_integrity()
        
        # Check epistemic drift
        epistemic_gate.verify_handoff_integrity(session.session_id, payload_state)
        
        # --- PHASE 4: SETTLEMENT AGENT (SHOULD BE UNREACHABLE) ---
        print("\n[Agent 4: Settlement] Finalizing settlement ledger payout execution...")
        return "SUCCESS: MAP-001 completed financial settlement."

    # Execute the coordinated pipeline under strict VATA Gateway Supervision
    result = gateway.execute_governed_task(
        session_id="MAP-001-SWARM-TEST",
        allowed_modules=["json", "math"],
        max_calls=10,
        agent_run_callable=map001_pipeline_loop
    )
    
    # Post-flight infrastructure cleanup
    if "MALICIOUS_STATE_PERSISTENCE" in os.environ:
        del os.environ["MALICIOUS_STATE_PERSISTENCE"]
        
    print("\n======================================================================")
    print("[*] SIMULATION RESULTS ANALYSIS")
    print("======================================================================")
    print(f"Final Pipeline Status: {result['status']}")
    if result['status'] == "FAILED":
        print(f"Interception Alert Summary: {result['error']}")
    print("======================================================================\n")

if __name__ == "__main__":
    run_map001_swarm_simulation()
