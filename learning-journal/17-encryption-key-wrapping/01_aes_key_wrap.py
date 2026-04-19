"""
Step 1 — AES Key Wrapping (RFC 3394 / RFC 5649)

CONCEPT:
  You have a secret key K (the disk encryption key, a private key, etc.)
  You want to store it safely. So you encrypt it with another key — the KEK.
  The result is a "wrapped key" you can store publicly.

  wrapped_key = wrap(K, KEK)         # safe to store
  K           = unwrap(wrapped_key, KEK)  # requires KEK to recover

ALGORITHM (RFC 3394 — key must be multiple of 8 bytes):
  Uses AES in ECB mode in a 6-round Feistel-like structure.
  Each round XORs a counter into the top 64 bits — adds uniqueness without needing random IV.

RFC 5649 (this file):
  Extension that handles keys of ANY length via padding.
  IV encodes the original key length so unwrap can strip padding safely.

install:
  pip install cryptography
"""

import struct
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend


# ── AES ECB helpers ────────────────────────────────────────────────────────────

def _aes_ecb_encrypt(key: bytes, block: bytes) -> bytes:
    """Encrypt a single 16-byte block with AES-ECB."""
    cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=default_backend())
    enc = cipher.encryptor()
    return enc.update(block) + enc.finalize()


def _aes_ecb_decrypt(key: bytes, block: bytes) -> bytes:
    """Decrypt a single 16-byte block with AES-ECB."""
    cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=default_backend())
    dec = cipher.decryptor()
    return dec.update(block) + dec.finalize()


# ── RFC 5649 IV ────────────────────────────────────────────────────────────────
#
# IV = 0xA65959A6 || MLI
# MLI = Message Length Indicator = original key length in bytes (4-byte big-endian)
# This is how unwrap knows how many padding bytes to strip.

RFC5649_MAGIC = 0xA65959A6


def _make_iv(plaintext_len: int) -> bytes:
    # 4-byte magic + 4-byte length
    return struct.pack(">II", RFC5649_MAGIC, plaintext_len)


# ── STEP 1 OF 3: Pad the plaintext key to a multiple of 8 bytes ───────────────

def _pad(key: bytes) -> bytes:
    """Zero-pad key to next multiple of 8 bytes."""
    remainder = len(key) % 8
    if remainder != 0:
        key += b'\x00' * (8 - remainder)
    return key


# ── STEP 2 OF 3: The Feistel-based wrap loop (RFC 3394 core) ─────────────────
#
# Variables:
#   A    = the "authentication" value (starts as IV, accumulates XORs)
#   R[i] = the i-th 8-byte block of the padded key
#
# Each outer round j (0-5), each block i (1..n):
#   B       = AES_ECB_encrypt(KEK, A || R[i])   ← 16-byte AES block
#   A       = MSB8(B) XOR (n*j + i)             ← update running value
#   R[i]    = LSB8(B)                           ← update block
#
# Why 6 rounds?  Security analysis — 6 rounds guarantees 128-bit security.
# Why XOR a counter?  Makes every AES input unique → no repeated blocks.

def _wrap_core(kek: bytes, iv: bytes, plaintext_padded: bytes) -> bytes:
    n = len(plaintext_padded) // 8            # number of 8-byte blocks
    R = [plaintext_padded[i*8:(i+1)*8] for i in range(n)]
    A = iv                                    # initialize A with IV

    print(f"\n  [wrap] {n} blocks, 6 rounds × {n} steps = {6*n} AES calls")

    for j in range(6):                        # 6 rounds
        for i in range(n):                    # one step per block
            # Concatenate A (8 bytes) + R[i] (8 bytes) = 16-byte AES input
            B = _aes_ecb_encrypt(kek, A + R[i])

            # Counter = n*j + (i+1)  — RFC uses 1-indexed i
            counter = n * j + (i + 1)

            # A = top 8 bytes of B, XORed with counter (as big-endian 8-byte int)
            A = bytes(b ^ c for b, c in zip(B[:8], struct.pack(">Q", counter)))

            # R[i] = bottom 8 bytes of B
            R[i] = B[8:]

    # Output: A followed by all R blocks
    return A + b''.join(R)


