"""
aes_key_wrap_lib.py — importable module exposing wrap_key / unwrap_key.

This is the same implementation as 01_aes_key_wrap.py but stripped to
just the public API so other files (03_disk_encryption_workflow.py) can import it.
"""

import struct
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

RFC5649_MAGIC = 0xA65959A6


def _aes_ecb_encrypt(key: bytes, block: bytes) -> bytes:
    c = Cipher(algorithms.AES(key), modes.ECB(), backend=default_backend())
    e = c.encryptor()
    return e.update(block) + e.finalize()


def _aes_ecb_decrypt(key: bytes, block: bytes) -> bytes:
    c = Cipher(algorithms.AES(key), modes.ECB(), backend=default_backend())
    d = c.decryptor()
    return d.update(block) + d.finalize()


def _pad(key: bytes) -> bytes:
    r = len(key) % 8
    return key + b'\x00' * (8 - r if r else 0)


def _wrap_core(kek: bytes, iv: bytes, padded: bytes) -> bytes:
    n = len(padded) // 8
    R = [padded[i*8:(i+1)*8] for i in range(n)]
    A = iv
    for j in range(6):
        for i in range(n):
            B    = _aes_ecb_encrypt(kek, A + R[i])
            A    = bytes(b ^ c for b, c in zip(B[:8], struct.pack(">Q", n*j + i + 1)))
            R[i] = B[8:]
    return A + b''.join(R)


def _unwrap_core(kek: bytes, wrapped: bytes) -> tuple[bytes, bytes]:
    A = wrapped[:8]
    n = (len(wrapped) - 8) // 8
    R = [wrapped[8 + i*8: 16 + i*8] for i in range(n)]
    for j in range(5, -1, -1):
        for i in range(n - 1, -1, -1):
            A_x  = bytes(b ^ c for b, c in zip(A, struct.pack(">Q", n*j + i + 1)))
            B    = _aes_ecb_decrypt(kek, A_x + R[i])
            A    = B[:8]
            R[i] = B[8:]
    return A, b''.join(R)


def wrap_key(plaintext_key: bytes, kek: bytes) -> bytes:
    iv     = struct.pack(">II", RFC5649_MAGIC, len(plaintext_key))
    return _wrap_core(kek, iv, _pad(plaintext_key))


def unwrap_key(wrapped_key: bytes, kek: bytes) -> bytes:
    iv, padded      = _unwrap_core(kek, wrapped_key)
    magic, orig_len = struct.unpack(">II", iv)
    if magic != RFC5649_MAGIC:
        raise ValueError("Unwrap failed: wrong KEK or corrupted data")
    return padded[:orig_len]
