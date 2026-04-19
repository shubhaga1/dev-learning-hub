"""
SYMMETRIC ENCRYPTION — AES in Python

WHY "SYMMETRIC"?
  Same key used to ENCRYPT and DECRYPT.
  Like a padlock — one key both locks and unlocks.
  Contrast: asymmetric uses TWO keys (public to lock, private to unlock).

AES-256:
  AES = Advanced Encryption Standard. The number = key length in bits.
  256-bit key = 32 bytes = os.urandom(32)
  2^256 possible keys — more than atoms in the observable universe.
  "Fastest" because:
    - Symmetric math is just XOR + bitwise shifts on 128-bit blocks
    - Modern CPUs have AES-NI hardware instructions → GB/s throughput
    - Compare: RSA needs giant exponentiation (100-1000x slower)
  Used for: bulk data, database fields, file encryption

WHAT IS FERNET?
  Fernet is NOT a cipher. It's a high-level RECIPE (a wrapper) that bundles:
    ┌──────────────────────────────────────────────────────┐
    │  AES-128-CBC      → the actual encryption            │
    │  HMAC-SHA256      → tamper detection (integrity)     │
    │  URL-safe base64  → output is a readable string      │
    │  Auto IV          → random init vector, handled for  │
    │                     you (never reused)               │
    │  Timestamp        → baked in, can enforce expiry     │
    └──────────────────────────────────────────────────────┘
  If anyone modifies the ciphertext → decryption raises InvalidToken.
  Named after Fernet-Branca (Italian liquor) — cryptography lib authors
  named their high-level recipes after drinks.
  Trade-off: AES-128 not 256, no associated data auth → use AES-GCM for prod.

Install: pip install cryptography
"""

from cryptography.fernet import Fernet
import os, base64
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

# ── Simple AES with Fernet (beginner-friendly) ────────────────────────────────
print("=== 1. Fernet (AES-128-CBC + HMAC-SHA256, easiest API) ===")

# generate_key() → random 32-byte key, base64-encoded as a URL-safe string
# internally split: first 16 bytes = signing key (HMAC), next 16 = encryption key (AES)
key = Fernet.generate_key()
print("Key:", key.decode()[:40] + "...")

fernet = Fernet(key)                 # create Fernet instance with that key

message = b"Hello, this is a secret message!"

# encrypt() does all of this automatically:
#   1. Generates random IV (16 bytes)
#   2. Encrypts with AES-128-CBC
#   3. Signs with HMAC-SHA256
#   4. Packages into: version | timestamp | IV | ciphertext | HMAC → base64
encrypted = fernet.encrypt(message)
print("Encrypted:", encrypted[:40], "...")

# decrypt() verifies HMAC first → raises InvalidToken if tampered
# then decrypts and strips padding → returns original plaintext
decrypted = fernet.decrypt(encrypted)
print("Decrypted:", decrypted.decode())
print("Match?", decrypted == message)

# ── AES-256-GCM (production grade) ───────────────────────────────────────────
print("\n=== 2. AES-256-GCM (production) ===")

key256 = os.urandom(32)              # 32 bytes = 256 bits
nonce  = os.urandom(12)              # 12 bytes nonce (like IV)

aesgcm = AESGCM(key256)

plaintext = b"Bank transfer: $5000 to Alice"
ciphertext = aesgcm.encrypt(nonce, plaintext, None)
print("Ciphertext:", ciphertext.hex()[:40] + "...")

recovered = aesgcm.decrypt(nonce, ciphertext, None)
print("Decrypted:", recovered.decode())

print("\n--- KEY DISTRIBUTION PROBLEM ---")
print("AES is fast but: how do Alice and Bob share the key safely?")
print("If sent over internet → attacker intercepts key → decrypts everything")
print("Solution: use RSA/ECC to share the AES key → see 02_asymmetric_rsa.py")