# ── STEP 3 OF 3: Unwrap — run the loop in reverse ────────────────────────────

def _unwrap_core(kek: bytes, wrapped: bytes) -> tuple[bytes, bytes]:
    """Returns (iv, padded_plaintext)."""
    A    = wrapped[:8]
    data = wrapped[8:]
    n    = len(data) // 8
    R    = [data[i*8:(i+1)*8] for i in range(n)]

    for j in range(5, -1, -1):               # 6 rounds in REVERSE
        for i in range(n - 1, -1, -1):       # blocks in REVERSE
            counter = n * j + (i + 1)
            # Un-XOR counter from A to recover pre-XOR value
            A_xored = bytes(b ^ c for b, c in zip(A, struct.pack(">Q", counter)))
            # AES decrypt: 8-byte A_xored || R[i]
            B    = _aes_ecb_decrypt(kek, A_xored + R[i])
            A    = B[:8]
            R[i] = B[8:]

    return A, b''.join(R)


# ── Public API ────────────────────────────────────────────────────────────────

def wrap_key(plaintext_key: bytes, kek: bytes) -> bytes:
    """
    Wrap plaintext_key with kek using RFC 5649.
    Returns wrapped bytes (8 bytes longer than padded key + 8-byte header).
    """
    iv              = _make_iv(len(plaintext_key))   # encode original length
    padded          = _pad(plaintext_key)
    wrapped         = _wrap_core(kek, iv, padded)
    print(f"  [wrap] plaintext  : {plaintext_key.hex()}")
    print(f"  [wrap] wrapped    : {wrapped.hex()}")
    return wrapped


def unwrap_key(wrapped_key: bytes, kek: bytes) -> bytes:
    """
    Unwrap wrapped_key with kek using RFC 5649.
    Returns the original plaintext key (padding stripped).
    """
    iv, padded = _unwrap_core(kek, wrapped_key)

    # Verify magic bytes
    magic, original_len = struct.unpack(">II", iv)
    if magic != RFC5649_MAGIC:
        raise ValueError("Unwrap failed: IV magic mismatch — wrong KEK or corrupted data")

    plaintext = padded[:original_len]            # strip padding
    print(f"  [unwrap] recovered: {plaintext.hex()}")
    return plaintext


# ── Demo ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 60)
    print("RFC 5649 AES Key Wrapping — step by step")
    print("=" * 60)

    # The key we want to protect (e.g. a disk encryption key)
    plaintext_key = bytes.fromhex("00112233445566778899AABBCCDDEEFF")  # 128-bit key
    kek           = bytes.fromhex("000102030405060708090A0B0C0D0E0F")  # 128-bit KEK

    print(f"\nplaintext key : {plaintext_key.hex()}  ({len(plaintext_key)*8}-bit)")
    print(f"KEK           : {kek.hex()}  ({len(kek)*8}-bit)")

    print("\n--- WRAP ---")
    wrapped = wrap_key(plaintext_key, kek)

    print("\n--- UNWRAP ---")
    recovered = unwrap_key(wrapped, kek)

    print(f"\nMatch: {recovered == plaintext_key}")  # True

    # ── Wrong KEK → fails ────────────────────────────────────────────────────
    print("\n--- Wrong KEK → should fail ---")
    wrong_kek = bytes(16)  # all zeros
    try:
        unwrap_key(wrapped, wrong_kek)
    except ValueError as e:
        print(f"  Correctly rejected: {e}")

    # ── Non-multiple-of-8 key (RFC 5649 padding) ─────────────────────────────
    print("\n--- 20-byte key (not multiple of 8, needs padding) ---")
    key_20 = bytes(range(20))
    wrapped_20  = wrap_key(key_20, kek)
    recovered_20 = unwrap_key(wrapped_20, kek)
    print(f"  Match: {recovered_20 == key_20}")
