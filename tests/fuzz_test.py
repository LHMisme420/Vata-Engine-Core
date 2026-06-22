import unittest
import random
import string
from vata_sdk.wrappers import VATAGovernedAgentWrapper, VATAEngineException
from vata_kernel.crypto import CryptographicAnchor

class VATACoreFuzzTester(unittest.TestCase):
    def setUp(self):
        self.secret_key = b"VATA_FUZZING_RECOVERY_KEY_LONG_2026"
        self.workspace = "./vata_safe_zone"
        self.wrapper = VATAGovernedAgentWrapper(self.workspace, self.secret_key)
        self.crypto = CryptographicAnchor(self.secret_key)

    def _generate_random_garbage(self, length: int) -> str:
        """Generates completely random alphanumeric and special character sequences."""
        chars = string.ascii_letters + string.digits + "{}[].:=,噴"
        return "".join(random.choice(chars) for _ in range(length))

    def test_aggressive_input_fuzzing_matrix(self):
        print("\n[*] Starting VATA Core input shield fuzzing sequence (100 iterations)...")
        
        # Inject 100 variations of random malformed, nested, and corrupted text
        for i in range(100):
            length = random.randint(10, 500)
            payload = self._generate_random_garbage(length)
            
            # We don't care if it passes or gets blocked, we only want to guarantee 
            # that the system handles it gracefully without an unhandled system crash.
            try:
                self.wrapper.sanitize_input_template(payload)
            except VATAEngineException:
                pass  # Successfully intercepted signature fault
            except Exception as unhandled_error:
                self.fail(f"VATA Fuzzing Vulnerability: Unhandled exception type discovered! -> {type(unhandled_error).__name__}")

    def test_cryptographic_tamper_fuzzing(self):
        print("[*] Starting cryptographic anchor integrity fuzzing sequence (100 iterations)...")
        
        base_payload = b'{"transaction_id": 999}'
        context = "fuzz_context"
        valid_sig = self.crypto.generate_signature(base_payload, context)
        
        for _ in range(100):
            # Mutate random bytes inside the payload or randomize the signature entirely
            fuzzed_sig = "".join(random.choice(string.hexdigits) for _ in range(len(valid_sig)))
            
            # Ensure the gate safely returns False without breaking bitwise loops
            is_valid = self.crypto.verify_payload(base_payload, context, fuzzed_sig)
            self.assertFalse(is_valid)

if __name__ == "__main__":
    unittest.main()
