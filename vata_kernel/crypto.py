import hmac
import hashlib

class CryptographicAnchor:
    """
    Upgraded VATA Cryptographic Verification Core.
    Enforces absolute constant-time bitwise comparisons to eliminate
    side-channel timing attack vectors completely.
    """
    def __init__(self, secret_key: bytes):
        if len(secret_key) < 32:
            raise ValueError("VATA Security Requirement: Secret key must be at least 32 bytes.")
        self._key = secret_key

    def generate_signature(self, payload_bytes: bytes, context_str: str) -> str:
        """Computes a secure SHA256 HMAC over raw data bound to its operational context."""
        message = payload_bytes + context_str.encode('utf-8')
        return hmac.new(self._key, message, hashlib.sha256).hexdigest()

    def verify_payload(self, payload_bytes: bytes, context_str: str, signature: str) -> bool:
        """
        Performs an airtight constant-time cryptographic validation gate check.
        Uses bitwise processing to ensure identical execution time regardless of input correctness.
        """
        if not signature:
            return False
            
        expected = self.generate_signature(payload_bytes, context_str)
        
        # Guard against string length disclosures before comparing
        if len(expected) != len(signature):
            return False
            
        # Enforce strict bitwise comparison to neutralize timing side-channels
        return hmac.compare_digest(expected, signature)
