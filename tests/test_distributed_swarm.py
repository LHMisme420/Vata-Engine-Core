import unittest
from vata_kernel.distributed import VATADistributedForensics

class TestVATADistributedSwarm(unittest.TestCase):
    def test_upstream_partial_proof_propagation(self):
        """
        Simulate a remote cluster node executing transaction steps, 
        generating a partial proof path, and sending it upstream for validation.
        """
        engine = VATADistributedForensics()
        
        # Simulated remote node execution logs (e.g., Worker Node 04)
        node_logs = [
            "NODE_OP: Init process context mapping",
            "NODE_OP: Executed financial ledger read",
            "NODE_OP: Verified signature payload match",
            "NODE_OP: Prepared clearance transaction block"
        ]
        
        # We want to verify the integrity of the 3rd operation ("Verified signature payload match")
        target_index = 2
        target_log_string = node_logs[target_index]
        target_hash = engine.sha256_hash(target_log_string)
        
        # Remote node generates local root and partial execution path
        package_to_propagate = engine.generate_proof(node_logs, target_index)
        
        local_root = package_to_propagate["local_root"]
        partial_proof_path = package_to_package_proof = package_to_propagate["proof"]
        
        print(f"\n[*] Worker Node compiled Local Root: {local_root}")
        print(f"[*] Propagating {len(partial_proof_path)} partial hash steps upstream...")
        
        # Upstream Validator verifies the remote execution state without knowing the full log array
        is_verified = engine.verify_partial_proof(
            target_hash=target_hash,
            proof=partial_proof_path,
            expected_root=local_root
        )
        
        self.assertTrue(is_verified, "VATA Distributed Fault: Upstream validator failed to verify partial path integrity.")
        print("[+] Upstream Validator successfully authenticated remote node execution sequence!")

if __name__ == "__main__":
    unittest.main()
