"""
AES INTERNALS 3/5 — ShiftRows: spreading bytes across columns

THE PROBLEM SHIFTROWS SOLVES:
  AES processes a 4x4 grid of bytes (the "state").
  MixColumns (next step) mixes bytes WITHIN a column.
  Without ShiftRows, each column would encrypt independently —
  an attacker could break one column at a time (4x easier).

SHIFTROWS: rotate each row left by its row index
  Row 0: no shift      (stays the same)
  Row 1: shift left 1  (bytes move one position left, wrap around)
  Row 2: shift left 2
  Row 3: shift left 3

After ShiftRows, each column contains bytes from DIFFERENT original columns.
Then MixColumns mixes those → one byte affects all 4 columns.
This is called the "avalanche effect" — 1 bit change spreads everywhere.

No arithmetic. Just array rotation.
"""

def print_state(state, label):
    print(f"  {label}")
    for row in state:
        print("    " + "  ".join(f"{b:02X}" for b in row))

def shift_rows(state):
    return [
        state[0],                         # row 0: unchanged
        state[1][1:] + state[1][:1],      # row 1: rotate left 1
        state[2][2:] + state[2][:2],      # row 2: rotate left 2
        state[3][3:] + state[3][:3],      # row 3: rotate left 3
    ]

print("=" * 50)
print("  ShiftRows — row rotation")
print("=" * 50)

# Use column-labeled bytes so the movement is obvious
# Col:   0    1    2    3
state = [
    [0x00, 0x01, 0x02, 0x03],   # row 0
    [0x10, 0x11, 0x12, 0x13],   # row 1
    [0x20, 0x21, 0x22, 0x23],   # row 2
    [0x30, 0x31, 0x32, 0x33],   # row 3
]

print()
print_state(state, "Before ShiftRows:  (col 0  col 1  col 2  col 3)")
shifted = shift_rows(state)
print_state(shifted, "After  ShiftRows:")

print("""
  Notice:
    Row 0: 00 01 02 03 → 00 01 02 03  (unchanged)
    Row 1: 10 11 12 13 → 11 12 13 10  (10 moved to end)
    Row 2: 20 21 22 23 → 22 23 20 21  (two bytes wrapped)
    Row 3: 30 31 32 33 → 33 30 31 32  (three bytes wrapped)

  Now column 0 contains: 00, 11, 22, 33  — one byte from each original column
  MixColumns will now mix bytes that came from all 4 columns.
""")

# ── Avalanche preview ─────────────────────────────────────────
print("── Why this creates the avalanche effect ──")
print("""
  Round N:
    byte at (row=1, col=0) changes

  After ShiftRows:
    that byte moves to (row=1, col=3)

  After MixColumns:
    that byte affects all 4 bytes in column 3

  After next ShiftRows:
    those 4 bytes spread into 4 different columns

  After next MixColumns:
    now ALL 16 bytes are affected

  → 2 rounds to fully spread 1 bit change across the entire block.
""")

print("Next: 01e_mixcolumns.py — column mixing (the diffusion step)")
