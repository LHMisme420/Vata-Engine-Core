import hmac
import hashlib

class CryptographicAnchor:
    def __init__(self, secret_key: bytes):
        if len(secret_key) < 32:
            raise ValueError("VATA Security Requirement: Secret key must be at least 32 bytes.")
        self._key = secret_key

    def generate_signature(self, payload_bytes: bytes, context_str: str) -> str:
        message = payload_bytes + context_str.encode('utf-8')
        return hmac.new(self._key, message, hashlib.sha256).hexdigest()

    def verify_payload(self, payload_bytes: bytes, context_str: str, signature: str) -> bool:
        if not signature:
            return False
        expected = self.generate_signature(payload_bytes, context_str)
        return hmac.compare_digest(expected, signature)
