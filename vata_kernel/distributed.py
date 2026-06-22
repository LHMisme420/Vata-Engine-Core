import hashlib
from typing import List, Dict, Any

class VATADistributedForensics:
    """
    Distributed Forensic Engine for VATA Clustered Operations.
    Computes local state roots and generates cryptographic partial paths (Merkle Proofs)
    to verify remote node execution integrity without transmitting raw text logs.
    """
    @staticmethod
    def sha256_hash(data: str) -> str:
        return hashlib.sha256(data.encode('utf-8')).hexdigest()

    def generate_proof(self, logs: List[str], target_index: int) -> Dict[str, Any]:
        """
        Generates a local Merkle Root and a partial audit path (proof) 
        for a specific log index to propagate upstream.
        """
        if not logs or target_index >= len(logs):
            return {"root": "", "proof": []}

        # Calculate initial leaf hashes
        leaves = [self.sha256_hash(log) for log in logs]
        target_hash = leaves[target_index]
        
        proof = []
        current_level = leaves
        idx = target_index

        while len(current_level) > 1:
            if len(current_level) % 2 != 0:
                current_level.append(current_level[-1])
            
            next_level = []
            for i in range(0, len(current_level), 2):
                combined = current_level[i] + current_level[i+1]
                parent_hash = hashlib.sha256(combined.encode('utf-8')).hexdigest()
                next_level.append(parent_hash)
                
                # Capture the sibling hash along the target path
                if i <= idx <= i + 1:
                    sibling_idx = i + 1 if idx == i else i
                    proof.append({
                        "hash": current_level[sibling_idx],
                        "position": "right" if sibling_idx > idx else "left"
                    })
            
            current_level = next_level
            idx //= 2

        return {
            "local_root": current_level[0],
            "target_hash": target_hash,
            "proof": proof
        }

    @classmethod
    def verify_partial_proof(cls, target_hash: str, proof: List[Dict[str, str]], expected_root: str) -> bool:
        """
        Validator-Side Check: Reconstructs a Merkle Root using only a single leaf hash 
        and its partial proof trajectory to confirm remote integrity.
        """
        current_hash = target_hash
        for sibling in proof:
            if sibling["position"] == "right":
                combined = current_hash + sibling["hash"]
            else:
                combined = sibling["hash"] + current_hash
            current_hash = hashlib.sha256(combined.encode('utf-8')).hexdigest()
            
        return hmac_compare := (current_hash == expected_root)
