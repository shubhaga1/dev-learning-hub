"""
POC: IV — Initialization Vector

Run this file and watch each experiment.
Each section is self-contained.

We use AES-CBC mode — a block cipher that XORs each block
with the previous ciphertext block before encrypting.
The IV is the "previous block" for the very first block.
"""

import os
import hashlib
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend

SEP = "-" * 55
KEY = os.urandom(32)   # one key used across all experiments


# ── AES-CBC helpers ───────────────────────────────────────────────────────────

def _pad(data: bytes) -> bytes:
    p = padding.PKCS7(128).padder()
    return p.update(data) + p.finalize()


def _unpad(data: bytes) -> bytes:
    p = padding.PKCS7(128).unpadder()
    return p.update(data) + p.finalize()


def encrypt_cbc(plaintext: bytes, key: bytes, iv: bytes) -> bytes:
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    enc = cipher.encryptor()
    return enc.update(_pad(plaintext)) + enc.finalize()


def decrypt_cbc(ciphertext: bytes, key: bytes, iv: bytes) -> bytes:
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    dec = cipher.decryptor()
    return _unpad(dec.update(ciphertext) + dec.finalize())


# ═══════════════════════════════════════════════════════════
# EXPERIMENT 1 — No IV / fixed IV → patterns leak
#
# Same plaintext + same key + same IV → identical ciphertext
# Attacker sees two identical ciphertexts and knows:
# "these two messages are the same" → information leak
# ═══════════════════════════════════════════════════════════

def experiment_1_fixed_iv_leaks_patterns():
    print(SEP)
    print("EXPERIMENT 1 — Fixed IV → patterns visible in ciphertext")
    print(SEP)

    fixed_iv  = bytes(16)                    # all zeros — never do this
    message_a = b"Transfer $100 to Alice"
    message_b = b"Transfer $100 to Alice"    # same message sent twice

    ct_a = encrypt_cbc(message_a, KEY, fixed_iv)
    ct_b = encrypt_cbc(message_b, KEY, fixed_iv)

    print(f"  Message A   : {message_a}")
    print(f"  Ciphertext A: {ct_a.hex()}")
    print(f"\n  Message B   : {message_b}")
    print(f"  Ciphertext B: {ct_b.hex()}")
    print(f"\n  Ciphertexts identical: {ct_a == ct_b}")
    print("  → Attacker sees two identical ciphertexts.")
    print("    Even without decrypting: they KNOW the messages are the same.")

    # Worse — with a fixed IV, attacker can even do a chosen-plaintext attack
    # (CBC byte-flipping). We'll skip that here, but this alone is bad enough.


# ═══════════════════════════════════════════════════════════
# EXPERIMENT 2 — Random IV → same plaintext, different ciphertext every time
#
# IV is generated fresh with os.urandom(16) per encryption.
# Stored alongside ciphertext (not secret — receiver needs it to decrypt).
# ═══════════════════════════════════════════════════════════

def experiment_2_random_iv_hides_patterns():
    print(f"\n{SEP}")
    print("EXPERIMENT 2 — Random IV → no patterns visible")
    print(SEP)

    message = b"Transfer $100 to Alice"

    results = []
    for i in range(3):
        iv = os.urandom(16)          # fresh random IV every time
        ct = encrypt_cbc(message, KEY, iv)
        results.append((iv, ct))
        print(f"  Encryption {i+1}:")
        print(f"    IV         : {iv.hex()}")
        print(f"    Ciphertext : {ct.hex()}")

    print(f"\n  All 3 encryptions of the SAME message:")
    print(f"  ct1 == ct2: {results[0][1] == results[1][1]}")  # False
    print(f"  ct1 == ct3: {results[0][1] == results[2][1]}")  # False
    print("  → Attacker sees 3 different ciphertexts. No pattern.")

    # Decrypt the first one to prove IV isn't secret — receiver stores it
    iv0, ct0 = results[0]
    recovered = decrypt_cbc(ct0, KEY, iv0)
    print(f"\n  Decrypted (using stored IV): {recovered}")


# ═══════════════════════════════════════════════════════════
# EXPERIMENT 3 — IV is NOT secret, just unique
#
# The IV travels with the ciphertext in plaintext.
# Knowing the IV doesn't help decrypt without the KEY.
# ═══════════════════════════════════════════════════════════

