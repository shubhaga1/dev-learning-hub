"""
Step 2 — Key Derivation: turning a PASSWORD into a KEK

PROBLEM:
  Humans remember passwords, not 256-bit AES keys.
  You need a way to turn a password into a KEK reproducibly.

WHY NOT just SHA256(password)?
  SHA256 is fast — an attacker can try billions of guesses/second.
  KDFs are INTENTIONALLY SLOW — they add computation cost to each guess.

THREE KDFs COMPARED:
  PBKDF2 — widely supported, tunable via iterations
  bcrypt  — GPU-resistant (uses Blowfish, not AES — GPU can't parallelize it)
  scrypt  — memory-hard (needs lots of RAM, defeats ASICs and GPUs)

THE SALT:
  Random bytes stored alongside the wrapped key (not secret).
  Ensures two users with the same password get different KEKs.
  Defeats rainbow tables (precomputed hash lookups).

install:
  pip install cryptography bcrypt
"""

import os
import time
import bcrypt
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend


# ── Helpers ───────────────────────────────────────────────────────────────────

def _timed(label: str, fn):
    start  = time.perf_counter()
    result = fn()
    elapsed = time.perf_counter() - start
    print(f"  {label:<30} {elapsed*1000:.0f} ms   key={result.hex()[:16]}...")
    return result


# ── PBKDF2 ───────────────────────────────────────────────────────────────────
#
# PBKDF2(password, salt, iterations, key_length, hash_function)
# Standard: NIST SP 800-132, used in iOS passcode encryption, WPA2, ZIP
# Weakness: each iteration is cheap on GPUs — attacker parallelizes easily
# Recommended iterations (2024): ≥ 600,000 for HMAC-SHA256

def derive_pbkdf2(password: str, salt: bytes, iterations: int = 600_000) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,              # 256-bit KEK
        salt=salt,
        iterations=iterations,
        backend=default_backend(),
    )
    return kdf.derive(password.encode())


# ── bcrypt ────────────────────────────────────────────────────────────────────
#
# bcrypt(password, cost_factor)
# cost_factor = 2^N rounds of Blowfish key setup
# GPU-resistant because Blowfish has expensive key setup not suited to GPUs
# Output is always 60 bytes (includes algorithm, cost, salt, hash)
# Limitation: truncates passwords >72 bytes and keys to 31 bytes
#
# For a 32-byte KEK: derive with bcrypt then hash the result

def derive_bcrypt(password: str, cost: int = 12) -> tuple[bytes, bytes]:
    """Returns (kek, salt). Salt is embedded in bcrypt hash."""
    salt = bcrypt.gensalt(rounds=cost)
    raw  = bcrypt.hashpw(password.encode(), salt)
    # bcrypt output is ASCII — hash it to get 32 bytes of uniform key material
    from cryptography.hazmat.primitives import hashes as h
    digest = h.Hash(h.SHA256(), backend=default_backend())
    digest.update(raw)
    kek = digest.finalize()
    return kek, salt


# ── scrypt ────────────────────────────────────────────────────────────────────
#
# scrypt(password, salt, N, r, p, key_length)
# N  = CPU/memory cost factor (must be power of 2)
# r  = block size (affects memory bandwidth requirement)
# p  = parallelization factor
# Memory used ≈ 128 * N * r bytes
#
# N=2^17 (131072), r=8, p=1 → uses ~128 MB RAM
# An attacker needs that RAM for EACH guess → defeats ASICs and GPU farms
# Used by: Litecoin, 1Password, macOS FileVault (via PBKDF2 → scrypt hybrid)

def derive_scrypt(password: str, salt: bytes,
                  N: int = 2**14, r: int = 8, p: int = 1) -> bytes:
    # N=2^14 for demo speed — production use 2^17 or 2^20
    kdf = Scrypt(salt=salt, length=32, n=N, r=r, p=p, backend=default_backend())
    return kdf.derive(password.encode())


# ── Side-by-side comparison ───────────────────────────────────────────────────

def compare_kdfs(password: str = "my-secure-password") -> None:
    print(f"\nDeriving 256-bit KEK from password: '{password}'\n")

    salt = os.urandom(16)   # one random salt for PBKDF2 and scrypt
    print(f"Salt (hex): {salt.hex()}\n")

    print(f"{'KDF':<30} {'Time':>8}   {'KEK (first 8 bytes)':}")
    print("-" * 60)

    _timed("PBKDF2-SHA256 (600k iter)",   lambda: derive_pbkdf2(password, salt, 600_000))
    kek_bcrypt, _  = derive_bcrypt(password, cost=12)
    print(f"  {'bcrypt (cost=12)':<30} {'?':>8} ms   key={kek_bcrypt.hex()[:16]}...")
    _timed("scrypt (N=2^14, demo)",       lambda: derive_scrypt(password, salt, N=2**14))

    print(f"""
  Notes:
    PBKDF2 : Fast per iteration — must use 600k+ to compensate
    bcrypt  : Built-in GPU resistance — cost factor doubles work each +1
    scrypt  : Best against specialized hardware (ASICs) — memory-hard

  For a password-based KEK: scrypt > bcrypt > PBKDF2 (security ranking)
  For compatibility (mobile, older systems): PBKDF2 still widely acceptable
    """)


# ── The salt question ─────────────────────────────────────────────────────────

def demo_same_password_different_salt(password: str = "hello") -> None:
    print("\n--- Same password, two different salts → completely different KEKs ---")
    salt1 = os.urandom(16)
    salt2 = os.urandom(16)
    kek1  = derive_pbkdf2(password, salt1, iterations=10_000)
    kek2  = derive_pbkdf2(password, salt1, iterations=10_000)  # same salt
    kek3  = derive_pbkdf2(password, salt2, iterations=10_000)  # different salt

    print(f"  kek1 (salt1): {kek1.hex()}")
    print(f"  kek2 (salt1): {kek2.hex()}  ← same salt → reproducible ✓")
    print(f"  kek3 (salt2): {kek3.hex()}  ← different salt → different KEK ✓")
    print(f"\n  kek1 == kek2: {kek1 == kek2}")
    print(f"  kek1 == kek3: {kek1 == kek3}")


if __name__ == "__main__":
    print("=" * 60)
    print("Key Derivation Functions (KDF) — step by step")
    print("=" * 60)

    compare_kdfs("my-secure-password")
    demo_same_password_different_salt("hello")
