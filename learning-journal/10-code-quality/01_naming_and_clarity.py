"""
Code Review Level 1 → Level 10
================================
Each example shows BAD code first, then the review comments, then the FIXED code.
Goal: Train your eye to spot issues at increasing complexity.

LEVEL 1 — Naming & Clarity
"""

# ─────────────────────────────────────────────────────────
# ❌ BAD CODE
# ─────────────────────────────────────────────────────────

def calc(x, y, z):
    t = x * y
    r = t - z
    if r < 0:
        r = 0
    return r

data = [1, 2, 3, 4, 5]
d2 = []
for i in data:
    if i % 2 == 0:
        d2.append(i * i)


# ─────────────────────────────────────────────────────────
# 🔍 REVIEW COMMENTS
# ─────────────────────────────────────────────────────────
"""
[L1] calc() — what does it calculate? quantity * price - discount?
[L2] x, y, z — meaningless parameter names. Reader must guess intent.
[L3] t, r — single-letter variables. t = total? r = result? refund?
[L4] data, d2 — what kind of data? d2 is especially bad.
[L5] The loop logic is invisible — what is this producing?
"""


# ─────────────────────────────────────────────────────────
# ✅ FIXED CODE
# ─────────────────────────────────────────────────────────

def calculate_discounted_price(unit_price: float, quantity: int, discount: float) -> float:
    total = unit_price * quantity
    discounted = total - discount
    return max(0, discounted)  # price can't go below zero

order_quantities = [1, 2, 3, 4, 5]
squared_even_quantities = [q * q for q in order_quantities if q % 2 == 0]


# ─────────────────────────────────────────────────────────
# 🧪 TEST — run and compare
# ─────────────────────────────────────────────────────────

print("Bad  :", calc(10, 3, 5))
print("Fixed:", calculate_discounted_price(unit_price=10, quantity=3, discount=5))

print("Bad  :", d2)
print("Fixed:", squared_even_quantities)
