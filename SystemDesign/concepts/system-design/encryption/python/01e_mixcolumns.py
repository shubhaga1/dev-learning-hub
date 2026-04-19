"""
AES INTERNALS 4/5 — MixColumns: column diffusion

WHAT IT DOES:
  Takes each column of 4 bytes and mixes them together.
  Every output byte depends on ALL 4 input bytes of that column.
  Change 1 input byte → all 4 output bytes change.

THE MATH (looks scary, is actually just XOR + shifts):
  Multiplies each column by a fixed matrix in GF(2^8).
  GF(2^8) = Galois Field — all arithmetic is mod 2 (XOR instead of add/subtract).
  The only "multiply" needed is xtime() = left shift + conditional XOR.
  No division. No modular exponentiation. No primes.

  Output byte 0 = (2×a) XOR (3×b) XOR c XOR d
  Output byte 1 = a XOR (2×b) XOR (3×c) XOR d
  Output byte 2 = a XOR b XOR (2×c) XOR (3×d)
  Output byte 3 = (3×a) XOR b XOR c XOR (2×d)

  where "2×b" means xtime(b), and "3×b" means xtime(b) XOR b
"""

def xtime(b):
    """Multiply by 2 in GF(2^8): left shift, XOR with 0x1B if bit 7 was set."""
    # 0x1B = the AES reduction polynomial (x^8 + x^4 + x^3 + x + 1, dropping x^8)
    # This keeps the result within 8 bits (0-255)
    return ((b << 1) ^ 0x1B) & 0xFF if (b & 0x80) else (b << 1) & 0xFF

def mix_column(col):
    a, b, c, d = col
    return [
        xtime(a) ^ xtime(b) ^ b ^ c ^ d,
        a ^ xtime(b) ^ xtime(c) ^ c ^ d,
        a ^ b ^ xtime(c) ^ xtime(d) ^ d,
        xtime(a) ^ a ^ b ^ c ^ xtime(d),
    ]

print("=" * 50)
print("  MixColumns — column diffusion")
print("=" * 50)

# ── Verify against AES specification example ──────────────────
print("\nVerify against AES spec (NIST FIPS 197, page 11):")
col_spec = [0xDB, 0x13, 0x53, 0x45]
result   = mix_column(col_spec)
expected = [0x8E, 0x4D, 0xA1, 0xBC]
print(f"  input   : {[hex(b) for b in col_spec]}")
print(f"  output  : {[hex(b) for b in result]}")
print(f"  expected: {[hex(b) for b in expected]}  ← from spec")
print(f"  match   : {result == expected}")

# ── Diffusion demo: change 1 byte → all 4 output bytes change ─
print("\nDiffusion demo (change 1 input byte → how many outputs change?):")
col_a = [0xDB, 0x13, 0x53, 0x45]
col_b = [0xDC, 0x13, 0x53, 0x45]   # only first byte changed by 1

out_a = mix_column(col_a)
out_b = mix_column(col_b)

changed = sum(1 for x, y in zip(out_a, out_b) if x != y)
print(f"  col A  : {[hex(b) for b in col_a]}")
print(f"  col B  : {[hex(b) for b in col_b]}  ← first byte +1")
print(f"  out A  : {[hex(b) for b in out_a]}")
print(f"  out B  : {[hex(b) for b in out_b]}")
print(f"  {changed}/4 output bytes changed from 1 input byte change")

print("""
xtime() is the ONLY "math" in AES:
  xtime(b) = (b << 1) ^ 0x1B   (if overflow)
           = (b << 1)           (if no overflow)
  That's a bit shift and an XOR — two CPU instructions.

Compare to RSA:
  RSA multiply: pow(1234...2048bits, 65537, n)  ← thousands of steps
  AES xtime:    b << 1  ← one instruction

Next: 01f_one_round.py — all 4 steps in sequence
""")
