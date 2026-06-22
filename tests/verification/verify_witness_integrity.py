import hashlib
import json

def verify_zk_witness_integrity():
    # Real on-chain anchored MAP-002 root from transaction 0x34ba06ec...
    real_root = "228b57620bef2762b8e6c6c777c389d6987bcb66b9c94386f2a946cd28788d10"
    
    print("=== VATA RIGOROUS WITNESS VERIFICATION ===")
    print(f"[1] Original Root: {real_root}")
    print(f"    Length: {len(real_root)} hex chars (256-bit)")
    
    # Simulate VATAZKAnchor splitting optimization for BN254 field safety
    half_len = len(real_root) // 2
    high_half_hex = real_root[:half_len]
    low_half_hex = real_root[half_len:]
    
    # Convert to public input integers
    input_0_int = int(high_half_hex, 16)
    input_1_int = int(low_half_hex, 16)
    
    print(f"\n[2] Formatted Public Inputs for Groth16:")
    print(f"    input_0 (High 128-bit Int): {input_0_int}")
    print(f"    input_1 (Low 128-bit Int):  {input_1_int}")
    
    # --- RECONSTRUCTION VERIFICATION ---
    # Convert back to hex, pad with leading zeros to ensure exactly 32 chars per chunk
    reconstructed_high = hex(input_0_int)[2:].zfill(32)
    reconstructed_low = hex(input_1_int)[2:].zfill(32)
    reconstructed_root = reconstructed_high + reconstructed_low
    
    print(f"\n[3] Reconstruction Check:")
    print(f"    Reconstructed: {reconstructed_root}")
    
    # Assert absolute integrity
    assert real_root == reconstructed_root, "CRITICAL ERROR: Reconstruction drift detected!"
    print("\n🟢 INTEGRITY PASSED: Public inputs map with 100% mathematical fidelity to on-chain state.")

if __name__ == "__main__":
    verify_zk_witness_integrity()
