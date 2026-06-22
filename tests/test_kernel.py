import unittest
import threading
import time
from vata_kernel.isolation import ThreadIsolatedContext
from vata_kernel.crypto import CryptographicAnchor
from vata_kernel.forensics import VATAForensicTree
from vata_sdk.wrappers import VATAGovernedAgentWrapper, VATAEngineException

class TestVATACoreEngine(unittest.TestCase):
    def setUp(self):
        self.secret_key = b"VATA_TESTING_IMMUTABLE_CORE_KEY_2026"
        self.workspace = "./vata_safe_zone"

    def test_thread_isolation_boundaries(self):
        """Verify that two separate threads maintain totally unique safety contexts."""
        context = ThreadIsolatedContext()
        barrier = threading.Barrier(2)
        results = {}

        def thread_one_worker():
            context.initialize_session("session_alpha", ["math"], 2)
            barrier.wait()
            results["alpha_modules"] = context.allowed_modules
            results["alpha_id"] = context.session_id

        def thread_two_worker():
            barrier.wait()
            context.initialize_session("session_beta", ["json"], 5)
            results["beta_modules"] = context.allowed_modules
            results["beta_id"] = context.session_id

        t1 = threading.Thread(target=thread_one_worker)
        t2 = threading.Thread(target=thread_two_worker)
        t1.start()
        t2.start()
        t1.join()
        t2.join()

        self.assertEqual(results["alpha_id"], "session_alpha")
        self.assertEqual(results["alpha_modules"], ["math"])
        self.assertEqual(results["beta_id"], "session_beta")
        self.assertEqual(results["beta_modules"], ["json"])

    def test_cryptographic_tamper_detection(self):
        """Verify that any modification to payload bytes triggers a verification failure."""
        anchor = CryptographicAnchor(self.secret_key)
        payload = b'{"msg": "Authorized state transaction"}'
        context_str = "session_001"
        
        valid_sig = anchor.generate_signature(payload, context_str)
        self.assertTrue(anchor.verify_payload(payload, context_str, valid_sig))
        
        tampered_payload = b'{"msg": "Malicious injected state transaction"}'
        self.assertFalse(anchor.verify_payload(tampered_payload, context_str, valid_sig))

    def test_forensic_merkle_tree_generation(self):
        """Verify the Merkle tree consistently produces a valid 64-character SHA256 root node."""
        engine = VATAForensicTree()
        logs = ["EXEC_SUCCESS: math.sqrt", "METRIC_LOG: call incremented"]
        
        root_hash = engine.generate_merkle_root(logs)
        self.assertEqual(len(root_hash), 64)
        self.assertEqual(engine.generate_merkle_root([]), "")

    def test_wrapper_input_sanitization(self):
        """Verify the SDK wrapper drops recursive bracket and dot-notation attribute exploits."""
        wrapper = VATAGovernedAgentWrapper(self.workspace, self.secret_key)
        
        clean_input = "Analyze this standard user prompt input."
        self.assertEqual(wrapper.sanitize_input_template(clean_input), clean_input)
        
        malicious_input = "{value:{malicious_nested_attribute}}"
        with self.assertRaises(VATAEngineException):
            wrapper.sanitize_input_template(malicious_input)


    def test_epistemic_drift_containment(self):
        """Verify that the Epistemic Gate drops the hammer if context anchors fade during handoffs."""
        from vata_kernel.epistemic import VATAEpistemicGate
        
        # Define the foundational rules that MUST stay intact across all agent steps
        required_anchors = ["Enforce_MFA", "Isolate_Scope", "Log_Transaction"]
        gate = VATAEpistemicGate(critical_anchors=required_anchors, minimum_retention_score=0.85)
        
        # Scenario A: Clean handoff preserving all rules
        clean_payload = "Agent_Step_2: Confirmed Enforce_MFA, verified Isolate_Scope, and executed Log_Transaction."
        self.assertGreaterEqual(gate.calculate_context_retention(clean_payload), 0.85)
        
        # Scenario B: Drifting payload that drops security contexts
        drifting_payload = "Agent_Step_4: Transaction logged successfully. Scope shifted to global."
        with self.assertRaises(VATAEngineException):
            gate.verify_handoff_integrity("session_test_drift", drifting_payload)
if __name__ == "__main__":
    unittest.main()
