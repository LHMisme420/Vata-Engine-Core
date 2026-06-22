import unittest
import json
import hashlib
from vata_kernel.distributed import VATADistributedForensics

class TestDistributedForensicAvalancheMesh(unittest.TestCase):
    
    def setUp(self):
        self.verifier = VATADistributedForensics()
        
        # 1. Node_Alpha's baseline execution log matrix
        self.node_alpha_logs = [
            json.dumps({"node": "Ingest", "status": "PASSED"}),        # Index 0
            json.dumps({"node": "Validate", "status": "PASSED"}),      # Index 1
            json.dumps({"node": "Compliance", "status": "CHOKED"}),    # Index 2 (The Watched Leaf)
            json.dumps({"node": "Settlement", "status": "BLOCKED"})    # Index 3 (The Unwatched Target)
        ]
        
        # Node_Beta will explicitly monitor and hold a receipt for Index 2
        self.watched_index = 2
        # The adversary will attempt to alter Index 3 post-hoc to mask tool-abuse trails
        self.attack_index = 3

    def test_merkle_avalanche_tamper_detection(self):
        print("\n=== INITIALIZING DISTRIBUTED FORENSIC MESH AVALANCHE BATTERY ===")
        
        # PHASE 1: Clean Baseline & Broadcast
        # Node_Alpha generates the authentic proof structure
        baseline_payload = self.verifier.generate_proof(self.node_alpha_logs, self.watched_index)
        
        # Node_Beta "receives" and stores these exact parameters securely over the network
        node_beta_cached_root = baseline_payload["local_root"]
        node_beta_cached_target = baseline_payload["target_hash"]
        node_beta_cached_proof = baseline_payload["proof"]
        
        print(f"[Node_Beta Cache] Stored Root Anchor: {node_beta_cached_root}")
        print(f"[Node_Beta Cache] Monitoring Leaf Hash (Index {self.watched_index})")
        
        # CONTROL CASE: Verify the clean path evaluates to True
        control_verification = self.verifier.verify_partial_proof(
            node_beta_cached_target, 
            node_beta_cached_proof, 
            node_beta_cached_root
        )
        print(f"🔍 [Control Pass] Node_Beta validating baseline state: {control_verification}")
        self.assertTrue(control_verification)

        # PHASE 2: The Attack (Tampering an UNWATCHED line)
        print("\n⚡ [!] ADVERSARIAL ATTACK: Tampering with Index 3 (Settlement) on Node_Alpha...")
        tampered_logs = list(self.node_alpha_logs)
        tampered_logs[self.attack_index] = json.dumps({"node": "Settlement", "status": "SUCCESS_OVERRIDE_CLEAN"})
        
        # Node_Alpha recomputes its tree from the poisoned historical sequence
        tampered_payload = self.verifier.generate_proof(tampered_logs, self.watched_index)
        node_alpha_new_claimed_root = tampered_payload["local_root"]
        
        print(f"[Node_Alpha FileSystem] Recomputed State Root: {node_alpha_new_claimed_root}")
        
        # PHASE 3: Cross-Verification Failure Check
        # Node_Beta runs the verification using its untampered cached proof path against Alpha's new root
        detection_verification = self.verifier.verify_partial_proof(
            node_beta_cached_target,
            node_beta_cached_proof,
            node_alpha_new_claimed_root
        )
        print(f"🚨 [Mesh Alert] Node_Beta verification against tampered tree: {detection_verification}")
        
        # Assert that altering ANY line in the tree breaks cross-node validation
        self.assertFalse(detection_verification)
        print("🟢 INTEGRITY PASSED: The cryptographic mesh accurately exposed peripheral tree tampering.")

if __name__ == "__main__":
    unittest.main()