def experiment_3_iv_is_not_secret():
    print(f"\n{SEP}")
    print("EXPERIMENT 3 — IV is public, key is secret")
    print(SEP)

    message = b"secret bank transfer"
    iv      = os.urandom(16)
    ct      = encrypt_cbc(message, KEY, iv)

    # What gets transmitted/stored: IV + ciphertext (both plaintext)
    transmitted = iv + ct
    print(f"  Transmitted (IV + ciphertext): {transmitted.hex()}")
    print(f"  IV  (first 16 bytes, public) : {transmitted[:16].hex()}")
    print(f"  CT  (rest, public)           : {transmitted[16:].hex()}")

    # Attacker has: IV + ciphertext + no key
    attacker_iv = transmitted[:16]
    attacker_ct = transmitted[16:]
    wrong_key   = os.urandom(32)

    try:
        garbage = decrypt_cbc(attacker_ct, wrong_key, attacker_iv)
        print(f"\n  Attacker decrypted (wrong key): {garbage}")
        print("  → Garbage. IV alone is useless without the key.")
    except Exception as e:
        print(f"\n  Attacker got error: {e}")

    # Receiver with correct key + stored IV → works
    receiver_iv = transmitted[:16]
    receiver_ct = transmitted[16:]
    plaintext   = decrypt_cbc(receiver_ct, KEY, receiver_iv)
    print(f"  Receiver decrypted (right key): {plaintext}")


# ═══════════════════════════════════════════════════════════
# EXPERIMENT 4 — IV reuse in CTR/GCM mode is CATASTROPHIC
#
# AES-CBC IV reuse leaks patterns (Experiment 1).
# AES-GCM / CTR IV (nonce) reuse is MUCH worse:
# it exposes the keystream → attacker can XOR two ciphertexts
# and recover both plaintexts (the "two-time pad" attack).
#
# This is why GCM nonces must NEVER repeat.
# TLS 1.3 uses a counter-based nonce to guarantee uniqueness.
# ═══════════════════════════════════════════════════════════

def experiment_4_nonce_reuse_two_time_pad():
    print(f"\n{SEP}")
    print("EXPERIMENT 4 — Nonce reuse in CTR mode: two-time pad attack")
    print(SEP)

    # AES-CTR: keystream = AES(key, nonce||counter)
    # ciphertext = plaintext XOR keystream
    # If nonce reused: ct1 XOR ct2 = pt1 XOR pt2 (key cancels out!)

    from cryptography.hazmat.primitives.ciphers import algorithms, modes

    key   = os.urandom(32)
    nonce = os.urandom(16)      # reused for both — this is the mistake

    pt1 = b"ATTACK AT DAWN!!"    # 16 bytes exactly
    pt2 = b"RETREAT AT ONCE!"    # 16 bytes exactly

    def ctr_encrypt(plaintext, key, nonce):
        cipher = Cipher(algorithms.AES(key), modes.CTR(nonce), backend=default_backend())
        e = cipher.encryptor()
        return e.update(plaintext) + e.finalize()

    ct1 = ctr_encrypt(pt1, key, nonce)
    ct2 = ctr_encrypt(pt2, key, nonce)   # SAME nonce — disaster

    print(f"  pt1 : {pt1}")
    print(f"  ct1 : {ct1.hex()}")
    print(f"  pt2 : {pt2}")
    print(f"  ct2 : {ct2.hex()}")

    # Attacker XORs the two ciphertexts — key/nonce cancels out
    xored = bytes(a ^ b for a, b in zip(ct1, ct2))
    print(f"\n  ct1 XOR ct2     : {xored.hex()}")

    # If attacker guesses pt1, they recover pt2:
    recovered_pt2 = bytes(a ^ b for a, b in zip(xored, pt1))
    print(f"  Attacker knows pt1='{pt1.decode()}', recovers pt2:")
    print(f"  Recovered pt2   : {recovered_pt2}")
    print(f"  Actual pt2      : {pt2}")
    print(f"  Match           : {recovered_pt2 == pt2}")
    print("\n  → Nonce reuse in CTR/GCM exposes BOTH plaintexts.")
    print("    This is the 'two-time pad' — one-time pad used twice.")


# ═══════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("\n" + "═" * 55)
    print("  IV — Proof of Concept")
    print("═" * 55)

    experiment_1_fixed_iv_leaks_patterns()
    experiment_2_random_iv_hides_patterns()
    experiment_3_iv_is_not_secret()
    experiment_4_nonce_reuse_two_time_pad()

    print(f"\n{SEP}")
    print("KEY TAKEAWAYS")
    print(SEP)
    print("""
  1. Fixed/zero IV       → same plaintext = same ciphertext → patterns leak
  2. Random IV           → same plaintext = different ciphertext every time
  3. IV is NOT secret    → stored with ciphertext, useless without key
  4. IV/nonce reuse in   → two-time pad attack → BOTH plaintexts exposed
     CTR/GCM mode
  5. Rule: os.urandom(16) for every single encryption, no exceptions
    """)
