"""
POC: HMAC — Hash-based Message Authentication Code

Run this file and watch each attack succeed or fail.
Each section is a self-contained experiment.
"""

import hmac
import hashlib
import json

SEP = "-" * 55


# ═══════════════════════════════════════════════════════════
# EXPERIMENT 1 — Plain hash offers ZERO tamper protection
#
# Attacker intercepts: message + hash
# Attacker changes message, recomputes hash → undetectable
# ═══════════════════════════════════════════════════════════

def experiment_1_plain_hash_is_broken():
    print(SEP)
    print("EXPERIMENT 1 — Plain hash (SHA256) — attacker wins")
    print(SEP)

    message  = b'{"amount": 100, "to": "alice"}'
    digest   = hashlib.sha256(message).hexdigest()

    print(f"  Original message : {message}")
    print(f"  SHA256 hash      : {digest[:20]}...")

    # Attacker intercepts both. Changes message. Recomputes hash.
    tampered = b'{"amount": 99999, "to": "mallory"}'
    forged   = hashlib.sha256(tampered).hexdigest()

    print(f"\n  [ATTACKER] tampered message : {tampered}")
    print(f"  [ATTACKER] forged hash      : {forged[:20]}...")

    # Receiver checks: does hash match message?
    received_ok = hashlib.sha256(tampered).hexdigest() == forged
    print(f"\n  Receiver thinks message is valid: {received_ok}")  # True — attack works!
    print("  → Plain hash FAILS. Attacker forged it successfully.")


# ═══════════════════════════════════════════════════════════
# EXPERIMENT 2 — HMAC stops the attacker
#
# Now the hash requires a SECRET KEY.
# Attacker can change the message but CANNOT recompute the HMAC
# without the key → receiver detects tampering.
# ═══════════════════════════════════════════════════════════

def experiment_2_hmac_stops_attacker():
    print(f"\n{SEP}")
    print("EXPERIMENT 2 — HMAC — attacker fails")
    print(SEP)

    secret_key = b"super-secret-key-never-share"
    message    = b'{"amount": 100, "to": "alice"}'

    # Sender computes HMAC
    tag = hmac.new(secret_key, message, hashlib.sha256).hexdigest()
    print(f"  Original message : {message}")
    print(f"  HMAC tag         : {tag[:20]}...")

    # Attacker intercepts, changes message
    tampered = b'{"amount": 99999, "to": "mallory"}'

    # Attacker tries to forge HMAC — but has no key
    # Best they can do: use plain sha256 (won't match)
    forged_attempt = hashlib.sha256(tampered).hexdigest()
    print(f"\n  [ATTACKER] tampered  : {tampered}")
    print(f"  [ATTACKER] forged tag: {forged_attempt[:20]}...")

    # Receiver: recompute HMAC of tampered message with real key
    expected = hmac.new(secret_key, tampered, hashlib.sha256).hexdigest()
    valid    = hmac.compare_digest(expected, forged_attempt)

    print(f"\n  Receiver: HMAC valid? {valid}")  # False — attack detected!
    print("  → HMAC WINS. Tampering detected.")


# ═══════════════════════════════════════════════════════════
# EXPERIMENT 3 — Timing attack on naive comparison
#
# if computed_hmac == received_hmac  ← DANGEROUS
#
# Python's == exits as soon as it finds a mismatch.
# Attacker measures response time to guess the HMAC byte by byte.
# hmac.compare_digest() takes CONSTANT TIME regardless of match position.
# ═══════════════════════════════════════════════════════════

def experiment_3_timing_safe_comparison():
    print(f"\n{SEP}")
    print("EXPERIMENT 3 — Timing-safe comparison")
    print(SEP)

    key  = b"my-key"
    msg  = b"transfer $100"
    real = hmac.new(key, msg, hashlib.sha256).digest()

    # Almost-correct HMAC — first 31 bytes match, last byte wrong
    almost = bytearray(real)
    almost[-1] ^= 0xFF        # flip last byte
    almost = bytes(almost)

    # DANGEROUS: == short-circuits
    # naive_match = (real == almost)  ← don't do this in crypto code

    # SAFE: always takes the same time
    safe_match = hmac.compare_digest(real, almost)

    print(f"  Real HMAC    : {real.hex()}")
    print(f"  Almost HMAC  : {almost.hex()}")
    print(f"  compare_digest result: {safe_match}")
    print("  → Always use hmac.compare_digest(), never ==")


# ═══════════════════════════════════════════════════════════
# EXPERIMENT 4 — Real-world pattern: API request signing
#
# This is exactly how webhook signatures work (Stripe, GitHub, etc.)
# Sender signs the payload. Receiver verifies before processing.
# ═══════════════════════════════════════════════════════════

def sign_request(payload: dict, secret: bytes) -> str:
    body = json.dumps(payload, separators=(',', ':')).encode()
    return "sha256=" + hmac.new(secret, body, hashlib.sha256).hexdigest()


def verify_request(payload: dict, received_signature: str, secret: bytes) -> bool:
    expected = sign_request(payload, secret)
    return hmac.compare_digest(expected, received_signature)


def experiment_4_api_signing():
    print(f"\n{SEP}")
    print("EXPERIMENT 4 — API request signing (like Stripe webhooks)")
    print(SEP)

    secret  = b"webhook-secret-from-dashboard"
    payload = {"event": "payment.success", "amount": 100}

    # Sender (Stripe) signs and sends
    sig = sign_request(payload, secret)
    print(f"  Payload   : {payload}")
    print(f"  Signature : {sig[:30]}...")

    # Receiver (your server) verifies
    ok = verify_request(payload, sig, secret)
    print(f"  Valid?    : {ok}")  # True

    # Attacker replays with modified payload
    tampered_payload = {"event": "payment.success", "amount": 99999}
    ok_tampered = verify_request(tampered_payload, sig, secret)
    print(f"\n  Tampered payload valid? {ok_tampered}")  # False


# ═══════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("\n" + "═" * 55)
    print("  HMAC — Proof of Concept")
    print("═" * 55)

    experiment_1_plain_hash_is_broken()
    experiment_2_hmac_stops_attacker()
    experiment_3_timing_safe_comparison()
    experiment_4_api_signing()

    print(f"\n{SEP}")
    print("KEY TAKEAWAYS")
    print(SEP)
    print("""
  1. SHA256(message)          → anyone can forge   → useless for auth
  2. HMAC(key, message)       → requires secret key → tamper-proof
  3. ==                       → timing leak         → use compare_digest
  4. Real use: webhook signing, JWT signatures, cookie signing
    """)
