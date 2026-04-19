"""
Step 3 — Complete Disk Encryption Workflow

This ties Steps 1 and 2 together into the full workflow used by
tools like VeraCrypt, TrueCrypt, macOS FileVault, and LUKS (Linux).

WORKFLOW:

  SETUP (one time):
    1. Generate a random DISK KEY (the actual key that encrypts your data)
    2. Derive a KEK from the user's password + random salt (via scrypt/PBKDF2)
    3. Wrap (encrypt) the DISK KEY with the KEK → WRAPPED KEY
    4. Store: SALT + WRAPPED KEY on disk (public — safe to store)
    5. The DISK KEY is never stored — only the wrapped form

  UNLOCK:
    1. Read SALT + WRAPPED KEY from disk
    2. Ask user for password
    3. Derive KEK from password + stored SALT
    4. Unwrap WRAPPED KEY using KEK → DISK KEY
    5. Use DISK KEY to decrypt the disk data

WHY THIS DESIGN?
  - Changing the password only requires re-wrapping the DISK KEY, not re-encrypting the disk
  - Multiple passwords can wrap the same DISK KEY (multi-user disk access)
  - The DISK KEY is random and strong — not limited by password entropy
"""

import os
import json
import base64
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend

from aes_key_wrap_lib import wrap_key, unwrap_key  # our Step 1 implementation


# ── KDF (using scrypt for strong protection) ──────────────────────────────────

def derive_kek(password: str, salt: bytes) -> bytes:
    """Derive a 256-bit KEK from password + salt using scrypt."""
    kdf = Scrypt(
        salt=salt,
        length=32,      # 256-bit KEK
        n=2**14,        # N — increase to 2**17+ in production
        r=8,
        p=1,
        backend=default_backend(),
    )
    return kdf.derive(password.encode())


# ── Key store format ──────────────────────────────────────────────────────────
#
# Stored on disk (JSON for readability — real tools use binary):
# {
#   "salt"       : "<base64>",   ← random, not secret
#   "wrapped_key": "<base64>",   ← encrypted disk key, safe to store
#   "kdf"        : "scrypt",
#   "kdf_params" : { "n": 16384, "r": 8, "p": 1 }
# }

def _encode(b: bytes) -> str:
    return base64.b64encode(b).decode()


def _decode(s: str) -> bytes:
    return base64.b64decode(s.encode())


# ── SETUP ─────────────────────────────────────────────────────────────────────

def setup_disk_encryption(password: str) -> dict:
    """
    One-time setup:
      - Generate random disk key
      - Derive KEK from password
      - Wrap disk key
      - Return key store dict (save this to disk)
    """
    print("\n[SETUP]")

    # Step 1: generate random disk key (this is what actually encrypts your files)
    disk_key = os.urandom(32)           # 256-bit AES key
    print(f"  disk_key (NEVER stored in plaintext) : {disk_key.hex()}")

    # Step 2: generate random salt
    salt = os.urandom(16)
    print(f"  salt (stored, not secret)            : {salt.hex()}")

    # Step 3: derive KEK from password + salt
    kek = derive_kek(password, salt)
    print(f"  KEK (derived, never stored)          : {kek.hex()}")

    # Step 4: wrap the disk key with the KEK
    wrapped_key = wrap_key(disk_key, kek)
    print(f"  wrapped_key (stored on disk)         : {wrapped_key.hex()}")

    # What gets saved to disk
    key_store = {
        "salt"       : _encode(salt),
        "wrapped_key": _encode(wrapped_key),
        "kdf"        : "scrypt",
        "kdf_params" : {"n": 2**14, "r": 8, "p": 1},
    }

    print(f"\n  Key store saved (safe to store publicly):")
    print(f"  {json.dumps(key_store, indent=4)}")

    # disk_key is DISCARDED here — only wrapped form is kept
    return key_store


# ── UNLOCK ────────────────────────────────────────────────────────────────────

def unlock_disk(key_store: dict, password: str) -> bytes:
    """
    Unlock:
      - Load salt + wrapped key from key store
      - Derive KEK from password + salt
      - Unwrap to recover disk key
    """
    print("\n[UNLOCK]")

    salt        = _decode(key_store["salt"])
    wrapped_key = _decode(key_store["wrapped_key"])
    params      = key_store["kdf_params"]

    print(f"  Loaded salt        : {salt.hex()}")
    print(f"  Loaded wrapped_key : {wrapped_key.hex()}")

    # Re-derive KEK — same password + same salt → same KEK (deterministic)
    kdf = Scrypt(
        salt=salt,
        length=32,
        n=params["n"],
        r=params["r"],
        p=params["p"],
        backend=default_backend(),
    )
    kek = kdf.derive(password.encode())
    print(f"  Re-derived KEK     : {kek.hex()}")

    # Unwrap the disk key
    disk_key = unwrap_key(wrapped_key, kek)
    print(f"  Recovered disk_key : {disk_key.hex()}")
    return disk_key


# ── PASSWORD CHANGE (no re-encryption of data!) ───────────────────────────────

def change_password(key_store: dict, old_password: str, new_password: str) -> dict:
    """
    Change password without re-encrypting the disk:
      1. Unlock with old password → get disk key
      2. New salt + new KEK from new password
      3. Re-wrap disk key with new KEK
      4. Store new key store
    The actual disk data is untouched.
    """
    print("\n[CHANGE PASSWORD]")

    # Unlock with old password
    disk_key = unlock_disk(key_store, old_password)

    # New salt (always generate fresh — defeats rainbow table on new password too)
    new_salt = os.urandom(16)
    new_kek  = derive_kek(new_password, new_salt)
    new_wrapped = wrap_key(disk_key, new_kek)

    new_key_store = {
        "salt"       : _encode(new_salt),
        "wrapped_key": _encode(new_wrapped),
        "kdf"        : "scrypt",
        "kdf_params" : key_store["kdf_params"],
    }
    print(f"  New key store (new salt + new wrapped key):")
    print(f"  {json.dumps(new_key_store, indent=4)}")
    return new_key_store


# ── Demo ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 60)
    print("Disk Encryption Workflow — step by step")
    print("=" * 60)

    PASSWORD = "correct-horse-battery-staple"

    # ── Setup ──────────────────────────────────────────────────────────────────
    key_store = setup_disk_encryption(PASSWORD)

    # ── Unlock with correct password ───────────────────────────────────────────
    recovered = unlock_disk(key_store, PASSWORD)

    # ── Unlock with WRONG password → should fail ──────────────────────────────
    print("\n[WRONG PASSWORD — should fail]")
    try:
        unlock_disk(key_store, "wrong-password")
    except Exception as e:
        print(f"  Correctly rejected: {e}")

    # ── Change password ───────────────────────────────────────────────────────
    NEW_PASSWORD = "new-super-secret-passphrase"
    new_key_store = change_password(key_store, PASSWORD, NEW_PASSWORD)

    # ── Unlock with new password ──────────────────────────────────────────────
    recovered_after_change = unlock_disk(new_key_store, NEW_PASSWORD)

    print(f"\n{'='*60}")
    print("Summary:")
    print(f"  Disk key consistent after password change: "
          f"{recovered == recovered_after_change}")
    print(f"  Old key store still exists but new one uses new KEK")
    print(f"  Disk data was NEVER re-encrypted")
