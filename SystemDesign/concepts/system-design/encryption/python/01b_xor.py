"""
AES INTERNALS 1/5 — XOR: the foundation of AES

AES uses NO heavy math like RSA.
Every step inside AES is built on bitwise operations — XOR is the most fundamental.

WHY XOR?
  - Perfectly reversible: (a ^ k) ^ k == a  (encrypt then decrypt = original)
  - Every bit flips independently — no carry, no overflow
  - CPU does 64 XORs in ONE instruction
  - RSA by contrast: pow(m, e, n) with 2048-bit numbers — 1000x slower

^ truth table:
  0 ^ 0 = 0   (same → 0)
  1 ^ 1 = 0   (same → 0)
  0 ^ 1 = 1   (different → 1)
  1 ^ 0 = 1   (different → 1)
"""

print("=" * 50)
print("  XOR — AES foundation")
print("=" * 50)

# ── Concept: XOR is its own inverse ──────────────────────────
a = 0b10110011   # 179 — the plaintext byte
k = 0b11001010   # 202 — the key byte

encrypted = a ^ k
decrypted = encrypted ^ k   # same key reverses it

print(f"\nplaintext : {a:08b}  ({a})")
print(f"key       : {k:08b}  ({k})")
print(f"encrypted : {encrypted:08b}  ({encrypted})")
print(f"decrypted : {decrypted:08b}  ({decrypted})  ← same as plaintext!")

# ── AddRoundKey: XOR every byte of the block with the round key ───────────
print("\n── AddRoundKey (XOR each byte with key) ──")

block   = [0x48, 0x65, 0x6C, 0x6C]   # "Hell" in ASCII
key_row = [0x2B, 0x7E, 0x15, 0x16]   # fake round key bytes

after = [b ^ k for b, k in zip(block, key_row)]

print(f"  block  : {[hex(b) for b in block]}  ({''.join(chr(b) for b in block)!r})")
print(f"  key    : {[hex(k) for k in key_row]}")
print(f"  result : {[hex(b) for b in after]}")

# ── Reversibility proof ───────────────────────────────────────
recovered = [b ^ k for b, k in zip(after, key_row)]
print(f"  recover: {[hex(b) for b in recovered]}  ← XOR again → original!")

# ── What happens after XOR — the full round pipeline ─────────
#
# After XOR (AddRoundKey), the 4×4 grid looks like this:
#
#   plaintext grid          key grid             XOR result ("scrambled grid")
#   ┌──────────────┐        ┌──────────────┐     ┌──────────────┐
#   │ 48  65 6C 6C │        │ 2B  7E 15 16 │     │ 63  1B 79 7A │
#   │ 6F  2C 20 74 │  XOR   │ 28  AE D2 A6 │  =  │ 47  82 F2 D2 │
#   │ 68  69 73 20 │        │ AB  F7 15 88 │     │ C3  9E 66 A8 │
#   │ 69  73 20 61 │        │ 09  CF 4F 3C │     │ 60  BC 6F 5D │
#   └──────────────┘        └──────────────┘     └──────────────┘
#
# "scrambled grid" just means: the result of XOR — not readable,
# not encrypted yet, just mixed with the key for this round.
#
# This XOR result is the INPUT to the next 3 steps of the round:
#
#   scrambled grid (XOR output)
#        ↓
#   SubBytes  — replace every cell using S-Box lookup table
#               (adds non-linearity so attacker can't solve equations)
#        ↓
#   ShiftRows — rotate each row left (row0=no shift, row1=1, row2=2, row3=3)
#               (spreads bytes so each column has bytes from different rows)
#        ↓
#   MixColumns — mix all 4 bytes within each column
#               (ensures 1 changed byte affects all 4 bytes in that column)
#        ↓
#   AddRoundKey again — XOR with the NEXT round key (derived from your key)
#        ↓
#   repeat this entire cycle 10 times (AES-128) or 14 times (AES-256)
#        ↓
#   final output = ciphertext block (16 bytes, looks like random noise)
#
# Each step alone is weak. All 4 together × 10 rounds = unbreakable.

print("""
Key insight:
  AES calls this step "AddRoundKey" — applied at the START
  and at the END of every round (10-14 rounds total).
  The round keys are derived from your original key via Key Schedule.

Next: 01c_subbytes.py — why XOR alone isn't enough (it's too linear)
""")
