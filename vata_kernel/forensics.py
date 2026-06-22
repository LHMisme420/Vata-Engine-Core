import hashlib
from typing import List

class VATAForensicTree:
    @staticmethod
    def _hash_pair(left: str, right: str) -> str:
        combined = (left + right).encode('utf-8')
        return hashlib.sha256(combined).hexdigest()

    def generate_merkle_root(self, execution_logs: List[str]) -> str:
        if not execution_logs:
            return ""
        current_level = [hashlib.sha256(log.encode('utf-8')).hexdigest() for log in execution_logs]
        while len(current_level) > 1:
            if len(current_level) % 2 != 0:
                current_level.append(current_level[-1])
            next_level = []
            for i in range(0, len(current_level), 2):
                parent_hash = self._hash_pair(current_level[i], current_level[i+1])
                next_level.append(parent_hash)
            current_level = next_level
        return current_level[0]
